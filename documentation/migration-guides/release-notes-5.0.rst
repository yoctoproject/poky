.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Release notes for 5.0 (scarthgap)
---------------------------------

New Features / Enhancements in 5.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Linux kernel 6.6, gcc 13.2, glibc 2.39, LLVM 18.1, and over XXX other recipe upgrades

-  New variables:

   -  :term:`CVE_DB_INCR_UPDATE_AGE_THRES`: Configure the maximum age of the
      internal CVE database for incremental update (instead of a full
      redownload).

-  Architecture-specific enhancements:

-  Kernel-related enhancements:

-  New core recipes:

-  QEMU / ``runqemu`` enhancements:

   -  QEMU has been upgraded to version 8.2.1

-  Rust improvements:

   -  Rust has been upgraded to version 1.75

-  wic Image Creator enhancements:

   -  Allow the imager's output file extension to match the imager's name,
      instead of hardcoding it to ``direct`` (i.e., the default imager)

   -  For GPT-based disks, add reproducible Disk GUID generation

   -  Allow generating reproducible ext4 images

   -  Add feature to fill a specific range of a partition with zeros

   -  ``bootimg-efi``: add ``install-kernel-into-boot-dir`` parameter to
      configure kernel installation point(s) (i.e., rootfs and/or boot partition)

   -  ``rawcopy``: add support for zstd decompression

-  SDK-related improvements:

-  Testing:

   -  Add an optional ``unimplemented-ptest`` QA warning to detect upstream
      packages with tests, that do not use ptest.

-  Utility script changes:

   -  New ``recipetool/create_go.py`` script added to support Go recipe creation

-  BitBake improvements:

-  Packaging changes:

-  Security improvements:

   -  Improve incremental CVE database download from NVD. Rejected CVEs are
      removed, configuration is kept up-to-date. The age threshold for
      incremental update can be configured with :term:`CVE_DB_INCR_UPDATE_AGE_THRES`
      variable.

-  Prominent documentation updates:

-  Miscellaneous changes:

   -  Systemd's following :term:`PACKAGECONFIG` options were added:
      ``cryptsetup-plugins``, ``no-ntp-fallback``, and ``p11kit``.

   -  ``systemd-boot`` can, from now on, be compiled as ``native``, thus
      providing ``ukify`` tool to build UKI images.

   -  systemd: split bash completion for ``udevadm`` in a new
      ``udev-bash-completion`` package.

   -  The :ref:`ref-classes-go-vendor` class was added to support offline builds
      (i.e., vendoring). It can also handle modules from the same repository,
      taking into account their versions.

   -  Disable strace support of bluetooth by default.

Known Issues in 5.0
~~~~~~~~~~~~~~~~~~~

-  N/A

Recipe License changes in 5.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following corrections have been made to the :term:`LICENSE` values set by recipes:

-  ``systemd``: make the scope of ``LGPL`` more accurate (``LGPL-2.1`` -> ``LGPL-2.1-or-later``)
-  ``libsystemd``: set its own :term:`LICENSE` value (``LGPL-2.1-or-later``) to add more granularity

Security Fixes in 5.0
~~~~~~~~~~~~~~~~~~~~~

Recipe Upgrades in 5.0
~~~~~~~~~~~~~~~~~~~~~~

-  go: update 1.20.10 -> 1.22.1

Contributors to 5.0
~~~~~~~~~~~~~~~~~~~

Thanks to the following people who contributed to this release:

Repositories / Downloads for Yocto-5.0
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

