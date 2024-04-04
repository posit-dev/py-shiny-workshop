from shiny.express import render, ui
import pandas as pd
from pathlib import Path
from data_import import df


@render.data_frame
def table():
    account_counts = df.groupby("account").size().reset_index(name="counts")
    return account_counts
