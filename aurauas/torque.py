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
	a = Instrument("torque.svg", 512, 512, "Bo105 torquemeter; " + __version__).fg_size(384, 384)
	a.angle = lambda x: 230.0 * (x - 60) / 120 - 90

	#-- face ------------------------------------------------------------------------

	if a.region(-100, -100, 175, 175, name = "TEST").begin():
		#a.square(200, color = '#202020')
		a.disc(100, color = '#202020')

		if a.scale(0.92).begin():
			for i in range(0, 120, 2):
				a.tick(i, 82, 99, 1)

			a.arc(0, 80, 94.5, width = 10, color = "#00c000")

			for i in range(0, 121, 10):
				a.tick(i, 82, 99.5, 3)

			a.tick(80, 81, 99.5, 3, color = "#ffc000")
			a.tick(110, 70, 99.5, 3.3, color = "#c00000")

			if a.begin(font_size = 20):
				a.at(-60, 38).text("0")
				a.at(-61, -8).text("20")
				a.at(-39, -46).text("40")
				a.at(0, -61).text("60")
				a.at(39, -46).text("80")
				a.at(56, -8).text("100")
				a.at(50, 38).text("120")
				a.end()

			a.at(0, 55).text("%", font_size = 17)
			a.at(0, 75).text("TORQUE", font_size = 20)

			a.at(0, -30).screw(0.12, 30)
			a.at(0, 30).screw(0.12, 70)

			a.disc(8, color = 'black')
			a.disc(0.4, color = 'red')
			a.end()

		bezelshadow = RadialGradient()
		bezelshadow.stop("0%", 0, alpha = 0)
		bezelshadow.stop("85%", 0, alpha = 0)
		bezelshadow.stop("100%", 0, alpha = 0.4)
		a.gradient(bezelshadow).square(200)
		a.end()

	#-- needle ----------------------------------------------------------------------

	if True:
		if 0:
			a.translate(88, -12).begin()       # separate (for final rendering)
			a.begin()
		else:
			a.translate(-12.5, -12.5).begin()  # centered (for tests)
			a.rotate(-113).begin()

		tip = Path(-3, -30).up(30).lineto(3, -19).lineto(3, 19).down(30).close()
		a.shape(tip, fill = "#fff0d0", stroke = "#000000", stroke_width = 0.1)

		tail = Path(-3, -30).down(50).arc(7, 7, 0, 1, 0, 6, 0).up(50).close()
		a.shape(tail, fill = "#242424", stroke = "#181818", stroke_width = 0.6)

		# counter weight overlay
		weight = RadialGradient().stop("0%", 38).stop("90%", 35).stop("100%", 28)
		a.at(0, 26.25).gradient(weight).disc(7)

		# engine number
		a.at(0.3, -50).text("1", color = "#101010")

		#tip.debug(a)
		#tail.debug(a)
		a.end()

		# top cap
		g = RadialGradient("50%", "50%", "80%", "0%", "0%")
		g.stop("0%", 60)
		g.stop("90%", 20)
		g.stop("100%", 5)
		a.gradient(g).disc(9)
		a.end()


	# generate animation XML file for FlightGear
	xml = a.xml("torque")
	xml.animation("Lneedle", "sim/model/bo105/torque-pct", [0, 60, 120])
	xml.animation("Rneedle", "sim/model/bo105/torque-pct", [0, 60, 120])

except Error as e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

