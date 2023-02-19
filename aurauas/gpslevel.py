#!/usr/bin/env python

from svginstr import *
import sys

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://gitorious.org/svginstr/"
__version__ = "0.2"
__license__ = "GPL v2+"
__doc__ = """
"""


try:
    levels = 5
    texture_w = 256
    texture_h = 256
    dl = 180.0 / levels

    w = 180.0 / (levels+1)
    h = w / 1.15

    gray = '#909090'
    green = '#80FF80'
    yellow = '#FFFF80'
    red = '#FF8080'

    for level in range(levels):
        svg_name = "gpslevel" + str(level) + ".svg"
        a = Instrument(svg_name, texture_w, texture_h, "GPS Icon; " + __version__).fg_size(texture_w, texture_h)


        if a.region(-100, -100, 200, 200, name = "TEST").begin():
            if level <= 1:
                color = red
            elif level <= 2:
                color = yellow
            else:
                color = green
            a.translate(0,80).disc(10, color=color)

            for i in range(levels):
                if i > level:
                    color = gray
                a.at(0,80).arc(-35, 35, i*dl, width=w, color=color)

            if level == 0:
                # full
                #a.at(0,0+knob_h*0.5).rectangle(w, h, color=green)
                #a.at(0,0-knob_h*0.5).rectangle(knob_w, h, color=green)
                print "hello"
            elif level < levels - 1:
                # partial
                percent = 1.0 - float(level-1) / float(levels-2)
                print "percent = " + str(percent)
                voffset = (h - h*percent) * 0.5
                color = green
                if percent < 0.10:
                    color = red
                elif percent < 0.25:
                    color = yellow
                #a.at(0,0+knob_h*0.5+voffset).rectangle(w, h*percent, color=color)
            a.end()

except Error as e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

