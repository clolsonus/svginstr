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
	a = Instrument("hdg_hud.svg", 512, 512, "Heading Indicator; " + __version__).fg_size(384, 384)

	#-- face ------------------------------------------------------------------------

	text_size = 15

	if a.region(-100, -100, 200, 200, name = "TEST").begin():
		#a.square(200, color = '#202020')
		#a.disc(97, color = '#202020')

		if a.scale(1.0).begin():
			# a.circle(radius = 99, width = 2, color = "#f0f0f0")

			for i in range(0, 360, 5):
				a.tick(i, 88, 99, 1)

			for i in range(0, 360, 10):
				a.tick(i, 83, 99, 1.5)

			for i in range(0, 360, 30):
				a.tick(i, 78, 99, 2)

			#a.tick(80, 81, 99.5, 3, color = "#ffc000")
			#a.tick(red_line, 70, 99.5, 3.3, color = "#c00000")

			radius = 62
			a.arctext(0-5, radius, "N", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(90-5, radius, "E", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(180-5, radius, "S", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(270-7, radius, "W", size = text_size, color = "#f0f0f0", font_weight = "bold")

			a.arctext(30-4, radius, "3", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(60-4, radius, "6", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(120-8, radius, "12", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(150-8, radius, "15", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(210-8, radius, "21", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(240-8, radius, "24", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(300-8, radius, "30", size = text_size, color = "#f0f0f0", font_weight = "bold")
			a.arctext(330-8, radius, "33", size = text_size, color = "#f0f0f0", font_weight = "bold")

			#a.at(0, -30).screw(0.12, 30)
			#a.at(0, 30).screw(0.12, 70)

			#a.disc(8, color = 'black')
			#a.disc(0.4, color = 'red')
			a.end()

		#bezelshadow = RadialGradient()
		#bezelshadow.stop("0%", 0, alpha = 0)
		#bezelshadow.stop("85%", 0, alpha = 0)
		#bezelshadow.stop("100%", 0, alpha = 0.4)
		#a.gradient(bezelshadow).square(200)
		a.end()

	# generate animation XML file for FlightGear
	#xml = a.xml("torque")
	#xml.animation("Lneedle", "sim/model/bo105/torque-pct", [0, 60, 120])
	#xml.animation("Rneedle", "sim/model/bo105/torque-pct", [0, 60, 120])

except Error as e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

