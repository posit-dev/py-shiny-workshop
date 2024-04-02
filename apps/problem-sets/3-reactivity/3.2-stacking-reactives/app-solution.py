from shiny.express import render, ui, input
from shiny import reactive
from data_import import df
from plots import plot_auc_curve, plot_precision_recall_curve, plot_score_distribution
from shinywidgets import render_plotly


@reactive.calc
def account_data():
    return df[df["account"] == input.account()]


@reactive.calc()
def character_filter():
    return account_data()[(account_data()["text"].str.len().between(*input.chars()))]


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

with ui.layout_columns():

    with ui.card():
        ui.card_header("Model Metrics")

        @render_plotly
        def metric():
            if input.metric() == "ROC Curve":
                return plot_auc_curve(
                    character_filter(), "is_electronics", "training_score"
                )
            else:
                return plot_precision_recall_curve(
                    character_filter(), "is_electronics", "training_score"
                )

        ui.input_select("metric", "Metric", choices=["ROC Curve", "Precision Recall"])

    with ui.card():
        ui.card_header("Model Scores")

        @render_plotly
        def score_dist():
            return plot_score_distribution(character_filter())
