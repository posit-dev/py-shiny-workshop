from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui

app_ui = ui.page_fluid(
    ui.input_text("input_txt", "Enter text"),
    ui.input_action_button("send", "Enter"),
    ui.output_text_verbatim("output_txt"),
)


def server(input, output, session):
    @output
    @render.text
    @reactive.event(input.send)
    def output_txt():
        return input.input_txt()


app = App(app_ui, server)
