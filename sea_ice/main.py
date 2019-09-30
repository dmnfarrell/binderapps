import glob,os,sys
import pandas as pd
import numpy as np
import itertools
import panel as pn
import panel.widgets as pnw
from bokeh.models import ColumnDataSource
from bokeh.plotting import figure
from bokeh.models.glyphs import Line
from bokeh.palettes import Category10
pn.extension()

year_select = pnw.RangeSlider(name='year',start=2000,end=2015,value=(2000,2003))
plot = pn.pane.Bokeh()

def plot_extent(event):

    years = range(year_select.value[0],year_select.value[1])
    df=pd.read_csv('seaice_extent_cleaned.csv',index_col=0)
    df['day_of_year'] = pd.to_datetime(df.date).dt.dayofyear
    df = df[df.year.isin(years)]
    df['year'] = df.year.astype(str)
    data = pd.pivot_table(df,index='day_of_year',columns='year',values='Extent').reset_index()
    source = ColumnDataSource(data)
    p = figure(plot_width=700, plot_height=300)
    years = [str(i) for i in years]
    colors = Category10[10]
    i=0
    for y in years:
        glyph = Line(x="day_of_year", y=y, line_color=colors[i], line_width=2, line_alpha=0.6)
        p.add_glyph(source, glyph)
        i+=1
    p.y_range.start=0
    p.y_range.end=21
    plot.object = p
    return

year_select.param.watch(plot_extent, 'value')
year_select.param.trigger()
app = pn.Column(year_select,plot)
app.servable()
