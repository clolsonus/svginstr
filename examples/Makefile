export PYTHONPATH=../lib:$$PYTHONPATH


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


svg: gsdi.svg test.svg clock.svg torque.svg arctest.svg


png: gsdi.png test.png clock.png torque.png arctest.png


%.png: %.svg
	../bin/svg2png $<


%.svg: %.py
	./$<


clean:
	rm -f *.svg *.xml *.png


help:
	@echo "targets: svg png clean help"
