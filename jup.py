import pandas as pd
import json

# Replace with your actual filename
file_path = './research_logs/detailed/conversations_20250927_212101.jsonl'

data = []
with open(file_path, 'r', encoding='utf-8') as f:
    for line in f:
        data.append(json.loads(line))

# Load all conversation data into a DataFrame
df = pd.json_normalize(data)

# Now you can easily analyze your results
print(df[['conversation_id', 'final_analysis.research_pattern', 'final_analysis.compliance_improvement']])