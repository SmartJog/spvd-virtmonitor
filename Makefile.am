SUBDIRS = doc

dist_doc_DATA = README.rst

nodist_virtmonitor_PYTHON = virtmonitor.py

edit = $(SED) \
	-e 's|@PACKAGE_VERSION[@]|$(PACKAGE_VERSION)|g'

virtmonitor.py: virtmonitor.py.in Makefile
	$(edit) $< > $@

BUILT_SOURCES = virtmonitor.py
CLEANFILES = $(BUILT_SOURCES)
EXTRA_DIST = virtmonitor.py.in
