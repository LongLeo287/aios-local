---
name: sheets_skill
display_name: Google Sheets Interaction
description: >
  Skills for reading, writing, and manipulating Google Sheets via Apps Script
  or API. Covers CRUD operations, data validation, named ranges, and
  SpreadsheetApp patterns for real-world data management.
version: 1.0.0
author: LongLeo (adapted for AI OS)
tier: 3
category: data
domain: google-workspace
tags: [google, sheets, spreadsheet, data, crud]
cost_tier: economy
accessible_by:
  - Claude Code
  - Developer
dependencies:
  - gas_skill
load_on_boot: false
promoted_from: D:\GA\Workspaces\LongLeo\.claude\skills\
---

# Google Sheets Interaction Skill

## When to Use
Load when project uses Google Sheets as data store, reporting layer,
or lightweight database substitute.

## Core Patterns

### Read Data (Batch — Preferred)
```javascript
function readSheetData(sheetName) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet()
    .getSheetByName(sheetName);
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  return data.slice(1).map(row =>
    Object.fromEntries(headers.map((h, i) => [h, row[i]]))
  );
}
```

### Write Data (Append Row)
```javascript
function appendRow(sheetName, rowData) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet()
    .getSheetByName(sheetName);
  sheet.appendRow(Object.values(rowData));
}
```

### Find and Update Row
```javascript
function updateRow(sheetName, keyCol, keyValue, updates) {
  const sheet = SpreadsheetApp.getActiveSpreadsheet()
    .getSheetByName(sheetName);
  const data = sheet.getDataRange().getValues();
  const headers = data[0];
  const keyIdx = headers.indexOf(keyCol);
  for (let i = 1; i < data.length; i++) {
    if (data[i][keyIdx] === keyValue) {
      Object.entries(updates).forEach(([col, val]) => {
        const colIdx = headers.indexOf(col);
        sheet.getRange(i + 1, colIdx + 1).setValue(val);
      });
      return true;
    }
  }
  return false;
}
```

## Best Practices
- Use Named Ranges for headers (robust against column changes)
- Cache frequently read data with CacheService
- Use `getDataRange()` not `getLastRow()` loops
