#!/usr/bin/env python

import sys
sys.path.insert(0, "/home/curt/Projects/svginstr/lib")
from svginstr import *

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://gitorious.org/svginstr/"
__version__ = "0.2"
__license__ = "GPL v2+"
__doc__ = """
"""


Global.indent = '\t'


try:
	a = Instrument("aura-asi1.svg", 512, 512, "Aura ASI; " + __version__).fg_size(384, 384)

	#-- face ------------------------------------------------------------------------

	if a.region(-100, -100, 200, 200, name = "TEST").begin():
		#a.square(200, color = '#202020')
		a.disc(100, color = '#202020')

except Error as e:
	print >>sys.stderr, "\033[31;1m%s\033[m\n" % e

