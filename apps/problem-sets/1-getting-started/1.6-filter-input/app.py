from shiny.express import render, ui
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

ui.h2("Hello Penguins!")


@render.data_frame
def table():
    df = penguins.copy()
    summary = (
        df.set_index("species")
        .groupby(level="species")
        .agg({"bill_length": "mean", "bill_depth": "mean"})
        .reset_index()
    )
    return summary
