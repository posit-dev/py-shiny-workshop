from shiny.express import render, ui
import pandas as pd
from pathlib import Path
from data_import import df

# All the inputs start with `ui.input_*`, which adds an input to the app.
# Note that this input doesn't do anything because we haven't connected it
# to a rendering function.

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
    account_counts = df.groupby("account").size().reset_index(name="counts")
    return account_counts
