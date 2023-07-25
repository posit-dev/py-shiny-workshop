from shiny import App, render, ui, reactive
import pandas as pd
from pathlib import Path
from plots import dist_plot, scatter_plot

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
    ui.input_checkbox("trend", "Add trendline"),
    ui.output_plot("scatter"),
)


def server(input, output, session):
    @reactive.Calc
    def filt_df():
        df = penguins.copy()
        filtered = df.loc[df["Body Mass (g)"] < input.mass()]
        return filtered

    @output
    @render.data_frame
    def table():
        summary = (
            filt_df()
            .set_index("Species")
            .groupby(level="Species")
            .agg({"Bill Length (mm)": "mean", "Bill Depth (mm)": "mean"})
            .reset_index()
        )
        return summary

    @output
    @render.plot
    def dist():
        return dist_plot(filt_df())

    @output
    @render.plot
    def scatter():
        return scatter_plot(filt_df(), input.trend())


app = App(app_ui, server)
