from shiny import Inputs, Outputs, Session, App, ui

app_ui = ui.page_fluid(ui.h1(""))


def server(input: Inputs, output: Outputs, session: Session):
    None


app = App(app_ui, server)
