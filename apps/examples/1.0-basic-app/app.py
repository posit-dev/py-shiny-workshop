from shiny import App, render, ui


def my_slider(id, label):
    return ui.input_slider(id, label + "Number", 0, 100, 20)


numbers = ["n1", "n2", "n3", "n4", "n5", "n6"]
labels = ["First", "Second", "Third", "Fourth", "Fifth", "Sixth"]

app_ui = ui.page_fluid([my_slider(x, y) for x, y in zip(numbers, labels)])

app = App(app_ui, None)
