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
	# applying color() methods separately ...
	linear = LinearGradient("0%", "0%", "0%", "100%")
	linear.color("0%", 13, 30, 40)
	linear.color("49%", 51, 132, 179)
	linear.color("49%", 255, 255, 255)
	linear.color("51%", 255, 255, 255)
	linear.color("51%", 216, 140, 30)
	linear.color("100%", 78, 55, 24)

	# or concatenating them
	radial = RadialGradient("50%", "50%", "50%", "50%", "50%").color("0%", 230, 200, 0).color("100%", 0, 100, 0)

	a = Instrument("gradienttest.svg", 512, 512, "Gradient Test; " + __version__)
	a.gradient(radial).disc(98)
	a.gradient(linear).circle(11, 4)

	a.at(50, 50).gradient(linear).rectangle(90, 70)

	for i in range(12):
		a.tick(30 * i, 77, 93, 4)


except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

