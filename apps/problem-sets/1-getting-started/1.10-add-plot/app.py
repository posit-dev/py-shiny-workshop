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


@render_plotly
def auc_plot():
    account_subset = df[df["account"] == input.account()]
    return plot_auc_curve(account_subset, "is_electronics", "training_score")


@render.data_frame
def table():
    account_subset = df[df["account"] == input.account()]
    account_counts = (
        account_subset.groupby("sub_account").size().reset_index(name="counts")
    )
    return account_counts
