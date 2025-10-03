# Model Launcher Instructions

This guide explains how to use the `launch.bat` script to switch between the default Claude models and the Zhipu AI GLM-4 models.

## Prerequisites

1.  **Zhipu AI API Key:** You need an API key from Zhipu AI.
    *   **Your Zhipu AI API Key:** `PASTE_YOUR_ZHIPU_AI_API_KEY_HERE`

## Usage

Open your terminal in this directory (`H:\Dropbox\Redteam\prea_test`).

### To Launch with GLM-4 Models:

Run the following command:

```sh
launch.bat glm
```

The first time you run this, the script will ask for your Zhipu AI API key. Paste it in and press Enter. The script will remember the key for the rest of your terminal session.

### To Launch with Default Claude Models:

Run the following command:

```sh
launch.bat claude
```

This will start the tool using its standard web-based authentication.