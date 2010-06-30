export PYTHONPATH=../lib:$$PYTHONPATH

PYFILES=$(wildcard *.py)
SVGFILES=$(PYFILES:.py=.svg)
PNGFILES=$(PYFILES:.py=.png)

all: svg

svg: $(SVGFILES)

png: $(PNGFILES)

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
