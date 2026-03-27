@echo off
chcp 65001 >nul
echo.
echo ========================================
echo   AI OS Corp - Claude Code Phase 4
echo   Fix: CT-01 to CT-10
echo ========================================
echo.
cd /d "D:\LongLeo\AI OS CORP\AI OS"
claude --dangerously-skip-permissions "BOOT: Read CLAUDE.md first. Then read brain/shared-context/blackboard.json. Your task is CLAWTASK-REVIEW-2026-03-24. Read subagents/mq/claude_code_tasks.md for the full task list. Execute ALL tasks: CT-01 (add API Bridge to startup.ps1), CT-02 (pin lobe_chat docker tag, remove :latest), CT-03 (add LightRAG to startup.ps1), CT-04 (add 9router to SERVICES dict in services_control.py), CT-05 (document module_crewai and module_keys), CT-07 (add log paths for all 12 services), CT-09 (fix encoding in handoff_to_claude_code.ps1), CT-10 (fix encoding in startup.ps1 line 1). When all done: write receipt to telemetry/receipts/CLAWTASK-REVIEW-2026-03-24.md and update brain/shared-context/blackboard.json handoff_trigger to COMPLETE."
