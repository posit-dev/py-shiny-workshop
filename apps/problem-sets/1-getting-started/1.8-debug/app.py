from shiny.express import render, ui, input
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

ui.h2("Hello Penguins!")

ui.input_slider(
    "mass",
    "Mass",
    2000,
    8000,
    6000,
)


@render.data_frame
def table():
    df = penguins.copy()
    filtered = df.loc[df["body_mass"] < input.mass]
    summary = (
        filtered.set_index("species")
        .groupby(level="species")
        .agg({"bill_length": "mean", "bill_depth": "mean"})
        .reset_index()
    )
    return summary
