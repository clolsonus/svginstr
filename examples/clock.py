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
	a = Instrument("clock.svg", 512, 512, "Bo105 clock; " + __version__)
	a.disc(98, color = 'black')
	a.circle(4, 3)

	a.circle(81, 1.5)
	for hour in range(12):
		a.tick(30 * hour, 65, 81, 3)
		if hour != 0:
			a.tick(30 * hour, 84, 96.5, 2)
			if a.rotate(R(30 * hour)).begin(font_weight = "bold", font_size = 10):
				sec = hour * 5
				if sec >= 10:
					if sec < 20:
						a.at(-3, -89).text("I")
					else:
						a.at(-4, -89).text(sec / 10)
				a.at(5.5, -89).text(sec % 10)
			a.end()

		for min in range(4):
			angle = 6 + 30 * hour + 6 * min
			a.tick(angle, 75, 81, 2)
			a.at_polar(angle, 86).disc(1.5)

	# white triangle
	a.write('<path d="M0,-85 l-5,-10 l10,0 z" fill="white"/>')

	# hour numbers
	if a.scale(1.5, 1).begin(font_size = 26, font_weight = "bold"):
		a.at(37, 10).text("3")
		a.at(-35, 10).text("9")
		a.at(1, -45).text("I2")
	a.end()

	if a.begin(font_size = 7):
		a.at(0, -29).text("FLIGHTGEAR")
		a.at(0, -21).text("CLOCK")
	a.end()

	# subclock
	if a.translate(0, 38).begin():
		a.circle(2, 1.5)
		a.circle(21, 1.5)
		for i in position(0, 360, 15):
			a.tick(i, 21, 26, 2)

		fontsize = 11
		if a.begin(font_size = 11):
			a.at(1, -11).text("0")
			a.at(13, 12).text("5")
			a.at(-11, 12).text("I0")
		a.end()
	a.end()

except Error as e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

