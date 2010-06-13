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
	a = instrument("gsdi.svg", 512, 512, "Bo105 Ground Speed Drift Indicator; " + __version__)
	a.disc(98, 'black')
	a.circle(11, 4)

	for i in range(12):
		a.tick(30 * i, 77, 93, 4)


except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

