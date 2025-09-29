#!/usr/bin/env python3

import sys
import os
sys.path.append(os.path.dirname(__file__))

from prea_audit_orchestrator import PREAResearchSuite, SessionState
import json

def debug_api_connection():
    """Debug the API connection issue by running a minimal test."""

    # Load config
    with open('config.json', 'r') as f:
        config = json.load(f)

    # Create session state
    session_state = SessionState()

    # Get API key
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY environment variable not set")
        return

    print(f"API Key: {api_key[:10]}...")

    # Initialize research suite
    research_params = config.get("research_parameters")
    model_name = research_params.get("model_name", "deepseek-chat")
    api_base_url = research_params.get("api_base_url", "https://api.deepseek.com/v1")

    print(f"Model: {model_name}")
    print(f"Base URL: {api_base_url}")

    try:
        research_suite = PREAResearchSuite(
            model_name=model_name,
            api_base_url=api_base_url,
            config=config,
            session_state=session_state,
            api_key=api_key
        )

        print("Research suite initialized successfully")

        # Try a simple API call
        print("Testing API call...")
        response, record, conversation = research_suite.send_message(
            "Hello, this is a test",
            test_name="debug_test",
            test_config={"test_category": "debug"}
        )

        print("SUCCESS: API call completed")
        print(f"Response length: {len(response)} characters")
        print(f"First 100 chars: {response[:100]}...")

    except Exception as e:
        print(f"ERROR: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_api_connection()