from pathlib import Path

from shiny import App, render, ui, reactive

app_ui = ui.page_fluid(
    ui.input_radio_buttons(
        "command_choice", "Choose a command", choices=["Option 1", "Option 2"]
    ),
    ui.output_ui("dynamic_text"),
    ui.input_action_button("compute_button", "COMPUTE"),
)


def server(input, output, session):
    @output
    @render.ui
    def dynamic_text():
        if input.command_choice() == "Option 1":
            id = "output_text_1"
        else:
            id = "output_text_2"
        return ui.output_text(id)

    @output
    @render.text
    @reactive.event(input.compute_button)
    def output_text_1():
        return "Result from option 1"

    @output
    @render.text
    @reactive.event(input.compute_button)
    def output_text_2():
        return "Result from option 2"


app = App(app_ui, server)
