#!/usr/bin/env python

from svginstr import *
import sys

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://members.aon.at/mfranz/flightgear/"
__version__ = "$Id: clock.py,v 1.1 2005/11/08 21:22:05 m Exp m $; GPL v2"
__doc__ = """
"""


try:
	a = instrument("kclock.svg", 200.0, 200.0, "kclock")
	a.disc(100.0, 'black')
	for hour in range(12):
		a.tick(82.5, 98.0, 30 * hour, 4.0)

		for min in range(4):
			angle = 6 + 30 * hour + 6 * min
			a.tick(92.0, 98.0, angle, 1.5)

except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

