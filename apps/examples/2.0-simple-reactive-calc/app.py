from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui
import pandas as pd
from plotnine import ggplot, geom_histogram, labs, aes
import numpy as np

app_ui = ui.page_fluid(
    ui.input_slider("n_rows", "Sample rows", 0, 100, 20),
    ui.output_plot("hist"),
    ui.output_table("df"),
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.table
    def df():
        rand = np.random.rand(input.n_rows(), 1)
        df = pd.DataFrame(rand, columns=["col_1"])
        return df

    @output
    @render.plot
    def hist():
        rand = np.random.rand(input.n_rows(), 1)
        df = pd.DataFrame(rand, columns=["col_1"])
        plot = (
            ggplot(df, aes(x="col_1"))
            + geom_histogram(binwidth=0.1, fill="blue", color="black")
            + labs(x="Random Values", y="Frequency", title="Histogram of Random Data")
        )
        return plot


app = App(app_ui, server)
