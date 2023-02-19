#!/usr/bin/env python

import sys
#sys.path.append('../lib')
from svginstr import *

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://gitorious.org/svginstr/"
__version__ = "0.2"
__license__ = "GPL v2+"
__doc__ = """
"""


try:
    levels = 8
    texture_w = 256
    texture_h = 256

    w = 200 * 0.9
    h = w / 1.15
    knob_w = w * 0.5
    knob_h = h * 0.15

    gray = '#909090'
    green = '#80FF80'
    yellow = '#FFFF80'
    red = '#FF8080'

    for level in range(levels):
        svg_name = "battery" + str(level) + ".svg"
        a = Instrument(svg_name, texture_w, texture_h, "Battery Icon; " + __version__).fg_size(texture_w, texture_h)


        if a.region(-100, -100, 200, 200, name = "TEST").begin():
            a.at(0,0+knob_h*0.5).rectangle(w, h, color = gray)
            a.at(0,0-knob_h*0.5).rectangle(knob_w, h, color=gray)

            if level == 0:
                # full
                a.at(0,0+knob_h*0.5).rectangle(w, h, color=green)
                a.at(0,0-knob_h*0.5).rectangle(knob_w, h, color=green)
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
                a.at(0,0+knob_h*0.5+voffset).rectangle(w, h*percent, color=color)
            else:
                # !!!
                dim = h / 6
                a.at(0,0-h*0.10).rectangle(dim*2, dim*3, color=red)
                a.at(0,0+h*0.30).rectangle(dim*2, dim, color=red)

            a.end()

except Error as e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

