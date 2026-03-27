---
name: gas_skill
display_name: Google Apps Script Execution
description: >
  Skills for writing, deploying, and debugging Google Apps Script (GAS).
  Covers doGet/doPost handlers, LockService for concurrency, SpreadsheetApp
  operations, MailApp, DriveApp, and time-based triggers.
version: 1.0.0
author: LongLeo (adapted for AI OS)
tier: 3
category: integration
domain: google-workspace
tags: [google, apps-script, gas, automation, sheets, backend]
cost_tier: economy
accessible_by:
  - Claude Code
  - Developer
dependencies: []
load_on_boot: false
promoted_from: D:\GA\Workspaces\LongLeo\.claude\skills\
---

# Google Apps Script Execution Skill

## When to Use
Load this skill when the project uses Google Apps Script as backend or
automation layer (e.g. Sheets automation, form handlers, scheduled tasks).

## Core Patterns

### doGet / doPost Handler
```javascript
function doGet(e) {
  const action = e.parameter.action;
  // Route to handler
  return ContentService.createTextOutput(JSON.stringify(result))
    .setMimeType(ContentService.MimeType.JSON);
}
```

### LockService (Prevent Race Conditions)
```javascript
const lock = LockService.getScriptLock();
lock.waitLock(10000); // Wait up to 10s
try {
  // Critical section
} finally {
  lock.releaseLock();
}
```

### SpreadsheetApp Batch Operations
```javascript
// Read entire range at once (not row by row)
const sheet = SpreadsheetApp.getActiveSpreadsheet().getSheetByName('Data');
const data = sheet.getDataRange().getValues();
// Process in memory, then write back in one call
sheet.getRange(1, 1, data.length, data[0].length).setValues(data);
```

### Time-Based Triggers
```javascript
ScriptApp.newTrigger('myFunction')
  .timeBased()
  .everyHours(1)
  .create();
```

## Common Pitfalls
- Never read/write cells in a loop — batch all operations
- Always use LockService for shared resource writes
- Quota: 6min script execution limit (use time-based chunking for long tasks)
- Test deployments: use version-locked /exec URLs in production
