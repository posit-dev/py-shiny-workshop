from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.input_checkbox("show_slider", "Show Slider"),
    ui.panel_conditional(
        "input.show_slider", ui.input_slider("slider", "Slider", 0, 100, 50)
    ),
)

app = App(app_ui, None)
