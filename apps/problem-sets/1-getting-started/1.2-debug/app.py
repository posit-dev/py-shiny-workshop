from shiny.express import ui, render
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "model_data.csv"
df = pd.read_csv(infile)
df = df.drop(columns=["text"])


@render.plot
def penguins_df():
    return df
