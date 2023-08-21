from shiny import App, render, ui
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "data/gapminder2023.csv"
world = pd.read_csv(infile)

app_ui = ui.page_fluid(
    ui.h2("Hello World"),
    ui.input_select(
        "region", 
        "Select a region",
        ["Americas", "Africa", "Asia", "Europe", "Oceania"],
        selected = "Americas"
    ),
    ui.output_data_frame("df")
)

def server(input, output, session):
    @output
    @render.data_frame
    def df():
        df = world.copy()
        filtered = df.loc[df["continent"] == "Americas"]
        return filtered

app = App(app_ui, server)