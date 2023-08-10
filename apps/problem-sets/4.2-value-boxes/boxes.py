import shiny.experimental as x
from shiny import ui


def make_value_box(title: str, value: float):
    return x.ui.value_box(title, value.__round__(2))
