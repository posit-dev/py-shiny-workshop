from shiny.express import ui, render
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "model_data.csv"
df = pd.read_csv(infile)
df = df.drop(columns=["text"])


# It's important that you use the right decorator for your funciton's return value
# in this case since the function is returning a dataframe we need to use the
# `@render.data_frame` decorator.
@render.data_frame
def penguins_df():
    return df
