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
	# applying stop() methods separately ...
	horizon = LinearGradient("0%", "0%", "0%", "100%")
	horizon.stop("0%", 13, 30, 40)
	horizon.stop("49%", 51, 132, 179)
	horizon.stop("49%", 255, 255, 255)
	horizon.stop("51%", 255, 255, 255)
	horizon.stop("51%", 216, 140, 30)
	horizon.stop("100%", 78, 55, 24)

	# or concatenating them
	radial = RadialGradient("50%", "50%", "50%", "50%", "50%").stop("0%", 230, 200, 0).stop("100%", 0, 100, 0)

	a = Instrument("gradienttest.svg", 512, 512, "Gradient Test; " + __version__)
	a.gradient(radial).disc(98)
	a.circle(11, 4)

	a.at(50, 50).gradient(horizon).rectangle(90, 70)

	for i in range(12):
		a.tick(30 * i, 77, 93, 4)


except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

