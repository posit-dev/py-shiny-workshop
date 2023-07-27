from shiny import App, Inputs, Outputs, Session, reactive, ui, render

app_ui = ui.page_fluid(
    ui.input_action_button("show", "Show modal dialog"), ui.output_text("txt")
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Effect
    @reactive.event(input.show)
    def show_modal():
        m = ui.modal(
            "This is a somewhat important message.",
            title="Click outside the modal to close",
            easy_close=True,
            footer=None,
        )
        ui.modal_show(m)


app = App(app_ui, server)
