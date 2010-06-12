all:
	$(MAKE) -C examples

clean:
	$(MAKE) -C examples clean
	$(MAKE) -C lib clean

help:
	@echo "targets: all clean help"
