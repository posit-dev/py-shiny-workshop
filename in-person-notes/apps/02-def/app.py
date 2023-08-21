from shiny import App, render, ui
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "data/gapminder2023.csv"
world = pd.read_csv(infile)

app_ui = ui.page_fluid(
    ui.h2("Hello World"),
    ui.output_data_frame("world")
)

def server(input, output, session):
    def ____():
    return world

app = App(app_ui, server)