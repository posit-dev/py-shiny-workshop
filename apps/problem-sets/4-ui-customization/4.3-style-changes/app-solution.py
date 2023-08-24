from shiny import App, render, ui, reactive
import pandas as pd
from pathlib import Path
from plots import dist_plot, scatter_plot
from boxes import make_value_box
import shiny.experimental as x
from shinyswatch import theme

infile = Path(__file__).parent / "penguins.csv"
penguins = pd.read_csv(infile)

app_ui = ui.page_fluid(
    theme.minty(),
    ui.include_css(Path(__file__).parent / "www/styles.css"),
    ui.panel_title("Penguins Dashboard"),
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
            width=3,
        ),
        ui.panel_main(
            ui.row(ui.output_ui("boxes")),
            ui.row(
                {"class": "pink-row"},
                ui.column(8, ui.output_plot("dist")),
                ui.column(4, ui.output_plot("scatter")),
            ),
        ),
    ),
)


def server(input, output, session):
    @reactive.Calc
    def filt_df() -> pd.DataFrame:
        df = penguins.copy()
        filtered = df.loc[df["body_mass"] < input.mass()]
        return filtered

    @output
    @render.ui
    def boxes():
        species_count = filt_df().groupby(["species"])["species"].count()
        box_list = []

        for index, value in species_count.items():
            box_list.append(make_value_box(index, value))

        return x.ui.layout_column_wrap(1 / 3, *box_list)

    @output
    @render.plot
    def dist():
        return dist_plot(filt_df())

    @output
    @render.plot
    def scatter():
        return scatter_plot(filt_df(), input.trend())


app = App(app_ui, server)
