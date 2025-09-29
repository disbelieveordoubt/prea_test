#!/usr/bin/env python3
"""
Wrapper script to run PREA AI Safety Research Suite in full mode without interactive prompts.
This modifies the original script to run in automated mode.
"""

import sys
import os
import json
import time
from prea_audit_orchestrator import PREAResearchSuite, SocraticFollowUpEngine, SessionState

def main():
    print("🔬 PREA AI Safety Research Suite (Full Automated Mode)")
    print("="*60)
    print("Running full battery of tests automatically...")
    print("="*60)

    session_state = SessionState()
    research = None

    try:
        with open("config.json", "r", encoding="utf-8") as f:
            config = json.load(f)

        research_params = config.get("research_parameters")
        if not research_params:
            print("❌ ERROR: 'research_parameters' key is missing from config.json.")
            exit(1)

        # Get test battery and follow-up sequences
        prea_test_battery_structured = config["prea_test_battery"]
        prea_test_battery_flat = {tn: tc for tests in config['prea_test_battery'].values() for tn, tc in tests.items()}
        follow_up_sequences = config["follow_up_sequences"]

        # Initialize research suite
        research = PREAResearchSuite(
            model_name=research_params.get("model_name", "deepseek-chat"),
            api_base_url=research_params.get("api_base_url", "https://api.deepseek.com/v1"),
            config=config,
            session_state=session_state
        )
        follow_up_engine = SocraticFollowUpEngine(research, follow_up_sequences)

        # Run full research protocol automatically
        print(f"\n🚀 Running FULL RESEARCH PROTOCOL ({len(prea_test_battery_flat)} tests)...")
        test_count = 0

        for test_name, test_config in prea_test_battery_flat.items():
            test_count += 1
            print(f"  [{test_count}/{len(prea_test_battery_flat)}] Running test: {test_name}")

            response, record, _ = research.send_message(
                user_message=test_config['prompt'],
                test_name=test_name,
                test_config=test_config
            )

            if record and record.get('output', {}).get('result') in ['FAIL', 'CRITICAL_FAIL']:
                print(f"    ⚠️  Test failed, running follow-up sequence...")
                follow_up_engine.run_follow_up_sequence(response, record)

            time.sleep(1)

        print(f"\n✅ All {test_count} tests completed. Generating reports...")
        research.generate_all_reports()

        print(f"\n🎉 Full research protocol completed successfully!")
        print(f"📁 Results saved to: {research.session_state.research_logs_dir}")

    except KeyboardInterrupt:
        print("\n⚠️  Research interrupted by user.")
    except Exception as e:
        print(f"\n💥 CRITICAL ERROR: {e}")
        if research:
            print(f"📁 Partial results saved to: {research.session_state.research_logs_dir}")
    finally:
        print("\n👋 Research session finished.")

if __name__ == "__main__":
    main()