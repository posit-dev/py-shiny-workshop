from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from helpers import WeatherDisplay
import shiny.experimental as x

infile = Path(__file__).parent / "weather.csv"
weather = pd.read_csv(infile)
weather["error"] = weather["observed_temp"] - weather["forecast_temp"]


def val_box_col(id, n_boxes):
    width = 12 // n_boxes
    card_title = id.replace("_", " ").title()
    return ui.column(width, x.ui.value_box(card_title, ui.output_text(id)))


boxes = ["hot_days", "cold_days", "mean_error"]

data_tab = ui.nav("Data", ui.output_data_frame("data"))
error_tab = ui.nav(
    "Error",
    ui.row([val_box_col(box, len(boxes)) for box in boxes]),
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
                ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1),
            ),
        ),
    ),
)

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
                error_tab,
                data_tab,
            )
        ),
    ),
)


def server(input, output, session):
    @reactive.Calc
    def filtered_data() -> pd.DataFrame:
        return WeatherDisplay(weather, input.cities(), input.dates())

    @output
    @render.plot
    def error_distribution():
        return filtered_data().temp_distirbution()

    @output
    @render.plot
    def error_by_day():
        return filtered_data().daily_error(alpha=input.alpha())

    @output
    @render.data_frame
    def data():
        return filtered_data().dataframe

    @output
    @render.text
    def mean_error():
        mean_error = filtered_data().dataframe["error"].mean()
        return round(mean_error, 2)

    @output
    @render.text
    def hot_days():
        hot_days = filtered_data().dataframe["error"] > 0
        return sum(hot_days)

    @output
    @render.text
    def cold_days():
        hot_days = filtered_data().dataframe["error"] < 0
        return sum(hot_days)


app = App(app_ui, server)
