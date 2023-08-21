import pandas as pd
from plotnine import ggplot, aes, geom_line, scale_y_continuous

def format_large_numbers(numbers):
    formatted_numbers = []

    for x in numbers:
        if x >= 1e12:
            formatted_numbers.append(f'{x / 1e12:.0f}T')
        elif x >= 1e9:
            formatted_numbers.append(f'{x / 1e9:.0f}B')
        elif x >= 1e6:
            formatted_numbers.append(f'{x / 1e6:.0f}M')
        elif x >= 1e3:
            formatted_numbers.append(f'{x / 1e3:.0f}K')
        else:
            formatted_numbers.append(f'{x:.0f}')
    
    return formatted_numbers


def top_5_line_plot(data, var):
    top5names = (
        data.sort_values(var, ascending=False)["country"]
        .unique()[:5]
        .tolist()
    )
    top5 = data.loc[data["country"].isin(top5names)]
    p = (
        ggplot(data, aes(x = "year", y = var, group = "country"))
        + geom_line(color = "lightgrey")
        + geom_line(aes(color = "country"), top5)
        + scale_y_continuous(labels = format_large_numbers)
    )
    return p