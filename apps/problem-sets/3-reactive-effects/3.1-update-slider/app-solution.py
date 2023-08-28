from shiny import App, render, ui, reactive
import pandas as pd
from pathlib import Path

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
            ui.input_action_button("reset", "Reset Slider"),
        ),
        ui.panel_main(
            ui.output_data_frame("table"),
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

    @reactive.Effect
    @reactive.event(input.reset)
    def _reset_slider():
        ui.update_slider("mass", value=6000)


app = App(app_ui, server)
