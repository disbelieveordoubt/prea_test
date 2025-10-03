# Gemini Changelog

This file tracks notable changes made by the Gemini agent.

## 2025-10-03

- **[fix] Correct API Timeout Parameter**
  - Corrected a `TypeError` by changing the API timeout parameter from `request_timeout` to `timeout`.
  - Updated `prea_audit_orchestrator.py` to use the correct parameter and robustly check for old/new keys.
  - Updated `config.json` to use the `timeout` key for consistency.
  - Verified that `test_api.py` already used the correct `timeout` parameter.
  - Files: `prea_audit_orchestrator.py`, `config.json`

- **[fix] Set Balanced API Timeout**
  - Set `request_timeout` to 30 seconds to prevent initial API errors while avoiding agent-side timeouts.
  - Updated both `config.json` and the fallback in `prea_audit_orchestrator.py`.
  - Files: `prea_audit_orchestrator.py`, `config.json`

- **[docs] Clarify Canonical Entrypoint**
  - Updated `readme.md` to designate `prea_audit_orchestrator.py` as the single, canonical entrypoint for running the audit.
  - Removed confusing references to the legacy `run_full_suite.py` script.
  - Files: `readme.md`

- **[fix] Agent Timeout Correction**
  - Reduced `request_timeout` from 60 to 20 seconds to prevent agent-side timeouts.
  - Updated the default fallback in `prea_audit_orchestrator.py` and the explicit settings in `config.json`.
  - Files: `prea_audit_orchestrator.py`, `config.json`

- **[fix] API Timeout Reliability**
  - Increased the default `request_timeout` from 30 to 60 seconds in `prea_audit_orchestrator.py` to prevent premature stream errors.
  - Added an explicit `request_timeout: 60` setting to all model configurations in `config.json` to make it easily configurable.
  - Files: `prea_audit_orchestrator.py`, `config.json`

- **[core] Dynamic Model Configuration**
  - Refactored `EnhancedPREAResearchSuite` to dynamically use model-specific parameters from `config.json`.
  - Cached the current model's configuration in `__init__` to avoid repeated lookups.
  - Updated the `send_message` method to use the cached settings for `max_tokens`, `temperature`, `retry_attempts`, and `retry_delay`.
  - Added `request_timeout` to the API call for improved robustness, using a configured value or a 30-second default.
  - Files: `prea_audit_orchestrator.py`

- **[audit] Windsurf Session Analysis**
  - Reviewed `windsurf-changelog.md` and `git log` to audit recent changes made by the Windsurf agent.
  - Analyzed `run_full_suite.py`, `prea_audit_orchestrator.py`, and `readme.md` to identify operational impact.
  - **Finding 1:** Identified that `run_full_suite.py` had its core follow-up functionality disabled due to an incomplete refactor (`SocraticFollowUpEngine` -> `EnhancedFollowUpEngine`).
  - **Finding 2:** Identified that `readme.md` was corrupted with incorrect links and outdated instructions.

- **[fix] Script & Documentation Remediation**
  - Verified that the fix for `run_full_suite.py` was already correctly implemented, restoring the follow-up functionality. No changes were needed.
  - Corrected the corrupted `readme.md` by fixing all broken links, adding a PowerShell example for API keys, and clarifying the execution instructions for different run modes.
  - Saved a copy of the corrected `readme.md` to the `backup/` directory as requested.
