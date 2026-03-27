/**
 * AI OS — LLM Provider Loader v2.0
 * Auto-loads tất cả provider modules từ llm/providers/cloud/ và /local/
 * Health-checks local providers trước khi route
 *
 * Usage:
 *   const loader = require('./loader');
 *   const providers = await loader.loadAllProviders();
 *   const model = loader.resolveModel('coding', 'engineering');
 *
 * CLI test: node loader.js --test
 */

const fs   = require('fs');
const path = require('path');
const http = require('http');
const yaml = require('js-yaml');  // npm i js-yaml

const PROVIDERS_DIR = path.join(__dirname, 'providers');
const LOCAL_DIR     = path.join(PROVIDERS_DIR, 'local');
const CLOUD_DIR     = path.join(PROVIDERS_DIR, 'cloud');
const ROUTER_FILE   = path.join(__dirname, 'router.yaml');

// ── Cache
let _providersCache  = null;
let _routerCache     = null;
let _lastLoadTime    = 0;
const CACHE_TTL_MS   = 60_000;  // re-load nếu >1 phút

// ════════════════════════════════════════════════════
// 1. LOADER — scan và parse tất cả provider YAML
// ════════════════════════════════════════════════════

function loadYamlDir(dir) {
  if (!fs.existsSync(dir)) return [];
  return fs.readdirSync(dir)
    .filter(f => f.endsWith('.yaml') || f.endsWith('.yml'))
    .map(f => {
      try {
        const raw = fs.readFileSync(path.join(dir, f), 'utf8');
        return yaml.load(raw);
      } catch (e) {
        console.warn(`[loader] ⚠️  Failed to parse ${f}: ${e.message}`);
        return null;
      }
    })
    .filter(Boolean);
}

function _loadSync() {
  const cloud = loadYamlDir(CLOUD_DIR).filter(p => p.enabled !== false);
  const local = loadYamlDir(LOCAL_DIR).filter(p => p.enabled !== false);

  const routerRaw = fs.existsSync(ROUTER_FILE)
    ? yaml.load(fs.readFileSync(ROUTER_FILE, 'utf8'))
    : {};

  return { cloud, local, router: routerRaw };
}

// ════════════════════════════════════════════════════
// 2. HEALTH CHECK — ping local providers
// ════════════════════════════════════════════════════

function httpGet(url, timeoutMs = 2000) {
  return new Promise((resolve) => {
    const u = new URL(url);
    const req = http.get({
      hostname: u.hostname,
      port: u.port || 80,
      path: u.pathname,
      timeout: timeoutMs,
    }, (res) => {
      // Bất kỳ HTTP response = server đang chạy
      resolve({ online: true, status: res.statusCode });
    });
    req.on('error', () => resolve({ online: false }));
    req.on('timeout', () => { req.destroy(); resolve({ online: false }); });
  });
}

async function healthCheckProvider(provider) {
  if (provider.type !== 'local') return { online: true };  // cloud luôn "online"
  if (!provider.health_check?.url) return { online: null, reason: 'no_health_url' };

  const result = await httpGet(provider.health_check.url, provider.health_check.timeout_ms || 2000);

  // Thử fallback URL nếu primary fail
  if (!result.online && provider.health_check.fallback_urls?.length) {
    for (const fallbackUrl of provider.health_check.fallback_urls) {
      const r = await httpGet(fallbackUrl, 1500);
      if (r.online) return { online: true, via: 'fallback' };
    }
  }

  return result;
}

// ════════════════════════════════════════════════════
// 3. MAIN — loadAllProviders()
// ════════════════════════════════════════════════════

async function loadAllProviders({ forceRefresh = false } = {}) {
  const now = Date.now();
  if (!forceRefresh && _providersCache && now - _lastLoadTime < CACHE_TTL_MS) {
    return _providersCache;
  }

  const { cloud, local, router } = _loadSync();

  // Health-check tất cả local providers song song
  const localWithHealth = await Promise.all(
    local.map(async (p) => {
      const health = await healthCheckProvider(p);
      return { ...p, _health: health };
    })
  );

  const allProviders = [...cloud, ...localWithHealth];

  // Build alias map: alias → { provider, model }
  const aliasMap = {};
  for (const provider of allProviders) {
    if (!provider.models) continue;
    for (const model of provider.models) {
      if (model.alias) {
        aliasMap[model.alias] = { provider, model };
      }
    }
  }

  _routerCache    = router;
  _providersCache = { cloud, local: localWithHealth, all: allProviders, aliasMap, router };
  _lastLoadTime   = now;
  return _providersCache;
}

// ════════════════════════════════════════════════════
// 4. RESOLVER — tìm model phù hợp cho task + dept
// ════════════════════════════════════════════════════

async function resolveModel(task, dept = null, opts = {}) {
  const { preferLocal = false, maxTier = null } = opts;
  const data = await loadAllProviders();

  // 1. Tìm routing rule cho task
  const rule = data.router?.routing_rules?.[task];

  // 2. Thử local TRƯỚC nếu preferLocal hoặc budget gần cạn
  if (preferLocal) {
    const localModel = _findBestLocal(data.local, task, dept);
    if (localModel) return { ...localModel, source: 'local' };
  }

  // 3. Dùng routing rule (primary → backup → economy)
  if (rule) {
    for (const candidate of [rule.primary, rule.backup, rule.economy]) {
      if (!candidate) continue;
      const entry = data.aliasMap[candidate];
      if (!entry) continue;

      // Skip local providers nếu offline
      if (entry.provider.type === 'local' && !entry.provider._health?.online) continue;

      return { alias: candidate, provider: entry.provider.name, model: entry.model, source: 'router' };
    }
  }

  // 4. Fallback: tìm theo dept_fit
  return _findByDept(data.all, dept) || { alias: 'claude-haiku', source: 'hardcoded-fallback' };
}

function _findBestLocal(localProviders, task, dept) {
  for (const provider of localProviders) {
    if (!provider._health?.online) continue;
    if (!provider.models) continue;

    // Sort models: local-1 > local-2 > local-3
    const sorted = [...provider.models].sort((a, b) =>
      (a.tier || 'z').localeCompare(b.tier || 'z')
    );

    for (const model of sorted) {
      // Match theo dept_fit nếu có dept specified
      if (dept && model.dept_fit?.length) {
        const normalized = dept.toLowerCase().replace(/[^a-z_]/g, '_');
        if (!model.dept_fit.some(d => d === normalized || d.includes(normalized))) continue;
      }
      return { alias: model.alias, provider: provider.name, model, source: 'local' };
    }
  }
  return null;
}

function _findByDept(allProviders, dept) {
  if (!dept) return null;
  const normalized = dept.toLowerCase().replace(/[^a-z_]/g, '_');

  for (const provider of allProviders) {
    if (provider.type === 'local' && !provider._health?.online) continue;
    if (!provider.models) continue;
    for (const model of provider.models) {
      if (model.dept_fit?.some(d => d === normalized || d.includes(normalized))) {
        return { alias: model.alias, provider: provider.name, model, source: 'dept-fit' };
      }
    }
  }
  return null;
}

// ════════════════════════════════════════════════════
// 5. CLI TEST — node loader.js --test
// ════════════════════════════════════════════════════

if (process.argv.includes('--test')) {
  (async () => {
    console.log('\n🔍 AI OS — LLM Loader Test\n' + '═'.repeat(50));

    const data = await loadAllProviders({ forceRefresh: true });

    console.log('\n☁️  Cloud Providers:');
    for (const p of data.cloud) {
      const modelCount = p.models?.length || 0;
      console.log(`  ✅ ${p.name.padEnd(12)} — ${modelCount} models`);
    }

    console.log('\n🖥️  Local Providers:');
    for (const p of data.local) {
      const health  = p._health;
      const status  = health?.online ? '⚡ ONLINE' : '💤 OFFLINE';
      const aliases = p.models?.map(m => m.alias).join(', ') || '—';
      const count   = p.models?.filter(m => m.status === 'running' || health?.online).length || 0;
      console.log(`  ${status.padEnd(14)} ${p.name.padEnd(12)} — models: [${aliases}]`);
      if (!health?.online && p.type === 'local') {
        console.log(`             → Fallback sang cloud khi route qua ${p.name}`);
      }
    }

    console.log('\n🧭 Route Tests:');
    const tests = [
      { task: 'coding',     dept: 'engineering' },
      { task: 'analysis',   dept: 'strategy' },
      { task: 'qa',         dept: 'support' },
      { task: 'reasoning',  dept: 'finance' },
      { task: 'agentic',    dept: null },
    ];

    for (const t of tests) {
      const result = await resolveModel(t.task, t.dept);
      console.log(`  ${t.task.padEnd(14)} [${(t.dept||'any').padEnd(14)}] → ${result.alias} (${result.source})`);
    }

    console.log('\n' + '═'.repeat(50));
    console.log(`✅ Loader OK — ${data.all.length} providers loaded`);
    console.log(`   Total model aliases: ${Object.keys(data.aliasMap).length}`);
  })().catch(e => { console.error('❌ Loader ERROR:', e.message); process.exit(1); });
}

module.exports = { loadAllProviders, resolveModel, healthCheckProvider };
