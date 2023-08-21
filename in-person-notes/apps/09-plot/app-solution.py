from shiny import App, render, ui
import pandas as pd
from pathlib import Path
from helpers import top_5_line_plot

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
    ui.input_select(
        "var", 
        "Select Variable",
        {
            "population": "population",
            "lifeExp": "life expectancy",
            "gdpPerCapita": "GDP per capita",
        },
        selected = "population"
    ),
    ui.output_plot("plot"),
    ui.output_data_frame("df")
)

def server(input, output, session):
    @output
    @render.plot
    def plot():
        df = world.copy()
        filtered = df.loc[df["continent"] == input.region()]
        return top_5_line_plot(filtered, input.var())

    @output
    @render.data_frame
    def df():
        df = world.copy()
        filtered = df.loc[df["continent"] == input.region()]
        return filtered

app = App(app_ui, server)