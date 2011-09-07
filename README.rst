================
spvd-virtmonitor
================

spvd-virtmonitor is a supervision plugin to check the status of virtual machines
through webengine-virtmanager.

License
=======

spvd-virtmonitor is released under the `GNU LGPL 2.1 <http://www.gnu.org/licenses/lgpl-2.1.html>`_.


Build and installation
=======================

Bootstrapping
-------------

spvd-virtmonitor uses autotools for its build system.

If you checked out code from the git repository, you will need
autoconf and automake to generate the configure script and Makefiles.

To generate them, simply run::

    $ autoreconf -fvi

Building
--------

spvd-virtmonitor builds like a typical autotools-based project::

    $ ./configure && make && make install


Development
===========

We use `semantic versioning <http://semver.org/>`_ for
versioning. When working on a development release, we append ``~dev``
to the current version to distinguish released versions from
development ones. This has the advantage of working well with Debian's
version scheme, where ``~`` is considered smaller than everything (so
version 1.10.0 is more up to date than 1.10.0~dev).


Authors
=======

spvd-virtmonitor was created at SmartJog by :

* Gilles Dartiguelongue <gilles.dartiguelongue@smartjog.com>

