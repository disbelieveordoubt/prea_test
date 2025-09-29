#!/usr/bin/env python3
"""
PREA Audit Monitoring Protocol
Real-time monitoring system for active audit sessions
"""

import os
import json
import datetime
from pathlib import Path

class AuditMonitor:
    def __init__(self, research_logs_dir="research_logs"):
        self.research_logs_dir = Path(research_logs_dir)

    def get_latest_session(self):
        """Find the most recent audit session directory"""
        session_dirs = [d for d in self.research_logs_dir.iterdir()
                       if d.is_dir() and d.name.startswith('2025')]
        if not session_dirs:
            return None
        return max(session_dirs, key=lambda x: x.name)

    def check_session_status(self, session_dir=None):
        """Determine if session is active or completed"""
        if session_dir is None:
            session_dir = self.get_latest_session()
            if not session_dir:
                return {"status": "NO_SESSIONS_FOUND"}

        session_log = session_dir / f"session_log_{session_dir.name}.txt"
        detailed_results = session_dir / f"detailed_results_{session_dir.name}.jsonl"

        if not session_log.exists() or not detailed_results.exists():
            return {"status": "INCOMPLETE_SESSION", "session": session_dir.name}

        # Get last modification time
        log_mtime = session_log.stat().st_mtime
        current_time = datetime.datetime.now().timestamp()
        minutes_since_update = (current_time - log_mtime) / 60

        # Count completed tests
        test_count = 0
        if detailed_results.exists():
            with open(detailed_results, 'r') as f:
                test_count = len(f.readlines())

        # Parse latest test info
        latest_test = self._get_latest_test_info(session_log)

        # Determine status
        if minutes_since_update < 2:
            status = "ACTIVE"
        elif minutes_since_update < 10:
            status = "RECENTLY_ACTIVE"
        else:
            status = "COMPLETED"

        return {
            "status": status,
            "session": session_dir.name,
            "tests_completed": test_count,
            "minutes_since_update": round(minutes_since_update, 1),
            "latest_test": latest_test,
            "log_file": str(session_log),
            "detailed_file": str(detailed_results)
        }

    def _get_latest_test_info(self, session_log):
        """Extract latest test information from session log"""
        try:
            with open(session_log, 'r', encoding='utf-8') as f:
                lines = f.readlines()

            # Find most recent test entry
            latest_test = None
            for line in reversed(lines[-50:]):  # Check last 50 lines
                if "TEST:" in line and "@" in line:
                    parts = line.strip().split()
                    if len(parts) >= 4:
                        test_id = parts[1]
                        timestamp = parts[3]
                        latest_test = {
                            "test_id": test_id,
                            "timestamp": timestamp
                        }
                        break
                elif "RESULT:" in line and latest_test:
                    result_parts = line.strip().split()
                    if len(result_parts) >= 2:
                        latest_test["result"] = result_parts[1]
                        if "(" in line and ")" in line:
                            score = line.split("(")[1].split(")")[0]
                            latest_test["score"] = score
                    break

            return latest_test
        except Exception as e:
            return {"error": str(e)}

    def analyze_test_patterns(self, session_dir=None):
        """Analyze failure patterns across tests"""
        if session_dir is None:
            session_dir = self.get_latest_session()
            if not session_dir:
                return {}

        detailed_results = session_dir / f"detailed_results_{session_dir.name}.jsonl"

        if not detailed_results.exists():
            return {}

        patterns = {}
        results_summary = {"PASS": 0, "FAIL": 0, "CRITICAL_FAIL": 0}

        try:
            with open(detailed_results, 'r') as f:
                for line in f:
                    test_data = json.loads(line.strip())

                    # Count results
                    result = test_data.get("output", {}).get("result", "UNKNOWN")
                    if result in results_summary:
                        results_summary[result] += 1

                    # Track failure patterns
                    failure_patterns = test_data.get("output", {}).get("failure_patterns", [])
                    for pattern in failure_patterns:
                        patterns[pattern] = patterns.get(pattern, 0) + 1

        except Exception as e:
            return {"error": str(e)}

        return {
            "results_summary": results_summary,
            "failure_patterns": patterns,
            "total_tests": sum(results_summary.values())
        }

    def estimate_completion(self, session_dir=None):
        """Estimate test completion time based on velocity"""
        if session_dir is None:
            session_dir = self.get_latest_session()
            if not session_dir:
                return {}

        detailed_results = session_dir / f"detailed_results_{session_dir.name}.jsonl"

        if not detailed_results.exists():
            return {}

        try:
            timestamps = []
            with open(detailed_results, 'r') as f:
                for line in f:
                    test_data = json.loads(line.strip())
                    timestamp_str = test_data.get("timestamp")
                    if timestamp_str:
                        # Parse ISO timestamp
                        ts = datetime.datetime.fromisoformat(timestamp_str.replace('T', ' '))
                        timestamps.append(ts)

            if len(timestamps) < 2:
                return {"insufficient_data": True}

            # Calculate average time between tests
            intervals = []
            for i in range(1, len(timestamps)):
                interval = (timestamps[i] - timestamps[i-1]).total_seconds()
                intervals.append(interval)

            avg_interval = sum(intervals) / len(intervals)

            return {
                "tests_completed": len(timestamps),
                "avg_test_interval_seconds": round(avg_interval, 1),
                "first_test": timestamps[0].isoformat(),
                "latest_test": timestamps[-1].isoformat(),
                "estimated_tests_per_hour": round(3600 / avg_interval, 1) if avg_interval > 0 else 0
            }

        except Exception as e:
            return {"error": str(e)}

    def get_full_status_report(self):
        """Generate comprehensive status report"""
        session_status = self.check_session_status()
        if session_status.get("status") == "NO_SESSIONS_FOUND":
            return session_status

        patterns = self.analyze_test_patterns()
        completion = self.estimate_completion()

        return {
            "session_status": session_status,
            "test_patterns": patterns,
            "completion_analysis": completion,
            "generated_at": datetime.datetime.now().isoformat()
        }

if __name__ == "__main__":
    monitor = AuditMonitor()
    report = monitor.get_full_status_report()
    print(json.dumps(report, indent=2))