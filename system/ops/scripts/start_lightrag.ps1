<#
.SYNOPSIS
    Start LightRAG REST API server for AI OS â€” v1.4.11 compatible
.DESCRIPTION
    LightRAG-HKU v1.4.11 khÃ´ng cÃ³ create_app hay CLI.
    DÃ¹ng lightrag.server module hoáº·c FastAPI wrapper.
    Port: 9621 | Working dir: brain/knowledge/lightrag_db
#>

$AOS_ROOT = $env:AOS_ROOT
$LIGHTRAG_PORT = 9621
$WORKING_DIR = "$AOS_ROOT\brain\knowledge\lightrag_db"

Write-Host "=== AI OS LightRAG API Startup ===" -ForegroundColor Cyan
Write-Host "Version: lightrag-hku 1.4.11 | Port: $LIGHTRAG_PORT"

# Check if already running
$existing = Get-NetTCPConnection -LocalPort $LIGHTRAG_PORT -State Listen -ErrorAction SilentlyContinue
if ($existing) {
    Write-Host "[ALREADY RUNNING] LightRAG :$LIGHTRAG_PORT" -ForegroundColor Green
    exit 0
}

# Create working dir
New-Item -ItemType Directory -Force -Path $WORKING_DIR | Out-Null

# Create FastAPI server script if not exists
$serverScript = "$AOS_ROOT\ops\scripts\lightrag_server.py"
if (-not (Test-Path $serverScript)) {
    Write-Host "Creating lightrag_server.py..." -ForegroundColor Yellow
    # Script is created separately â€” run create_lightrag_server.py
    python -c "
import os
script = '''
from fastapi import FastAPI
from pydantic import BaseModel
import os

WORKING_DIR = r'<AI_OS_ROOT>\\brain\\knowledge\\lightrag_db'
os.makedirs(WORKING_DIR, exist_ok=True)
app = FastAPI(title='AI OS LightRAG API')
rag_instance = None

@app.get('/health')
def health():
    return {'status': 'ok', 'port': 9621}

@app.post('/init')
async def init_rag():
    global rag_instance
    try:
        from lightrag import LightRAG, QueryParam
        from lightrag.llm.ollama import ollama_model_complete, ollama_embed
        from lightrag.utils import EmbeddingFunc
        rag_instance = LightRAG(
            working_dir=WORKING_DIR,
            llm_model_func=ollama_model_complete,
            llm_model_name='gemma2:2b',
            llm_model_kwargs={'host': 'http://localhost:11434'},
            embedding_func=EmbeddingFunc(
                embedding_dim=768,
                max_token_size=8192,
                func=lambda texts: ollama_embed(texts, embed_model='nomic-embed-text', host='http://localhost:11434')
            ),
        )
        return {'status': 'initialized'}
    except Exception as e:
        return {'error': str(e)}

class QueryRequest(BaseModel):
    query: str
    mode: str = 'mix'

@app.post('/query')
async def query_rag(req: QueryRequest):
    if rag_instance is None:
        return {'error': 'Not initialized'}
    try:
        from lightrag import QueryParam
        result = await rag_instance.aquery(req.query, param=QueryParam(mode=req.mode))
        return {'result': result}
    except Exception as e:
        return {'error': str(e)}

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=9621)
'''
with open(r'<AI_OS_ROOT>\\ops\\scripts\\lightrag_server.py', 'w', encoding='utf-8') as f:
    f.write(script)
print('Created lightrag_server.py')
" 2>&1
}


# Check uvicorn
$uvicorn = pip show uvicorn 2>$null | Select-String "Name"
if (-not $uvicorn) {
    Write-Host "Installing uvicorn..."
    pip install uvicorn -q
}

# Check fastapi
$fastapi = pip show fastapi 2>$null | Select-String "Name"
if (-not $fastapi) {
    Write-Host "Installing fastapi..."
    pip install fastapi -q
}

Write-Host "Starting LightRAG server on :$LIGHTRAG_PORT..." -ForegroundColor Yellow
Start-Process python -ArgumentList "$serverScript" -NoNewWindow

Start-Sleep 2
$check = Get-NetTCPConnection -LocalPort $LIGHTRAG_PORT -State Listen -ErrorAction SilentlyContinue
if ($check) {
    Write-Host "[STARTED] LightRAG API :$LIGHTRAG_PORT" -ForegroundColor Green
} else {
    Write-Host "[WARNING] LightRAG may still be initializing â€” check in 5s" -ForegroundColor Yellow
    Write-Host "  Manual: python ops/scripts/lightrag_server.py"
}

