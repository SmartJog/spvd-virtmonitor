AC_PREREQ([2.67])

AC_INIT([spvd-virtmonitor],[0.2.0])

AM_INIT_AUTOMAKE([foreign])

AM_PATH_PYTHON([2.6])
AC_PATH_PROG(TXT2TAGS, txt2tags)

AC_SUBST([spvddir], [\$\(datadir\)/spvd])
AC_SUBST([virtmonitordir], [\$\(spvddir\)/plugins])

AC_CONFIG_FILES([
	Makefile
	doc/Makefile
])

AC_OUTPUT
