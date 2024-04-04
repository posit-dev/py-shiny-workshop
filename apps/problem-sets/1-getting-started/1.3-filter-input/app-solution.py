from shiny.express import render, ui
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
    account_counts = df.groupby("account").size().reset_index(name="counts")
    return account_counts
