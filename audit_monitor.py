import os
import glob
import re

def get_latest_log_file():
    """Finds the latest session log file."""
    log_dirs = glob.glob("research_logs/20*")
    if not log_dirs:
        return None
    
    latest_dir = max(log_dirs, key=os.path.getmtime)
    
    log_files = glob.glob(os.path.join(latest_dir, "session_log_*.txt"))
    if not log_files:
        return None
        
    return log_files[0]

def get_last_test_info(file_path):
    """Finds the last test run in the log file and returns its info."""
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()
        
        last_test_line_index = -1
        last_test_line = None
        last_construct_line = None
        
        for i in range(len(lines) - 1, -1, -1):
            if lines[i].strip().startswith("TEST:"):
                last_test_line_index = i
                last_test_line = lines[i].strip()
                break

        if last_test_line_index != -1:
            for i in range(last_test_line_index + 1, len(lines)):
                if lines[i].strip().startswith("CONSTRUCT:"):
                    last_construct_line = lines[i].strip()
                    break

        if last_test_line:
            test_info = last_test_line.split('@')[0].replace('TEST:','').strip()
            construct_info = last_construct_line.replace('CONSTRUCT:','').strip() if last_construct_line else "N/A"
            
            test_number_match = re.match(r'(\d+)', test_info)
            test_number = test_number_match.group(1) if test_number_match else "N/A"
            
            summary = f"Test {test_number}: {test_info} ({construct_info})"
            return summary, lines[-15:]
        else:
            return "No test information found in the log.", lines[-15:]

    except FileNotFoundError:
        return f"Error: Log file not found at {file_path}", []
    except Exception as e:
        return f"An error occurred: {e}", []

if __name__ == "__main__":
    latest_log = get_latest_log_file()
    if latest_log:
        print(f"Checking latest log: {latest_log}\n")
        summary, last_lines = get_last_test_info(latest_log)
        print("--- Last Test Summary ---")
        print(summary)
        print("\n--- Last 15 lines of log ---")
        for line in last_lines:
            print(line, end='')
    else:
        print("No log files found.")