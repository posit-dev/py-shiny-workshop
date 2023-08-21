from shiny import App, render, ui

app_ui = ui.page_fluid()

def server(input, output, session):
    return None

app = App(app_ui, server)
