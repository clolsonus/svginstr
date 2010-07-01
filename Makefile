all: svg

svg:
	$(MAKE) -C examples svg

png:
	$(MAKE) -C examples png

clean:
	$(MAKE) -C examples clean
	$(MAKE) -C lib clean

help:
	@echo "targets: all svg png clean help"
