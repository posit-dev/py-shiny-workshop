from shiny.express import render, ui, input
import pandas as pd
from pathlib import Path
from data_import import df

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


@render.data_frame
def table():
    # Inputs can only be called within a reactive context, which
    # means that if you refer to them outside of a rendering function
    # you'll get an error.
    account_subset = df[df["account"] == input.account()]
    account_counts = (
        account_subset.groupby("sub_account").size().reset_index(name="counts")
    )
    return account_counts
