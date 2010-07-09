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
	a = Instrument("test.svg", 512, 512, "test face; " + __version__)
	a.disc(98, color = 'black')
	a.disc(1)

	# define mapping function: map scale value 0-10 to angle 0-190 degree
	a.angle = lambda x: x * 190.0 / 10.0 - 90

	for i in range(0, 11):
		a.tick(i, 80, 96, 2)

	a.tick(3.7, 76, 96, 3, color = "lightgreen")

	for i in frange(0.5, 10, 1):
		a.tick(i, 87, 96, 1.5)

	for i in frange(0, 10, 0.1):	# scale values, not angles in degree!
		a.tick(i, 90, 96, 0.5)

	#a.default['color'] = "rgb(100, 200, 255)"

	# fc-list tells you the names of available fonts on Linux  (fc ... font cache)
	a.at(0, -15).text("FlightGear", size = 20, font = "Lucida Sans", color = "yellow")
	a.at(0, 55).text("SVG", size = 60, font = "Luxi Mono", color = "red")

	a.arctext(210, 80, "Better than MetaPost", size = 15, color = "lightblue", font = "Bitstream Vera Serif")

	if a.rotate(0).begin():
		a.write('<path d="M0,-94 A94,94 0 0,1 94,0" fill="none" stroke-width="4.5" stroke="yellow" opacity="0.8"/>')
	a.end()

	a.arc(2, 8, 80, width = 10, color = "pink", opacity = 0.6)

	# switch from scale angles back to normal svg angles (0-360)
	a.angle = lambda x: x - 90
	a.arc(0, 45, 70, width = 5, color = "orange", opacity = 1)


	if a.scale(0.8).rotate(60).translate(-20, -50).begin():
		triangle = Path().abs().moveto_polar(0, 20).lineto_polar(120, 20, -120, 20).close()
		a.write('<path d="%s" fill="white" stroke="maroon" stroke-width="5" opacity="1"/>' % str(triangle))
	a.end()

except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

