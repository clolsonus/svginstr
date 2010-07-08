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
	a = Instrument("torque.svg", 512, 512, "Bo105 torquemeter; " + __version__)

	if a.region(-100, -100, 175, 175).begin():
		#a.square(200, '#202020')
		a.disc(100, '#202020')

		if a.scale(0.92).begin():
			a.angle = lambda x: 230.0 * (x - 60) / 120 - 90

			for i in range(0, 120, 2):
				a.tick(i, 82, 99, 1)

			a.arc(0, 80, 94.5, width = 10, color = "#00c000")

			for i in range(0, 121, 10):
				a.tick(i, 82, 99.5, 3)

			a.tick(80, 81, 99.5, 3, color = "#ffc000")
			a.tick(110, 70, 99.5, 3.3, color = "red")

			fontsize = 20
			a.at(-60, 38).text("0", fontsize)
			a.at(-61, -8).text("20", fontsize)
			a.at(-39, -46).text("40", fontsize)
			a.at(0, -61).text("60", fontsize)
			a.at(39, -46).text("80", fontsize)
			a.at(56, -8).text("100", fontsize)
			a.at(50, 38).text("120", fontsize)

			a.at(0, 55).text("%", 17)
			a.at(0, 75).text("TORQUE", 20)

			a.at(0, -30).screw(0.12, 30)
			a.at(0, 30).screw(0.12, 70)

			a.disc(8, 'black')
			a.disc(0.4, 'red')
		a.end()

		bezelshadow = RadialGradient()
		bezelshadow.stop("0%", 0, alpha = 0)
		bezelshadow.stop("85%", 0, alpha = 0)
		bezelshadow.stop("100%", 0, alpha = 0.4)
		a.gradient(bezelshadow).square(200)
	a.end()


	#-- needle --
	g = RadialGradient("50%", "50%", "80%", "0%", "0%")
	g.stop("0%", 60)
	g.stop("90%", 20)
	g.stop("100%", 5)

	if True:
		if 0:
			a.translate(88, -12).begin()    # separate (for final rendering)
		else:
			a.rotate(-113).translate(-12.5, -12.5).begin()  # centered (for tests)

		top = Path(-3, -40).rel().up(20).lineto(3, -6).lineto(3, 6).down(20).close()
		a.write('<path d="%s" fill="white" stroke="#d0d0d0" stroke-width="0.6"/>' % str(top))

		bot = Path(-3, -40).rel().down(60).arc(7, 7, 0, 1, 0, 6, 0).up(60).close()
		a.write('<path d="%s" fill="#242424" stroke="#181818" stroke-width="0.6"/>' % str(bot))

		#top.debug(a)
		#bot.debug(a)
		a.gradient(g).disc(10)
	a.end()


	xml = a.xml("torque")
	xml.animation("Lneedle", "sim/model/bo105/torque-pct", [0, 60, 120])
	xml.animation("Rneedle", "sim/model/bo105/torque-pct", [0, 60, 120])

except Error, e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

