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
	a = Instrument("res3-asi.svg", 512, 512, "Resolution 3 ASI; " + __version__).fg_size(384, 384)

	stall_speed = 20
	min_speed = 25
	yellow_line = 50
	red_line = 65
	max_speed = 80
	a.angle = lambda x: x * 340.0 / max_speed - 90.0

	#-- face ------------------------------------------------------------------------

	if a.region(-100, -100, 200, 200, name = "TEST").begin():
		#a.square(200, color = '#202020')
		a.disc(100, color = '#202020')

		if a.scale(0.90).begin():
			a.arc(min_speed, yellow_line, 92, width = 14, color = "#00c000")
			a.arc(yellow_line, red_line, 93, width = 12, color = "#ffd000")
			a.arc(red_line, max_speed, 96, width = 6, color = "#d03030")

			for i in range(0, max_speed+1, 1):
				a.tick(i, 88, 99, 1)

			for i in range(0, max_speed+1, 5):
				a.tick(i, 83, 99, 1.5)

			for i in range(0, max_speed+1, 10):
				a.tick(i, 78, 99, 2)

			#a.tick(80, 81, 99.5, 3, color = "#ffc000")
			#a.tick(red_line, 70, 99.5, 3.3, color = "#c00000")

			if a.begin(font_size = 20, font_weight = "bold"):
				a.at(41, -41).text("10")
				a.at(64, 1).text("20")
				a.at(50, 45).text("30")
				a.at(11, 73).text("40")
				a.at(-35, 62).text("50")
				a.at(-61, 25).text("60")
				a.at(-54, -25).text("70")
				a.at(-24, -54).text("80")
				a.end()

			a.at(0, -25).text("AIRSPEED", font_size = 14)
			a.at(0, 40).text("KTS", font_size = 15)

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

