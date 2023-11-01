.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Release 4.3 (nanbield)
========================

Migration notes for 4.3 (nanbield)
------------------------------------

This section provides migration information for moving to the Yocto
Project 4.3 Release (codename "nanbield") from the prior release.

.. _migration-4.3-supported-kernel-versions:

Supported kernel versions
~~~~~~~~~~~~~~~~~~~~~~~~~

The :term:`OLDEST_KERNEL` setting has been changed to "5.15" in this release, meaning that
out the box, older kernels are not supported. There were two reasons for this.
Firstly it allows glibc optimisations that improve the performance of the system
by removing compatibility code and using modern kernel APIs exclusively. The second
issue was this allows 64 bit time support even on 32 bit platforms and resolves Y2038
issues.

It is still possible to override this value and build for older kernels, this is just
no longer the default supported configuration. This setting does not affect which
kernel versions SDKs will run against and does not affect which versions of the kernel
can be used to run builds.

.. _migration-4.3-layername-override:

Layername override implications
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Code can now know which layer a recipe is coming from through the newly added
:term:`FILE_LAYERNAME` variable and the ``layer-<layername> override``. This is being used
for enabling QA checks on a per layer basis. For existing code this has the
side effect that the QA checks will apply to things being bbappended to recipes
from other layers. Those other layers would need to have patch upstream status
entries for patches being bbappended for example.

.. _migration-4.3-compiling-changes:

Compiling changes
~~~~~~~~~~~~~~~~~

-  Code on 32 bit platforms is now compiled with largefile support and 64
   bit ``time_t``, to avoid the Y2038 time overflow issue. This breaks the ABI
   and could break existing programs in untested layers.

.. _migration-4.3-supported-distributions:

Supported distributions
~~~~~~~~~~~~~~~~~~~~~~~

This release supports running BitBake on new GNU/Linux distributions:

-  Ubuntu 22.10
-  Fedora 38
-  Debian 12
-  CentOS Stream 8
-  AlmaLinux 8.8
-  AlmaLinux 9.2

On the other hand, some earlier distributions are no longer supported:

-  Fedora 36
-  AlmaLinux 8.7
-  AlmaLinux 9.1

See :ref:`all supported distributions <system-requirements-supported-distros>`.

.. _migration-4.3-removed-machines:

Removed machines
~~~~~~~~~~~~~~~~

The ``edgerouter`` BSP in ``meta-yocto-bsp`` has been removed.

.. _migration-4.3-go-changes:

Go language changes
~~~~~~~~~~~~~~~~~~~

-  Support for the Glide package manager has been removed, as ``go mod``
   has become the standard.

.. _migration-4.3-systemd-changes:

Systemd changes
~~~~~~~~~~~~~~~

Upstream systemd is now more strict on filesystem layout and the ``usrmerge``
feature is therefore required alongside systemd. The Poky test configurations
have been updated accordingly for systemd.

.. _migration-4.3-recipe-changes:

Recipe changes
~~~~~~~~~~~~~~

-  Runtime testing of ptest now fails if no test results are returned by
   any given ptest.

.. _migration-4.3-class-changes:

Class changes
~~~~~~~~~~~~~

-  The ``perl-version`` class no longer provides the ``PERLVERSION`` and ``PERLARCH`` variables
   as there were no users in any core layer. The functions for this functionality
   are still available.

.. _migration-4.3-deprecated-variables:

Deprecated variables
~~~~~~~~~~~~~~~~~~~~

The following variables have been deprecated:

-  :term:`CVE_CHECK_IGNORE`: use :term:`CVE_STATUS` instead.

.. _migration-4.3-removed-variables:

Removed variables
~~~~~~~~~~~~~~~~~

The following variables have been removed:

-  ``AUTHOR``
-  ``PERLARCH``
-  ``PERLVERSION``

.. _migration-4.3-removed-recipes:

Removed recipes
~~~~~~~~~~~~~~~

The following recipes have been removed in this release:

-  ``glide``, as explained in :ref:`migration-4.3-go-changes`.

.. _migration-4.3-removed-classes:

Removed classes
~~~~~~~~~~~~~~~

The following classes have been removed in this release:

.. _migration-4.3-qemu-changes:

QEMU changes
~~~~~~~~~~~~

-  The ``runqemu`` script no longer systematically adds two serial ports
   (``--serial null`` and ``-serial mon:stdio``) to the QEMU emulated machine
   if the user already adds such ports through the ``QB_OPT_APPEND`` setting.

   If the user adds one port, only ``--serial null`` is added, and
   ``-serial mon:stdio`` is no longer passed. If the user adds more than one
   port, ``--serial null`` is no longer added either. This can break some
   existing QEMU based configurations expecting such serial ports to be added
   when ``runqemu`` is executed.

   This change was made to avoid exceeding two serial ports, which interferes
   with automated testing.

.. _migration-4.3-qa-changes:

QA check changes
~~~~~~~~~~~~~~~~

-  The fetcher in ``lib/bb/tests/fetch.py`` now uses the ``https`` protocol
   instead of ``git``, whenever possible.

.. _migration-4.3-misc-changes:

Miscellaneous changes
~~~~~~~~~~~~~~~~~~~~~

-  `jsDelivr <https://www.jsdelivr.com/`>__ now offers a new Content Delivery
   Network (CDN) to Yocto Project users, which is completely free of charge
   for Open Source projects. In particular, it can be used to efficiently
   access prebuilt binary artifacts (see :term:`SSTATE_MIRRORS`) from many
   different locations in the world. This is available to all supported Poky
   releases.

-  The ``-crosssdk`` suffix and any :term:`MLPREFIX` were removed from
   ``virtual/XXX`` provider/dependencies where a ``PREFIX`` was used as well,
   as we don't need both and it made automated dependency rewriting
   unnecessarily complex. In general this only affects internal toolchain
   dependencies so isn't end user visible.

