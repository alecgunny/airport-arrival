from collections import defaultdict
from itertools import cycle
import numpy as np

from bokeh.io import curdoc
from bokeh.themes import Theme
from bokeh.plotting import figure
from bokeh.models import HoverTool, ColumnDataSource

from config import theme, palette
curdoc().theme = Theme(json=theme)


def plot_distributions(dists, x_min=0, x_max=10, plot_kwargs={}):
    def _check_dist(dist):
        try:
            return dist.pdf
        except AttributeError:
            raise TypeError(
                "Expected `dists` to either be scipy distribution "
                "or dict of scipy distributions, found type {}".format(
                    type(dist)
                )
            )

    if isinstance(dists, dict):
        fs = {label: _check_dist(dist) for label, dist in dists.items()}
    else:
        fs = _check_dist(dist)
    return plot_functions(fs, x_min=x_min, x_max=x_max, plot_kwargs=plot_kwargs)


def plot_functions(fs, x_min=0, x_max=10, plot_kwargs={}):
    default_plot_kwargs = {
        "height": 400,
        "width": 700,
        "tools": "",
    }
    default_plot_kwargs.update(plot_kwargs)
    p = figure(**default_plot_kwargs)

    def _do_call(f, x):
        try:
            return f(x)
        except TypeError:
            raise TypeError(
                "Expected `fs` to either be callable or dict of callables, "
                "found type {}".format(type(f))
            )

    if isinstance(fs, dict):
        data = defaultdict(list)
        color_iterator = cycle(palette)
        for (legend_label, f), color in zip(fs.items(), color_iterator):
            x = np.linspace(x_min, x_max, 100)
            y = _do_call(f, x)

            data["xs"].append(x)
            data["ys"].append(y)
            data["label"].append(legend_label)
            data["color"].append(color)

        source = ColumnDataSource(data)
        p.multi_line(
            xs="xs",
            ys="ys",
            legend_group="label",
            line_color="color",
            source=source
        )
    else:
        x = np.linspace(x_min, x_max, 100)
        y = _do_call(fs, x)
        p.line(x=x, y=y)
    return p