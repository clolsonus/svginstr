# $Id: Makefile,v 1.3 2005/11/08 21:23:31 m Exp m $
FILES=gsdi.svg test.svg clock.svg torque.svg arctest.svg

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



all:
	./torque.py
	./clock.py
	./test.py
	./arctest.py
	./gsdi.py
	./kclock.py

#	${UPDATE}
#	./svg2png test.svg test.png


clean:
	rm -f {torque,clock,test,arctest,gsdi,kclock}.{svg,xml} svginstr.pyc
	rm -rf svginstr svginstr.tar.gz

arc: clean
	mkdir svginstr
	cp *.py Makefile svg2png* svginstr/
	tar -czf svginstr.tar.gz svginstr/
	rm -rf svginstr
	aon put svginstr.tar.gz

