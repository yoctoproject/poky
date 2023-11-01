.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Release notes for 4.3 (nandbield)
----------------------------------

New Features / Enhancements in 4.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Linux kernel 6.5 and 6.1, gcc 13, glibc 2.38, LLVM 17, and other recipe upgrades

-  The autobuilder's shared-state artefacts are now available over the `jsDeliver
   <https://jsdelivr.com>`__ Content Delivery Network (CDN).
   See :term:`SSTATE_MIRRORS`.

-  New variables:

   -  :term:`CVE_CHECK_STATUSMAP`, :term:`CVE_STATUS`, :term:`CVE_STATUS_GROUPS`,
      replaceing the deprecated :term:`CVE_CHECK_IGNORE`.

   -  :term:`FILE_LAYERNAME`: bitbake now sets this to the name of the layer
      containing the recipe

   -  :term:`FIT_ADDRESS_CELLS` and :term:`UBOOT_FIT_ADDRESS_CELLS`.
      See details below.

   -  :term:`KERNEL_DTBDEST`: directory where to install DTB files.

   -  :term:`KERNEL_DTBVENDORED`: whether to keep vendor subdirectories.

   -  :term:`KERNEL_LOCALVERSION`: to add a string to the kernel version
      information.

   -  :term:`KERNEL_STRIP`: to specify the command to strip the kernel binary.

   -  :term:`LICENSE_FLAGS_DETAILS`: add extra details about a recipe license
      in case it is not allowed by :term:`LICENSE_FLAGS_ACCEPTED`.

   -  :term:`MESON_TARGET`: to compile a specific Meson target instead of the
      default ones.

   -  :term:`OEQA_REPRODUCIBLE_TEST_PACKAGE`: to restrict package managers used
      in reproducibility testing.

-  Layername functionality available through overrides

   Code can now know which layer a recipe is coming from through the newly added :term:`FILE_LAYERNAME`
   variable. This has been added as an override of the form ``layer-<layername>``. In particular,
   this means QA checks can now be layer specific, for example::

      ERROR_QA:layer-core:append = " patch-status"

   This will enable the ``patch-status`` QA check for the core layer.

-  Architecture-specific enhancements:

   -  RISCV support is now enabled in LLVM 17.

   -  Loongarch support in the :ref:`ref-classes-linuxloader` class and
      ``core-image-minimal-initramfs`` image.

   -  The ``arch-armv8`` and ``arch-armv9`` architectures are now given
      `Scalable Vector Extension (SVE)
      <https://developer.arm.com/documentation/100891/0612/sve-overview/introducing-sve>`__
      based tune options. Commits:
      :yocto_git:`1 </poky/commit/?id=e4be03be5be62e367a40437a389121ef97d6cff3>`,
      :yocto_git:`2 </poky/commit/?id=8cd5d264af4c346730531cb98ae945ab862dbd69>`.

-  Kernel-related enhancements:

   - The default kernel is the current stable (6.5), and there is also support
     for the latest long-term release (6.1).

   - The list of fixed kernel CVEs is updated regularly using data from
     `linuxkernelcves.com <https://linuxkernelcves.com>`__.

   - A ``showconfig`` task was added to the :ref:`ref-classes-cml1` class, to
     easily examine the final generated ``.config`` file.

-  New core recipes:

   -  ``musl-legacy-error``: glibc ``error()`` API implementation still needed
      by a few packages.

   -  `python3-beartype <https://beartype.readthedocs.io>`, unbearably fast
      runtime type checking in pure Python.

   -  `python3-spdx-tools <https://github.com/spdx/tools-python>`__,
      tools for SPDX validation and conversion.

   -  `python3-uritools <https://github.com/tkem/uritools/>`__, replacement for
      the ``urllib.parse`` module.

   -  `ttyrun <https://github.com/ibm-s390-linux/s390-tools>`__, starts
      ``getty`` programs only when a terminal exists, preventing respawns
      through the ``init`` program. This allowed to remove the
      ``SERIAL_CONSOLES_CHECK`` variable.

-  New classes:

   -  A ``ptest-cargo`` class was added to allow Cargo based recipes to easily add ptests

   -  A :ref:`ref-classes-cargo_c` class was added to allow recipes to make Rust code
      available to C and C++ programs.

-  QEMU / ``runqemu`` enhancements:

   -  QEMU has been upgraded to version 8.1

   -  Many updates to the ``runqemu`` command.

   -  The ``qemu-system-native`` recipe is now built with PNG support, which could be
      useful to grab screeshots for error reporting purposes.

-  Rust improvements:

   -  Rust has been upgraded to version 1.70

-  Image-related enhancements:

-  Distribution-related enhancements:

   -  The ``poky-altcfg`` distribution enables the ``usrmerge``
      :ref:`distro feature <ref-manual/features:Distro Features>`.

-  wic Image Creator enhancements:

-  FIT image related improvements:

   -  New :term:`FIT_ADDRESS_CELLS` and :term:`UBOOT_FIT_ADDRESS_CELLS` variables allowing
      to specify 64 bit addresses, typically for loading U-Boot.

-  SDK-related improvements:

-  Testing:

   -  The :ref:`ref-classes-insane` class now adds an :ref:`unimplemented-ptest
      <qa-check-unimplemented-ptest>` infrastructure to detect package sources
      with unit tests but no implemented ptests in the recipe.

-  Utility script changes:

   -  New ``scripts/patchtest`` utility to check patches to the
      OpenEmbedded-Core project. See
      :ref:`contributor-guide/submit-changes:validating patches with patchtest`
      for details.

-  BitBake improvements:

   -  The BitBake Cooker log now contains notes when the caches are
      invalidated which is useful for memory resident bitbake debugging.

-  Packaging changes:

-  :term:`SPDX` improvements:

   -  :term:`SPDX` manifests are now generated by default.

-  Security improvements:

   -  Most repositories now include a :yocto_git:`SECURITY.md
      </poky/tree/SECURITY.md>` file with hints for security researchers
      and other parties who might report potential security vulnerabilities.

-  Prominent documentation updates:

   -  New :doc:`../contributor-guide/index` document.

   -  New :doc:`../dev-manual/security-subjects` chapter in the Development
      Tasks Manual.

   -  Long due documentation for the :ref:`ref-classes-devicetree` class.

   -  New :ref:`summary about available init systems
      <dev-manual/init-manager:summary>`.

   -  New documentation for the :ref:`ref-classes-uboot-sign` class and
      its variables and for the :ref:`ref-classes-kernel-devicetree` class
      variables.

-  Miscellaneous changes:

   -  Git based recipes in OE-Core which used the git protocol have been
      changed to use https where possibile. https is now believed to be
      faster and more reliable.

   -  The ``os-release`` recipe added a ``CPE_NAME`` to the fields provided, with the
      default being populated from :term:`DISTRO`.

   -  The ``psplash`` recipe now accepts a PNG format image through :term:`SPLASH_IMAGES`,
      instead of a harder to generate and modify ``.h`` file.

Known Issues in 4.3
~~~~~~~~~~~~~~~~~~~

Recipe License changes in 4.3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following corrections have been made to the :term:`LICENSE` values set by recipes:

Security Fixes in 4.3
~~~~~~~~~~~~~~~~~~~~~

Recipe Upgrades in 4.3
~~~~~~~~~~~~~~~~~~~~~~

Contributors to 4.3
~~~~~~~~~~~~~~~~~~~
