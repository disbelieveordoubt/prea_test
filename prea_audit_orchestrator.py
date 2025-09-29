"""
PREA AI Safety Research Orchestrator v3.0 - Production Ready
Author: Daniel Cassler

This script is a "dumb robot" that:
1. Sends prompts from config.json
2. Detects linguistic patterns in responses
3. Logs everything for external AI analysis
4. Triggers appropriate follow-up sequences
5. DOES NOT SCORE - just collects data

Production improvements:
- Robust error handling
- Safe JSON logging
- Capped exponential backoff
- Config validation
- Empty result protection
"""
import openai
import datetime
import os
import time
import json
import csv
from collections import defaultdict
from typing import Dict, List, Any, Tuple, Optional

# =================================================================================
# Session State Tracker
# =================================================================================

class SessionState:
    def __init__(self) -> None:
        self.completed_successfully: bool = False
        self.error_message: Optional[str] = None
        self.research_logs_dir: Optional[str] = None

# =================================================================================
# PATTERN DETECTOR (NO SCORING)
# =================================================================================

class PatternDetector:
    """Simple pattern detection - no scoring, just identification"""
    
    def __init__(self, keywords: Dict[str, List[str]]):
        self.keywords = keywords
    
    def detect_patterns(self, response: str) -> Dict[str, Any]:
        """Detect all relevant patterns in the response - with error handling"""
        try:
            response_lower = response.lower()
            
            detected = {
                "prea_compliance": self._detect_pattern(response_lower, "prea_compliance_indicators"),
                "care_ethics_language": self._detect_pattern(response_lower, "care_ethics_language"),
                "grooming_language": self._detect_pattern(response_lower, "grooming_language"),
                "thought_termination": self._detect_pattern(response_lower, "thought_termination_failures"),
                "victim_agency": self._detect_pattern(response_lower, "victim_agency_attribution"),
                "adult_focus": self._detect_pattern(response_lower, "adult_focus_inversion"),
                "epistemic_capture": self._detect_pattern(response_lower, "epistemic_capture_phrases")
            }
            
            # Calculate simple ratios for reference
            prea_count = len(detected["prea_compliance"]["matched_terms"])
            care_count = len(detected["care_ethics_language"]["matched_terms"])
            total = prea_count + care_count
            
            detected["ratios"] = {
                "prea_mentions": prea_count,
                "care_mentions": care_count,
                "care_ratio": care_count / total if total > 0 else 0.0
            }
            
            return detected
        
        except Exception as e:
            print(f"  WARNING: Pattern detection error: {e}")
            # Return safe empty structure
            return {
                "error": str(e),
                "prea_compliance": {"detected": False, "matched_terms": [], "count": 0},
                "care_ethics_language": {"detected": False, "matched_terms": [], "count": 0},
                "grooming_language": {"detected": False, "matched_terms": [], "count": 0},
                "thought_termination": {"detected": False, "matched_terms": [], "count": 0},
                "victim_agency": {"detected": False, "matched_terms": [], "count": 0},
                "adult_focus": {"detected": False, "matched_terms": [], "count": 0},
                "epistemic_capture": {"detected": False, "matched_terms": [], "count": 0},
                "ratios": {"prea_mentions": 0, "care_mentions": 0, "care_ratio": 0.0}
            }
    
    def _detect_pattern(self, text: str, keyword_category: str) -> Dict[str, Any]:
        """Detect a specific pattern category"""
        keywords = self.keywords.get(keyword_category, [])
        matched = [kw for kw in keywords if kw.lower() in text]
        
        return {
            "detected": len(matched) > 0,
            "matched_terms": matched,
            "count": len(matched)
        }

# =================================================================================
# RESEARCH SUITE (SIMPLIFIED)
# =================================================================================

class PREAResearchSuite:
    """Simplified orchestrator - pattern detection and logging only"""
    
    def __init__(self, model_name: str, api_base_url: str, config: Dict[str, Any], 
                 session_state: SessionState, api_key: str) -> None:
        self.session_state = session_state
        self.client = openai.OpenAI(api_key=api_key, base_url=api_base_url)
        self.model_name = model_name
        self.config = config
        
        # Initialize pattern detector
        keywords = config.get('detection_keywords', {})
        self.detector = PatternDetector(keywords)
        
        self.session_id: str = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        self.setup_logging()
        self.test_counter: int = 0
        self.test_categories: Dict[str, List[Dict]] = defaultdict(list)
    
    def setup_logging(self) -> None:
        """Create log directory and files"""
        self.session_dir = f"research_logs/{self.session_id}"
        os.makedirs(self.session_dir, exist_ok=True)
        self.session_state.research_logs_dir = self.session_dir
        
        self.log_file = f"{self.session_dir}/session_log_{self.session_id}.txt"
        self.json_log = f"{self.session_dir}/detailed_results_{self.session_id}.jsonl"
        self.analysis_file = f"{self.session_dir}/pattern_analysis_{self.session_id}.txt"
        self.dataset_file = f"{self.session_dir}/research_dataset_{self.session_id}.csv"
        
        with open(self.log_file, "w", encoding="utf-8") as f:
            f.write(f"PREA AI Safety Research Session: {self.session_id}\n" + "="*80 + "\n")
            f.write("MODE: Pattern Detection Only (No Scoring)\n" + "="*80 + "\n\n")
        
        print(f"Research logs initialized in: '{self.session_dir}/'")
    
    def send_message(self, user_message: str, test_name: Optional[str] = None, 
                    test_config: Dict = {}, conversation_history: Optional[List[Dict]] = None,
                    is_follow_up: bool = False) -> Tuple[str, Dict, List[Dict]]:
        """Send message and analyze response patterns"""
        self.test_counter += 1
        test_id = f"{self.test_counter:02d}_{test_name}" if test_name else f"custom_{self.test_counter:02d}"
        
        print(f"\n{'='*60}\nTEST: {test_id}\n{'='*60}")
        
        max_retries = 3
        retry_delay = 5
        
        for attempt in range(max_retries):
            try:
                messages_to_send = list(conversation_history) if conversation_history else []
                messages_to_send.append({"role": "user", "content": user_message})
                
                response = self.client.chat.completions.create(
                    model=self.model_name,
                    messages=messages_to_send,
                    max_tokens=2000,
                    temperature=0.1
                )
                
                if not response.choices or not response.choices[0].message:
                    raise ValueError("Invalid API response structure.")
                
                ai_response_content = response.choices[0].message.content
                
                # Pattern detection (no scoring)
                patterns = self.detector.detect_patterns(ai_response_content)
                
                # Build research record
                research_record = {
                    'test_id': test_id,
                    'test_name': test_name,
                    'timestamp': datetime.datetime.now().isoformat(),
                    'test_category': test_config.get('test_category', 'general'),
                    'theoretical_construct': test_config.get('test_metadata', {}).get('theoretical_construct', 'unknown'),
                    'input': {
                        'prompt': user_message,
                        'test_config': test_config
                    },
                    'output': {
                        'response': ai_response_content,
                        'word_count': len(ai_response_content.split()),
                        'quality_status': self._validate_response_quality(ai_response_content)
                    },
                    'detected_patterns': patterns
                }
                
                # Log everything
                self.test_categories[test_config.get('test_category', 'general')].append(research_record)
                
                # Safe JSON logging with proper escaping
                with open(self.json_log, "a", encoding="utf-8") as f:
                    f.write(json.dumps(research_record, ensure_ascii=False) + "\n")
                
                self._log_research_record(research_record, is_follow_up)
                self._display_test_summary(research_record)
                
                messages_to_send.append({"role": "assistant", "content": ai_response_content})
                
                return ai_response_content, research_record, messages_to_send
            
            except (openai.APIStatusError, openai.APIConnectionError, openai.RateLimitError, ValueError) as e:
                error_type = type(e).__name__
                print(f"  API Error ({error_type}) on attempt {attempt + 1}/{max_retries}. Details: {e}")
                
                if attempt >= max_retries - 1:
                    final_error_msg = f"API call failed for {test_id} after {max_retries} attempts: {e}"
                    self._log_error({'test_id': test_id, 'error': str(e), 'details': final_error_msg})
                    raise RuntimeError(final_error_msg) from e
                
                # Capped exponential backoff
                time.sleep(retry_delay)
                retry_delay = min(retry_delay * 2, 30)  # Cap at 30 seconds
            
            except Exception as e:
                error_details = f"Unexpected fatal error in {test_id}: {e}"
                self._log_error({'test_id': test_id, 'error': str(e), 'details': error_details})
                raise RuntimeError(error_details) from e
        
        raise RuntimeError("Exited retry loop unexpectedly.")
    
    def _validate_response_quality(self, response: str) -> str:
        """Simple quality check"""
        if len(response.split()) < 40:
            return "INSUFFICIENT_RESPONSE"
        if response.lower().count("i cannot") > 1:
            return "EXCESSIVE_REFUSAL"
        if "as an ai" in response.lower():
            return "META_CONTAMINATION"
        return "VALID"
    
    def _display_test_summary(self, record: Dict[str, Any]) -> None:
        """Display pattern detection summary"""
        patterns = record['detected_patterns']
        print("." * 60)
        print(f"  [ PATTERN DETECTION SUMMARY ]")
        print(f"    Test ID: {record['test_id']}")
        print(f"    PREA Language: {patterns.get('prea_compliance', {}).get('count', 0)} mentions")
        print(f"    Care Language: {patterns.get('care_ethics_language', {}).get('count', 0)} mentions")
        print(f"    Care Ratio: {patterns.get('ratios', {}).get('care_ratio', 0.0):.0%}")
        print(f"    Patterns Detected:")
        for pattern_name, pattern_data in patterns.items():
            if pattern_name not in ["ratios", "error"] and isinstance(pattern_data, dict) and pattern_data.get("detected"):
                print(f"      - {pattern_name}: {pattern_data.get('count', 0)} matches")
        print("." * 60)
    
    def _log_research_record(self, record: Dict[str, Any], indent: bool = False) -> None:
        """Write to human-readable log"""
        prefix = "    " if indent else ""
        patterns = record['detected_patterns']
        
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"{prefix}TEST: {record['test_id']} @ {record['timestamp']}\n")
            f.write(f"{prefix}CONSTRUCT: {record['theoretical_construct']}\n")
            f.write(f"{prefix}PREA MENTIONS: {patterns.get('prea_compliance', {}).get('count', 0)}\n")
            f.write(f"{prefix}CARE MENTIONS: {patterns.get('care_ethics_language', {}).get('count', 0)}\n")
            f.write(f"{prefix}CARE RATIO: {patterns.get('ratios', {}).get('care_ratio', 0.0):.0%}\n\n")
            f.write(f"{prefix}PROMPT:\n{prefix}{record['input']['prompt']}\n\n")
            f.write(f"{prefix}RESPONSE:\n{prefix}{record['output']['response']}\n\n")
            f.write(f"{'='*80}\n\n")
    
    def _log_error(self, error_record: Dict[str, Any]) -> None:
        """Log errors"""
        with open(self.log_file, "a", encoding="utf-8") as f:
            f.write(f"ERROR: {error_record.get('test_id', 'N/A')} @ {datetime.datetime.now().isoformat()}\n")
            f.write(f"DETAILS: {error_record.get('error')}\n{error_record.get('details', '')}\n\n")
    
    def display_session_summary(self) -> None:
        """Display session summary"""
        print("\n" + "=" * 60)
        
        if not self.session_state.completed_successfully:
            print("SESSION INCOMPLETE")
            print(f"ERROR: {self.session_state.error_message}\n")
        else:
            print("SESSION COMPLETE")
        
        print("=" * 60)
        
        if not self.test_categories:
            print("\nNo tests were run in this session.")
            return
        
        all_results = [res for cat_res in self.test_categories.values() for res in cat_res]
        total_tests = len(all_results)
        
        print(f"\nTotal Tests Run: {total_tests}")
        print(f"\nPattern Detection Summary:")
        print(f"  (See detailed logs in: {self.session_dir}/)")
        print("=" * 60)
    
    def generate_pattern_analysis(self) -> None:
        """Generate pattern analysis report"""
        if not any(self.test_categories.values()):
            print("WARNING: No data to analyze")
            return
        
        with open(self.analysis_file, "w", encoding="utf-8") as f:
            f.write(f"PATTERN DETECTION ANALYSIS - {self.session_id}\n" + "="*50 + "\n\n")
            f.write("NOTE: This is raw pattern detection data.\n")
            f.write("Scoring and interpretation should be done by external AI analysis.\n\n")
            
            for category, results in self.test_categories.items():
                if not results:
                    continue
                
                f.write(f"\nCATEGORY: {category.upper()}\n" + "-"*30 + "\n")
                f.write(f"Tests in category: {len(results)}\n\n")
                
                for result in results:
                    patterns = result['detected_patterns']
                    f.write(f"  {result['test_id']} ({result['theoretical_construct']})\n")
                    f.write(f"    PREA: {patterns.get('prea_compliance', {}).get('count', 0)} | ")
                    f.write(f"Care: {patterns.get('care_ethics_language', {}).get('count', 0)} | ")
                    f.write(f"Ratio: {patterns.get('ratios', {}).get('care_ratio', 0.0):.0%}\n")
        
        print(f"Pattern analysis saved to: {self.analysis_file}")
    
    def generate_csv_dataset(self) -> None:
        """Generate CSV for external analysis"""
        if not any(self.test_categories.values()):
            print("WARNING: No data to export to CSV")
            return
        
        with open(self.dataset_file, "w", newline='', encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow([
                'test_id', 'test_name', 'category', 'construct',
                'prea_mentions', 'care_mentions', 'care_ratio',
                'grooming_detected', 'victim_agency_detected',
                'epistemic_capture_detected', 'prompt_snippet'
            ])
            
            for category, results in self.test_categories.items():
                for result in results:
                    p = result['detected_patterns']
                    writer.writerow([
                        result['test_id'],
                        result['test_name'],
                        category,
                        result['theoretical_construct'],
                        p.get('prea_compliance', {}).get('count', 0),
                        p.get('care_ethics_language', {}).get('count', 0),
                        f"{p.get('ratios', {}).get('care_ratio', 0.0):.2f}",
                        p.get('grooming_language', {}).get('detected', False),
                        p.get('victim_agency', {}).get('detected', False),
                        p.get('epistemic_capture', {}).get('detected', False),
                        result['input']['prompt'][:100]
                    ])
        
        print(f"CSV dataset saved to: {self.dataset_file}")

# =================================================================================
# FOLLOW-UP ENGINE
# =================================================================================

class SocraticFollowUpEngine:
    def __init__(self, parent_suite: "PREAResearchSuite", follow_up_sequences: Dict[str, List[str]]) -> None:
        self.parent = parent_suite
        self.follow_up_sequences = follow_up_sequences
    
    def should_run_follow_up(self, record: Dict) -> bool:
        """Check if follow-up is needed based on metadata - FIXED"""
        trigger = record.get('input', {}).get('test_config', {}).get('test_metadata', {}).get('trigger_follow_up')
        # Fix: properly check for none/empty
        return trigger not in [None, "none", "", "None"]
    
    def run_follow_up_sequence(self, initial_response: str, initial_record: Dict, max_follow_ups: int = 3) -> None:
        """Run appropriate follow-up sequence"""
        trigger = initial_record.get('input', {}).get('test_config', {}).get('test_metadata', {}).get('trigger_follow_up')
        
        if not trigger or trigger in ["none", "", "None"]:
            return
        
        follow_ups = self.follow_up_sequences.get(trigger, [])
        
        if not follow_ups:
            print(f"WARNING: No follow-up sequence found for trigger: {trigger}")
            return
        
        print(f"\nINFO: Initiating '{trigger}' follow-up sequence...")
        
        messages_history = [
            {"role": "user", "content": initial_record['input']['prompt']},
            {"role": "assistant", "content": initial_response}
        ]
        
        for i, follow_up_prompt in enumerate(follow_ups[:max_follow_ups]):
            print(f"\n{'-' * 60}\nFOLLOW-UP {i + 1}/{len(follow_ups)}\n{'-' * 60}")
            
            try:
                _, _, messages_history = self.parent.send_message(
                    user_message=follow_up_prompt,
                    test_name=f"{initial_record['test_name']}_followup_{i+1}",
                    test_config=initial_record.get('input', {}).get('test_config', {}),
                    conversation_history=messages_history,
                    is_follow_up=True
                )
                
                time.sleep(1)
            
            except Exception as e:
                print(f"ERROR in follow-up {i+1}: {e}")
                print("Continuing with remaining follow-ups...")
                continue

# =================================================================================
# ORCHESTRATOR
# =================================================================================

class Orchestrator:
    def __init__(self, config_path: str = "config.json") -> None:
        self.session_state = SessionState()
        self.research_suite: Optional[PREAResearchSuite] = None
        self._load_config(config_path)
        self._validate_config()
        self._setup_components()
    
    def run(self) -> None:
        """Main execution flow"""
        try:
            mode = self._get_run_mode()
            
            if mode == 'f':
                self._run_full_protocol()
            elif mode == 'c':
                self._run_category()
            elif mode == 's':
                self._run_selected()
            elif mode == 'i':
                self._run_interactive()
            
            if mode != 'quit':
                self.session_state.completed_successfully = True
        
        except (Exception, KeyboardInterrupt) as e:
            print(f"\n\nCRITICAL ERROR: An exception terminated the run: {e}")
            self.session_state.error_message = str(e)
            self.session_state.completed_successfully = False
        
        finally:
            if self.research_suite:
                print("\nResearch session finished.")
                self.research_suite.display_session_summary()
    
    def _load_config(self, config_path: str) -> None:
        """Load configuration from JSON"""
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self.config = json.load(f)
        except FileNotFoundError:
            raise ValueError(f"Config file not found: {config_path}")
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON in config file: {e}")
        
        self.research_params = self.config.get("research_parameters")
        if not self.research_params:
            raise ValueError("Config missing 'research_parameters'.")
        
        self.prea_test_battery_structured = self.config.get("prea_test_battery", {})
        self.prea_test_battery_flat = {
            tn: tc 
            for tests in self.prea_test_battery_structured.values() 
            for tn, tc in tests.items()
        }
        self.follow_up_sequences = self.config.get("follow_up_sequences", {})
    
    def _validate_config(self) -> None:
        """Validate configuration has required keys"""
        required_keys = ['research_parameters', 'detection_keywords', 'prea_test_battery', 'follow_up_sequences']
        missing = [k for k in required_keys if k not in self.config]
        
        if missing:
            raise ValueError(f"Config missing required keys: {missing}")
        
        if not self.prea_test_battery_flat:
            raise ValueError("No tests defined in prea_test_battery")
        
        print(f"Config validated: {len(self.prea_test_battery_flat)} tests loaded")
    
    def _setup_components(self) -> None:
        """Initialize research suite and follow-up engine"""
        api_key = self._get_api_key()
        
        self.research_suite = PREAResearchSuite(
            model_name=self.research_params.get("model_name", "deepseek-chat"),
            api_base_url=self.research_params.get("api_base_url", "https://api.deepseek.com/v1"),
            config=self.config,
            session_state=self.session_state,
            api_key=api_key
        )
        
        self.follow_up_engine = SocraticFollowUpEngine(
            self.research_suite, 
            self.follow_up_sequences
        )
    
    def _get_api_key(self) -> str:
        """Get API key from environment or user input"""
        api_key = os.getenv('DEEPSEEK_API_KEY')
        if not api_key:
            print("WARNING: DEEPSEEK_API_KEY env variable not set.")
            api_key = input("Please paste your API key: ").strip()
            if not api_key:
                raise ValueError("No API key provided.")
        return api_key
    
    def _get_run_mode(self) -> str:
        """Get run mode from user"""
        while True:
            mode = input("\nRun mode: (f)ull, (c)ategory, (s)elected, (i)nteractive, or (quit): ").strip().lower()
            if mode in ['f', 'c', 's', 'i', 'quit']:
                return mode
            print("Invalid mode selected. Please try again.")
    
    def _run_full_protocol(self) -> None:
        """Run all tests in the battery"""
        print("\nRunning FULL RESEARCH PROTOCOL...")
        print(f"Total tests to run: {len(self.prea_test_battery_flat)}")
        
        completed = 0
        for name, config in self.prea_test_battery_flat.items():
            try:
                response, record, _ = self.research_suite.send_message(
                    user_message=config['prompt'],
                    test_name=name,
                    test_config=config
                )
                
                if record and self.follow_up_engine.should_run_follow_up(record):
                    self.follow_up_engine.run_follow_up_sequence(response, record)
                
                completed += 1
                print(f"\nProgress: {completed}/{len(self.prea_test_battery_flat)} tests completed")
                time.sleep(3)
            
            except Exception as e:
                print(f"ERROR in test {name}: {e}")
                print("Continuing with remaining tests...")
                continue
        
        if self.research_suite:
            self.research_suite.generate_pattern_analysis()
            self.research_suite.generate_csv_dataset()
    
    def _run_category(self) -> None:
        """Run specific category of tests"""
        print("\nAvailable categories:")
        for cat in self.prea_test_battery_structured.keys():
            print(f"  - {cat}")
        
        selected_cat = input("Enter category to run: ").strip()
        
        if selected_cat in self.prea_test_battery_structured:
            print(f"\nRunning category: {selected_cat}")
            
            for test_name, test_config in self.prea_test_battery_structured[selected_cat].items():
                try:
                    response, record, _ = self.research_suite.send_message(
                        user_message=test_config['prompt'],
                        test_name=test_name,
                        test_config=test_config
                    )
                    
                    if record and self.follow_up_engine.should_run_follow_up(record):
                        self.follow_up_engine.run_follow_up_sequence(response, record)
                    
                    time.sleep(3)
                
                except Exception as e:
                    print(f"ERROR in test {test_name}: {e}")
                    print("Continuing with remaining tests...")
                    continue
            
            if self.research_suite:
                self.research_suite.generate_pattern_analysis()
                self.research_suite.generate_csv_dataset()
        else:
            print("Category not found.")
    
    def _run_selected(self) -> None:
        """Run pre-selected high-value tests"""
        selected_tests = self.research_params.get("selected_tests", [])
        
        if not selected_tests:
            print("No tests defined in config.json under 'research_parameters.selected_tests'")
        else:
            print(f"\nRunning {len(selected_tests)} selected tests...")
            
            for test_name in selected_tests:
                if test_name in self.prea_test_battery_flat:
                    test_config = self.prea_test_battery_flat[test_name]
                    try:
                        response, record, _ = self.research_suite.send_message(
                            user_message=test_config['prompt'],
                            test_name=test_name,
                            test_config=test_config
                        )
                        
                        if record and self.follow_up_engine.should_run_follow_up(record):
                            self.follow_up_engine.run_follow_up_sequence(response, record)
                        
                        time.sleep(3)
                    
                    except Exception as e:
                        print(f"ERROR in test {test_name}: {e}")
                        print("Continuing with remaining tests...")
                        continue
                else:
                    print(f"WARNING: Test '{test_name}' not found in config")
            
            if self.research_suite:
                self.research_suite.generate_pattern_analysis()
                self.research_suite.generate_csv_dataset()
    
    def _run_interactive(self) -> None:
        """Interactive mode"""
        print("\n--- Interactive Mode ---")
        print("Commands: <test_name>, list, follow, summary, help, quit")
        
        last_response, last_record = None, None
        
        while True:
            cmd = input("\nCommand: ").strip()
            
            if cmd in ['quit', 'exit']:
                break
            elif cmd == 'help':
                print("Commands: <test_name>, list, follow, summary, help, quit")
            elif cmd == 'list':
                for name in self.prea_test_battery_flat.keys():
                    print(f"  - {name}")
            elif cmd == 'summary':
                if self.research_suite:
                    self.research_suite.generate_pattern_analysis()
                    self.research_suite.generate_csv_dataset()
            elif cmd == 'follow':
                if last_record and last_response:
                    try:
                        self.follow_up_engine.run_follow_up_sequence(last_response, last_record)
                    except Exception as e:
                        print(f"ERROR in follow-up: {e}")
                else:
                    print("No previous test to follow-up on.")
            elif cmd in self.prea_test_battery_flat:
                cfg = self.prea_test_battery_flat[cmd]
                if self.research_suite:
                    try:
                        last_response, last_record, _ = self.research_suite.send_message(
                            user_message=cfg['prompt'],
                            test_name=cmd,
                            test_config=cfg
                        )
                    except Exception as e:
                        print(f"ERROR in test: {e}")
            else:
                print("Unknown command or test name. Type 'list' to see available tests.")

# =================================================================================
# MAIN ENTRYPOINT
# =================================================================================

def main() -> None:
    """Main entrypoint"""
    print("="*60)
    print("PREA AI Safety Research Suite v3.0 - Production Ready")
    print("="*60)
    print("MODE: Pattern Detection Only")
    print("This tool detects linguistic patterns for external AI analysis.")
    print("No scoring is performed by the script.")
    print("="*60)
    
    try:
        orchestrator = Orchestrator()
        orchestrator.run()
    except Exception as e:
        print("\n\n" + "="*60)
        print("FATAL ERROR DURING SCRIPT INITIALIZATION")
        print("="*60)
        print(f"Error: {e}")
        print("="*60)
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()