from shiny.express import ui, input, render
from shiny import render_plot, req, reactive
import pandas as pd
from pathlib import Path
from plots import (
    plot_score_distribution,
    plot_auc_curve,
    plot_precision_recall_curve,
    plot_api_response,
)
import faicons as fa
import io
from shinywidgets import render_plotly

file_path = Path(__file__).parent / "simulated-data.csv"

ui.page_opts(title="Monitoring")


@reactive.file_reader(file_path, interval_secs=0.2)
def df():
    out = pd.read_csv(file_path)
    out["date"] = pd.to_datetime(out["date"], errors="coerce")
    return out


with ui.sidebar():
    ui.input_select(
        "account",
        "Account",
        choices=[
            "Berge & Berge",
            "Fritsch & Fritsch",
            "Hintz & Hintz",
            "Mosciski and Sons",
            "Wolff Ltd",
        ],
    )
    with ui.panel_conditional("input.tabs !== 'Training Dashboard'"):
        ui.input_date_range(
            "dates",
            "Dates",
            start="2023-01-01",
            end="2023-04-01",
        )
        ui.input_numeric("sample", "Sample Size", value=10000, step=5000)


@reactive.Calc
def sampled_data() -> pd.DataFrame:
    start_date, end_date = input.dates()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_value = df()
    out = df_value[
        (df_value["date"] > start_date) & (df_value["date"] <= end_date)
    ].sample(n=input.sample(), replace=True)
    return out


@reactive.Calc()
def filtered_data() -> pd.DataFrame:
    sample_df = sampled_data()
    sample_df = sample_df.loc[sample_df["account"] == input.account()]
    return sample_df.reset_index(drop=True)


ui.nav_spacer()

with ui.nav_panel("Training Dashboard"):
    with ui.layout_columns():
        with ui.card():
            ui.card_header("Model Metrics")

            @render_plotly
            def metric():
                df_value = df()
                df_filtered = df_value[df_value["account"] == input.account()]
                if input.metric() == "ROC Curve":
                    return plot_auc_curve(
                        df_filtered, "is_electronics", "training_score"
                    )
                else:
                    return plot_precision_recall_curve(
                        df_filtered, "is_electronics", "training_score"
                    )

            ui.input_select(
                "metric",
                "Metric",
                choices=["ROC Curve", "Precision-Recall"],
            )
        with ui.card():
            ui.card_header("Training Scores")

            @render_plotly
            def score_dist():
                df_value = df()
                df_filtered = df_value[df_value["account"] == input.account()]
                return plot_score_distribution(df_filtered)

    with ui.card(full_screen=True):
        with ui.card_header():
            "Data"
            with ui.popover(
                title="Download",
                class_="d-inline-block pull-right",
            ):
                fa.icon_svg("download")

                @render.download(filename="scores_data.csv")
                def download_data():
                    with io.BytesIO() as buf:
                        filtered_data().to_csv(buf, index=False)
                        buf.seek(0)
                        yield buf.getvalue()

        @render.data_frame
        def data_output():
            return filtered_data().drop(columns=["text"])


with ui.nav_panel("Model Monitoring"):
    with ui.layout_columns():
        with ui.card():
            ui.card_header("API Response Time")

            @render_plotly
            def api_response():
                return plot_api_response(filtered_data())

        with ui.card():
            ui.card_header("Production Scores")

            @render_plotly
            def prod_score_dist():
                return plot_score_distribution(filtered_data())
