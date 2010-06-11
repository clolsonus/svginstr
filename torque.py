#!/usr/bin/env python

from svginstr import *
import sys

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://members.aon.at/mfranz/flightgear/"
__version__ = "$Id: torque.py,v 1.1 2005/11/08 21:22:42 m Exp m $; GPL v2"
__doc__ = """
"""


try:
	a = instrument("torque.svg", 512, 512, "Bo105 torquemeter; " + __version__)
	a.disc(98, 'black')

	a.angle = lambda x: 230.0 * (x - 60) / 120 - 90

	for i in range(0, 120, 2):
		a.tick(80, 98, i, 1)

	a.arc(93, 0, 80, width = 10, color = "#00c000")

	for i in range(0, 121, 10):
		a.tick(80, 98, i, 3)

	a.tick(80, 98, 80, 3, color = "#ffc000")
	a.tick(70, 98, 110, 3, color = "red")

	fontsize = 20
	a.text(-58, 38, "0", fontsize)
	a.text(-59, -8, "20", fontsize)
	a.text(-37, -45, "40", fontsize)
	a.text(0, -58, "60", fontsize)
	a.text(40, -45, "80", fontsize)
	a.text(57, -8, "100", fontsize)
	a.text(53, 38, "120", fontsize)

	a.text(0, 75, "TORQUE", 20)

	#a.disc(1, 'red', 53, 38)
	#a.ptext(120, 60, "X", fontsize)

	xml = a.xml("torque")
	xml.animation("Lneedle", "sim/model/bo105/torque-pct", [0, 60, 120])
	xml.animation("Rneedle", "sim/model/bo105/torque-pct", [0, 60, 120])

except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

