from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error
import shiny.experimental as x

infile = Path(__file__).parent / "weather.csv"
weather = pd.read_csv(infile)
weather["error"] = weather["observed_temp"] - weather["forecast_temp"]


app_ui = ui.page_fluid(
    ui.panel_title("Weather error"),
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_date_range("dates", "Date", start="2022-01-01", end="2022-01-30"),
            ui.input_selectize(
                "cities",
                "Select Cities",
                weather["city"].unique().tolist(),
                selected="BUFFALO",
                multiple=True,
            ),
            width=3,
        ),
        ui.panel_main(
            ui.navset_tab(
                ui.nav(
                    "Error",
                    ui.row(
                        ui.column(
                            6,
                            x.ui.card(
                                x.ui.card_header("Distribution"),
                                ui.output_plot("error_distribution"),
                            ),
                        ),
                        ui.column(
                            6,
                            x.ui.card(
                                x.ui.card_header("Error by day"),
                                ui.output_plot("error_by_day"),
                                ui.input_slider(
                                    "alpha", "Plot Alpha", value=0.5, min=0, max=1
                                ),
                            ),
                        ),
                    ),
                ),
                ui.nav("Data", ui.output_data_frame("data")),
            )
        ),
    ),
)


def server(input, output, session):
    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df = df[df["city"].isin(input.cities())]
        df["date"] = pd.to_datetime(df["date"])
        dates = pd.to_datetime(input.dates())
        df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
        return df

    @output
    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())

    @output
    @render.plot
    def error_by_day():
        return daily_error(filtered_data(), input.alpha())

    @output
    @render.data_frame
    def data():
        return filtered_data()


app = App(app_ui, server)
