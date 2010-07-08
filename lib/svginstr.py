#!python

import sys
import gzip
import string
from math import ceil, sin, cos, pi, sqrt
from random import random

__author__ = "Melchior FRANZ < mfranz # aon : at >"
__url__ = "http://gitorious.org/svginstr/"
__version__ = "0.2"
__license__ = "GPL v2"
__doc__ = """
"""



class Error(Exception):
	pass



class Matrix:
	def __init__(self, a = 1, b = 0, c = 0, d = 1, e = 0, f = 0):
		self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f

	def __str__(self):
		return "[Matrix %f %f %f %f %f %f]" % (self.a, self.b, self.c, self.d, self.e, self.f)

	def copy(self):
		return Matrix(self.a, self.b, self.c, self.d, self.e, self.f)

	def transform(self, u, v):
		return u * self.a + v * self.c + self.e, u * self.b + v * self.d + self.f

	def multiply(self, mat):
		a = mat.a * self.a + mat.c * self.b
		b = mat.b * self.a + mat.d * self.b
		c = mat.a * self.c + mat.c * self.d
		d = mat.b * self.c + mat.d * self.d
		e = mat.a * self.e + mat.c * self.f + mat.e
		f = mat.b * self.e + mat.d * self.f + mat.f
		self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f
		return self

	def invert(self):
		det = (self.a * self.d - self.b * self.c)
		if det == 0.0:
			raise ValueError("Matrix not invertible")
		idet = 1.0 / det
		a = idet * self.d
		b = idet * -self.b
		c = idet * -self.c
		d = idet * self.a
		e = idet * (self.f * self.c - self.d * self.e)
		f = idet * (self.b * self.e - self.f * self.a)
		self.a, self.b, self.c, self.d, self.e, self.f = a, b, c, d, e, f
		return self

	def translate(self, dx, dy):
		return self.multiply(Matrix(1, 0, 0, 1, dx, dy))

	def scale(self, sx, sy = None):
		if sy == None:
			sy = sx
		return self.multiply(Matrix(sx, 0, 0, sy, 0, 0))

	def rotate(self, a):
		a = float(a) * pi / 180.0
		return self.multiply(Matrix(cos(a), sin(a), -sin(a), cos(a), 0, 0))

	def skewX(self, a):
		a = float(a) * pi / 180.0
		return self.multiply(Matrix(1, 0, tan(a), 1, 0, 0))

	def skewY(self, a):
		a = float(a) * pi / 180.0
		return self.multiply(Matrix(1, tan(a), 0, 1, 0, 0))



class Path:
	def __init__(self, x = None, y = None):
		self.dbg = False
		self.dbgpoints = []
		self.dbglines = []
		self.absolute = True
		self.str = ""

		if x != None and y != None:
			self.x, self.y = x, y
			self.str += "M %s %s" % (x, y)
			self.dbgpoints.append((x, y))
		else:
			self.x = self.y = 0

	def __str__(self):
		return self.str

	def _assert_multi_args(self, args, num):
		if len(args) % num:
			raise Error("Path: incomplete argument list")

	def _update(self, x, y):
		if self.absolute:
			self.x = x
			self.y = y
		else:
			self.x += x
			self.y += y

	def abs(self):
		self.absolute = True
		return self

	def rel(self):
		self.absolute = False
		return self

	def moveto(self, x, y):
		self.str += " %s %s %s" % (['m', 'M'][self.absolute], x, y)
		self._update(x, y)
		self.dbgpoints.append((self.x, self.y))
		return self

	def moveto_polar(self, angle, radius):
		x, y = radius * sind(angle), radius * cosd(angle)
		self.str += " %s %s %s" % (['m', 'M'][self.absolute], x, y)
		self._update(x, y)
		self.dbgpoints.append((self.x, self.y))
		return self

	def lineto(self, *args):
		self._assert_multi_args(args, 2)
		while args:
			x, y = args[0], args[1]
			args = args[2:]
			self.str += " %s %s %s" % (['l', 'L'][self.absolute], x, y)
			self._update(x, y)
			self.dbgpoints.append((self.x, self.x))
		return self

	def lineto_polar(self, *args):
		self._assert_multi_args(args, 2)
		while args:
			angle, radius, args = args[0], args[1], args[2:]
			x, y = radius * sind(angle), radius * cosd(angle)
			self.str += " %s %s %s" % (['l', 'L'][self.absolute], x, y)
			self._update(x, y)
			self.dbgpoints.append((self.x, self.y))
		return self

	def close(self):
		self.str += " z"
		return self

	def right(self, dx):
		self.str += " h %s" % dx
		self.x += dx
		self.dbgpoints.append((self.x, self.y))
		return self

	def left(self, dx):
		return self.right(-dx)

	def down(self, dy):
		self.str += " v %s" % dy
		self.y += dy
		self.dbgpoints.append((self.x, self.y))
		return self

	def up(self, dy):
		return self.down(-dy)

	def cubic_bezier(self, x1, y1, x2, y2, x, y): # TODO c
		self._update(x, y)
		self.dbgpoints.append((self.x, self.y))
		self.dbgpoints.append((x1, y1))
		self.dbgpoints.append((x2, y2))
		self.dbglines.append((x1, y1, x2, y2), (x2, y2, x, y))
		return self

	def smooth_cubic_bezier(self, x2, y2, x, y):  # TODO s
		self.dbgpoints.append((x, y))
		self.dbgpoints.append((x2, y2))
		self.dbglines.append((x2, y2, x, y))
		return self

	def quad_bezier(selfs, x1, y1, x, y):  # TODO q
		self.dbgpoints.append((x1, y1))
		self.dbgpoints.append((x, y))
		self.dbglines.append((x1, y1, x, y))
		return self

	def smooth_quad_bezier(self, x, y): # TODO t
		self.dbgpoints.append((x, y))
		return self

	def arc(self, rx, ry, rot, large, sweep, x, y):
		self.dbgpoints.append((x, y))
		self.str += " %s %s, %s %s %s, %s %s, %s" % (['a', 'A'][self.absolute], rx, ry, rot, large, sweep, x, y)
		return self

	def debug(self, instr):
		for l in self.dbglines:
			instr.write('<line x1="%s" y1="%s" x2="%s" y2="%s" stroke-width="%s" stroke="%s"/>' \
					% (l[0], l[1], l[2], l[3], instr.unit * 0.5, 'white'))
		for p in self.dbgpoints:
			instr.write('<circle cx="%s" cy="%s" r="%s" fill="%s"/>' % (p[0], p[1], instr.unit, 'green'))



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



class Global:
	transform = []
	style = []
	matrix = None  # for OpenGL UV



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
		self.matrices = [Global.matrix.copy()]
		self.matrix = None
		self.defs = []
		self.trans = []
		self.contents = []
		self.reset()
		self.unit = 0.01

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

	def begin(self, name = None):
		attr = ""
		if name:
			attr += ' id="%s"' % name

		if self.trans:
			t = self.trans[:]
			t.reverse()
			attr += ' transform="%s"' % string.join(t)

		self.write('<g%s>' % attr)

		self.matrices.append(self.matrix.multiply(self.matrices[-1]))

		x, y = self.matrices[-1].copy().invert().transform(0, 1)
		self.unit = 0.01 * sqrt(x * x + y * y)

		self.reset()
		return True

	def end(self):
		self.write('</g>')
		self.matrices.pop()

	def angle(self, alpha):
		return alpha - 90

	def reset(self):
		self.at_origin()
		self.styles = []
		self.trans = []
		self.matrix = Matrix()

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
		if radius == 0:
			radius = 0.00000000001

		attrib = "" # FIXME self._attrib()
		self.rotate(R(b))
		if self.x != 0 or self.y != 0:
			self.translate(self.x, self.y)
		self.begin()
		self.write('<path d="M%s,%s A%s,%s %s %s,1 %s,%s" ' \
				'fill="none" stroke-width="%s" stroke="%s" opacity="%s"%s/>' %\
				(radius, 0, radius, radius, e / 2, [0, 1][e >= 180], R(radius * cosd(e)), R(radius * sind(e)),
				p['stroke-width'], p['color'], p['opacity'], attrib))
		self.end()

	def tick(self, alpha, inner, outer, width = None, color = None, opacity = None, dic = {}):
		p = self.getparams(dic, {'color': color, '#stroke-width': width, 'opacity': opacity})
		attrib = "" # FIXME self._attrib()
		if self.x != 0 or self.y != 0:
			self.translate(self.x, self.y)
		self.rotate(R(self.angle(alpha)))
		self.begin()
		self.write('<line x1="%s" x2="%s" stroke-width="%s" stroke="%s" opacity="%s"%s/>' %\
				(R(inner), R(outer), p['stroke-width'], p['color'], p['opacity'], attrib))
		self.end()


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
		if y == None:
			y = 0
		self.trans.append("translate(%s, %s)" % (x, y))
		self.matrix.translate(x, y)
		return self

	def rotate(self, a, x = None, y = None):
		if x == None and y == None:
			self.trans.append("rotate(%s)" % a)
			self.matrix.rotate(a)
		else:
			self.trans.append("rotate(%s, %s, %s)" % (a, x, y))
			self.matrix.translate(-x, -y).rotate(a).translate(x, y)
		return self

	def scale(self, x, y = None):
		if y == None:
			y = x
		self.trans.append("scale(%s, %s)" % (x, y))
		self.matrix.scale(x, y)
		return self

	def xscale(self, x):
		self.trans.append("scale(%s, 1)" % x)
		self.matrix.scale(x, 1)
		return self

	def yscale(self, y):
		self.trans.append("scale(1, %s)" % y)
		self.matrix.scale(1, y)
		return self

	def xskew(self, a):
		self.trans.append("skewX(%s)" % a)
		self.matrix.skewX(a)
		return self

	def yskew(self, a):
		self.trans.append("skewY(%s)" % a)
		self.matrix.skewY(a)
		return self

	def matrix(self, a, b, c, d, e, f):
		self.trans.append("matrix(%s, %s, %s, %s, %s, %s)" % (a, b, c, d, e, f))
		self.matrix.multiply(Matrix(a, b, c, d, e, f))
		return self

	def region(self, x, y, w, h, clip = 1):
		W = max(w, h)       # scale and translate applied in reverse order:
		return self.scale(W / 200.0).translate(x + w * 0.5, y + h * 0.5)



class Instrument(SVG):
	def __init__(self, filename, w, h = None, desc = None):
		h = h or w
		# matrix that turns svginstr's coordinates into OpenGL UV coordinates
		Global.matrix = Matrix().translate(-0.5, -0.5).scale(200, -200).invert()
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
		self.write('<text fill="%s" font-family="%s" font-size="%s">' % (color, font, R(size)))
		self.write('<textPath xlink:href="#foo">%s</textPath>' % text)
		self.write('</text>')
		self.write('</g>')

	def screw(self, scale, rot = None):
		if rot == None:
			rot = random() * 180

		hole = RadialGradient()
		hole.stop("0%", 0, alpha = 1)
		hole.stop("30%", 0, alpha = 1)
		hole.stop("61%", 0, alpha = 0)

		head = RadialGradient("50%", "50%", "70%", "0%", "0%")
		head.stop("0%", 60)
		head.stop("90%", 25)
		head.stop("100%", 10)

		if self.scale(scale).translate(self.x, self.y).begin():
			self.gradient(hole).disc(100)
			self.gradient(head).disc(50)
			if self.rotate(rot).begin():
				self.rectangle(100, 19, color = "#1a1a1a")
			self.end()
		self.end()

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
