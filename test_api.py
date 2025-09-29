#!/usr/bin/env python3

import openai
import os

def test_deepseek_api():
    """Test the DeepSeek API connection."""

    # Get API key from environment
    api_key = os.environ.get('DEEPSEEK_API_KEY')
    if not api_key:
        print("ERROR: DEEPSEEK_API_KEY environment variable not set")
        return

    print(f"API Key (first 10 chars): {api_key[:10]}...")

    # Initialize client
    client = openai.OpenAI(
        api_key=api_key,
        base_url="https://api.deepseek.com/v1"
    )

    try:
        # Test connection with a simple completion
        print("Testing API connection...")
        response = client.chat.completions.create(
            model="deepseek-chat",
            messages=[
                {"role": "user", "content": "Hello, respond with just 'API test successful'"}
            ],
            max_tokens=10,
            timeout=30
        )

        print("SUCCESS: API connection working")
        print(f"Response: {response.choices[0].message.content}")

    except Exception as e:
        print(f"ERROR: API connection failed: {e}")
        print(f"Error type: {type(e)}")

if __name__ == "__main__":
    test_deepseek_api()