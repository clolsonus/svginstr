export PYTHONPATH=../lib:$$PYTHONPATH

PYFILES=$(wildcard *.py)
SVGFILES=$(PYFILES:.py=.svg)
PNGFILES=$(PYFILES:.py=.png)

UPDATE=@for konq in $$(dcop konqueror-*); do \
		echo $$konq; \
		for win in $$(dcop $$konq konqueror-mainwindow*); do \
			echo -e "\t$$win"; \
			url=$$(dcop $$konq $$win currentURL); \
			file=$${url/*\/};\
			for f in ${FILES}; do\
				if [ "$$f" == "$$file" ]; then \
					dcop $$konq $$win reload; \
				fi \
			done \
		done \
	done


all: svg
#	$(UPDATE)


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
