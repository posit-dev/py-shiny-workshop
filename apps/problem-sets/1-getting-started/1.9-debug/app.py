from shiny import App, render, ui
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

app_ui = ui.page_fluid(
    ui.h2("Hello Penguins!"),
    ui.input_slider(
        "mass",
        "Mass",
        2000,
        8000,
        6000,
    ),
    ui.output_data_frame("table"),
)


def server(input, output, session):
    df = penguins.copy()
    filtered = df.loc[df["body_mass"] < input.mass()]

    @output
    @render.data_frame
    def table():
        summary = (
            filtered.set_index("species")
            .groupby(level="species")
            .agg({"bill_length": "mean", "bill_depth": "mean"})
            .reset_index()
        )
        return summary


app = App(app_ui, server)
