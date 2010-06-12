#!/usr/bin/env python

from svginstr import *
import sys

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://members.aon.at/mfranz/flightgear/"
__version__ = "$Id: arctest.py,v 1.1 2005/11/08 21:21:52 m Exp m $; GPL v2"
__doc__ = """
"""


try:
	a = instrument("arctest.svg", 512, 512, "arctest")
	a.disc(98, 'black')

	for i in range(0, 360, 20):
		a.arc(98.0 * i / 360, 0, i, width = 2, color = "lightyellow")
		a.arc(98.0 * i / 360 + 3, 2*i, i + 20, width = 2, color = "red")

	a.arc(99, 0, 360-0.001, width = 2, color = "lightgreen")


except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

