from shiny import App, ui
import matplotlib.pyplot as plt
import numpy as np

style = "border: 1px solid #999;"

app_ui = ui.page_fluid(
    ui.row(
        ui.column(
            6,
            "row-1 col-2",
            ui.row(
                ui.column(4, "nest-1", style=style),
                ui.column(4, "nest-2", style=style),
                ui.column(4, "nest-2", style=style),
            ),
            style=style,
        ),
        ui.column(4, "row-1 col-2", style=style),
    ),
)


app = App(app_ui, None)
