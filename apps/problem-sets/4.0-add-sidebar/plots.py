from plotnine import ggplot, geom_density, aes, theme_light, geom_point, stat_smooth


def dist_plot(df):
    plot = (
        ggplot(df, aes(x="body_mass", fill="species"))
        + geom_density(alpha=0.2)
        + theme_light()
    )
    return plot


def scatter_plot(df, smoother=False):
    plot = (
        ggplot(
            df,
            aes(
                x="bill_length",
                y="bill_depth",
                color="species",
                group="species",
            ),
        )
        + geom_point()
        + theme_light()
    )

    if smoother:
        plot = plot + stat_smooth()

    return plot
