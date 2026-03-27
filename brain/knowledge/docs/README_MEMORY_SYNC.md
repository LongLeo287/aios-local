# 1-Click Memory Sync â€” User Manual

> Phase 15.1 | Smart Bookmark Manager AI OS Ecosystem

## Overview

Memory Sync allows you to **backup** and **restore** your AI conversation history (Gemini CLI) with a single double-click. This is useful when:

- Moving to a new computer
- Reinstalling your development environment
- Sharing workspace context with a teammate
- Creating a checkpoint before major changes

## Files

| File | Location | Purpose |
|------|----------|---------|
| `Backup_Memory.bat` | Workspace root | 1-click backup launcher |
| `WakeUp_Memory.bat` | Workspace root | 1-click restore launcher |
| `backup_soul.ps1` | `.memory/` | PowerShell backup logic |
| `wake_up.ps1` | `.memory/` | PowerShell restore logic |
| `soul_backup.zip` | `.memory/` | Generated backup archive |

## How to Backup

1. **Double-click** `Backup_Memory.bat` in the workspace root.
2. The script automatically:
   - Scans `C:\Users\YOUR_USERNAME\.gemini\antigravity\conversations\` for the latest `.pb` conversation file.
   - Copies the conversation + associated brain data into a temp folder.
   - Compresses everything into `.memory\soul_backup.zip`.
   - Cleans up the temp folder.
3. You will see `[SUCCESS] BACKUP COMPLETE!` in the terminal.
4. Commit and push to Git to preserve the backup remotely.

### What gets backed up

```
soul_backup.zip
  conversations/
    <conversation_id>.pb      # Latest conversation protobuf
  brain/
    <conversation_id>/        # Brain/memory files for that conversation
```

## How to Restore (Wake Up)

1. Clone or pull the repository on the new machine.
2. **Double-click** `WakeUp_Memory.bat` in the workspace root.
3. The script automatically:
   - Extracts `soul_backup.zip` from `.memory/`.
   - Copies conversations and brain data into `C:\Users\YOUR_USERNAME\.gemini\antigravity\`.
   - Cleans up the temp folder.
4. You will see `[SUCCESS] WAKE UP COMPLETE!` in the terminal.
5. Reload your AI extension in VS Code to access the restored chat history.

## Troubleshooting

| Symptom | Cause | Fix |
|---------|-------|-----|
| `No conversation found` | No `.pb` files in Gemini directory | Start a Gemini conversation first, then retry backup |
| `No soul_backup.zip found` | Missing backup file | Run `Backup_Memory.bat` first, or pull from Git |
| PowerShell script blocked | Execution policy restriction | The `.bat` wrappers already use `-ExecutionPolicy Bypass` â€” run the `.bat` file, not the `.ps1` directly |
| Zip creation fails | Temp folder permission issue | Run the terminal as Administrator |

## Security Notes

- The `.bat` wrappers use `powershell -ExecutionPolicy Bypass` scoped only to the invoked script â€” this does not change your system-wide policy.
- `soul_backup.zip` may contain conversation content. Add it to `.gitignore` if you do not want it pushed to a shared remote.

## Git Integration

To include backups in version control:

```bash
git add .memory/soul_backup.zip
git commit -m "chore: backup AI memory checkpoint"
git push
```

To exclude backups:

```bash
echo ".memory/soul_backup.zip" >> .gitignore
```

