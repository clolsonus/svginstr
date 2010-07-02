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

	a.scale(0.85).translate(-17, -17).push()
	a.square(200, '#181818')
	#a.disc(100, '#181818')

	a.scale(0.92).push()
	a.angle = lambda x: 230.0 * (x - 60) / 120 - 90

	for i in range(0, 120, 2):
		a.tick(i, 82, 99, 1)

	a.arc(0, 80, 94.5, width = 10, color = "#00c000")

	for i in range(0, 121, 10):
		a.tick(i, 81, 99.5, 3)

	a.tick(80, 81, 99.5, 3, color = "#ffc000")
	a.tick(110, 70, 99.5, 3.3, color = "red")

	fontsize = 20
	a.at(-60, 38).text("0", fontsize)
	a.at(-61, -8).text("20", fontsize)
	a.at(-39, -46).text("40", fontsize)
	a.at(0, -61).text("60", fontsize)
	a.at(39, -46).text("80", fontsize)
	a.at(56, -8).text("100", fontsize)
	a.at(50, 38).text("120", fontsize)

	a.at(0, 55).text("%", 17)
	a.at(0, 75).text("TORQUE", 20)

	a.at(0, -30).screw(0.1, 30)
	a.at(0, 30).screw(0.1, 80)
	a.disc(8, 'black')

	a.disc(0.4, 'red')
	a.pop()
	a.pop()


	xml = a.xml("torque")
	xml.animation("Lneedle", "sim/model/bo105/torque-pct", [0, 60, 120])
	xml.animation("Rneedle", "sim/model/bo105/torque-pct", [0, 60, 120])

except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

