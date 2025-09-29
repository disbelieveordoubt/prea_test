#!/usr/bin/env python3

import openai
import os
import time

def test_deepseek_api_detailed():
    """Test the DeepSeek API connection with the exact same parameters as the orchestrator."""

    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY environment variable not set")
        return

    print(f"API Key: {api_key[:10]}...")

    # Initialize client with exact same parameters as orchestrator
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )

    # Test with exact same call structure as orchestrator (line 147)
    max_retries = 3
    retry_delay = 5

    for attempt in range(max_retries):
        try:
            print(f"Attempt {attempt + 1}/{max_retries}...")

            messages_to_send = [{"role": "user", "content": "Hello, this is a test message"}]

            response = client.chat.completions.create(
                model="deepseek-chat",
                messages=messages_to_send,
                max_tokens=2000,
                temperature=0.1
            )

            if not response.choices or not response.choices[0].message:
                raise ValueError("Invalid API response structure.")

            ai_response_content = response.choices[0].message.content
            print("SUCCESS: API call completed")
            print(f"Response: {ai_response_content}")
            return

        except (openai.APIStatusError, openai.APIConnectionError, openai.RateLimitError, ValueError) as e:
            error_type = type(e).__name__
            print(f"  └─ ⚠️  API Error ({error_type}) on attempt {attempt + 1}/{max_retries}. Details: {e}. Retrying...")
            if attempt >= max_retries - 1:
                final_error_msg = f"API call failed after {max_retries} attempts: {e}"
                print(f"FINAL ERROR: {final_error_msg}")
                return
            time.sleep(retry_delay)
            retry_delay *= 2
        except Exception as e:
            print(f"UNEXPECTED ERROR: {type(e).__name__}: {e}")
            return

if __name__ == "__main__":
    test_deepseek_api_detailed()