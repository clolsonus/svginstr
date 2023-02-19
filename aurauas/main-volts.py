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
	a = Instrument("main-volts.svg", 512, 512, "Main Volts; " + __version__).fg_size(384, 384)

	# * 10
	max_cell = 42
	yellow_cell = 33
	red_cell = 30
	min_volts = int(red_cell * 3 / 10) * 10
	print "min_volts = " + str(min_volts) + "\n"
	max_volts = max_cell * 6
	a.angle = lambda x: (x-min_volts) * 340.0 / (max_volts-min_volts) - 90.0

	#-- face ------------------------------------------------------------------------

	if a.region(-100, -100, 200, 200, name = "TEST").begin():
		#a.square(200, color = '#202020')
		a.disc(100, color = '#202020')

		if a.scale(0.92).begin():
			a.arc(yellow_cell*3, max_cell*3, 88, width = 6, color = "#00c000")
			a.arc(red_cell*3, yellow_cell*3, 88, width = 6, color = "#ffc000")
			a.arc(yellow_cell*4, max_cell*4, 96, width = 6, color = "#00c000")
			a.arc(red_cell*4, yellow_cell*4, 96, width = 6, color = "#ffc000")
			a.arc(yellow_cell*5, max_cell*5, 88, width = 6, color = "#00c000")
			a.arc(red_cell*5, yellow_cell*5, 88, width = 6, color = "#ffc000")
			a.arc(yellow_cell*6, max_cell*6, 96, width = 6, color = "#00c000")
			a.arc(red_cell*6, yellow_cell*6, 96, width = 6, color = "#ffc000")

			for i in range(min_volts, max_volts+1, 1):
				a.tick(i, 93, 99, 1)

			for i in range(min_volts, max_volts+1, 5):
				a.tick(i, 90, 99, 2)

			for i in range(min_volts, max_volts+1, 10):
				a.tick(i, 84, 99, 2)

			#a.tick(red_line, 70, 99.5, 3.3, color = "#c00000")

			if a.begin(font_size = 20):
				a.at(22, -56).text("10")
				a.at(58, -23).text("12")
				a.at(62, 25).text("14")
				a.at(35, 65).text("16")
				a.at(-11, 74).text("18")
				a.at(-48, 51).text("20")
				a.at(-65, 3).text("22")
				a.at(-47, -39).text("24")
				a.end()

			a.at(0, -25).text("MAIN", font_size = 15)
			a.at(0, 40).text("VOLTS", font_size = 15)

			pos = (yellow_cell*3-min_volts) * 340.0 / (max_volts-min_volts)
			a.arctext(pos, 100, "3 Cell", size = 11, color = "#f0f0f0", font_weight = "bold")

			pos = (yellow_cell*4-min_volts) * 340.0 / (max_volts-min_volts)
			a.arctext(pos, 100, "4 Cell", size = 11, color = "#f0f0f0", font_weight = "bold")

			pos = ((yellow_cell+1)*5-min_volts) * 340.0 / (max_volts-min_volts)
			a.arctext(pos, 100, "5 Cell", size = 11, color = "#f0f0f0", font_weight = "bold")

			pos = ((yellow_cell+4)*6-min_volts) * 340.0 / (max_volts-min_volts)
			a.arctext(pos, 100, "6 Cell", size = 11, color = "#f0f0f0", font_weight = "bold")


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

