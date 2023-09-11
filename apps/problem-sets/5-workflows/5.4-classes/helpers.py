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


class WeatherDisplay:
    def __init__(self, data, cities, dates):
        df = data.copy()
        df = df[df["city"].isin(cities)]
        df["date"] = pd.to_datetime(df["date"])
        dates = pd.to_datetime(dates)
        df = df[(df["date"] > dates[0]) & (df["date"] <= dates[1])]
        self.dataframe = df

    def temp_distirbution(self):
        plot_df = self.dataframe[["observed_temp", "forecast_temp", "date"]]
        plot_df = pd.melt(
            plot_df, id_vars="date", value_vars=["observed_temp", "forecast_temp"]
        )
        out = (
            ggplot(plot_df, aes(x="value", group="variable", color="variable"))
            + geom_density()
            + theme_light()
        )
        return out

    def daily_error(self, alpha):
        out = (
            ggplot(self.dataframe, aes(x="date", y="error"))
            + geom_point(alpha=alpha)
            + theme_light()
            + theme(axis_text_x=element_text(rotation=45, hjust=1))
        )
        return out
