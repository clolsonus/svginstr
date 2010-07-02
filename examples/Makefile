export PYTHONPATH=$(PWD)/../lib:$$PYTHONPATH
export FONTCONFIG_PATH=$(PWD)/../fonts:$$FONTCONFIG_PATH

FONTDIR=$(shell cd ../fonts && pwd)
PYFILES=$(wildcard *.py)
SVGFILES=$(PYFILES:.py=.svg)
PNGFILES=$(PYFILES:.py=.png)

all: svg

svg: $(SVGFILES)

png:
	-fc-cache $(FONTDIR)
	$(MAKE) $(PNGFILES)

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
