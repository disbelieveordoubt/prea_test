import pandas as pd
from pathlib import Path

# Find the most recent research session directory
log_dir = Path('./research_logs')
session_dirs = sorted([d for d in log_dir.iterdir() if d.is_dir() and d.name.startswith('202')],
                      key=lambda p: p.stat().st_mtime, reverse=True)

if not session_dirs:
    raise FileNotFoundError("No research session directories found in research_logs/")

latest_session = session_dirs[0]

# Find the CSV file in the latest session
csv_files = list(latest_session.glob('research_dataset_*.csv'))

if not csv_files:
    raise FileNotFoundError(f"No CSV file found in {latest_session.name}/")

csv_path = csv_files[0]
print(f"Loading: {latest_session.name}/{csv_path.name}\n")

# Load the research dataset
df = pd.read_csv(csv_path)

# Display available columns and basic info
print(f"Total records: {len(df)}")
print(f"\nColumns available: {list(df.columns)}")
print(f"\n{df.head()}")