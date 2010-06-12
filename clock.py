#!/usr/bin/env python

from svginstr import *
import sys

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://members.aon.at/mfranz/flightgear/"
__version__ = "$Id: clock.py,v 1.1 2005/11/08 21:22:05 m Exp m $; GPL v2"
__doc__ = """
"""


try:
	a = instrument("clock.svg", 512, 512, "Bo105 clock; " + __version__)
	a.disc(98, 'black')
	a.circle(4, 3)

	a.circle(81, 1.5)
	for hour in range(12):
		a.tick(65, 81, 30 * hour, 3)
		if hour != 0:
			a.tick(84, 96.5, 30 * hour, 2)
			a.push('rotate(%s)' % R(30 * hour))
			sec = hour * 5
			if sec >= 10:
				if sec < 20:
					a.text(-3, -89, "I", 10, dic = {"font-weight": "bold"})
				else:
					a.text(-4, -89, sec / 10, 10, dic = {"font-weight": "bold"})
			a.text(5.5, -89, sec % 10, 10, dic = {"font-weight": "bold"})
			a.pop()

		for min in range(4):
			angle = 6 + 30 * hour + 6 * min
			a.tick(75, 81, angle, 2)
			a.bullet(86, angle, 1.5)

	# white triangle
	a.write('<path d="M0,-85 l-5,-10 l10,0 z" fill="white"/>')

	# hour numbers
	a.push('scale(1.5 1)')
	fontsize = 26
	a.text(37, 10, "3", fontsize, dic = {'font-weight': 'bold'})
	a.text(-35, 10, "9", fontsize, dic = {'font-weight': 'bold'})
	a.text(1, -45, "I2", fontsize, dic = {'font-weight': 'bold'})
	a.pop()

	fontsize = 7
	a.text(0, -29, "FLIGHTGEAR", fontsize)
	a.text(0, -21, "CLOCK", fontsize)

	# subclock
	a.push("translate(0 38)")
	a.circle(2, 1.5)
	a.circle(21, 1.5)
	for i in position(0, 360, 15):
		a.tick(21, 26, i, 2)

	fontsize = 11
	a.text(1, -11, "0", fontsize)
	a.text(13, 12, "5", fontsize)
	a.text(-11, 12, "I0", fontsize)
	a.pop()

except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

