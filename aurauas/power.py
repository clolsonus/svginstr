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
	a = Instrument("power.svg", 512, 512, "Power; " + __version__).fg_size(384, 384)

	# * 10
	max_watts = 500
	a.angle = lambda x: 255 - (x*150/max_watts)

	#-- face ------------------------------------------------------------------------

	if a.region(-100, -100, 200, 200, name = "TEST").begin():
		#a.square(200, color = '#202020')
		a.disc(100, color = '#202020')

		if a.scale(0.92).begin():
			#a.arc(yellow_cell*3, max_cell*3, 88, width = 6, color = "#00c000")
			#a.arc(red_cell*3, yellow_cell*3, 88, width = 6, color = "#ffc000")

			for i in range(0, max_watts+1, 10):
				a.tick(i, 93, 99, 1)

			for i in range(0, max_watts+1, 50):
				a.tick(i, 90, 99, 2)

			for i in range(0, max_watts+1, 100):
				a.tick(i, 84, 99, 2)

			#a.tick(red_line, 70, 99.5, 3.3, color = "#c00000")

			if a.begin(font_size = 18):
				a.at(-43, 63).text("100")
				a.at(-63, 30).text("200")
				a.at(-63, -15).text("300")
				a.at(-45, -45).text("400")
				a.end()

			a.at(-35, 5).text("Watts", font_size = 15)

                        a.angle = lambda x: 75 - x * 1.5
                        
			a.arc(0, 10, 93, width = 12, color = "#d03030")
			a.arc(10, 25, 93, width = 12, color = "#ffd000")
			a.arc(25, 100, 92, width = 14, color = "#00c000")

			for i in range(0, 100+1, 5):
				a.tick(i, 93, 99, 1)

			for i in range(0, 100+1, 25):
				a.tick(i, 84, 99, 2)

			if a.begin(font_size = 18):
				a.at(20, 75).text("E")
				a.at(65, 5).text("1/2")
				a.at(20, -63).text("F")
			        a.end()
                                
                        a.at(30, 5).text("Batt", font_size = 15)

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

