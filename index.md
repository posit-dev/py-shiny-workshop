---
title: "Shiny for Python Workshop"
execute: 
  keep-md: true
---




```{shinylive-python}
#| standalone: true
#| components: [editor, viewer]
#| layout: horizontal
from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error

app_ui = ui.page_fluid(
    ui.row(
        ui.column(
            4,
            ui.input_date_range(
                "dates",
                "Date",
                start="2022-01-01",
                end="2022-01-30",
            ),
        ),
        ui.column(8, ui.output_plot("error_distribution")),
    ),
    ui.row(
        ui.column(4, ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1)),
        ui.column(8, ui.output_plot("error_by_day")),
    ),
)


def server(input, output, session):
    infile = Path(__file__).parent / "weather.csv"
    weather = pd.read_csv(infile)
    weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df["date"] = pd.to_datetime(df["date"])
        dates = pd.to_datetime(input.dates())
        df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
        return df

    @output
    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())

    @output
    @render.plot
    def error_by_day():
        return daily_error(filtered_data(), input.alpha())


app = App(app_ui, server)


## file: app-solution.py
from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error


def divided_row(col1, col2):
    out = ui.row(ui.column(4, col1), ui.column(8, col2))
    return out


app_ui = ui.page_fluid(
    divided_row(
        ui.input_date_range(
            "dates",
            "Date",
            start="2022-01-01",
            end="2022-01-30",
        ),
        ui.output_plot("error_distribution"),
    ),
    divided_row(
        ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1),
        ui.output_plot("error_by_day"),
    ),
)


def server(input, output, session):
    infile = Path(__file__).parent / "weather.csv"
    weather = pd.read_csv(infile)
    weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df["date"] = pd.to_datetime(df["date"])
        dates = pd.to_datetime(input.dates())
        df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
        return df

    @output
    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())

    @output
    @render.plot
    def error_by_day():
        return daily_error(filtered_data(), input.alpha())


app = App(app_ui, server)


## file: plots.py
import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_density,
    theme_light,
    labs,
    geom_point,
    theme,
    element_text,
)


def temp_distirbution(plot_df: pd.DataFrame) -> ggplot:
    plot_df = plot_df[["observed_temp", "forecast_temp", "date"]]
    plot_df = pd.melt(
        plot_df, id_vars="date", value_vars=["observed_temp", "forecast_temp"]
    )
    out = (
        ggplot(plot_df, aes(x="value", group="variable", color="variable"))
        + geom_density()
        + theme_light()
    )
    return out


def daily_error(plot_df: pd.DataFrame, alpha: float) -> ggplot:
    out = (
        ggplot(plot_df, aes(x="date", y="error"))
        + geom_point(alpha=alpha)
        + theme_light()
        + theme(axis_text_x=element_text(rotation=45, hjust=1))
    )
    return out

```


# Exercise 


:::: {.column-screen}
::: {.panel-tabset}
## Target
```{shinylive-python}
#| standalone: true
#| components: [viewer]
#| layout: horizontal
from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error

app_ui = ui.page_fluid(
    ui.row(
        ui.column(
            4,
            ui.input_date_range(
                "dates",
                "Date",
                start="2022-01-01",
                end="2022-01-30",
            ),
        ),
        ui.column(8, ui.output_plot("error_distribution")),
    ),
    ui.row(
        ui.column(4, ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1)),
        ui.column(8, ui.output_plot("error_by_day")),
    ),
)


def server(input, output, session):
    infile = Path(__file__).parent / "weather.csv"
    weather = pd.read_csv(infile)
    weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df["date"] = pd.to_datetime(df["date"])
        dates = pd.to_datetime(input.dates())
        df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
        return df

    @output
    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())

    @output
    @render.plot
    def error_by_day():
        return daily_error(filtered_data(), input.alpha())


app = App(app_ui, server)


## file: app-solution.py
from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error


def divided_row(col1, col2):
    out = ui.row(ui.column(4, col1), ui.column(8, col2))
    return out


app_ui = ui.page_fluid(
    divided_row(
        ui.input_date_range(
            "dates",
            "Date",
            start="2022-01-01",
            end="2022-01-30",
        ),
        ui.output_plot("error_distribution"),
    ),
    divided_row(
        ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1),
        ui.output_plot("error_by_day"),
    ),
)


def server(input, output, session):
    infile = Path(__file__).parent / "weather.csv"
    weather = pd.read_csv(infile)
    weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df["date"] = pd.to_datetime(df["date"])
        dates = pd.to_datetime(input.dates())
        df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
        return df

    @output
    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())

    @output
    @render.plot
    def error_by_day():
        return daily_error(filtered_data(), input.alpha())


app = App(app_ui, server)


## file: plots.py
import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_density,
    theme_light,
    labs,
    geom_point,
    theme,
    element_text,
)


def temp_distirbution(plot_df: pd.DataFrame) -> ggplot:
    plot_df = plot_df[["observed_temp", "forecast_temp", "date"]]
    plot_df = pd.melt(
        plot_df, id_vars="date", value_vars=["observed_temp", "forecast_temp"]
    )
    out = (
        ggplot(plot_df, aes(x="value", group="variable", color="variable"))
        + geom_density()
        + theme_light()
    )
    return out


def daily_error(plot_df: pd.DataFrame, alpha: float) -> ggplot:
    out = (
        ggplot(plot_df, aes(x="date", y="error"))
        + geom_point(alpha=alpha)
        + theme_light()
        + theme(axis_text_x=element_text(rotation=45, hjust=1))
    )
    return out

```
## Problem
```{shinylive-python}
#| standalone: true
#| components: [editor, viewer]
#| layout: horizontal
from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error

app_ui = ui.page_fluid(
    ui.row(
        ui.column(
            4,
            ui.input_date_range(
                "dates",
                "Date",
                start="2022-01-01",
                end="2022-01-30",
            ),
        ),
        ui.column(8, ui.output_plot("error_distribution")),
    ),
    ui.row(
        ui.column(4, ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1)),
        ui.column(8, ui.output_plot("error_by_day")),
    ),
)


def server(input, output, session):
    infile = Path(__file__).parent / "weather.csv"
    weather = pd.read_csv(infile)
    weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df["date"] = pd.to_datetime(df["date"])
        dates = pd.to_datetime(input.dates())
        df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
        return df

    @output
    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())

    @output
    @render.plot
    def error_by_day():
        return daily_error(filtered_data(), input.alpha())


app = App(app_ui, server)


## file: plots.py
import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_density,
    theme_light,
    labs,
    geom_point,
    theme,
    element_text,
)


def temp_distirbution(plot_df: pd.DataFrame) -> ggplot:
    plot_df = plot_df[["observed_temp", "forecast_temp", "date"]]
    plot_df = pd.melt(
        plot_df, id_vars="date", value_vars=["observed_temp", "forecast_temp"]
    )
    out = (
        ggplot(plot_df, aes(x="value", group="variable", color="variable"))
        + geom_density()
        + theme_light()
    )
    return out


def daily_error(plot_df: pd.DataFrame, alpha: float) -> ggplot:
    out = (
        ggplot(plot_df, aes(x="date", y="error"))
        + geom_point(alpha=alpha)
        + theme_light()
        + theme(axis_text_x=element_text(rotation=45, hjust=1))
    )
    return out

```
## Solution
```{shinylive-python}
#| standalone: true
#| components: [editor, viewer]
#| layout: horizontal
from shiny import ui, render, reactive, App
import pandas as pd
from pathlib import Path
from plots import temp_distirbution, daily_error


def divided_row(col1, col2):
    out = ui.row(ui.column(4, col1), ui.column(8, col2))
    return out


app_ui = ui.page_fluid(
    divided_row(
        ui.input_date_range(
            "dates",
            "Date",
            start="2022-01-01",
            end="2022-01-30",
        ),
        ui.output_plot("error_distribution"),
    ),
    divided_row(
        ui.input_slider("alpha", "Plot Alpha", value=0.5, min=0, max=1),
        ui.output_plot("error_by_day"),
    ),
)


def server(input, output, session):
    infile = Path(__file__).parent / "weather.csv"
    weather = pd.read_csv(infile)
    weather["error"] = weather["observed_temp"] - weather["forecast_temp"]

    @reactive.Calc
    def filtered_data():
        df = weather.copy()
        df["date"] = pd.to_datetime(df["date"])
        dates = pd.to_datetime(input.dates())
        df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
        return df

    @output
    @render.plot
    def error_distribution():
        return temp_distirbution(filtered_data())

    @output
    @render.plot
    def error_by_day():
        return daily_error(filtered_data(), input.alpha())


app = App(app_ui, server)


## file: plots.py
import pandas as pd
from plotnine import (
    ggplot,
    aes,
    geom_density,
    theme_light,
    labs,
    geom_point,
    theme,
    element_text,
)


def temp_distirbution(plot_df: pd.DataFrame) -> ggplot:
    plot_df = plot_df[["observed_temp", "forecast_temp", "date"]]
    plot_df = pd.melt(
        plot_df, id_vars="date", value_vars=["observed_temp", "forecast_temp"]
    )
    out = (
        ggplot(plot_df, aes(x="value", group="variable", color="variable"))
        + geom_density()
        + theme_light()
    )
    return out


def daily_error(plot_df: pd.DataFrame, alpha: float) -> ggplot:
    out = (
        ggplot(plot_df, aes(x="date", y="error"))
        + geom_point(alpha=alpha)
        + theme_light()
        + theme(axis_text_x=element_text(rotation=45, hjust=1))
    )
    return out

```
:::
::::


