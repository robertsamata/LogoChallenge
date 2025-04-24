import pandas as pd

# Path to your Parquet file
input_path = "logos.snappy.parquet"

# Load the parquet file
df = pd.read_parquet(input_path)

# Save as CSV
output_path = "logos.csv"
df.to_csv(output_path, index=False)

print(f"Saved {len(df)} rows to {output_path}")
