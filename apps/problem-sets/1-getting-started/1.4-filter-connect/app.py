from shiny.express import render, ui, input
import pandas as pd
from pathlib import Path
from data_import import df

ui.input_select(
    id="account",
    label="Account",
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
    account_subset = df
    account_counts = (
        account_subset.groupby(["account", "sub_account"])
        .size()
        .reset_index(name="count")
    )
    return account_counts
