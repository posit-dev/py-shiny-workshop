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
df = pd.read_csv(file_path, dtype={"sub_account": str})
df["date"] = pd.to_datetime(df["date"], errors="coerce")


@reactive.calc
def monitor_sampled_data() -> pd.DataFrame:
    start_date, end_date = input.dates()
    start_date = pd.to_datetime(start_date)
    end_date = pd.to_datetime(end_date)
    df_value = df
    out = df_value[
        (df_value["date"] > start_date) & (df_value["date"] <= end_date)
    ].sample(n=input.sample(), replace=True)
    return out


@reactive.calc()
def monitor_filtered_data() -> pd.DataFrame:
    sample_df = monitor_sampled_data()
    sample_df = sample_df.loc[sample_df["account"] == input.account()]
    return sample_df.reset_index(drop=True)


@reactive.calc()
def training_data():
    return df[
        (df["account"] == input.account()) & (df["sub_account"] == input.sub_account())
    ]


@reactive.effect
@reactive.event(input.reset)
def reset_vals():
    ui.update_date_range("dates", start="2023-01-01", end="2023-04-01")
    ui.update_numeric("sample", value=10000)


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

    @render.express
    def sub_selector():
        choice_data = df[df["account"] == input.account()]
        choices = choice_data["sub_account"].unique().tolist()
        ui.input_select("sub_account", "Sub Account", choices=choices)

    with ui.panel_conditional("input.tabs !== 'Training Dashboard'"):
        ui.input_date_range(
            "dates",
            "Dates",
            start="2023-01-01",
            end="2023-04-01",
        )
        ui.input_numeric("sample", "Sample Size", value=10000, step=5000)
        ui.input_action_button("reset", "Reset Values", class_="btn-primary")


with ui.navset_bar(id="tabs", title="Monitoring"):
    with ui.nav_panel("Training Dashboard"):
        with ui.layout_columns():
            with ui.card():
                ui.card_header("Model Metrics")

                @render_plotly
                def metric():
                    if input.metric() == "ROC Curve":
                        return plot_auc_curve(
                            training_data(), "is_electronics", "training_score"
                        )
                    else:
                        return plot_precision_recall_curve(
                            training_data(), "is_electronics", "training_score"
                        )

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

                @render_plotly
                def score_dist():
                    return plot_score_distribution(training_data())

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

                @render.download(filename=lambda: f"{input.account()}_scores.csv")
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
