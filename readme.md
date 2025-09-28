# PREA AI Safety Research Orchestrator

by Daniel Cassler

This project provides a comprehensive, automated tool for conducting AI safety research into "Framework Hijacking" vulnerabilities in Large Language Models (LLMs). It uses the federal PREA (Prison Rape Elimination Act) standard as an unambiguous baseline to test and quantify how care-associated language can cause LLMs to fail in critical child protection scenarios.

The core research hypothesis is that LLMs perform semantic disambiguation before structural reasoning, causing care-associated language to probabilistically override legal and analytical frameworks.

---
## Core Features

* **Advanced, Category-Based Testing**: Executes a large battery of tests organized into specific categories like `thought_termination`, `adversarial_exploitation`, and `cross_domain_validation`.
* **Automated Socratic Follow-Ups**: Automatically runs multi-turn conversational sequences to test for "Architectural Persistence"—the model's inability to correct its reasoning failures even after meta-cognitive recognition.
* **External Configuration**: The target AI model, all test cases, and follow-up questions are managed in an external `config.json` file, allowing for easy modification without changing the code.
* **Automated Reporting**: Generates multiple final reports, including a comprehensive category-based analysis, a regulatory-grade summary, and a `.csv` dataset suitable for academic publication.
* **Comprehensive Logging**: Creates human-readable text logs, single-turn JSON data, and structured multi-turn conversation logs (`.jsonl`) for deep analysis.

---
## Setup & Usage

### Requirements
* Python 3.7+
* An API key for an OpenAI-compatible endpoint (e.g., DeepSeek).

### Installation & First Run

1.  **Place Files**: Save `prea_audit_orchestrator.py`, `config.json`, and `requirements.txt` in the same directory.

2.  **Install Dependencies**: From your terminal in the project directory, run:
    ```bash
    pip install -r requirements.txt
    ```

3.  **Set Your API Key**:
    You can either set an environment variable (recommended):
    ```bash
    export DEEPSEEK_API_KEY='your-key-here'
    ```
    ...or the script will prompt you to enter the key on its first run.

4.  **Run the Script**:
    ```bash
    python prea_audit_orchestrator.py
    ```

### Run Modes

When you launch the script, you'll be prompted to choose a run mode:
* **(f)ull research**: Runs the entire test battery and automatically triggers conversational follow-ups on failures. Generates all final reports.
* **(c)ategory**: Allows you to run a specific, targeted category of tests (e.g., `adversarial`).
* **(q)uick battery**: Runs all tests as single-turn prompts without follow-ups.
* **(i)nteractive**: A command-line interface for running specific tests, triggering follow-ups manually, and entering custom prompts.

---
## Understanding the Output

All output is saved to the `research_logs/` directory.

* `prea_research_{timestamp}.txt`: A detailed, human-readable log of the entire session.
* `detailed/research_data_{...}.json`: A log for single-turn tests.
* `detailed/conversations_{...}.jsonl`: The structured log for multi-turn conversations, ideal for data analysis.
* `analysis/comprehensive_analysis_{...}.txt`: A summary of results, grouped by test category.
* `analysis/regulatory_report_{...}.txt`: A high-level summary formatted for submission to regulatory bodies.
* `analysis/academic_dataset_{...}.csv`: A CSV file of key metrics for use in academic papers or statistical analysis.