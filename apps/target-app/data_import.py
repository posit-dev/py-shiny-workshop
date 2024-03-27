from pathlib import Path
import pandas as pd

file_path = Path(__file__).parent / "simulated-data.csv"

print("Running!")
df = pd.read_csv(file_path, dtype={"sub_account": str})
df["date"] = pd.to_datetime(df["date"], errors="coerce")
