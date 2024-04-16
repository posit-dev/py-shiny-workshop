from shiny.express import render, ui, input
from data_import import df
from plots import plot_auc_curve, plot_precision_recall_curve
from shinywidgets import render_plotly

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

# It's a good idea to use helper functions for things like drawing plots
# or displaying data frames because it makes your app more modular and easy to
# read.
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
