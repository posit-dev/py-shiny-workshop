from shiny import App, render, ui

app_ui = ui.page_fluid(
    ui.h2("Hello Shiny!"),
    ui.input_slider("n", "N", 0, 100, 20),
    ui.input_numeric("multiplier", "Multipler", min=0, max=100, step=1, value=5),
    ui.output_text_verbatim("txt"),
    ui.output_text_verbatim("divide"),
)


def server(input, output, session):
    @output
    @render.text
    def txt():
        k = input.multiplier()
        return f"n*{str(k)} is {input.n() * k}"

    @output
    @render.text
    def divide():
        k = input.multiplier()
        return f"n/{str(k)} is {input.n() / k}"


app = App(app_ui, server)
