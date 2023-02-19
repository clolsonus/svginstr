#!/usr/bin/env python

from svginstr import *
import sys

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://gitorious.org/svginstr/"
__version__ = "0.2"
__license__ = "GPL v2+"
__doc__ = """
"""


Global.indent = '\t'


try:
	a = Instrument("amps.svg", 512, 512, "Amp Load; " + __version__).fg_size(384, 384)

	# * 10
	max_amps = 50
	a.angle = lambda x: x * 340.0 / max_amps - 90.0

	#-- face ------------------------------------------------------------------------

	if a.region(-100, -100, 200, 200, name = "TEST").begin():
		#a.square(200, color = '#202020')
		a.disc(100, color = '#202020')

		if a.scale(0.92).begin():
			#a.arc(yellow_cell*3, max_cell*3, 88, width = 6, color = "#00c000")
			#a.arc(red_cell*3, yellow_cell*3, 88, width = 6, color = "#ffc000")

			for i in range(0, max_amps+1, 1):
				a.tick(i, 93, 99, 1)

			for i in range(0, max_amps+1, 5):
				a.tick(i, 90, 99, 2)

			for i in range(0, max_amps+1, 10):
				a.tick(i, 84, 99, 2)

			#a.tick(red_line, 70, 99.5, 3.3, color = "#c00000")

			if a.begin(font_size = 20):
				a.at(62, -21).text("10")
				a.at(45, 57).text("20")
				a.at(-30, 70).text("30")
				a.at(-66, 5).text("40")
				a.end()

			a.at(0, -40).text("AMP", font_size = 15)

			#a.at(0, -30).screw(0.12, 30)
			#a.at(0, 30).screw(0.12, 70)

			a.disc(8, color = 'black')
			#a.disc(0.4, color = 'red')
			a.end()

		#bezelshadow = RadialGradient()
		#bezelshadow.stop("0%", 0, alpha = 0)
		#bezelshadow.stop("85%", 0, alpha = 0)
		#bezelshadow.stop("100%", 0, alpha = 0.4)
		#a.gradient(bezelshadow).square(200)
		a.end()

	# generate animation XML file for FlightGear
	xml = a.xml("torque")
	xml.animation("Lneedle", "sim/model/bo105/torque-pct", [0, 60, 120])
	xml.animation("Rneedle", "sim/model/bo105/torque-pct", [0, 60, 120])

except Error as e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

