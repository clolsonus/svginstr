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
	a = Instrument("volts.svg", 512, 512, "Dual Voltmeter; " + __version__).fg_size(384, 384)


	#-- face ------------------------------------------------------------------------

	if a.region(-100, -100, 200, 200, name = "TEST").begin():
		a.disc(97, color = '#202020')

		a.angle = lambda x: (x-50) * 75.0 / 5.0 - 90.0

		if a.scale(0.92).begin():
			a.arc(49, 53, 92, width = 14, color = "#00c000")
			a.arc(48, 49, 93, width = 12, color = "#ffd000")
			a.arc(53, 54, 93, width = 12, color = "#ffd000")
			a.arc(45, 48, 93, width = 12, color = "#d03030")
			a.arc(54, 55, 93, width = 12, color = "#d03030")

			for i in range(45, 55+1, 1):
				a.tick(i, 93, 99, 1)

			#for i in range(45, 55+1, 1):
			#	a.tick(i, 84, 99, 2)

			for i in range(45, 55+1, 5):
				a.tick(i, 82, 99, 2)

			#a.tick(80, 81, 99.5, 3, color = "#ffc000")
			#a.tick(red_line, 70, 99.5, 3.3, color = "#c00000")

			if a.begin(font_size = 20):
				a.at(-62, -10).text("4.5")
				#a.at(-43, -45).text("4.5")
				a.at(0, -60).text("5.0")
				#a.at(43, -45).text("5.5")
				a.at(62, -10).text("5.5")
				a.end()

			a.at(0, -25).text("AVIONICS", font_size = 14)

			#a.at(0, -30).screw(0.12, 30)
			#a.at(0, 30).screw(0.12, 70)

			a.disc(8, color = 'black')
			#a.disc(0.4, color = 'red')

			a.angle = lambda x: (36-x) * 75.0 / 6.0 + 90.0

			a.arc(35, 42, 92, width = 14, color = "#00c000")
			a.arc(33, 35, 93, width = 12, color = "#ffd000")
			a.arc(30, 33, 93, width = 12, color = "#d03030")

			for i in range(30, 42+1, 1):
				a.tick(i, 93, 99, 1)

                        #for i in range(30, 42+1, 5):
			#	a.tick(i, 84, 99, 2)

			for i in range(30, 42+1, 5):
				a.tick(i, 82, 99, 2)

			#a.tick(80, 81, 99.5, 3, color = "#ffc000")
			#a.tick(red_line, 70, 99.5, 3.3, color = "#c00000")

			if a.begin(font_size = 20):
				a.at(-62, 25).text("3.0")
				a.at(-15, 75).text("3.5")
				a.at(45, 55).text("4.0")
				a.end()

			a.at(0, 35).text("PER CELL", font_size = 14)
			a.at(0, 50).text("VOLTS", font_size = 14)

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

