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
    levels = 2
    texture_w = 256
    texture_h = 256

    gray = '#909090'
    green = '#80FF80'
    yellow = '#FFFF80'
    red = '#FF8080'

    min = -80
    max = 80

    part = (max-min) / 6
    part1 = (max-min) / 5

    # peripheral
    p0 = (min, max)
    p1 = (part, max)
    p2 = (min, -part)

    p3 = (max, min)
    p4 = (-part, min)
    p5 = (max, part)

    p6 = (part1, min)
    p7 = (min, part1)
    p8 = (-part1, max)
    p9 = (max, -part1)

    for level in range(levels):
        svg_name = "link" + str(level) + ".svg"
        a = Instrument(svg_name, texture_w, texture_h, "Link Icon; " + __version__).fg_size(texture_w, texture_h)

        link = Path(p6[0],p6[1]).abs().lineto(p7[0],p7[1]).lineto(p8[0], p8[1]).lineto(p9[0],p9[1]).lineto(p6[0],p6[1]).close()
        print str(link)

        lower_tri = Path(p0[0],p0[1]).abs().lineto(p1[0],p1[1]).lineto(p2[0], p2[1]).lineto(p0[0],p0[1]).close()
        print str(lower_tri)

        upper_tri = Path(p3[0],p3[1]).abs().lineto(p4[0],p4[1]).lineto(p5[0], p5[1]).lineto(p3[0],p3[1]).close()
        print str(upper_tri)

        if a.region(-100, -100, 200, 200, name = "TEST").begin():
            if level == 0:
                a.shape( link, fill=gray, stroke=gray, stroke_width=1) 
                a.shape( lower_tri, fill=red, stroke=red, stroke_width=1)
                a.shape( upper_tri, fill=red, stroke=red, stroke_width=1) 
            else:
                a.shape( link, fill=green, stroke=green, stroke_width=1) 
                a.shape( lower_tri, fill=green, stroke=green, stroke_width=1)
                a.shape( upper_tri, fill=green, stroke=green, stroke_width=1) 

            a.end()

except Error as e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

