#!/usr/bin/env python
import sys, os, re
import numpy as np

from bokeh.plotting import *
import pandas as pd

from bokeh.charts import Donut, show, output_file, Histogram, Area
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data

import optparse

def avgfirmware(times):

    placeholder = []

    for i in times:
        placeholder.append(i[0])

    return sum(placeholder) / (len(placeholder))

def avgloader(times):

    placeholder = []

    for i in times:
        placeholder.append(i[1])

    return sum(placeholder) / (len(placeholder))

def avgkernel(times):

    placeholder = []

    for i in times:
        placeholder.append(i[2])

    return sum(placeholder) / (len(placeholder))

def avguserspace(times):

    placeholder = []

    for i in times:
        placeholder.append(i[3])

    return sum(placeholder) / (len(placeholder))

def avgtotaltime(times):

    placeholder = []

    for i in times:
        placeholder.append(i[4])

    return sum(placeholder) / (len(placeholder))

def totalboot(times):

    placeholder = []

    for i in times:
        placeholder.append(i[4])

    return placeholder

def showArea(times):
    data = dict(
        BootTime=totalboot(times)
    )

    area = Area(data, title="Area Chart", legend="top_left",
                xlabel='Start Up #', ylabel='Time (s)')

    show(area)

def showHistogram(times):
    mydict = {'Time (s)':totalboot(times)}

    hist = Histogram(pd.DataFrame(mydict), values="Time (s)", title="Total Boot Time (s)", legend="top_right", background_fill_alpha=0.6, bar_width=1)

    show(hist)

def showLineGraph(times):

    x = figure(plot_width=800, plot_height=800)
    counter = 0
    for i in times:
        x.circle([1, 2, 3, 4, 5], i, size=10, alpha=0.5)
        counter += 1

    show(x)

def main():

    home = os.path.expanduser("~")

    times = []

    file = open(home+"/time.txt", "r")
    for i in file.read().split("\n"):

        empty_array = []

        try:
            m = re.findall("[-+]?\d*\.\d+|\d+", i)

            if m:
                for i in m:
                    empty_array.append(float(i))

                times.append(empty_array)

        except AttributeError:
            pass

    print(times)

    avgf = avgfirmware(times)
    avgl = avgloader(times)
    avgk = avgkernel(times)
    avgu = avguserspace(times)
    avgt = avgtotaltime(times)

    percentf = avgf / avgt
    percentl = avgl / avgt
    percentk = avgk / avgt
    percentu = avgu / avgt

    print(times)
    print("AVG FIRMWARE TIME: ", avgf, percentf)
    print("AVG LOADER TIME: ", avgl, percentl)
    print("AVG KERNAL TIME: ", avgk, percentk)
    print("AVG USERSPACE TIME: ", avgu, percentu)
    print("AVG TOTAL TIME: ", avgt)

    percents = [0, percentf, percentf + percentl, percentf + percentl + percentk, 1]
    starts = [p * 2 * np.pi for p in percents[:-1]]
    ends = [p * 2 * np.pi for p in percents[1:]]

    colors = ["red", "green", "blue", "orange"]
    legends= ["Firmware", "Loader", "Kernal", "Userspace"]

    p = figure(x_range=(-1,1), y_range=(-1,1))

    p.wedge(x=0, y=0, radius=1, start_angle=starts, end_angle=ends, color=colors, alpha=0.6, line_color="black")

    output_file("pie.html")


    p = optparse.OptionParser()
    p.add_option('--displayall', '-a', default=False)
    p.add_option('--showAreaPlot', '-p', default=False)
    p.add_option('--showHistogram', '-g', default=False)
    p.add_option('--showPieGraph', '-i', default=False)
    p.add_option('--showLineGraph', '-l', default=False)

    options, arguments = p.parse_args()

    if options.displayall != False:
            showArea(times)
            showHistogram(times)
            show(p)
            return 1

    if options.showAreaPlot != False:
        showArea(times)

    if options.showHistogram != False:
        showHistogram(times)

    if options.showPieGraph != False:
        show(p)

    if options.showLineGraph != False:
        showLineGraph(times)



if __name__=="__main__":
    main()
