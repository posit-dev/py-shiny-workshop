from shiny import Inputs, Outputs, Session, App, ui, render
import pandas as pd
from pathlib import Path

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

app_ui = ui.page_fluid(ui.output_data_frame("penguins_df"))


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.plot
    def penguins_df():
        return penguins


app = App(app_ui, server)
