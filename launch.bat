@echo off
SETLOCAL

IF /I "%1"=="glm" (
    ECHO --- Configuring for GLM-4 ---
    REM Set the base URL to point to the Zhipu/Z.AI API endpoint
    SET "ANTHROPIC_BASE_URL=https://api.z.ai/api/paas/v4/"

    REM Set the specific GLM models to override the default Claude models
    SET "ANTHROPIC_DEFAULT_HAIKU_MODEL=glm-4.5-air"
    SET "ANTHROPIC_DEFAULT_SONNET_MODEL=glm-4.6"
    SET "ANTHROPIC_DEFAULT_OPUS_MODEL=glm-4.6"
    
    REM Prompt for the Zhipu API key if not already set in the session
    IF NOT DEFINED ZHIPU_API_KEY (
        SET /p "ZHIPU_API_KEY=Please enter your Zhipu AI API Key: "
    )
    REM Set the API key for the tool to use
    SET "ANTHROPIC_API_KEY=%ZHIPU_API_KEY%"
    
    ECHO Starting Claude Code with GLM-4 configuration...

) ELSE IF /I "%1"=="claude" (
    ECHO --- Configuring for default Claude ---
    REM Clear the environment variables to revert to default behavior
    SET ANTHROPIC_BASE_URL=
    SET ANTHROPIC_API_KEY=
    SET ANTHROPIC_DEFAULT_HAIKU_MODEL=
    SET ANTHROPIC_DEFAULT_SONNET_MODEL=
    SET ANTHROPIC_DEFAULT_OPUS_MODEL=
    ECHO Starting Claude Code with default web-auth configuration...

) ELSE (
    ECHO Invalid argument. Use 'glm' or 'claude'.
    GOTO :EOF
)

REM Launch the claude-code toolclaude
ENDLOCAL