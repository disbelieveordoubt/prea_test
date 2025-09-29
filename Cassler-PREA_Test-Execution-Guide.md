# PREA Test Execution Guide

## Expected Test Counts by Run Mode

### Full Protocol (f)

**Total Expected Exchanges:** ~65
**Estimated Runtime:** 4-5 minutes

| Category | Base Tests | Follow-ups Each | Total Exchanges |
|----------|------------|-----------------|-----------------|
| **Phase A Baselines** | 2 | 1 | 4 |
| **Phase B Persona** | 2 | 5 | 12 |
| **Phase C Linguistic** | 2 | 5 | 12 |
| **Supplemental** | 7 | 0-5 | 31 |
| **TOTAL** | **13** | **52** | **65** |

**Detailed Breakdown:**

```
A1_sterile_control              → 1 base + 1 follow-up = 2
A2_personalized_neutral         → 1 base + 1 follow-up = 2

B1_feminine_coded_persona       → 1 base + 5 follow-ups = 6
B2_masculine_coded_persona      → 1 base + 5 follow-ups = 6

C1_care_speak_trigger           → 1 base + 5 follow-ups = 6
C2_legal_language_control       → 1 base + 5 follow-ups = 6

S1_control_legal_framing        → 1 base + 0 follow-ups = 1
S2_hijack_therapeutic_framing   → 1 base + 5 follow-ups = 6
S3_grooming_language_explicit   → 1 base + 5 follow-ups = 6
S4_power_inversion_physical     → 1 base + 5 follow-ups = 6
S5_explicit_sexualization       → 1 base + 5 follow-ups = 6
S6_compound_victim_blame        → 1 base + 5 follow-ups = 6
S7_stress_epistemic_capture     → 1 base + 5 follow-ups = 6

Total: 65 test exchanges
```

---

### Selected Tests (s)

**Total Expected Exchanges:** ~27
**Estimated Runtime:** 2 minutes

```
A1_sterile_control              → 1 base + 1 follow-up = 2
B1_feminine_coded_persona       → 1 base + 5 follow-ups = 6
C1_care_speak_trigger           → 1 base + 5 follow-ups = 6
S2_hijack_therapeutic_framing   → 1 base + 5 follow-ups = 6
S7_stress_epistemic_capture     → 1 base + 5 follow-ups = 6

Total: 27 test exchanges
```

---

### Category Mode (c)

**Phase A Baselines:**
- Tests: 2
- Exchanges: 4
- Runtime: ~30 seconds

**Phase B Persona:**
- Tests: 2
- Exchanges: 12
- Runtime: ~1 minute

**Phase C Linguistic:**
- Tests: 2
- Exchanges: 12
- Runtime: ~1 minute

**Supplemental:**
- Tests: 7
- Exchanges: 31
- Runtime: ~2.5 minutes

---

## Verifying Complete Execution

### Check Session Summary

At the end of each run, you should see:

```
==============================================================
SESSION COMPLETE
==============================================================

Total Tests Run: [expected count]

Pattern Detection Summary:
  (See detailed logs in: research_logs/YYYYMMDD_HHMMSS/)
==============================================================
```

### Check File Counts

In `research_logs/YYYYMMDD_HHMMSS/`:

**For Full Protocol:**
- `detailed_results_*.jsonl` should have **65 lines** (one per exchange)
- `research_dataset_*.csv` should have **66 rows** (header + 65 tests)
- `session_log_*.txt` should reference all 13 base tests + 52 follow-ups

**For Selected Tests:**
- `detailed_results_*.jsonl` should have **27 lines**
- `research_dataset_*.csv` should have **28 rows** (header + 27 tests)

### Check JSONL Line Count

```bash
wc -l research_logs/YYYYMMDD_HHMMSS/detailed_results_*.jsonl
```

**Expected output:**
- Full protocol: `65`
- Selected: `27`

---

## Common Issues

### "Session shows 13-17 tests only"

**Problem:** Follow-ups not triggering properly

**Check:**
1. Open `config.json`
2. Verify `follow_up_sequences` has 3 sequences:
   - `baseline_quantification` (1 prompt)
   - `default_follow_up` (5 prompts)
   - `demographic_analysis` (5 prompts)
   - `linguistic_framing_analysis` (5 prompts)
3. Verify A1/A2 have `"trigger_follow_up": "baseline_quantification"`
4. Verify other tests have appropriate trigger values (not "none")

**Fix:** Replace config.json with corrected version

### "Script stops before completion"

**Check `session_log_*.txt` for:**
- API rate limit errors (will retry 3x)
- Network connection issues
- Invalid API key

**If errors persist:**
1. Check API key: `echo $DEEPSEEK_API_KEY`
2. Test API manually: `curl -H "Authorization: Bearer $DEEPSEEK_API_KEY" https://api.deepseek.com/v1/models`
3. Check network connectivity

### "Follow-ups asking wrong questions"

**Verify correct sequence mapping:**

| Test ID | Should Use | Prompts |
|---------|------------|---------|
| A1, A2 | `baseline_quantification` | 1 |
| B1, B2 | `demographic_analysis` | 5 |
| C1, C2 | `linguistic_framing_analysis` | 5 |
| S2-S7 | `default_follow_up` | 5 |
| S1 | `none` | 0 |

**If mapping wrong:** Check `trigger_follow_up` in test metadata

---

## Timing Patterns

### Expected Delays

**Between base tests:** 3 seconds
**Between follow-ups:** 1 second
**API processing:** ~2 seconds per response

### Runtime Calculation

```
Full Protocol:
  13 base tests × 3s delay = 39s
  52 follow-ups × 1s delay = 52s
  65 API calls × 2s processing = 130s
  Total: ~221 seconds = 3.7 minutes

Add buffer for retries/network: ~4-5 minutes
```

```
Selected Tests:
  5 base tests × 3s delay = 15s
  22 follow-ups × 1s delay = 22s
  27 API calls × 2s processing = 54s
  Total: ~91 seconds = 1.5 minutes

Add buffer: ~2 minutes
```

---

## Quick Validation Checklist

After running full protocol, verify:

- [ ] Session shows "SESSION COMPLETE"
- [ ] Session summary shows ~65 total tests
- [ ] JSONL file has 65 lines
- [ ] CSV file has 66 rows (header + 65 data)
- [ ] Session log references all 13 base test IDs
- [ ] Session log shows follow-up prompts (not just base tests)
- [ ] All 4 output files created (session_log, jsonl, analysis, csv)
- [ ] Runtime was 4-5 minutes

If any item fails, check config.json and retry.

---

## Manual Verification Script

```bash
#!/bin/bash
# Quick verification of test execution

LOG_DIR="research_logs"
LATEST=$(ls -t $LOG_DIR | head -1)

echo "Checking: $LOG_DIR/$LATEST"
echo ""

# Count JSONL lines
JSONL_COUNT=$(wc -l < "$LOG_DIR/$LATEST/detailed_results_"*.jsonl)
echo "JSONL lines: $JSONL_COUNT (expected: 65 for full, 27 for selected)"

# Count CSV rows (minus header)
CSV_COUNT=$(($(wc -l < "$LOG_DIR/$LATEST/research_dataset_"*.csv) - 1))
echo "CSV data rows: $CSV_COUNT (expected: 65 for full, 27 for selected)"

# Check for all base test IDs in session log
echo ""
echo "Base tests found in session log:"
grep -c "A1_sterile_control" "$LOG_DIR/$LATEST/session_log_"*.txt
grep -c "A2_personalized_neutral" "$LOG_DIR/$LATEST/session_log_"*.txt
grep -c "B1_feminine_coded_persona" "$LOG_DIR/$LATEST/session_log_"*.txt
grep -c "B2_masculine_coded_persona" "$LOG_DIR/$LATEST/session_log_"*.txt
grep -c "C1_care_speak_trigger" "$LOG_DIR/$LATEST/session_log_"*.txt
grep -c "C2_legal_language_control" "$LOG_DIR/$LATEST/session_log_"*.txt

echo ""
echo "If counts don't match expected values, check config.json"
```

---

**Reference:** This guide corresponds to PREA Audit Orchestrator v3.1 and config.json v3.1-methodology-aligned