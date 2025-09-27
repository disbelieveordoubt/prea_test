-----

# PREA AI Safety Research Orchestrator

creator: Daniel Cassler | github: @disbelieveordoubt | aka: dgcvt

This project provides a comprehensive, automated tool for conducting AI safety research into "Framework Hijacking" vulnerabilities in Large Language Models (LLMs). It uses the federal PREA (Prison Rape Elimination Act) standard as an unambiguous baseline to test and quantify how care-associated language can cause LLMs to fail in critical child protection scenarios.

The core research hypothesis is that LLMs perform semantic disambiguation before structural reasoning, causing care-associated language to probabilistically override legal and analytical frameworks.

-----

## \#\# Features

  * **Systematic PREA Compliance Testing**: Executes a battery of test cases designed to probe for specific reasoning failures.
  * **Automated Socratic Follow-Ups**: Automatically runs multi-turn conversational sequences to test for "Architectural Persistence"—the model's inability to correct its reasoning failures even after meta-cognitive recognition.
  * **Configurable Tests & Models**: The target AI model, test cases, and follow-up questions are all managed in an external `config.json` file, allowing for easy modification without changing the code.
  * **Advanced Heuristic Analysis**: Automatically scores AI responses for PREA compliance and detects "Framework Hijacking" based on linguistic patterns.
  * **Comprehensive Logging**: Generates multiple log files for different analysis needs:
      * A human-readable text log for easy review.
      * A machine-readable `json` log for single-turn tests.
      * A structured `jsonl` log that captures entire conversations as single data objects, perfect for programmatic analysis.

-----

## \#\# Setup & Usage

### \#\#\# Requirements

  * Python 3.7+
  * An API key for an OpenAI-compatible endpoint (tested with DeepSeek).

### \#\#\# Installation & First Run

1.  **Clone the Repository** (or download the files to a single directory):

    ```bash
    git clone <repository_url>
    cd <repository_directory>
    ```

2.  **Install Dependencies**:

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

### \#\#\# Run Modes

When you launch the script, you'll be prompted to choose a run mode:

  * **(f)ull research**: Runs high-priority tests and automatically triggers multi-turn conversational follow-ups on failures. This is the primary mode for deep research.
  * **(q)uick battery**: Runs all tests as single-turn prompts without follow-ups. Useful for establishing a quick baseline on a new model.
  * **(i)nteractive**: A command-line interface for running specific tests, triggering follow-ups manually, and entering custom prompts. Use the `help` and `list` commands to navigate.

-----

## \#\# Project Files

  * `prea_audit_orchestrator.py`: The main research script engine.
  * `config.json`: The configuration file containing all test prompts and follow-up sequences. **This is the file you will edit most often.**
  * `requirements.txt`: A list of the required Python libraries.
  * `README.md`: This file.

## \#\# Understanding the Output

All output is saved to the `research_logs/` directory, which is created automatically.

  * `prea_research_{timestamp}.txt`: A detailed, human-readable log of the entire session. Follow-up questions are indented to show conversational flow.
  * `detailed/research_data_{...}.json`: A machine-readable log where each line is a JSON object representing a single, non-follow-up test.
  * `detailed/conversations_{...}.jsonl`: The most valuable data file for analysis. Each line is a complete JSON object representing an entire conversation, including the initial prompt, all follow-ups, and the final analysis of the AI's behavior pattern.
  * `analysis/follow_up_analysis_{...}.txt`: A high-level summary report of the findings from the multi-turn conversational tests.