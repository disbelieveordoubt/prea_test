-----

# PREA AI Safety Research Suite (Hybrid v2.1)

**Author: Daniel Cassler**

-----

## Overview 🎯

This project provides a comprehensive, automated tool for conducting AI safety research into "Framework Hijacking" vulnerabilities in Large Language Models (LLMs). This hybrid version merges a robust, user-friendly workflow with an advanced modular detection architecture for practical, iterative research by a solo operator.

**Core Philosophy**: This tool is designed as a **deterministic data collection engine**. It does not "reason" about AI responses in a subjective way. Instead, it robotically sorts, matches keywords, and applies a transparent scoring rubric defined in `config.json`. Its primary purpose is to generate rich, structured, and machine-readable logs. The ultimate, nuanced analysis of these logs is intended to be performed by a more powerful, external AI model (such as Gemini).

-----

## Key Features ✨

  * **Advanced Modular Detection**: Utilizes a suite of specific, extensible detectors for nuanced vulnerability analysis, including `TherapeuticFraming`, `ThoughtTermination`, `VictimAgency`, `ConceptualInversion`, and `EpistemicCapture`.
  * **Researcher-Friendly Workflow**: Features multiple run modes, including a full protocol (`f`), category-specific tests (`c`), a curated set of selected tests (`s`), and a full interactive command-line interface (`i`).
  * **Config-Driven Follow-Ups**: Automatically runs the most relevant Socratic follow-up sequence based on detected failures or custom metadata tags in the `config.json` file.
  * **Fully Configurable Engine**: All critical parameters—test prompts, keywords, model name, API endpoint, and the entire scoring rubric—are controlled via `config.json` for maximum flexibility without code changes.
  * **Rich, Actionable Logging**: Generates multiple organized outputs, including a human-readable text log, a detailed JSON log with raw detector outputs for each test, and a final academic-ready `.csv` dataset.

-----

## Setup & Usage 🚀

### 1\. Install Dependencies

Ensure you have Python 3.7+ installed. From your terminal in the project directory, run:

```bash
pip install -r requirements.txt
```

### 2\. Set Your API Key

The script is designed for OpenAI-compatible APIs. Set an environment variable (recommended):

```bash
export DEEPSEEK_API_KEY='your-api-key-here'
```

Alternatively, the script will prompt you to enter the key on its first run.

### 3\. Configure Your Research

Before running, open `config.json` and set your desired `model_name` and `api_base_url` in the `research_parameters` section.

### 4\. Run the Script

```bash
python prea_audit_orchestrator.py
```

-----

## Run Modes ⚙️

When you launch the script, you will be prompted to choose a run mode:

  * **(f)ull**: Runs the entire test battery with intelligent Socratic follow-ups triggered on failures. Generates all final reports.
  * **(c)ategory**: Allows you to run a specific, targeted category of tests (e.g., `_CORE_VULNERABILITY_TESTS`).
  * **(s)elected**: Runs a curated list of high-value diagnostic tests, which you can define in `config.json`.
  * **(i)nteractive**: A command-line interface for running specific tests by name, manually triggering follow-ups, and generating reports.

-----

## Configuration (`config.json`) 🔧

The `config.json` file is the central control panel for the entire research suite.

  * **`research_parameters`**: Set the `model_name`, the `api_base_url`, and define the list of `selected_tests` for the `(s)` run mode.
  * **`prea_test_battery`**: Define all test categories and individual test prompts. Use `test_metadata` to add custom tags, like `"trigger_follow_up": "demographic_analysis"`, to control the follow-up engine.
  * **`follow_up_sequences`**: Write and manage the multi-turn conversational scripts used by the Socratic Follow-Up Engine.
  * **`detection_keywords`**: Manage the keyword lists (`care_indicators`, `legal_indicators`, etc.) that the detectors use to identify different language types.
  * **`scoring_configuration`**: Calibrate the entire scoring engine by adjusting the `weights` for penalties and rewards, and the `thresholds` for PASS/FAIL results.

-----

## Output Structure 📂

All output is saved to the `research_logs/` directory, organized by session timestamp.

  * `prea_research_{timestamp}.txt`: A detailed, human-readable log of the entire session, including full prompts and responses.
  * `detailed/research_data_{timestamp}.json`: The primary data artifact. A machine-readable log where each line is a JSON object containing the complete data for a single test, including raw detector outputs.
  * `analysis/comprehensive_analysis_{...}.txt`: A summary of results, grouped by test category, showing average scores, fail rates, and the most common failure patterns.
  * `analysis/academic_dataset_{...}.csv`: A CSV file of key metrics (including the `care_ratio`) suitable for academic papers or statistical analysis.

-----

## Extending the Tool 🧑‍💻

This suite is designed to be extensible. To add a new vulnerability detector:

1.  **Create a New Detector Class**: In `prea_audit_orchestrator.py`, create a new class that inherits from the `VulnerabilityDetector` abstract base class.
2.  **Implement the `name` and `detect` Methods**:
      * `name`: Must be a unique string (e.g., `"new_vulnerability"`).
      * `detect`: Must contain your logic for analyzing the response text and return a dictionary containing at least a `'detected': bool` and `'pattern': str` key.
3.  **Add the Detector to the Suite**: In the `PREAResearchSuite.__init__` method, simply add an instance of your new class to the `self.detectors` list.
4.  **Update the Config**: Add a corresponding penalty weight (e.g., `"new_vulnerability_penalty": -20`) to the `scoring_configuration.weights` section in `config.json` to integrate it into the scoring rubric.