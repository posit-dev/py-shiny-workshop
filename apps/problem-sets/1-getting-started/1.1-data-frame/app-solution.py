from shiny.express import ui, render
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "simulated-data.csv"
df = pd.read_csv(infile)
df = df.drop(columns=["text"])

# The render.data_frame decorator is used to display dataframes.


@render.data_frame
def penguins_df():
    return df
