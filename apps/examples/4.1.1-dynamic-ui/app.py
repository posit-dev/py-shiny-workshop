from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.input_numeric("max_slider", "Slider max", value=100),
    ui.output_ui("dynamic_slider"),
)


def server(input, output, session):
    @output
    @render.ui
    def dynamic_slider():
        return ui.input_slider("n", "N", 0, input.max_slider(), 20)


app = App(app_ui, server)
