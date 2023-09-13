from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.input_checkbox("show_checkbox", "Show Checkbox"),
    ui.panel_conditional(
        "input.show_checkbox",
        ui.input_checkbox("show_slider", "Show Slider"),
    ),
    ui.output_ui("dynamic_slider"),
)


def server(input, output, session):
    @output
    @render.ui
    def dynamic_slider():
        print(input.show_slider())
        if input.show_slider():
            return ui.input_slider("n", "N", 0, 100, 20)


app = App(app_ui, server)
