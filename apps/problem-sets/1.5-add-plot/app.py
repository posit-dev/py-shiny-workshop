from shiny import App, render, ui
import pandas as pd
from pathlib import Path
from plots import dist_plot

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
    ui.output_plot("dist"),
)


def server(input, output, session):
    @output
    @render.data_frame
    def table():
        df = penguins.copy()
        filtered = df.loc[df["Body Mass (g)"] < input.mass()]
        summary = (
            filtered.set_index("Species")
            .groupby(level="Species")
            .agg({"Bill Length (mm)": "mean", "Bill Depth (mm)": "mean"})
            .reset_index()
        )
        return summary

    @output
    @render.plot
    def dist():
        df = penguins.copy()
        filtered = df.loc[df["Body Mass (g)"] < input.mass()]
        return dist_plot(filtered)


app = App(app_ui, server)
