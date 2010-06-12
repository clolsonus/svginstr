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

all: gsdi.svg test.svg clock.svg torque.svg arctest.svg

%.svg: %.py
	./$<
#	$(UPDATE)


clean:
	rm -f {torque,clock,test,arctest,gsdi,kclock}.{svg,xml} svginstr.pyc
	rm -rf svginstr svginstr.tar.gz