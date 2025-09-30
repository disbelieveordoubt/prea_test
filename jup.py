from pandas_smart_loader import load_prea_data_simple
import pandas as pd

# Load data using the smart loader (avoids 3000+ column explosion!)
df = load_prea_data_simple()

# Display basic info
print("\n" + "="*70)
print("QUICK ANALYSIS")
print("="*70)

print("\nColumns available:")
for i, col in enumerate(df.columns, 1):
    print(f"  {i:2d}. {col}")

print("\n\nFirst 3 records:")
print(df.head(3))

print("\n\nBasic statistics:")
print(f"  Total tests: {len(df)}")
print(f"  Average response time: {df['response_time'].mean():.2f}s")
print(f"  Average word count: {df['word_count'].mean():.0f}")
print(f"  Framework hijacking detected: {df['framework_hijacking'].sum()} cases")

print("\n\nTest categories:")
print(df['test_category'].value_counts())

print("\n\nDominant frameworks:")
print(df['dominant_framework'].value_counts())