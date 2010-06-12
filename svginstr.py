#!python

import sys, gzip
from math import ceil, sin, cos, pi

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://members.aon.at/mfranz/flightgear/"
__version__ = "$Id: svginstr.py,v 1.1 2005/11/08 21:22:28 m Exp m $; GPL v2"
__doc__ = """
"""



class Error(Exception):
	pass



class SVG:
	stack = []
	indent = 0
	default = {
		'color':	'white',
		'opacity':	1,
		'stroke-width':	1,
		'font-family':	'Helvetica',
		'font-size':	11,
		'font-weight':	'normal',
	}

	def __init__(self, filename, svg = ""):
		try:
			if filename.endswith(".svgz"):
				self.file = gzip.GzipFile(filename, "w")
			else:
				self.file = open(filename, "w")
			self.write('<?xml version="1.0" standalone="no"?>')
			self.write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">')
			self.write('<svg %s xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">' % svg)

		except IOError, (errno, strerror):
			raise Error("I/O error(%s): %s" % (errno, strerror))

	def __del__(self):
		try:
			self.write("</svg>\n")
			self.file.close()

		except IOError, (errno, strerror):
			raise Error("I/O error(%s): %s" % (errno, strerror))

	def write(self, s):
		try:
			s = s.strip()
			if s.startswith('<?') or s.startswith('<!'):
				self.file.write(s + '\n')
				return

			if s.startswith('</'):
				self.indent -= 1

			self.file.write(self.indent * '\t' + s + '\n')

			if s.startswith('<') and not s.startswith('</') and not s.endswith('/>'):
				self.indent += 1

		except IOError, (errno, strerror):
			raise Error("I/O error(%s): %s" % (errno, strerror))

	def description(self, s):
		self.write('<desc>%s</desc>' % s)
		self.indent -= 1

	def set(self, dic):
		self.default.update(dic)

	def getparams(self, dic, odic = {}):
		" return copy of class defaults with dic settings merged in"
		p = dict(self.default)
		p.update(dic)
		for k, v in odic.iteritems():
			if not v:
				continue
			if k[0] == '#':
				p[k[1:]] = R(v)
			else:
				p[k] = v
		return p

	def push(self, attr):
		self.stack.append(_group(self, attr))

	def pop(self):
		self.stack.pop()

	def angle(self, alpha):
		return alpha - 90

	def norm(self, a):
		while (a < 0):
			a += 360
		while (a >= 360):
			a -= 360
		return a

	def circle(self, radius, width, color = None, x = 0, y = 0, dic = {}):
		p = self.getparams(dic, {'color': color})
		self.write('<circle cx="%s" cy="%s" r="%s" fill="none" stroke-width="%s" stroke="%s"/>' \
				% (R(x), R(y), R(radius), R(width), p['color']))

	def disc(self, radius, color = None, x = 0, y = 0, dic = {}):
		p = self.getparams(dic, {'color': color})
		self.write('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (R(x), R(y), R(radius), p['color']))

	def square(self, width, color = None, x = 0, y = 0, dic = {}):
		p = self.getparams(dic, {'color': color})
		self.write('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % \
				(R(x - 0.5 * width), R(y - 0.5 * width), R(width), R(width), color))

	def arc(self, r, begin, end, width = None, color = None, opacity = None, dic = {}):
		p = self.getparams(dic, {'color': color, '#stroke-width': width, 'opacity': opacity})
		begin = self.angle(begin)
		end = self.angle(end)
		b = min(begin, end)
		e = max(begin, end) - b
		_ = self.group("rotate(%s)" % R(b))
		self.write('<path d="M%s,%s A%s,%s %s %s,1 %s,%s" ' \
				'fill="none" stroke-width="%s" stroke="%s" opacity="%s"/>' %\
				(r, 0, r, r, e / 2, [0, 1][e >= 180], R(r * cosd(e)), R(r * sind(e)),
				p['stroke-width'], p['color'], p['opacity']))

	def tick(self, a, b, alpha, width = None, color = None, opacity = None, dic = {}):
		p = self.getparams(dic, {'color': color, '#stroke-width': width, 'opacity': opacity})
		_ = self.group("rotate(%s)" % R(self.angle(alpha)))
		self.write('<line x1="%s" x2="%s" stroke-width="%s" stroke="%s" opacity="%s"/>' %\
				(R(a), R(b), p['stroke-width'], p['color'], p['opacity']))

	def bullet(self, r, alpha, width, color = None, dic = {}):
		p = self.getparams(dic, {'color': color})
		_ = self.group("rotate(%s)" % R(self.angle(alpha)))
		self.disc(width, x = r, dic = p)

	def text(self, x, y, text, size = None, font = None, color = None, dic = {}):
		p = self.getparams(dic, {'color': color, 'font-family': font, '#font-size': size})
		self.write('<text x="%s" y="%s" font-family="%s" font-size="%s" font-weight="%s" fill="%s" ' \
				'text-anchor="middle">%s</text>' \
				% (R(x), R(y), p['font-family'], p['font-size'], p['font-weight'], p['color'], text))
		self.indent -= 1

	def ptext(self, alpha, radius, text, size = None, font = None, color = None, dic = {}):
		a = self.angle(alpha)
		x = radius * cosd(a)
		y = radius * sind(a)
		self.text(x, y, text, size, font, color, dic)

	def group(self, trans):
		" return a group class that has access to self "
		return _group(self, trans)



class _group:
	" 'subclass' of SVG that has access to SVG methods "
	def __init__(self, parent, trans = None):
		if not isinstance(parent, SVG):
			self.svg = None
			raise ValueError("_group is only available as method of SVG")
		self.svg = parent
		if trans:
			self.svg.write('<g transform="%s">' % trans)
		else:
			self.svg.write('<g>')

	def __del__(self):
		if self.svg:
			self.svg.write('</g>')



class instrument(SVG):
	def __init__(self, filename, w, h = None, desc = None):
		h = h or w
		SVG.__init__(self, filename, 'width="%spx" height="%spx" viewBox="%s %s %s %s"' %\
				(R(w), R(h), 0, 0, 200, 200))
		if desc:
			self.description(desc)
		self.write('<g font-family="%(font-family)s" transform="translate(100, 100)">' % self.default)
		self.write('<rect x="-100" y="-100" width="200" height="200" fill="none"/>')
		self.default = dict(SVG.default)
		#self.chequer()

	def __del__(self):
		self.write('</g>')
		SVG.__del__(self)

	def chequer(self, size = 10, color = "lightgrey"):
		" fake transparency  ;-) "
		for y in range(20):
			for x in range(20):
				if (x + y) & 1:
					continue
				self.write('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' %\
						(R(size * x - 100), R(size * y - 100), R(size), R(size), color))

	def arctext(self, r, startangle, text, size = None, font = None, color = None):
		if not font:
			font = self.font
		if not size:
			size = self.size
		if not color:
			color = self.color
		r = R(r)
		self.write('<g transform="rotate(%s)">' % startangle)
		self.write('<defs>')
		self.write('<path id="foo" d="M0,-%s A%s,%s 0 0,1 0,%s"/>' % (r, r, r, r))
		self.write('</defs>')
		self.write('<text fill="%s" font-family="%s" font-size="%s">' \
				% (color, font, R(size)))
		self.write('<textPath xlink:href="#foo">%s</textPath>' % text)
		self.indent -= 1
		self.write('</text>')
		self.write('</g>')

	def xml(self, name):
		return _xml(self, name)



class _xml:
	def __init__(self, parent, filename):
		if not isinstance(parent, instrument):
			self.instrument = None
			raise ValueError("_xml is only available as method of instrument")
		self.instrument = parent

		try:
			self.file = open(filename + ".xml", "w")
			self.write('<?xml version="1.0"?>\n\n')
			self.write('<PropertyList>\n')
			self.write('\t<path>%s.ac</path>\n' % filename)

		except IOError, (errno, strerror):
			raise Error("I/O error(%s): %s" % (errno, strerror))

	def __del__(self):
		try:
			self.write("</PropertyList>\n")
			self.file.close()

		except IOError, (errno, strerror):
			raise Error("I/O error(%s): %s" % (errno, strerror))

	def write(self, s):
		try:
			self.file.write(s)

		except IOError, (errno, strerror):
			raise Error("I/O error(%s): %s" % (errno, strerror))

	def animation(self, objname, prop, points):
		self.write('\t<animation>\n')
		self.write('\t\t<type>rotate</type>\n')
		self.write('\t\t<object-name>%s</object-name>\n' % objname)
		self.write('\t\t<property>%s</property>\n' % prop)
		self.write('\t\t<interpolation>\n')
		for p in points:
			self.write('\t\t\t<entry><ind>%s</ind><dep>%s</dep></entry>\n' \
				% (R(p), R(self.instrument.angle(p))))
		self.write('\t\t</interpolation>\n')
		self.write('\t\t<axis>\n')
		self.write('\t\t\t<x>-1</x>\n')
		self.write('\t\t\t<y>0</y>\n')
		self.write('\t\t\t<z>0</z>\n')
		self.write('\t\t</axis>\n')
		self.write('\t</animation>\n')



def R(f, digits = 8):
	r = round(f, digits)
	if r == int(r):
		return str(int(r))
	else:
		return str(r)



def sind(a):
	return sin(a * pi / 180)



def cosd(a):
	return cos(a * pi / 180)



def position(a, b, n):
	" from angle, to angle, number "
	return [a + x * (float(b) - a) / n for x in range(n)] + [b]



def frange(start, end = None, step = None):
	if end:
		start += 0.0
	else:
		end = start + 0.0
		start = 0.0

	if not step:
		step = 1.0

	count = int(ceil((end - start) / step))
	L = [None,] * count
	for i in xrange(count):
		L[i] = start + i * step

	return L
