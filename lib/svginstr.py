#!python

import sys, gzip, string
from math import ceil, sin, cos, pi

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://gitorious.org/svginstr/"
__version__ = "0.2"
__license__ = "GPL v2"
__doc__ = """
"""



class Error(Exception):
	pass



class Global:
	transform = []
	style = []



class Gradient:
	counter = 0

	def __init__(self):
		self.stops = []
		Gradient.counter += 1
		self.name = "gradient%d" % Gradient.counter

	def stop(self, offset, red, green = None, blue = None, alpha = 1):
		if green == None:
			green = red
		if blue == None:
			blue = green
		self.stops.append((offset, red, green, blue, alpha))
		return self

	def code(self):
		return ["<stop offset=\"%s\" style=\"stop-color:rgb(%s, %s, %s); stop-opacity:%s\"/>" \
				% b for b in self.stops]



class LinearGradient(Gradient):
	def __init__(self, x1 = "0%", y1 = "0%", x2 = "100%", y2 = "100%"):
		Gradient.__init__(self)
		self.x1, self.y1, self.x2, self.y2 = x1, y1, x2, y2

	def copy(self):
		c = LinearGradient(self.x1, self.y1, self.x2, self.y2)
		c.stops = self.stops[:]
		return c

	def code(self):
		return ["<linearGradient id=\"%s\" x1=\"%s\" y1=\"%s\" x2=\"%s\" y2=\"%s\">" \
				% (self.name, self.x1, self.y1, self.x2, self.y2)] \
				+ Gradient.code(self) + ["</linearGradient>"]



class RadialGradient(Gradient):
	def __init__(self, cx = "50%", cy = "50%", r = "50%", fx = None, fy = None):
		Gradient.__init__(self)
		if fx == None:
			fx = cx
		if fy == None:
			fy = cy
		self.cx, self.cy, self.r, self.fx, self.fy = cx, cy, r, fx, fy

	def copy(self):
		c = RadialGradient(self.cx, self.cy, self.r, self.fx, self.fy)
		c.stops = self.stops[:]
		return c

	def code(self):
		return ["<radialGradient id=\"%s\" cx=\"%s\" cy=\"%s\" r=\"%s\" fx=\"%s\" fy=\"%s\">" \
				% (self.name, self.cx, self.cy, self.r, self.fx, self.fy)] \
				+ Gradient.code(self) + ["</radialGradient>"]



class SVG:
	default = {
		'color': 'white',
		'opacity': 1,
		'stroke-width': 1,
		'font-family': 'Helvetica',
		'font-size': 11,
		'font-weight': 'normal',
	}

	def __init__(self, filename, svg = ""):
		self.x = 0
		self.y = 0
		self.indent = 0
		self.stack = []
		self.defs = []
		self.trans = []
		self.contents = []
		self.reset()

		try:
			if filename.endswith(".svgz") or filename.endswith(".svg.gz"):
				self.file = gzip.GzipFile(filename, "w")
			else:
				self.file = open(filename, "w")
			self._write('<?xml version="1.0" standalone="no"?>')
			self._write('<!DOCTYPE svg PUBLIC "-//W3C//DTD SVG 1.1//EN" "http://www.w3.org/Graphics/SVG/1.1/DTD/svg11.dtd">')
			self._write()
			self._write('<svg %s xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink" version="1.1">' % svg)

		except IOError, (errno, strerror):
			raise Error("I/O error(%s): %s" % (errno, strerror))

	def __del__(self):
		try:
			if self.defs:
				self._write("<defs>")
				for d in self.defs:
					for i in d.code():
						self._write(i)
				self._write("</defs>")

			for i in self.contents:
				self._write(i)

			self._write("</svg>\n")
			self.file.close()

		except IOError, (errno, strerror):
			raise Error("I/O error(%s): %s" % (errno, strerror))

	def _write(self, s = ""):
		""" For internal purposes only. Don't use from outside! """
		try:
			s = s.strip()
			if s.startswith('<?') or s.startswith('<!'):
				self.file.write(s + '\n')
				return

			if s.startswith('</'):
				self.indent -= 1

			self.file.write(self.indent * '\t' + s + '\n')

			if s.startswith('<') and s.find('</') > 0:
				pass
			elif s.startswith('<') and not s.startswith('</') and not s.endswith('/>'):
				self.indent += 1

		except IOError, (errno, strerror):
			raise Error("I/O error(%s): %s" % (errno, strerror))

	def write(self, s = ""):
		self.contents.append(s)

	def title(self, s):
		self._write('<title>%s</title>' % s)

	def description(self, s):
		self._write('<desc>%s</desc>' % s)

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

	def group(self, trans):
		" return a group class that has access to self "
		return _group(self, trans)

	def push(self):
		self.stack.append(_group(self, string.join(self.trans)))
		self.trans = []

	def pop(self):
		self.stack.pop()

	def angle(self, alpha):
		return alpha - 90

	def reset(self):
		self.at_origin()
		self.styles = []
		self.trans = []

	def _attrib(self):
		return string.join([self._style(), self._trans()], " ")

	# drawing primitives
	def circle(self, radius, width, color = None, dic = {}):
		p = self.getparams(dic, {'color': color})
		self.write('<circle cx="%s" cy="%s" r="%s" fill="none" stroke-width="%s" stroke="%s"%s/>' \
				% (self.x, self.y, R(radius), R(width), p['color'], self._attrib()))
		self.reset()

	def disc(self, radius, color = None, dic = {}):
		p = self.getparams(dic, {'color': color})
		self.write('<circle cx="%s" cy="%s" r="%s" fill="%s"%s/>' \
				% (self.x, self.y, R(radius), p['color'], self._attrib()))
		self.reset()

	def rectangle(self, width, height, color = None, dic = {}):
		p = self.getparams(dic, {'color': color})
		self.write('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"%s/>' % \
				(self.x - 0.5 * width, self.y - 0.5 * height, R(width), R(height), \
				color, self._attrib()))
		self.reset()

	def square(self, width, color = None, dic = {}):
		self.rectangle(width, width, color, dic)

	def text(self, text, size = None, font = None, color = None, dic = {}):
		p = self.getparams(dic, {'color': color, 'font-family': font, '#font-size': size})
		self.write('<text x="%s" y="%s" font-family="%s" font-size="%s" font-weight="%s" fill="%s" ' \
				'text-anchor="middle"%s>%s</text>' \
				% (self.x, self.y, p['font-family'], p['font-size'], p['font-weight'], p['color'], \
				self._attrib(), text))
		self.reset()

	def arc(self, begin, end, radius, width = None, color = None, opacity = None, dic = {}):
		p = self.getparams(dic, {'color': color, '#stroke-width': width, 'opacity': opacity})
		begin = self.angle(begin)
		end = self.angle(end)
		b = min(begin, end)
		e = max(begin, end) - b
		if self.x == 0 and self.y == 0: # FIXME
			trans = ""
		else:
			trans = "translate(%s %s) " % (self.x, self.y)
		if radius == 0:
			radius = 0.00000000001;
		_ = self.group("%srotate(%s)" % (trans, R(b)))
		self.write('<path d="M%s,%s A%s,%s %s %s,1 %s,%s" ' \
				'fill="none" stroke-width="%s" stroke="%s" opacity="%s"%s/>' %\
				(radius, 0, radius, radius, e / 2, [0, 1][e >= 180], R(radius * cosd(e)), R(radius * sind(e)),
				p['stroke-width'], p['color'], p['opacity'], self._attrib()))
		self.reset()

	def tick(self, alpha, inner, outer, width = None, color = None, opacity = None, dic = {}):
		p = self.getparams(dic, {'color': color, '#stroke-width': width, 'opacity': opacity})
		if self.x == 0 and self.y == 0: # FIXME
			trans = ""
		else:
			trans = "translate(%s %s) " % (self.x, self.y)
		_ = self.group("%srotate(%s)" % (trans, R(self.angle(alpha))))
		self.write('<line x1="%s" x2="%s" stroke-width="%s" stroke="%s" opacity="%s"%s/>' %\
				(R(inner), R(outer), p['stroke-width'], p['color'], p['opacity'], self._attrib()))
		self.reset()


	# positioning methods
	def at_origin(self):
		self.x = self.y = 0
		return self

	def at(self, x, y):
		return self.at_origin().offset(x, y)

	def at_polar(self, angle, radius):
		return self.at_origin().polar_offset(angle, radius)

	def offset(self, x, y):
		self.x += x
		self.y += y
		return self

	def polar_offset(self, angle, radius):
		"""first choose the azimuth (angle), then go the distance (radius)!"""
		a = self.angle(angle)
		self.x = radius * cosd(a)
		self.y = radius * sind(a)
		return self


	# style methods
	def _style(self):
		""" return assembled style """
		t = Global.style + self.styles
		if t:
			return " style=\"%s\"" % string.join(t, "; ")
		else:
			return ""

	def style(self, s):
		""" add one style """
		self.styles.append(s)
		return self

	def gradient(self, g, name = None):
		self.defs.append(g)
		return self.style("fill:url(#%s)" % (name or g.name))


	# transform methods
	def _trans(self):
		""" return assembled transformation """
		t = Global.transform + self.trans
		if t:
			return " transform=\"%s\"" % string.join(t, " ")
		else:
			return ""

	def translate(self, x, y = None):
		self.trans.append("translate(%s, %s)" % (x, y or 0))
		return self

	def rotate(self, a, x = None, y = None):
		if x == None and y == None:
			self.trans.append("rotate(%s)" % a)
		else:
			self.trans.append("rotate(%s, %s, %s)" % (a, x, y))
		return self

	def scale(self, x, y = None):
		if y == None:
			y = x
		self.trans.append("scale(%s, %s)" % (x, y))
		return self

	def xscale(self, x):
		self.trans.append("scale(%s, 1)" % x)
		return self

	def yscale(self, y):
		self.trans.append("scale(1, %s)" % y)
		return self

	def xskew(self, a):
		self.trans.append("skewX(%s)" % a)
		return self

	def yskew(self, a):
		self.trans.append("skewY(%s)" % a)
		return self

	def matrix(self, a, b, c, d, e, f):
		self.trans.append("matrix(%s, %s, %s, %s, %s, %s)" % (a, b, c, d, e, f))
		return self



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



class Instrument(SVG):
	def __init__(self, filename, w, h = None, desc = None):
		h = h or w
		SVG.__init__(self, filename, 'width="%spx" height="%spx" viewBox="%s %s %s %s"' % \
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
				self.write('<rect x="%s" y="%s" width="%s" height="%s" fill="%s"/>' % \
						(R(size * x - 100), R(size * y - 100), R(size), R(size), color))

	def arctext(self, startangle, r, text, size = None, font = None, color = None):
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

	def screw(self, scale, rot):
		g = RadialGradient("50%", "50%", "50%", "50%", "50%")
		g.stop("0%", 24)
		g.stop("45%",24)
		g.stop("50%", 30)
		g.stop("50%", 10, alpha = 1)
		g.stop("70%", 30, alpha = 0.1)
		g.stop("100%", 0, alpha = 0)

		x, y = self.x, self.y
		self.at_origin()
		self.translate(x, y).push()
		self.rotate(rot).scale(scale).push()
		self.gradient(g).disc(100)
		self.rectangle(100, 16, color = "#141414")
		self.pop()
		self.pop()

	def xml(self, name):
		return _xml(self, name)



class _xml:
	def __init__(self, parent, filename):
		if not isinstance(parent, Instrument):
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



def norm_angle(self, a):
	while (a < 0):
		a += 360
	while (a >= 360):
		a -= 360
	return a
