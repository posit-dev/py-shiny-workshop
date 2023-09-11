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
