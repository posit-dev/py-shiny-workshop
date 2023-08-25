from shiny import App, render, ui
import pandas as pd
from pathlib import Path
from plots import dist_plot, scatter_plot

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

app_ui = ui.page_fluid(
    ui.panel_title("Hello Penguins!"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_slider(
                "mass",
                "Mass",
                2000,
                8000,
                6000,
            ),
            ui.input_checkbox("trend", "Add trendline"),
        ),
        ui.panel_main(
            ui.output_plot("scatter"),
            ui.output_data_frame("table"),
            ui.output_plot("dist"),
        ),
    ),
)


def server(input, output, session):
    @output
    @render.data_frame
    def table():
        df = penguins.copy()
        filtered = df.loc[df["body_mass"] < input.mass()]
        summary = (
            filtered.set_index("species")
            .groupby(level="species")
            .agg({"bill_length": "mean", "bill_depth": "mean"})
            .reset_index()
        )
        return summary

    @output
    @render.plot
    def dist():
        df = penguins.copy()
        filtered = df.loc[df["body_mass"] < input.mass()]
        return dist_plot(filtered)

    @output
    @render.plot
    def scatter():
        df = penguins.copy()
        filtered = df.loc[df["body_mass"] < input.mass()]
        return scatter_plot(filtered, input.trend())


app = App(app_ui, server)
