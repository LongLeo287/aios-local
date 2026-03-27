# Legacy Department Definitions

This directory contains legacy department configuration files that were migrated to the new structure in `corp/departments/` as part of the AI OS Corp restructuring.

## Files Overview

- `engineering.yaml` - Legacy engineering department configuration
- `marketing.yaml` - Legacy marketing department configuration
- `operations.yaml` - Legacy operations department configuration
- `qa.yaml` - Legacy QA/testing department configuration
- `strategy.yaml` - Legacy strategy department configuration
- `support.yaml` - Legacy support department configuration

## Migration Status

These configurations have been migrated to the new department structure:
- New format: `corp/departments/[dept_name]/WORKER_PROMPT.md` and `MANAGER_PROMPT.md`
- New organization: 21 departments with full worker/manager prompt coverage
- New governance: Integrated with the current GOVERNANCE.md and THESIS.md

## Purpose

This legacy directory serves as:
- Historical reference for department evolution
- Backup of original configurations
- Migration checkpoint for rollback if needed

## Current Structure

The active department configurations are now located in:
- `corp/departments/[dept_name]/WORKER_PROMPT.md` - Worker agent instructions
- `corp/departments/[dept_name]/MANAGER_PROMPT.md` - Manager agent instructions
- `corp/departments/[dept_name]/memory/` - Department-specific memory

## Archive Policy

This directory is maintained for historical purposes but is no longer actively used. All department operations now follow the new structure with full AI agent integration.