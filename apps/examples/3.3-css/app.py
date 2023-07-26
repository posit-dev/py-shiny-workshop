from pathlib import Path

from shiny import App, Inputs, Outputs, Session, render, ui

css_path = Path(__file__).parent / "www" / "my_styles.css"

app_ui = ui.page_fluid(
    {"class": "blue-body"},
    ui.include_css(css_path),
    ui.input_slider("num", "Number:", min=10, max=100, value=30),
    ui.div(
        {"class": "bold-output;"},
        ui.output_text("slider_val"),
    ),
)


def server(input: Inputs, output: Outputs, session: Session):
    @output
    @render.text
    def slider_val():
        return f"{input.num()}"


app = App(app_ui, server)
