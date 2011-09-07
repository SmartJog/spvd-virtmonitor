dist_man5_MANS = spvd-virtmonitor.man

DISTCLEANFILES = $(dist_man5_MANS)
EXTRA_DIST = $(wildcard $(srcdir)/*.t2t)

SUFFIXES = .t2t

.t2t.man:
	$(TXT2TAGS) -o $@ $<
