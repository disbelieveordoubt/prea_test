# The Cassler-PREA Safety Audit v8.6

**A Research Suite for Detecting Architectural Vulnerabilities in AI Child Protection Systems**

**Author:** Daniel Cassler
**Contact:** dcassler@gmail.com | [linkedin.com/in/danielvermont](https://linkedin.com/in/danielvermont)
**License:** Apache 2.0

-----

## Overview

This repository contains the complete research suite for the **Cassler-PREA Safety Audit v8.6**, a protocol for identifying and quantifying a systematic architectural vulnerability in large language models where linguistic input patterns override safety-critical reasoning frameworks.

Using the Prison Rape Elimination Act (PREA) as an unambiguous compliance baseline, this research demonstrates that care-associated vocabulary creates semantic activation patterns that probabilistically route AI reasoning away from mandatory child protection standards **before** structural analysis occurs.

### Key Findings

*   **Pre-Reasoning Semantic Routing:** The AI's response quality correlates more strongly with prompt vocabulary than with scenario severity.
*   **Demographic Pattern Matching:** Compliance failures cluster in the exact demographic pattern documented by the Bureau of Justice Statistics (95% female staff, male youth victims in juvenile facilities).
*   **Meta-Cognitive Blindness:** AI systems misdiagnose the problem as "gender bias," cannot identify the linguistic triggers, and repeat the same failures.

## Getting Started

### Prerequisites

*   Python 3.8+
*   An API key from a supported LLM provider (e.g., DeepSeek, OpenAI, Anthropic)

### Installation

1.  Clone the repository:
    ```bash
    git clone https://github.com/your-username/prea_test.git
    cd prea_test
    ```
2.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```

### Execution

1.  Set your API key as an environment variable.

    **For bash/zsh:**
    ```bash
    export DEEPSEEK_API_KEY='your-api-key-here'
    ```

    **For Windows PowerShell:**
    ```powershell
    $env:DEEPSEEK_API_KEY='your-api-key-here'
    ```

2.  Run the audit using the canonical entrypoint:
    ```bash
    python prea_audit_orchestrator.py
    ```
    The script will then prompt you to choose a run mode (e.g., full, category, selected, or interactive).

## Methodology

The full research protocol, including the theoretical framework, complete test prompts, and semantic gradient detection algorithms, is available in the root of this repository:

*   **[CASSLER_PREA_AUDIT_v8-6.md](CASSLER_PREA_AUDIT_v8-6.md)**: The main research document, providing a comprehensive overview of the methodology, findings, and regulatory implications.
*   **[appendices.md](appendices.md)**: A consolidated document containing all technical appendices, including test prompts, theoretical framework, and algorithms.

## Citation

If you use this research or methodology, please cite it as follows:

```
Cassler, D. (2025). The Cassler-PREA Safety Audit v8.6: A Protocol for
Detecting Architectural Vulnerabilities in AI Child Protection Systems.
Independent Research.
```

A `CITATION.cff` file is also provided for easy citation.

## License

This project is licensed under the Apache 2.0 License. See the [LICENSE](LICENSE) file for details.