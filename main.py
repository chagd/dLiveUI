#!/usr/bin/env python
from __future__ import print_function

import smopy
import os
from PIL import Image
import math
import Tkinter as tk

import matplotlib
matplotlib.use("TkAgg")
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.animation import FuncAnimation

import numpy as np

import rospy
from geometry_msgs.msg import Pose2D

topic = "GPS"

map_ = False

__version__ = "0.0.5"

#hardcoded values i found for IIT Delhi
lat = (28.54072, 28.5455)
lon = (77.18342, 77.1898)
zoom = 16

#setting up the basic window
win = tk.Tk()
win.title("dLive GUI by Dharun" + " - version :: " + __version__)
win.geometry('{}x{}'.format(1020, 1020))

#left_top_frame
ltf = tk.Frame(win, width = 250 , height = 550, pady = 5)

#left_bottom frame
lbf = tk.Frame(win, width = 250, height = 550, pady = 5)

win.grid_rowconfigure(1, weight=1)
win.grid_columnconfigure(0,weight=1)



#check if map directory exists :: make it if it doesn't
if not os.path.isdir('./map'):
    os.mkdir('./map')

#check if it's empty
if len(os.listdir('./map')) == 0:
    map = smopy.Map((lat[0],lon[0],lat[1],lon[1]),zoom = zoom)
    map.save_png('./map/map.png')
    map_ = True

img = Image.open('./map/map.png')

fig = plt.Figure(figsize=(6,5), dpi = 150)
ax = fig.add_subplot(111)

lat0, lon0, lat1, lon1 = smopy.extend_box((lat[0], lon[0], lat[1], lon[1]))

def deg2num(lat_deg, lon_deg, zoom):
    lat_rad = math.radians(lat_deg)
    n = 2.0 ** zoom
    xtile = ((lon_deg + 180.0) / 360.0 * n)
    ytile = ((1.0 - math.log(math.tan(lat_rad) + (1 / math.cos(lat_rad))) / math.pi) / 2.0 * n)
    return(xtile, ytile)

canvas = FigureCanvasTkAgg(fig, win)
canvas.draw()
canvas.get_tk_widget().pack(side=tk.RIGHT, fill=tk.BOTH, expand=1)

#transforming the coordinates given for better plotting
lat0, lon0, lat1, lon1 = smopy.extend_box((lat[0], lon[0], lat[1], lon[1]))

#require the coordiantes of the origin for pltting the path
x3, y3 = deg2num(lat1,lon1,zoom = zoom)
x4, y4 = deg2num(lat0,lon0,zoom = zoom)

def plot(lat_, lon_):
    global map_
    global lat
    global lon
    global zoom
    tilesize = 256
    global x4, y4

    if map_:
        x,y = map.to_pixels(lat_, lon_)
    else:
        x_, y_ = deg2num(lat_, lon_, zoom)
        x, y = abs(x_ - x4 )*tilesize, abs(y_ - y3)*tilesize

    return x, y

xList = []
yList = []


def animat(i):
    file = open("map_plot.txt", "r")
    for line in file:
        if len(line) > 1 :
            x, y = line.split(",")
            x_, y_ = plot(float(x), float(y))
            xList.append(x_)
            yList.append(y_)

    ax.scatter(xList, yList, c = "blue" , marker = "P")

ax.imshow(img)
anim = FuncAnimation(fig = fig, func = animat, interval = 1000)
#animat()
print ("hello")
win.mainloop()

