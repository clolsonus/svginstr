#!/usr/bin/env python

from svginstr import *
import sys

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://gitorious.org/svginstr/"
__version__ = "0.1"
__license__ = "GPL v2+"
__doc__ = """
"""


try:
	a = instrument("test.svg", 512, 512, "test face; " + __version__)
	a.disc(98, color = 'black')
	
	a.disc(1)

	" define mapping function: map scale value 0-10 to angle 0-190 degree "
	a.angle = lambda x: x * 190.0 / 10.0 - 90

	for i in range(0, 11):
		a.tick(80, 96, i, 2)

	a.tick(76, 96, 3.7, 3, color = "lightgreen")

	for i in frange(0.5, 10, 1):
		a.tick(87, 96, i, 1.5)

	for i in frange(0, 10, 0.1):	# scale values, not angles in degree!
		a.tick(90, 96, i, 0.5)

	#a.default['color'] = "rgb(100, 200, 255)"

	# fc-list tells you the names of available fonts on Linux  (fc ... font cache)
	a.text(0, -15, "FlightGear", size = 20, font = "Lucida Sans", color = "yellow")
	a.text(0, +55, "SVG", size = 60, font = "Luxi Mono", color = "red")

	a.arctext(80, 210, "Better than MetaPost", size = 15, color = "lightblue", font = "Bitstream Vera Serif")

	a.push("rotate(0)")
	a.write('<path d="M0,-94 A94,94 0 0,1 94,0" fill="none" stroke-width="4.5" stroke="yellow" opacity="0.8"/>')
	a.pop()

	a.arc(80, 2, 8, width = 10, color = "pink", opacity = 0.6)

	# switch back to normal svg angles (0-360), not scale angles
	a.angle = lambda x: x - 90
	a.arc(70, 0, 45, width = 5, color = "orange", opacity = 1)


except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

