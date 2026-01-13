import pandas as pd

# Load your original CSV
df = pd.read_csv("/Applications/PostgreSQL 18/Developer/Tier_1_Project/csv_files/samples.csv")

# Drop the 'notes' column
df = df.drop(columns=["notes"])

# Save the new CSV
df.to_csv("/Applications/PostgreSQL 18/Developer/Tier_1_Project/csv_files/samples.csv", index=False)
print("Saved!")
