from shiny import Inputs, Outputs, Session, App, reactive, render, req, ui

app_ui = ui.page_fluid(
    ui.navset_tab(
        ui.nav(
            "Tab1",
            ui.input_slider("slider", "Slider", 0, 100, 20),
        ),
        ui.nav("Tab2", ui.input_action_button("button", "Button")),
        ui.nav("Tab3", ui.input_action_button("button2", "Button 2")),
    )
)

app = App(app_ui, None)
