export PYTHONPATH=../lib:$$PYTHONPATH

FONTDIR=$(shell cd ../fonts && pwd)
PYFILES=$(wildcard *.py)
SVGFILES=$(PYFILES:.py=.svg)
PNGFILES=$(PYFILES:.py=.png)

all: svg

svg: $(SVGFILES)

png:
	mkfontdir $(FONTDIR)
	xset +fp $(FONTDIR)
	xset fp rehash
	$(MAKE) $(PNGFILES)
	xset -fp $(FONTDIR)

%.png: %.svg
	../bin/svg2png $<

%.svg: %.py
	./$<

check: $(SVGFILES)
	@echo -e "\nchecking ..."
	@for i in $(SVGFILES); do echo -en "\t$$i ... "; xmllint $$i >/dev/null && echo OK; done

clean:
	rm -f *.svg *.xml *.png

help:
	@echo "targets: svg png check clean help"
