from shiny.express import ui, render
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "simulated-data.csv"
df = pd.read_csv(infile)
df = df.drop(columns=["text"])


@render.data_frame
def penguins_df():
    return df
