from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_density,
    theme_light,
    labs,
    geom_point,
    theme,
    element_text,
)


app_ui = ui.page_fluid(
    ui.layout_sidebar(
        ui.panel_sidebar(
            ui.input_selectize(
                "state", "State", choices=["NY", "CO", "OR", "MI"], selected="NY"
            ),
            ui.output_ui("cities_ui"),
        ),
        ui.panel_main(
            ui.output_plot("error_distribution"),
        ),
    )
)


def server(input, output, session):
    infile = Path(__file__).parent / "weather.csv"
    weather = pd.read_csv(infile)
    weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

    @output
    @render.ui
    def cities_ui():
        opts = weather[weather["state"] == input.state()]["city"].unique().tolist()
        return ui.input_selectize(
            "cities", "Cities", choices=opts, selected=opts[0], multiple=True
        )

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df = df[df["city"].isin(input.cities())]
        return df

    @output
    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())


def temp_distirbution(plot_df: pd.DataFrame) -> ggplot:
    plot_df = plot_df[["observed_temp", "forecast_temp", "date"]]
    plot_df = pd.melt(
        plot_df, id_vars="date", value_vars=["observed_temp", "forecast_temp"]
    )
    out = (
        ggplot(plot_df, aes(x="value", group="variable", color="variable"))
        + geom_density()
        + theme_light()
    )
    return out


app = App(app_ui, server)
