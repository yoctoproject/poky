.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Release notes for 4.2 (mickledore)
----------------------------------

New Features / Enhancements in 4.2
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Python 3.8 is the minimum Python version required on the build host.
   For host distributions that do not provide it, this is included as part of the
   :term:`buildtools` tarball.

-  BitBake in this release now supports a new ``addpylib`` directive to enable
   Python libraries within layers.

   This directive should be added to your layer configuration
   as in the below example from ``meta/conf/layer.conf``::

      addpylib ${LAYERDIR}/lib oe

-  BitBake has seen multiple internal changes that may impact
   memory and disk usage as well as parsing time, in particular:

   -  BitBake's Cooker server is now multithreaded.

   -  BitBake's cache has been extended to include more hash
      debugging data, but has also been optimized to :yocto_git:`compress
      cache data <https://git.yoctoproject.org/poky/commit/?h=mickledore&id=7d010055e2af3294e17db862f42664ca689a9356>`.

   -  BitBake's Cooker server :yocto_git:`can now be pinged
      </poky/commit/?h=mickledore&id=26f255da09>`
      from the UI.

-  Architecture-specific enhancements:

   -  This release adds initial support for the
      :wikipedia:`LoongArch <Loongson#LoongArch>`
      (``loongarch64``) architecture, though there is no testing for it yet.

-  Kernel-related enhancements:

-  QEMU/runqemu enhancements:

-  Image-related enhancements:

-  New variables:

   - :term:`VOLATILE_TMP_DIR` allows to specify
     whether ``/tmp`` should be on persistent storage
     or in RAM.

-  Rust improvements:

   -  This release adds Cargo support on the target, and includes
      automated QA tests for this functionality.

   -  It also supports checksums for Rust crates and makes
      them mandatory for each crate in a recipe.

-  Testing:

   -  The ptest images have changed structure in this release. The
      underlying ``core-image-ptest`` recipe now uses :term:`BBCLASSEXTEND` to
      create a variant for each ptest enabled recipe in OE-Core. 

      For example, this means that ``core-image-ptest-bzip2``,
      ``core-image-ptest-lttng-tools`` and many more image targets now exist
      and can be built/tested individually. 

      The ``core-image-ptest-all`` and ``core-image-ptest-fast`` targets are now
      wrappers that target groups of individual images and means that the tests
      can be executed in parallel during our automated testing. This also means
      the dependencies are more accurately tested.

   -  It is now possible to track regression changes between releases using
      :oe_git:`yocto_testresults_query.py </openembedded-core/tree/scripts/yocto_testresults_query.py>`,
      which is a thin wrapper over :oe_git:`resulttool
      </openembedded-core/tree/scripts/resulttool>`. Here is an example
      command, which allowed to spot and fix a regression in the
      ``quilt`` ptest::

         yocto_testresults_query.py regression-report 4.2_M1 4.2_M2

      See this `blog post about regression detection
      <https://bootlin.com/blog/continuous-integration-in-yocto-improving-the-regressions-detection/>`__.

   -  This release adds support for parallel ptest execution with a ptest per image.
      This takes ptest execution time from 3.5 hours to around 45 minutes on the autobuilder.

-  Miscellaneous changes:

   -  Supporting 64 bit dates on 32 bit platforms: several packages have been
      updated to pass Y2038 tests.

   -  Many packages were updated to add large file support.
