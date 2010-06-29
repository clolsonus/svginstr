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
	a = Instrument("torque.svg", 512, 512, "Bo105 torquemeter; " + __version__)
	a.disc(98, 'black')

	a.angle = lambda x: 230.0 * (x - 60) / 120 - 90

	for i in range(0, 120, 2):
		a.tick(i, 80, 98, 1)

	a.arc(0, 80, 93.3, width = 10, color = "#00c000")

	for i in range(0, 121, 10):
		a.tick(i, 80, 98, 3)

	a.tick(80, 80, 98, 3, color = "#ffc000")
	a.tick(110, 70, 98, 3, color = "red")

	fontsize = 20
	a.at(-58, 38).text("0", fontsize)
	a.at(-59, -8).text("20", fontsize)
	a.at(-37, -45).text("40", fontsize)
	a.at(0, -58).text("60", fontsize)
	a.at(40, -45).text("80", fontsize)
	a.at(57, -8).text("100", fontsize)
	a.at(53, 38).text("120", fontsize)

	a.at(0, 75).text("TORQUE", 20)

	#a.at(53, 38).disc(1, 'red')
	#a.at_polar(120, 60).text("X", fontsize)

	xml = a.xml("torque")
	xml.animation("Lneedle", "sim/model/bo105/torque-pct", [0, 60, 120])
	xml.animation("Rneedle", "sim/model/bo105/torque-pct", [0, 60, 120])

except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

