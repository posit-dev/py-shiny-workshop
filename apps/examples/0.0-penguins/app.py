from pathlib import Path
from typing import List, Dict, Tuple
import matplotlib.colors as mpl_colors

import pandas as pd
import seaborn as sns
import shinyswatch

import shiny.experimental as x
from shiny import App, Inputs, Outputs, Session, reactive, render, req, ui

sns.set_theme()

www_dir = Path(__file__).parent.resolve() / "www"

df = pd.read_csv(Path(__file__).parent / "penguins.csv", na_values="NA")
numeric_cols: List[str] = df.select_dtypes(include=["float64"]).columns.tolist()
species: List[str] = df["Species"].unique().tolist()
species.sort()

app_ui = x.ui.page_fillable(
    shinyswatch.theme.minty(),
    ui.layout_sidebar(
        ui.panel_sidebar(
            # Artwork by @allison_horst
            ui.input_selectize(
                "xvar",
                "X variable",
                numeric_cols,
                selected="Bill Length (mm)",
            ),
            ui.input_selectize(
                "yvar",
                "Y variable",
                numeric_cols,
                selected="Bill Depth (mm)",
            ),
            ui.input_checkbox_group(
                "species", "Filter by species", species, selected=species
            ),
            ui.hr(),
            ui.input_switch("by_species", "Show species", value=True),
            ui.input_switch("show_margins", "Show marginal plots", value=True),
            width=2,
        ),
        ui.panel_main(
            ui.output_ui("value_boxes"),
            x.ui.output_plot("scatter", fill=True),
            ui.help_text(
                "Artwork by ",
                ui.a("@allison_horst", href="https://twitter.com/allison_horst"),
                class_="text-end",
            ),
        ),
    ),
)


def server(input: Inputs, output: Outputs, session: Session):
    @reactive.Calc
    def filtered_df() -> pd.DataFrame:
        """Returns a Pandas data frame that includes only the desired rows"""

        # This calculation "req"uires that at least one species is selected
        req(len(input.species()) > 0)

        # Filter the rows so we only include the desired species
        return df[df["Species"].isin(input.species())]

    @output
    @render.plot
    def scatter():
        """Generates a plot for Shiny to display to the user"""

        # The plotting function to use depends on whether margins are desired
        plotfunc = sns.jointplot if input.show_margins() else sns.scatterplot

        plotfunc(
            data=filtered_df(),
            x=input.xvar(),
            y=input.yvar(),
            palette=palette,
            hue="Species" if input.by_species() else None,
            hue_order=species,
            legend=False,
        )

    @output
    @render.ui
    def value_boxes():
        df = filtered_df()

        def penguin_value_box(title: str, count: int, bgcol: str, showcase_img: str):
            return x.ui.value_box(
                title,
                count,
                {"class_": "pt-1 pb-0"},
                showcase=x.ui.as_fill_item(
                    ui.tags.img(
                        {"style": "object-fit:contain;"},
                        src=showcase_img,
                    )
                ),
                theme_color=None,
                style=f"background-color: {bgcol};",
            )

        if not input.by_species():
            return penguin_value_box(
                "Penguins",
                len(df.index),
                bg_palette["default"],
                # Artwork by @allison_horst
                showcase_img="penguins.png",
            )

        value_boxes = [
            penguin_value_box(
                name,
                len(df[df["Species"] == name]),
                bg_palette[name],
                # Artwork by @allison_horst
                showcase_img=f"{name}.png",
            )
            for name in species
            # Only include boxes for _selected_ species
            if name in input.species()
        ]

        return x.ui.layout_column_wrap(1 / len(value_boxes), *value_boxes)


# "darkorange", "purple", "cyan4"
colors = [[255, 140, 0], [160, 32, 240], [0, 139, 139]]
colors = [(r / 255.0, g / 255.0, b / 255.0) for r, g, b in colors]

palette: Dict[str, Tuple[float, float, float]] = {
    "Adelie": colors[0],
    "Chinstrap": colors[1],
    "Gentoo": colors[2],
    "default": sns.color_palette()[0],  # type: ignore
}

bg_palette = {}
# Use `sns.set_style("whitegrid")` to help find approx alpha value
for name, col in palette.items():
    # Adjusted n_colors until `axe` accessibility did not complain about color contrast
    bg_palette[name] = mpl_colors.to_hex(sns.light_palette(col, n_colors=7)[1])  # type: ignore


app = App(
    app_ui,
    server,
    static_assets=str(www_dir),
)
