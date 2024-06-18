# Reactive Web Dashboards with Shiny Course

This is the repository for Talk Python's [Reactive Web Dashboards with Shiny course](https://training.talkpython.fm/courses/reactive-web-dashboards-with-shiny-for-data-science). This 2-hour video course is 100% free so [visit the course page and sign up](https://training.talkpython.fm/courses/reactive-web-dashboards-with-shiny-for-data-science) if you're interested.

# Installation

You will need to install a few things to render the website locally:

1) [Install quarto](https://quarto.org/docs/get-started/)
2) Install the shinylive python package `pip install shinylive --upgrade`
3) Install the shinylive quarto materials `quarto add quarto-ext/shinylive`

## How to edit the materials

This is a quarto website, so to make changes to the course text modify the `.qmd` files, or the `_quarto.yml`.
To do a live preview run `quarto preview --render html`, note that while `--render html` is a bit slower, it's the best way to see changes with the included applications. 

## Creating an including Shiny Apps

All of the apps live in the `apps` folder, which means that you can use VS Code to edit and test them out. 
To include an application insert an asis quarto chuck which looks like this:

```{python}
#| echo: false
#| output: asis

include_shiny_folder("apps/basic-app")
```

You can also pass optins to this function to modify the behaviour of the included app. 

To include a set of problem tabs, your app should have two application files. `app.py` which shows the starting point for the problem and `app-solution.py` which shows the target application. 
You can then use the `problem_tabs` function to include the tabs.

```{python}
#| echo: false
#| output: asis

problem_tabs("apps/basic-app")
```

## Inserting multiple choice questions

You can insert a shinylive app which displays sets of multiple choice questions by supplying a dictionary. 
It is a good idea to always wrap this dictionary with the `Quiz` class which validates that it is the right format for the application.

```{python}
# | echo: false
# | output: asis

from helpers import multiple_choice_app, Quiz

questions = Quiz(
    {
        "What ui input is used for plots?": {
            "choices": ["ui.input_plot", "ui.plot_input", "ui.plotInput"],
            "answer": "ui.Input_plot",
        },
        "How do you remove a reacitve link??": {
            "choices": ["reactive.isolate", "req", "reactive.Effect"],
            "answer": "reactive.isolate",
        },
        "What should you use to save an image of a plot to disk?": {
            "choices": ["reactive.Calc", "@ui.output_plot", "reactive.Effect"],
            "answer": "reactive.Effect",
        },
    }
)

multiple_choice_app(questions)
```