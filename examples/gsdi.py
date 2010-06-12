#!/usr/bin/env python

from svginstr import *
import sys

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://members.aon.at/mfranz/flightgear/"
__version__ = "$Id: clock.py,v 1.1 2005/11/08 21:22:05 m Exp m $; GPL v2"
__doc__ = """
"""


try:
	a = instrument("gsdi.svg", 512, 512, "Bo105 Ground Speed Drift Indicator; " + __version__)
	a.disc(98, 'black')
	a.circle(11, 4)

	for i in range(12):
		a.tick(77, 93, 30 * i, 4)


except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

