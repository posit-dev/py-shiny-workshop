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
        return penguins


app = App(app_ui, server)
