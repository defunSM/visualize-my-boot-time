#!/usr/bin/env python
import sys, os, re
import numpy as np

from bokeh.plotting import *
import pandas as pd

from bokeh.charts import Donut, show, output_file, Histogram, Area
from bokeh.charts.utils import df_from_json
from bokeh.sampledata.olympics2014 import data


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

def main():

    home = os.path.expanduser("~")

    times = []

    file = open(home+"/time.txt", "r")
    for i in file.read().split("\n"):
        try:
            m = re.findall("[-+]?\d*\.\d+|\d+", i)

            if m:
                times.append(m)

        except AttributeError:
            pass

    times = np.array(times, dtype='|S4')
    times = times.astype(np.float)

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

    mydict = {'Time (s)':totalboot(times)}

    hist = Histogram(pd.DataFrame(mydict), values="Time (s)", title="Total Boot Time (s)", legend="top_right", background_fill_alpha=0.6, bar_width=1)


    data = dict(
        BootTime=totalboot(times)
        )

    area = Area(data, title="Area Chart", legend="top_left",
                xlabel='Start Up #', ylabel='Time (s)')

    show(area)
    show(hist)
    show(p)

if __name__=="__main__":
    main()
