export PYTHONPATH=$$PYTHONPATH:../lib
SVG2PNG=../bin/svg2png

all: aura-asi-bg.png aura-asi-kt.png aura-asi-mps.png glass-pfd-horiz.png glass-pfd-main.png glass-pfd-parts.png glass-pfd-tapes.png torque.png res3-asi.png avionics-vcc.png main-volts.png volts.png amps.png power.png hdg.png hdg_hud.png

extra: battery gpslevel link

%.svg:	%.py
	./$<

%.png: %.svg
	../bin/svg2png $<

battery:
	./battery.py
	$(SVG2PNG) battery0.svg
	$(SVG2PNG) battery1.svg
	$(SVG2PNG) battery2.svg
	$(SVG2PNG) battery3.svg
	$(SVG2PNG) battery4.svg
	$(SVG2PNG) battery5.svg
	$(SVG2PNG) battery6.svg
	$(SVG2PNG) battery7.svg

gpslevel:
	./gpslevel.py
	$(SVG2PNG) gpslevel0.svg
	$(SVG2PNG) gpslevel1.svg
	$(SVG2PNG) gpslevel2.svg
	$(SVG2PNG) gpslevel3.svg
	$(SVG2PNG) gpslevel4.svg

link:
	./link.py
	$(SVG2PNG) link0.svg
	$(SVG2PNG) link1.svg
