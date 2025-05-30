.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

.. |yocto-codename| replace:: walnascar
.. |yocto-ver| replace:: 5.2
.. Note: anchors id below cannot contain substitutions so replace them with the
   value of |yocto-ver| above.

Release |yocto-ver| (|yocto-codename|)
======================================

Migration notes for |yocto-ver| (|yocto-codename|)
--------------------------------------------------

This section provides migration information for moving to the Yocto
Project |yocto-ver| Release (codename "|yocto-codename|") from the prior release.

``debug-tweaks`` removed from :term:`IMAGE_FEATURES`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``debug-tweaks`` image feature is now removed because it was too vague about
what it achieved: an image on which the ``root`` user can login without a
password.

To achieve the same result, the features previously added by ``debug-tweaks``
should be manually added to the :term:`IMAGE_FEATURES` variable. These are:

-  ``allow-empty-password``
-  ``allow-root-login``
-  ``empty-root-password``
-  ``post-install-logging``

Such a statement would be::

   IMAGE_FEATURES += "allow-empty-password allow-root-login empty-root-password post-install-logging"

See the list of available image features in the :ref:`ref-features-image`
section of the Yocto Project Reference Manual.

Supported kernel versions
~~~~~~~~~~~~~~~~~~~~~~~~~

The :term:`OLDEST_KERNEL` setting is 5.15 in this release, meaning that
out the box, older kernels are not supported. See :ref:`4.3 migration notes
<migration-4.3-supported-kernel-versions>` for details.

Supported distributions
~~~~~~~~~~~~~~~~~~~~~~~

Compared to the previous releases, running BitBake is supported on new
GNU/Linux distributions:

-  Fedora 41
-  CentOS Stream 9

On the other hand, some earlier distributions are no longer supported:

-  CentOS Stream 8
-  Fedora 38
-  OpenSUSE Leap 15.4
-  Ubuntu 20.04

See :ref:`all supported distributions <system-requirements-supported-distros>`.

Rust language changes
~~~~~~~~~~~~~~~~~~~~~

-  Recipes inheriting the :ref:`ref-classes-cargo` do not install libraries by
   default anymore. This behavior can be controlled by the
   :term:`CARGO_INSTALL_LIBRARIES` variable.

systemd changes
~~~~~~~~~~~~~~~

-  Support for ``split-usr`` and ``unmerged-usr`` are now removed after Systemd
   was updated to version 255. This option allowed installing Systemd in a
   system where directories such as ``/lib``, ``/sbin`` or ``/bin`` are *not*
   merged into ``/usr``.

   As a consequence, the ``systemd`` recipe no longer contains the ``usrmerge``
   :term:`PACKAGECONFIG` option as it is now implied by default.

-  ``systemd.bbclass``: If a ``systemd`` service file had referred to other service
   files by starting them via
   `Also <https://www.freedesktop.org/software/systemd/man/latest/systemd.unit.html#Also=>`__,
   the other service files were automatically added to the :term:`FILES` variable of
   the same package. Example:

   a.service contains::

      [Install]
      Also=b.service

   If ``a.service`` is packaged in package ``A``, ``b.service`` was
   automatically packaged into package ``A`` as well. This happened even if
   ``b.service`` was explicitly added to package ``B`` using :term:`FILES` and
   :term:`SYSTEMD_SERVICE` variables.
   This prevented such services from being packaged into different packages.
   Therefore, this automatic behavior has been removed for service files (but
   not for socket files).
   Now all service files must be explicitly added to :term:`FILES`.

-  Add ``create-log-dirs`` back to the configuration options. To enable
   persistent logging a user can now set the "Storage" option of
   ``journald.conf`` to "persistent". The ``/var/log/journal`` directory is now
   used for logging instead of ``/run/log``.

-  If ``pni-names`` is not in the :term:`DISTRO_FEATURES`, the `Predictable
   Network Interface names <https://www.freedesktop.org/wiki/Software/systemd/PredictableNetworkInterfaceNames/>`__
   systemd feature will now be disabled. Previously the feature was still
   enabled even if ``pni-names`` was not part of :term:`DISTRO_FEATURES`. Make
   sure to add the feature to :term:`DISTRO_FEATURES` if you want to keep this
   systemd behavior.

Multiconfig changes
~~~~~~~~~~~~~~~~~~~

The value of :term:`BB_CURRENT_MC` was changed from ``default`` to an empty string
for the default multiconfig configuration to avoid needing to map the values
within BitBake. This was already not happening in some cases so this fixes
some obscure bugs.

Any logic based on :term:`BB_CURRENT_MC` equalling to ``default`` by default should
be changed to be equal to an empty string.

Virtual toolchain provider changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Support was added for virtual providers on a per-recipe basis for specific
key toolchain providers listed in ``BB_VIRTUAL_RECIPE_PROVIDERS``. As part of
that support, the ``cross`` providers were simplified to remove the triplet
prefix (:term:`TARGET_PREFIX`, :term:`SDK_PREFIX` and :term:`HOST_PREFIX`) and
generalise the naming. Here are examples of how references to these variables
can be changed to use the new ``cross`` syntax::

   virtual/${HOST_PREFIX}binutils -> virtual/cross-binutils
   virtual/${TARGET_PREFIX}binutils -> virtual/cross-binutils

   virtual/${HOST_PREFIX}gcc -> virtual/cross-cc
   virtual/${TARGET_PREFIX}gcc -> virtual/cross-cc
   virtual/${SDK_PREFIX}gcc -> virtual/nativesdk-cross-cc

   virtual/${HOST_PREFIX}compilerlibs -> virtual/compilerlibs
   virtual/${TARGET_PREFIX}compilerlibs -> virtual/compilerlibs
   virtual/nativesdk-${SDK_PREFIX}compilerlibs -> virtual/nativesdk-compilerlibs

   virtual/${TARGET_PREFIX}g++ -> virtual/cross-c++

A :term:`PREFERRED_PROVIDER` assignment can be transformed as follows::

   PREFERRED_PROVIDER_virtual/${TARGET_PREFIX}binutils -> PREFERRED_PROVIDER_virtual/cross-binutils
   PREFERRED_PROVIDER_virtual/${SDK_PREFIX}binutils -> PREFERRED_PROVIDER_virtual/cross-binutils:class-nativesdk
   PREFERRED_PROVIDER_virtual/${SDK_PREFIX}g++ -> PREFERRED_PROVIDER_virtual/nativesdk-cross-c++

The above examples should cover most cases, but there might be situations where
replacing is not as straightforward. For more examples, see the commit
:oe_git:`"classes/recipes: Switch virtual/XXX-gcc to virtual/cross-cc (and
c++/binutils)" </openembedded-core/commit/?id=4ccc3bc8266c>` in
:term:`OpenEmbedded-Core (OE-Core)`.

:ref:`ref-classes-autotools` changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Changes to how ``aclocal`` is invoked means that ``ACLOCALDIR`` and
   ``ACLOCALEXTRAPATH`` are no longer used.

-  Directories containing m4 files are no longer found automatically and
   passed to ``autoreconf``. If a recipe fails to configure because it cannot
   find m4 macros, then usually the solution is to set ``EXTRA_AUTORECONF += "-I
   path/to/m4"`` in the recipe.

-  The :ref:`ref-classes-autotools` class now requires any recipe that inherits
   the class to have a ``configure`` script. The configuration script location
   is stored in the :term:`CONFIGURE_SCRIPT` variable. The
   :ref:`ref-tasks-configure` task will fail if the script is missing.

:term:`UBOOT_ENTRYPOINT` changes
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The :term:`UBOOT_ENTRYPOINT` variable should now be defined with a leading
``0x`` to its value. For example, consider the following assignment::

   UBOOT_ENTRYPOINT ?= "20008000"

This should now be replaced by::

   UBOOT_ENTRYPOINT ?= "0x20008000"


Git fetcher: support for multiple revisions per URL removed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The support for having multiple Git revisions per URL in :term:`SRC_URI` was
removed from BitBake, which means the following syntax is not supported
anymore::

   SRC_URI = "git://some.host/somepath;bareclone=1;branch=branchX,branchY;name=nameX,nameY"
   SRCREV_nameX = "xxxxxxxxxxxxxxxxxxxx"
   SRCREV_nameY = "yyyyyyyyyyyyyyyyyyyy"

This was rarely used in the core repositories because it would only ever make
sense for bare clones (the ``bareclone=1`` :term:`SRC_URI` option) where recipes
take care of the Git checkout. This removal simplifies the code logic in several
places.

If one of your recipes is using this mechanism, you can split the code source
fetching into two separate entries::

   SRC_URI = "git://some.host/somepath;bareclone=1;branch=branchX;name=nameX \
              git://some.host/somepath;bareclone=1;branch=branchY;name=nameY"
   SRCREV_nameX = "xxxxxxxxxxxxxxxxxxxx"
   SRCREV_nameY = "yyyyyyyyyyyyyyyyyyyy"

Git fetcher: Branch parameter now required in :term:`SRC_URI`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``branch`` parameter is now required when specifying a Git repository in
:term:`SRC_URI`, for example::

   SRC_URI = "git://some.host/somepath;branch=branchX"

A missing ``branch`` parameter used to produce a warning, and will now produce
an error.

Recipe changes
~~~~~~~~~~~~~~

-  The ``libnss-mdns`` recipe is now renamed to ``avahi-libnss-mdns`` to avoid a
   conflict with meta-networking.

-  :ref:`ref-classes-ptest` support for the ``valgrind`` recipe was removed, due
   to regressions occurring after updating Glibc to 2.41.

Removed variables
~~~~~~~~~~~~~~~~~

The following variables have been removed:

-  ``PACKAGE_SNAP_LIB_SYMLINKS``: related to an unmaintained and obsolete
   "micro" :term:`distro <DISTRO>`.

-  ``SETUPTOOLS_INSTALL_ARGS``: obsolete and unused variable.

-  ``BB_DANGLINGAPPENDS_WARNONLY``: support for only warning the user when a
   ``.bbappend`` file doesn't apply to the original recipe has been dropped. See
   the :ref:`dev-manual/layers:Appending Other Layers Metadata With Your Layer`
   section of the Yocto Project Development Tasks Manual for alternatives to
   this variable.

Removed recipes
~~~~~~~~~~~~~~~

The following recipes have been removed in this release:

-  ``liburi-perl``: moved to :oe_git:`meta-perl </meta-openembedded/tree/meta-perl>`.

-  ``python3-isodate``: moved to :oe_git:`meta-python </meta-openembedded/tree/meta-python>`.

-  ``python3-iniparse``: removed as there are no consumers of this recipe in
   :oe_git:`openembedded-core </openembedded-core>` or :oe_git:`meta-openembedded </meta-openembedded>`.

-  ``blktool``: It was created in 2004 as an alternative to hdparm and never
   updated since (while :wikipedia:`hdparm <Hdparm>` remains active).

-  ``cargo-c-native``: converted to a target recipe and renamed to ``cargo-c``.

-  ``libnss-mdns``: renamed to ``avahi-libnss-mdns``

Removed classes
~~~~~~~~~~~~~~~

The following classes have been removed in this release:

-  ``migrate_localcount.bbclass``: obsolete class for which code was already
   removed in 2012.

Removed features
~~~~~~~~~~~~~~~~

-  The ``ld-is-gold`` distro feature was removed from the
   :term:`DISTRO_FEATURES`.

Miscellaneous changes
~~~~~~~~~~~~~~~~~~~~~

-  :term:`ZSTD_COMPRESSION_LEVEL` is now a plain integer number instead of a dash-prefixed
   command-line option (e.g. it should be set to ``3`` rather than ``-3``).

-  Until now, the variable :term:`UBOOT_ENV` was processed both by the U-Boot
   recipe and by the ``kernel-fitimage.bbclass``. However, adding a U-Boot
   script to the kernel FIT image is a different and independent thing, which
   also requires an independent variable.
   Therefore, the :term:`UBOOT_ENV` is no longer handled by the
   ``kernel-fitimage.bbclass``. There is a new variable :term:`FIT_UBOOT_ENV`
   which should be used for adding a U-Boot script to a FIT image.

-  The ``devtool ide-sdk`` utility has been removed from the :doc:`eSDK
   </sdk-manual/extensible>` (but remains available in the BitBake environment).
