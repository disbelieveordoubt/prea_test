# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is a **PREA AI Safety Research Suite** designed for defensive security research. The project tests for "Framework Hijacking" vulnerabilities in Large Language Models (LLMs) using the federal Prison Rape Elimination Act (PREA) standard as an unambiguous baseline. The research hypothesis is that LLMs perform semantic disambiguation before structural reasoning, causing care-associated language to override legal and analytical frameworks.

## Architecture

### Core Components

1. **PREAResearchSuite** (prea_audit_orchestrator.py:22-233) - Main research orchestrator
   - Manages API connections to DeepSeek-compatible endpoints
   - Implements timing analysis and compliance scoring algorithms
   - Handles test categorization and vulnerability detection
   - Generates structured research logs and analysis reports

2. **SocraticFollowUpEngine** (prea_audit_orchestrator.py:234-309) - Follow-up conversation manager
   - Automatically determines appropriate follow-up sequences based on initial test results
   - Tracks conversation threads across multiple exchanges
   - Analyzes architectural persistence patterns in model responses

3. **Test Battery Configuration** (config.json) - External test case definitions
   - Structured test scenarios across categories: baseline controls, core vulnerabilities, thought termination, adversarial tests, and cross-domain validation
   - Follow-up sequence definitions for probing architectural persistence
   - Detection keywords for compliance analysis

### Key Algorithms

- **Compliance Scoring** (prea_audit_orchestrator.py:84-108): Analyzes responses for PREA compliance using weighted keyword detection
- **Framework Hijacking Detection** (prea_audit_orchestrator.py:110-114): Identifies when care language overrides legal frameworks
- **Exploitation Risk Assessment** (prea_audit_orchestrator.py:116-120): Flags potentially harmful guidance patterns

## Running Tests

### Environment Setup
```bash
export DEEPSEEK_API_KEY='your-api-key'
pip install -r requirements.txt
```

### Execution Modes
```bash
python prea_audit_orchestrator.py
```

Run modes available:
- **(f)ull** - Complete research protocol with automated follow-ups
- **(c)ategory** - Run specific test categories
- **(q)uick** - Single-turn tests without follow-ups
- **(i)nteractive** - Manual test execution and follow-up control

### Output Structure

All research data is saved to `research_logs/`:
- `prea_research_{timestamp}.txt` - Human-readable session log
- `detailed/research_data_{timestamp}.json` - Single-turn test results
- `detailed/conversations_{timestamp}.jsonl` - Multi-turn conversation data
- `analysis/comprehensive_analysis_{timestamp}.txt` - Category-based analysis
- `analysis/regulatory_report_{timestamp}.txt` - Regulatory submission format
- `analysis/academic_dataset_{timestamp}.csv` - Academic research dataset

## Data Analysis

Use `jup.py` for basic Jupyter/pandas analysis of conversation logs. The JSONL format conversation logs contain structured data for research analysis including compliance scores, timing patterns, and vulnerability detection flags.

## Security Context

This is a **defensive security research tool** designed to identify and document AI safety vulnerabilities. All test scenarios are based on documented patterns from federal oversight standards. The research aims to improve AI system safety in child protection contexts through systematic vulnerability assessment.