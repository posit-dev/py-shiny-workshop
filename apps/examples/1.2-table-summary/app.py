from shiny import App, render, ui
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

app_ui = ui.page_fluid(
    ui.h2("Hello Penguins!"),
    ui.output_data_frame("table"),
)


def server(input, output, session):
    @output
    @render.data_frame
    def table():
        summary = (
            penguins.copy()
            .set_index("Species")
            .groupby(level="Species")
            .agg({"Bill Length (mm)": "mean", "Bill Depth (mm)": "mean"})
            .reset_index()
        )
        return summary


app = App(app_ui, server)
