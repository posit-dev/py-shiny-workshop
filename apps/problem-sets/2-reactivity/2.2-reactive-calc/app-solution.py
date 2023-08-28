from shiny import App, render, ui, reactive
import pandas as pd
from pathlib import Path
from plots import dist_plot

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

app_ui = ui.page_fluid(
    ui.panel_title("Hello Penguins!"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_numeric("sample", "Sample Size", value=100),
            ui.input_slider(
                "mass",
                "Mass",
                2000,
                8000,
                6000,
            ),
            ui.input_selectize(
                "columns",
                "Columns",
                choices=penguins.columns.tolist(),
                selected=["species", "island"],
                multiple=True,
            ),
        ),
        ui.panel_main(
            ui.output_plot("mass_plot"),
            ui.output_text("row_count"),
            ui.output_data_frame("species_summary"),
        ),
    ),
)


def server(input, output, session):
    @reactive.Calc
    def sampled_df():
        return sample_data(penguins.copy(), input.sample())

    @reactive.Calc
    def filtered_df():
        df = sampled_df()
        return df.loc[df["body_mass"] < input.mass()]

    @output
    @render.plot
    def mass_plot():
        return dist_plot(sampled_df())

    @output
    @render.text
    def row_count():
        return f"{filtered_df().shape[0]} rows in filtered sample"

    @output
    @render.data_frame
    def species_summary():
        return filtered_df()[list(input.columns())]


app = App(app_ui, server)


def sample_data(data: pd.DataFrame, n: int) -> pd.DataFrame:
    # This loop is here to simulate a lengthy computation
    # pyodide does not support time.sleep() so this is the
    # workaround.
    for i in range(10000):
        out = data.sample(n, replace=True)
    return out
