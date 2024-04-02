from shiny.express import render, ui, input
from data_import import df
from plots import plot_auc_curve, plot_precision_recall_curve
from shinywidgets import render_plotly

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


@render_plotly
def precision_recall_plot():
    account_subset = df[df["account"] == input.account()]
    return plot_precision_recall_curve(
        account_subset, "is_electronics", "training_score"
    )


@render_plotly
def auc_plot():
    account_subset = df[df["account"] == input.account()]
    return plot_auc_curve(account_subset, "is_electronics", "training_score")
