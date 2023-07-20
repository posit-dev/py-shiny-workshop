from shiny import App, render, ui, reactive, req
import json
from pathlib import Path

with open(Path(__file__).parent / "questions.json", "r") as file:
    questions = json.load(file)

app_ui = ui.page_fluid(ui.output_ui("question"), ui.output_ui("validation"))


def server(input, output, session):
    q_num = reactive.Value(0)

    question_keys = list(questions.keys())

    @reactive.Calc
    def current_q():
        return questions[question_keys[q_num()]]

    @output
    @render.ui
    def question():
        return ui.div(
            ui.h5(question_keys[q_num()], style="margin-bottom: 20px"),
            ui.input_radio_buttons(
                "question",
                "",
                choices=current_q()["choices"],
                selected="",
            ),
        )

    @output
    @render.ui
    def validation():
        req(input.question())
        if input.question() == current_q()["answer"]:
            if q_num() == len(question_keys) - 1:
                return ui.p("Correct! Quiz complete.")
            else:
                return ui.div(
                    ui.p("Correct!"), ui.input_action_button("next", "Next Question")
                )
        return ui.p("Not quite right, try again")

    @reactive.Effect
    @reactive.event(input.next)
    def next_question():
        q_num.set(q_num.get() + 1)


app = App(app_ui, server)
