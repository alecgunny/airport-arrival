from collections import defaultdict
from itertools import cycle, product
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

    if not isinstance(fs, dict):
        fs = {None: fs}

    dashes = ["solid", "2 2", "4 4"]
    prop_iterator = cycle(product(dashes, palette))
    for (legend_label, f), (dash, color) in zip(fs.items(), prop_iterator):
        x = np.linspace(x_min, x_max, 100)
        y = _do_call(f, x)

        kwargs = {}
        if legend_label is not None:
            kwargs["legend_label"] = legend_label
        p.line(
            x=x,
            y=y,
            line_color=color,
            line_dash=dash,
            **kwargs
        )
    return p