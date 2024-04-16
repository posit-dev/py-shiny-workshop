from pathlib import Path
import pandas as pd
import numpy as np

file_path = Path(__file__).parent / "simulated-data.csv"

df = pd.read_csv(file_path, dtype={"sub_account": str})
df["date"] = pd.to_datetime(df["date"], errors="coerce")

