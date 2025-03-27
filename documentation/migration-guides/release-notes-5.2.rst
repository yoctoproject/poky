.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

.. |yocto-codename| replace:: walnascar
.. |yocto-ver| replace:: 5.2

Release notes for |yocto-ver| (|yocto-codename|)
------------------------------------------------

New Features / Enhancements in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Linux kernel 6.12, gcc 14.2, glibc 2.41, LLVM 19.1.7, and over 300 other
   recipe upgrades.

-  Minimum Python version required on the host: 3.9.

-  New variables:

   -  ``linux-firmware``: Add the :term:`FIRMWARE_COMPRESSION` variable which
      allows compression the firmwares provided by the ``linux-firmware`` recipe.
      Possible values are ``xz`` and ``zst``.

   -  Reproducibility: Add the :term:`OEQA_REPRODUCIBLE_TEST_LEAF_TARGETS`
      variable which enables a reproducibility test on recipes using
      :ref:`Shared State <overview-manual/concepts:Shared State>` for the
      dependencies. See :doc:`/test-manual/reproducible-builds`.

   -  ``systemd``: Add term:`WATCHDOG_RUNTIME_SEC`: for controlling the
      ``RuntimeWatchdogSec`` option in ``/etc/systemd/system.conf``.

   -  :term:`FIT_UBOOT_ENV` to allow including a u-boot script as a text in a
      fit image. See the :ref:`ref-classes-kernel-fitimage` for more information.

   -  :ref:`ref-classes-meson`: :term:`MESON_INSTALL_TAGS` to allow passing
      install tags (``--tags``) to the ``meson install`` command during the
      :ref:`ref-tasks-install` task.

   -  :ref:`ref-classes-cve-check`: :term:`NVD_DB_VERSION` to allow choosing the
      CVE feed when using the :ref:`ref-classes-cve-check` class.

   -  The :term:`BB_USE_HOME_NPMRC` controls whether or not BitBake uses the
      user's ``.npmrc`` file within their home directory within the npm fetcher.
      This can be used for authentication of private NPM registries, among other
      uses.

-  Kernel-related changes:

   -  :ref:`ref-classes-cml1`: in :ref:`ref-tasks-diffconfig`, do not override
      ``.config`` with ``.config.orig``. This applies to other recipes using the
      class :ref:`ref-classes-cml1`.

   -  ``linux-firmware``: add following new firmware packages:

       -  ``qcom-qcm6490-audio``
       -  ``qcom-qcm6490-compute``
       -  ``qcom-adreno-a663``
       -  ``qcom-qcm6490-adreno``
       -  ``qcom-sa8775p-adreno``
       -  ``qcom-qcm6490-ipa``
       -  ``qcom-x1e80100-audio``
       -  ``qcom-qcs615-adreno``
       -  ``qcom-aic100``
       -  ``qcom-qdu100``
       -  ``qca-qca2066``
       -  ``qca-qca61x4-serial``
       -  ``qca-qca61x4-usb``
       -  ``qca-qca6390``
       -  ``qca-qca6698``
       -  ``qca-wcn3950``
       -  ``qca-wcn3988``
       -  ``qca-wcn399x``
       -  ``qca-wcn6750``
       -  ``qca-wcn7850``
       -  ``qcom-2-license``
       -  ``qcom-aic100``
       -  ``qcom-qcm6490-wifi``
       -  ``qcom-qdu100``
       -  ``qcom-sa8775p-audio``
       -  ``qcom-sa8775p-compute``
       -  ``qcom-sa8775p-generalpurpose``
       -  ``qcom-x1e80100-lenovo-t14s-g6-adreno``
       -  ``qcom-x1e80100-lenovo-t14s-g6-audio``
       -  ``qcom-x1e80100-lenovo-t14s-g6-compute``

   -  ``linux-firmware``: split ``amgpu``, ``ath10k``, ``ath11k`` and ``ath12k``
      in separate packages.

   -  The :ref:`ref-classes-kernel-yocto` classes now supports in-tree
      configuration fragments. These can be added with the
      :term:`KERNEL_FEATURES` variable.

   -  Kernel configuration audit can now be disabled by setting
      :term:`KMETA_AUDIT` to 1.

   -  The ``kern-tools`` recipe is now able to recognize files ending with
      ``.config`` for :ref:`ref-classes-kernel-yocto`-based Kernel recipes.

   -  Support the LZMA compression algorithm in the
      :ref:`ref-classes-kernel-uboot` class. This can be done by setting the
      variable :term:`FIT_KERNEL_COMP_ALG` to ``lzma``.

   -  :ref:`ref-classes-kernel-yocto`: Reproducibility for commits created by
      the :ref:`ref-classes-kernel-yocto` class was improved.

   -  ``kernel-arch``: add ``-fmacro-prefix-map`` in ``KERNEL_CC`` to fix a
      reproducibility issue.

-  New core recipes:

   -  ``python3-pefile``: required for the :ref:`ref-classes-uki` class.

   -  Add initial support for the `Barebox <https://www.barebox.org>`__
      bootloader, along with associated OEQA test cases. This adds the
      ``barebox`` and the ``barebox-tools`` recipes.

   -  Import ``makedumpfile`` from meta-openembedded, as the ``kexec-tools``
      recipe :term:`RDEPENDS` on it.

   -  The ``tcl-8`` recipe was added back to support the build of ``expect``.

   -  Add the ``libdisplay-info`` recipe, an EDID and DisplayID library,
      required for Weston 14.0.1 and newer.

   -  The ``hwdata`` recipe was imported from :oe_git:`meta-openembedded
      </meta-openembedded>`, a recipe for hardware identification and
      configuration data, needed by ``libdisplay-info``.

   -  The ``cve-update-db-native`` was restored from kirkstone and can be used
      to update the CVE National Vulnerability Database (NVD). Add support for
      the FKIE-CAD (https://github.com/fkie-cad/nvd-json-data-feeds) CVE source
      for it.

   -  The ``rpm-sequoia-crypto-policy`` to ship a crypto policy file for the
      ``rpm-sequoia`` recipe.

   -  The ``libsass`` and ``sassc`` for the C/C++ port of the Sass CSS
      pre-compiler, required by the ``libadwaita`` recipe.

   -  ``python3-roman-numerals-py``: module providing utilities for working with
      well-formed Roman numerals. ``python3-sphinx`` relies on this recipe.

   -  The ``fastfloat`` recipe, a header-only library for fast number parsing.
      This will be a dependency for the ``vte`` recipe in later versions.

   -  The ``avahi-libnss-mdns`` was renamed from ``libnss-mdns``.

   -  The ``cargo-c`` was renamed from ``cargo-c-native``.

   -  The ``tcl8`` recipe was added to support the failing build of ``expect``.
      The ``tcl`` recipe (version 9) remains the main recipe for this component.

   -  The ``scdoc`` recipe is imported from
      :oe_layerindex:`/layerindex/branch/master/layer/meta-wayland` to support
      the generation of the man-pages of ``kdoc``.

-  New core classes:

   -  New :ref:`ref-classes-uki` class for building Unified Kernel Images (UKI).
      Associated OEQA tests were also added for this class.

   -  New :ref:`ref-classes-cython` class for python recipes that require Cython
      for their compilation. Existing recipes depending on Cython now inherit
      this class. This class also strips potential build paths in the compilation
      output for reproducibility.

   -  New :ref:`ref-classes-ptest-python-pytest` class to automatically
      configure :ref:`ref-classes-ptest` for Python packages using the `pytest
      <https://docs.pytest.org>`__ unit test framework.

-  Architecture-specific changes:

   -  ``tune-cortexa32``: set tune feature to ``armv8a``.

   -  Add the ``loongarch64`` architecture for the ``grub2`` and ``llvm``
      recipes. It was also added to build with ``musl`` as the toolchain.

-  QEMU / ``runqemu`` changes:

   -  ``qemu/machine``: change the  ``QEMU_EXTRAOPTIONS_${TUNE_PKGARCH}`` syntax
      in QEMU machine definitions to ``QEMU_EXTRAOPTIONS:tune-${TUNE_PKGARCH}``
      to follow the same patterns as other QEMU-related variables.

-  Documentation changes:

   -  Use ``rsvg`` as a replacement of ``inkscape`` to convert svg files in the
      documentation.

   -  The ``cve`` role was replaced by ``cve_nist`` to avoid a conflict with
      more recent version of Sphinx.

   -  New documentation on the multiconfig feature: :doc:`/dev-manual/multiconfig`.

   -  New documentation on ``bblock``: :doc:`/dev-manual/bblock`.

-  Go changes:

   -  The :ref:`ref-classes-go-mod` class now sets an internal variable
      ``GO_MOD_CACHE_DIR`` to enable the use of the Go module fetchers for
      downloading and unpacking module dependencies to the module cache.

   -  Make the :ref:`ref-tasks-compile` task run before
      :ref:`ref-tasks-populate_lic` in the :ref:`ref-classes-go-mod` class so
      license files are found by :ref:`ref-tasks-populate_lic` after the ``go
      install`` command is run in :ref:`ref-tasks-compile`.

-  Rust changes:

   -  ``rust-target-config``: Update the data layout for the *x86-64* target, as
      it was different in Rust from LLVM, which produced a data layout error.

-  Wic Image Creator changes:

   -  Allow the ``--exclude-path`` option to exclude symlinks.

   -  Add the variable :term:`WIC_SECTOR_SIZE` to control the sector size of Wic
      images.

   -  ``bootimg-efi``: Support "+" symbol in filenames passed in
      :term:`IMAGE_EFI_BOOT_FILES`.

-  SDK-related changes:

   -  Add support for ZST-compression through :term:`SDK_ARCHIVE_TYPE`, by
      setting its value to ``tar.zst``.

   -  The ``debug-tweaks`` features were removed from ``-sdk`` images
      (``core-image-*-sdk.bb``).

   -  Enable ``ipv6``, ``acl``, and ``xattr`` in :term:`DISTRO_FEATURES_NATIVESDK`.

   -  Toolchain SDKs (``meta-toolchain``) now properly supports the ``usrmerge``
      feature (part of :term:`DISTRO_FEATURES`).

   -  The ``pipefail`` shell option is now added to the SDK installer script.

-  Testing-related changes:

   -  ``oeqa/postactions``: Fix archive retrieval from target.

   -  ``oeqa/selftest/gcc``: Fix kex exchange identification error.

   -  ``oeqa/utils/qemurunner``: support ignoring vt100 escape sequences.

   -  ``oeqa``: support passing custom boot patterns to runqemu.

   -  ``oeqa/selftest/cases``: add basic U-boot and Barebox tests.

   -  ``oeqa/selftest/rust``: skip on all MIPS platforms.

   -  Lots of changes and improvements to the :term:`Toaster` OEQA tests.

   -  ``oeqa/selftest``: add a test for bitbake "-e" and "-getvar" difference.

   -  ``oeqa/selftest``: Fix failure when configuration contains ``BBLAYERS:append``

   -  ``oeqa/ssh``: improve performance and log sizes when handling large files.

   -  ``oeqa/poisoning``: fix and improve gcc include poisoning tests.

-  Utility script changes:

   -  The ``patchreview.py`` script now uses the ``check_upstream_status`` from
      ``oe.qa`` to get patch statuses.

   -  ``resulttool``:

      -  Allow store to filter to specific revisions (``--revision`` flag).

      -  Use single space indentation in JSON output, to save disk
         space.

      -  Add ``--logfile-archive`` option to store and archive log files
         separately.

      -  Handle LTP raw logs as well as Ptest.

   -  ``yocto-check-layer``:

      -  Check for the presence of a ``SECURITY.md`` file in layers and make it
         mandatory.

      -  The :ref:`ref-classes-yocto-check-layer` class now uses
         :term:`CHECKLAYER_REQUIRED_TESTS` to get the list of QA checks to verify
         when running the ``yocto-check-layer`` script.

   -  New ``oe-image-files-spdx`` script utility directory under
      ``scripts/contrib`` to that processes the SPDX 3.0.1 output from a build
      and lists all the files on the root file system with their checksums.

   -  ``install-buildtools``:

      -  Add the ``--downloads-directory`` argument to the script to allow
         specifying the location of the artifact download directory.

      -  The download URL are now stored next to the download artifacts for
         traceability.

   -  New ``clean-hashserver-database`` under ``scripts/`` that can be used to
      clean the hashserver database based on the files available in the sstate
      directory (see :ref:`overview-manual/concepts:Hash Equivalence` for more
      information).

-  BitBake changes:

   -  Add a new ``include_all`` directive, which can be used to include multiple
      files present in the same location in different layers.

   -  Fetcher related changes (``fetch2``):

      -  Do not preserve ownership when unpacking.

      -  switch from Sqlite ``persist_data`` to a standard cache file
         for checksums, and drop ``persist_data``.

      -  add support for GitHub codespaces by adding the
         ``GITHUB_TOKEN`` to the list of variables exported during ``git``
         invocations.

      -  set User-Agent to 'bitbake/version' instead of a "fake
         mozilla" user agent.

      -  ``wget``: handle HTTP 308 Permanent Redirect.

      -  ``wget``: increase timeout to 100s from 30s to match CDN worst
         response time.

      -  Add support for fast initial shallow fetch. The fetcher will prefer an
         initial shallow clone, but will re-utilize an existing bare clone if
         there is one. If the remote server does not allow shallow fetches, the
         fetcher falls back to a bare clone. This improves the data transfer
         size on the initial fetch of a repository, eliminates the need to use
         an HTTPS tarball :term:`SRC_URI` to reduce data transfer, and allows
         SSH-based authentication when using non-public repos, so additional
         HTTPS tokens may not be required.

   -  ``compress``: use ``lz4`` instead of ``lz4c``, as ``lz4c`` as been
      considered deprecrated since 2018.

   -  ``server/process``: decrease idle/main loop frequency, as it is idle and
      main loops have socket select calls to know when to execute.

   -  ``bitbake-worker``:

      -  improve bytearray truncation performance when large
         amounts of data are being transferred from the cooker to the worker.

      -  ``cooker``: increase the default pipe size from 64KB to
         512KB for better efficiency when transferring large amounts of data.

   -  ``bitbake-getvar``: catch ``NoProvider`` exception to improve error
      readability when a recipe is not found with ``--recipe``.

   -  ``bb/build``: add a function ``bb.build.listtasks()`` to list the tasks in
      a datastore.

   -  Remove custom exception backtrace formatting, and replace occurences of
      ``bb.exception.format_exception()`` by ``traceback.format_exception()``.

   -  ``runqueue``: various performance optimizations including:

      -  Fix performance of multiconfigs with large overlap.
      -  Optimise ``setscene`` loop processing by starting where it
         was left off in the previous execution.

   -  ``knotty`` now hints the user if :term:`MACHINE` was not set in
      the ``local.conf`` file.

   -  ``utils``: add Go mod h1 checksum support, specific to Go modules. Use
      with ``goh1``.

   -  The parser now catches empty variable name assignments such as::

         += "value"

      The previous code would have assigned ``value`` to the variable named ``+``.

   -  ``hashserv``: Add the ``gc-mark-stream`` command for batch hash marking.


-  Packaging changes:

   -  ``systemd``: extract dependencies from ``.note.dlopen`` ELF segments, to
      better detect dynamically linked libraries at runtime.

   -  ``package_rpm``: use ZSTD's default compression level from the variable
      :term:`ZSTD_COMPRESSION_LEVEL`.

   -  ``package_rpm``: restrict RPM packaging to 4 threads to improve
      the compression speed.

   -  ``sign_rpm``: ``rpm`` needs the ``sequoia`` :term:`PACKAGECONFIG`
      config set to be able to generate signed packages.

-  LLVM related changes:

   -  Set ``LLVM_HOST_TRIPLE`` for cross-compilation, which is recommended when
      cross-compiling Llvm.

-  SPDX-related changes:

   -  SPDX 3.0:

      -  Find local sources when searching for debug sources.

      -  Map ``gitsm`` URIs to ``git``.

      -  Link license and build by alias instead of SPDX ID.

   -  Fix SPDX tasks not running when code changes (use of ``file-checksums``).

-  ``devtool`` changes:

   -  Remove the "S = WORKDIR" workaround as now :term:`S` cannot be equal to
      :term:`WORKDIR`.

   -  The already broken ``--debug-build-config`` option of
      ``devtool ide-sdk`` has been replaced by a new ``--debug-build`` option
      of ``devtool modify``. The new ``devtool ide-sdk`` workflow is:
      ``devtool modify my-recipe --debug-build`` followed by
      ``devtool ide-sdk my-recipe my-image``.

   -  ``create-spdx``: support line numbers for :term:`NO_GENERIC_LICENSE`
      license types.

   -  ``spdx30``: Adds a "contains" relationship that relates the root file
      system package to the files contained in it. If a package provides a file
      with a matching hash and path, it will be linked, otherwise a new File
      element will be created.

-  Patchtest-related changes:

   -  Refactor pattern definitions in a ``patterns`` module.

   -  Refactor and improve the ``mbox`` module.

   -  Split out result messages.

   -  Add a check for user name tags in patches (for example "fix added by
      @username").

-  :ref:`ref-classes-insane` class related changes:

   -  Only parse ELF if they are files and not symlinks.

   -  Check for ``RUNPATH`` in addition to ``RPATH`` in binaries.

   -  Ensure :ref:`ref-classes-insane` tasks of dependencies run in builds when
      expected.

-  Security changes:

   -  The ``PIE`` gcc flag is now passed for the *powerpc* architecture after a
      bugfix in gcc (https://gcc.gnu.org/bugzilla/show_bug.cgi?id=81170).

   -  ``openssh``: be more restrictive on private key file permissions by
      setting them from the :ref:`ref-tasks-install` task.

-  :ref:`ref-classes-cve-check` changes:

   -  Update the :term:`DL_DIR` database location name
      (``${DL_DIR}/CVE_CHECK2``).

   -  Add the field "modified" to the JSON report (from "NVD-modified").

   -  Add support for CVSS v4.0.

   -  Fix malformed cve status description with ``:`` characters.

   -  Restore the :term:`CVE_CHECK_SHOW_WARNINGS` variable and functionality. It
      currently prints warning message for every unpatched CVE the
      :ref:`ref-classes-cve-check` class finds.

   -  Users can control the NVD database source using the :term:`NVD_DB_VERSION`
      variable with possible values ``NVD1``, ``NVD2``, or ``FKIE``.

   -  The default feed for CVEs is now ``FKIE`` instead of ``NVD2`` (see
      :term:`NVD_DB_VERSION` for more information).

-  New :term:`PACKAGECONFIG` options for individual recipes:

   -  ``perf``: ``zstd``
   -  ``ppp``: ``pam``, ``openssl``
   -  ``libpciaccess``: ``zlib``
   -  ``gdk-pixbuf``: ``gif``, ``others``
   -  ``libpam``: ``selinux``
   -  ``libsecret``: ``pam``
   -  ``rpm``: ``sequoia``
   -  ``systemd``: ``apparmor``, ``fido``, ``mountfsd``, ``nsresourced``
   -  ``ovmf``: ``debug``
   -  ``webkitgtk``: ``assertions``

-  Systemd related changes:

   -  ``systemd``:

      -  set better sane time at startup by creating the ``clock-epoch`` file in
         ``${libdir}`` if the ``set-time-epoch`` :term:`PACKAGECONFIG` config is
         set.

      -  really disable Predictable Network Interface names if the ``pni-names``
         feature is not part of :term:`DISTRO_FEATURES`. Previously it was only
         really disable for QEMU machines.

      -  split ``networkd`` into its own package named ``systemd-networkd``.

   -  ``systemd-bootchart``: now supports the 32-bit *riscv* architecture.

   -  ``systemd-boot``: now supports the *riscv* architecture.

   -  ``systemd-serialgetty``:

      -  the recipe no longer sets a default value for
         :term:`SERIAL_CONSOLES`, and uses the one set in ``bitbake.conf``.

      -  the recipe no longer ships a copy of the ``serial-getty@.service`` as
         it is provided by systemd directly.

      -  Don't set a default :term:`SERIAL_CONSOLES` value in the
         ``systemd-serialgetty`` recipe and take the global value that should
         already be set.

      -  Replace custom unit files by existing unit files provided in the
         systemd source code.

   -  User unit supports was improved. All the user units are now enabled by
      default.

   -  The custom implementation of ``systemctl`` in :term:`OpenEmbedded-Core
      (OE-Core)` was removed to use the upstream one. This ``systemctl`` binary
      is now compiled and used for systemd-related operations.

-  :ref:`ref-classes-sanity` class changes:

   -  Add a sanity check to validate that the C++ toolchain is functional on the
      host.

   -  Add a sanity check to verify that :term:`TOPDIR` does not contain
      non-ASCII characters, as it may lead to unexpected build errors.

-  Miscellaneous changes:

   -  ``bluez``: fix mesh build when building with musl.

   -  ``python3-pip``: the ``pip`` executable is now left and not deleted, and
      can be used instead of ``pip3`` and ``pip2``.

   -  ``tar`` image types are now more reproducible as the :term:`IMAGE_CMD` for
      ``tar`` now strips ``atime`` and ``ctime`` from the archive content.

   -  :term:`SOLIBSDEV` and :term:`SOLIBS` are now defined for the *mingw32*
      architecture (``.dll``).

   -  :ref:`rootfs-postcommands <ref-classes-rootfs*>`: make ``opkg`` status
      reproducible.

   -  The default :term:`KERNEL_CONSOLE` value is no longer ``ttyS0`` but the
      first entry from the :term:`SERIAL_CONSOLES` variable.

   -  ``virglrenderer``: add a patch to fix ``-int-conversion`` build issue.

   -  ``ffmpeg``: disable asm optimizations for the *x86* architecture as PIC is
      required and *x86* ASM code is not PIC.

   -  ``udev-extraconf``: fix the ``network.sh`` script that did not configure
      hotplugged interfaces.

   -  ``classes-global/license``: move several functions and logic to library
      code in :oe_git:`meta/lib/oe/license.py </openembedded-core/tree/meta/lib/oe/license.py>`.

   -  The recipe ``cairo`` now disables the features ``symbol-lookup``,
      ``spectre`, and ``tests`` by default.

   -  The recipe ``glib-2.0`` now disables the feature ``sysprof`` by default.

   -  The recipe ``gstreamer1.0-libav`` now disables the feature ``doc`` by default.

   -  ``rxvt-unicode``: change ``virtual/x-terminal-emulator`` from
      :term:`PROVIDES` to :term:`RPROVIDES` as ``virtual-x-terminal-emulator``.
      Also make this recipe depend on the ``x11`` distro features with
      :term:`REQUIRED_DISTRO_FEATURES`.

   -  ``rxvt-unicode.inc``: disable the ``terminfo`` installation by setting
      ``TIC`` to ``:`` in :term:`EXTRA_OECONF`, to avoid host contamination.

   -  ``matchbox-terminal``: add ``x-terminal-emulator`` as :term:`RPROVIDES`
      and set :term:`ALTERNATIVE` for the recipe.

   -  ``default-providers.conf``: set ``rxvt-unicode`` as the default
      ``virtual-x-terminal-emulator`` runtime provider with
      :term:`PREFERRED_RPROVIDER`.

   -  ``cve-update-nvd2-native``: updating the database will now result in an
      error if :term:`BB_NO_NETWORK` is enabled and
      :term:`CVE_DB_UPDATE_INTERVAL` is not set to ``-1``. Users can control the
      NVD database source using the :term:`NVD_DB_VERSION` variable with
      possible values ``NVD1``, ``NVD2``, or ``FKIE``.

   -  ``systemtap``: add ``--with-extra-version="oe"`` configure option to
      improve the reproducibility of the recipe.

   -  ``python3``: package ``tkinter``'s shared objects separately in the
      ``python3-tkinter`` package.

   -  ``init-manager``: set the variable ``VIRTUAL-RUNTIME_dev_manager`` to
      ``udev`` by default in
      :oe_git:`meta/conf/distro/include/init-manager-none.inc
      </openembedded-core/tree/meta/conf/distro/include/init-manager-none.inc>`
      and :oe_git:`meta/conf/distro/include/init-manager-sysvinit.inc
      </openembedded-core/tree/meta/conf/distro/include/init-manager-sysvinit.inc>`,
      instead of :oe_git:`meta/recipes-core/packagegroups/packagegroup-core-boot.bb
      </openembedded-core/tree/meta/recipes-core/packagegroups/packagegroup-core-boot.bb>`
      only.

      Likewise, the same is done for ``VIRTUAL-RUNTIME_keymaps`` with
      ``keymaps`` as its default value.

   -  ``seatd``: Create a ``seat`` group and package the systemd service
      ``seatd.service`` with correct permissions.

      That way, the ``weston`` user in ``weston-init.bb`` was added to the
      ``seat`` group to be able to properly establish connection between the
      Weston and the ``seatd`` socket.

   -  ``webkitgtk``:

      -  Fix build on 32bit arches with 64bit ``time_t`` only.

      -  Disable JIT on RISCV64.

   -  :ref:`ref-classes-report-error`: Add :term:`PN` to error report files.

   -  ``initrdscripts``: add UBI support for mounting a live ``ubifs`` rootfs.

   -  ``uboot-extlinux-config.bbclass``: add support for device tree overlays.

   -  ``glibc``: add ``ld.so.conf`` to :term:`CONFFILES`.

   -  ``udev-extraconf``: Allow FAT mount group to be specified with
      :term:`MOUNT_GROUP`.

   -  New ``bbverbnote`` log utility which can be used to print on the console
      (equivalent to the ``bb.verbnote`` Python implementation).

   -  :ref:``ref-classes-grub-efi``: Add :term:`GRUB_TITLE` variable to set
      custom GRUB titles.

   -  ``gawk``: Enable high precision arithmetic support by default (``mpfr``
      enabled by default in :term:`PACKAGECONFIG`).

   -  ``licenses``: Map the license ``SGIv1`` to ``SGI-OpenGL``, as ``SGIv1`` is
      not an SPDX license identifier.

   -  Configuration files for the `b4 <https://b4.docs.kernel.org>`__
      command-line tool was added to the different Yocto Project and OpenEmbedded
      repositories.

   -  :ref:`ref-classes-kernel-fitimage`: handle :doc:`multiconfig
      </dev-manual/multiconfig>` dependency when
      :term:`INITRAMFS_MULTICONFIG` is set.

   -  ``psplash``: when using the ``systemd`` feature from
      :term:`DISTRO_FEATURES`, start the ``psplash`` service when the
      ``/dev/fb0`` framebuffer is detected with Udev.

   -  ``gdb``: is now compiled with xz support by default (``--with-lzma``).

   -  ``busybox``: drop net-tools from the default ``defconfig``, since these tools
      (``ifconfig``, etc.) have been deprecated since `2009
      <https://lists.debian.org/debian-devel/2009/03/msg00780.html>`__.

   -  ``perf`` is built with ``zstd`` in :term:`PACKAGECONFIG` by default.

   -  ``boost``: add ``charconv`` to built libraries by default.

   -  ``mirrors``: rationalise Debian mirrors to point at the canonical server
      (deb.debian.org) instead of country specific ones. This server is backed
      by a :wikipedia:`CDN <Content_delivery_network>` to properly balance the
      server load.

   -  ``lib: sbom30``: Add action statement for affected VEX statements with
      "Mitigation action unknown", as these are not tracked by the existing
      code.

Known Issues in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  The :ref:`ref-classes-cve-check` class is based on the `National
   Vulnerability Database <https://nvd.nist.gov/>`__ (NVD). Since the beginning
   of 2024, the maintainers of this database have stopped annotating CVEs with
   the affected CPEs. This prevents the :ref:`ref-classes-cve-check` class to
   properly report CVEs as CPEs are used to match Yocto recipes with CVEs
   affecting them. As a result, the current CVE reports may look good but the
   reality is that some vulnerabilities are just not reported.

   During that time, users may look up the 'CVE database
   <https://www.cve.org/>'__ for entries concerning software they use, or follow
   release notes of such projects closely.

   Please note, that the :ref:`ref-classes-cve-check` tool has always been a
   helper tool, and users are advised to always review the final result. Results
   of an automatic scan may not take into account configuration options,
   compiler options and other factors.

Recipe License changes in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following corrections have been made to the :term:`LICENSE` values set by recipes:

Security Fixes in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recipe Upgrades in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Contributors to |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thanks to the following people who contributed to this release:

-  Aditya Tayade
-  Adrian Freihofer
-  Alban Bedel
-  Aleksandar Nikolic
-  Alessio Cascone
-  Alexander Hirsch
-  Alexander Kanavin
-  Alexander Sverdlin
-  Alexander van Gessel
-  Alexander Yurkov
-  Alexandre Marques
-  Alexis Cellier
-  Alex Kiernan
-  Andrej Valek
-  Angelo Ribeiro
-  Antonin Godard
-  Archana Polampalli
-  Artur Kowalski
-  Awais Belal
-  Balaji Pothunoori
-  Bartosz Golaszewski
-  Bastian Germann
-  Bastian Krause
-  Bastien JAUNY
-  BELHADJ SALEM Talel
-  Benjamin Bara
-  Benjamin Grossschartner
-  Benjamin Szőke
-  Bin Lan
-  Bruce Ashfield
-  Changhyeok Bae
-  Changqing Li
-  Chen Qi
-  Chris Laplante
-  Christian Lindeberg
-  Christian Taedcke
-  Christos Gavros
-  Claus Stovgaard
-  Clayton Casciato
-  Colin McAllister
-  Daniel Ammann
-  Daniel McGregor
-  Dan McGregor
-  Deepesh Varatharajan
-  Deepthi Hemraj
-  Denis OSTERLAND-HEIM
-  Denys Dmytriyenko
-  Derek Straka
-  Divya Chellam
-  Dmitry Baryshkov
-  Enrico Jörns
-  Enrico Scholz
-  Eric Meyers
-  Esben Haabendal
-  Etienne Cordonnier
-  Fabio Berton
-  Fabio Estevam
-  Gaël PORTAY
-  Georgi, Tom
-  Guðni Már Gilbert
-  Guénaël Muller
-  Harish Sadineni
-  Haseeb Ashraf
-  Hiago De Franco
-  Hongxu Jia
-  Igor Opaniuk
-  Jagadeesh Krishnanjanappa
-  Jamin Lin
-  Jason Schonberg
-  Jean-Pierre Geslin
-  Jermain Horsman
-  Jesse Riemens
-  Jiaying Song
-  Jinfeng Wang
-  João Henrique Ferreira de Freitas
-  Joerg Schmidt
-  Jonas Gorski
-  Jon Mason
-  Jörg Sommer
-  Jose Quaresma
-  Joshua Watt
-  Julien Stephan
-  Justin Bronder
-  Kai Kang
-  Katariina Lounento
-  Katawann
-  Kevin Hao
-  Khem Raj
-  Koen Kooi
-  Lee Chee Yang
-  Lei Maohui
-  Lei YU
-  Leon Anavi
-  Louis Rannou
-  Maik Otto
-  Makarios Christakis
-  Marc Ferland
-  Marco Felsch
-  Marek Vasut
-  Mark Hatle
-  Markus Volk
-  Marta Rybczynska
-  Martin Jansa
-  Mathieu Dubois-Briand
-  Matthias Schiffer
-  Maxin John
-  Michael Estner
-  Michael Halstead
-  Michael Nazzareno Trimarchi
-  Michael Opdenacker
-  Michelle Lin
-  Mikko Rapeli
-  Ming Liu
-  Moritz Haase
-  Nick Owens
-  Nicolas Dechesne
-  Nikolai Merinov
-  Niko Mauno
-  Ninette Adhikari
-  Ola x Nilsson
-  Oleksandr Hnatiuk
-  Oliver Kästner
-  Omri Sarig
-  Pascal Eberhard
-  Patrik Nordvall
-  Paul Barker
-  Pavel Zhukov
-  Pedro Ferreira
-  Peter Bergin
-  Peter Delevoryas
-  Peter Kjellerstedt
-  Peter Marko
-  Peter Tatrai
-  Philip Lorenz
-  Priyal Doshi
-  Purushottam Choudhary
-  Quentin Schulz
-  Ralph Siemsen
-  Randy MacLeod
-  Ranjitsinh Rathod
-  Rasmus Villemoes
-  Regis Dargent
-  Ricardo Salveti
-  Richard Purdie
-  Robert Yang
-  Rohini Sangam
-  Roland Hieber
-  Ross Burton
-  Ryan Eatmon
-  Savvas Etairidis
-  Sean Nyekjaer
-  Sebastian Zenker
-  Sergei Zhmylev
-  Shunsuke Tokumoto
-  Sid-Ali
-  Simon A. Eugster
-  Simone Weiß
-  Slawomir Stepien
-  Sofiane HAMAM
-  Stefan Gloor
-  Stefan Herbrechtsmeier
-  Stefan Koch
-  Stefan Mueller-Klieser
-  Steve Sakoman
-  Sunil Dora
-  Sven Kalmbach
-  Talel BELHAJSALEM
-  Thomas Perrot
-  Thomas Roos
-  Tim Orling
-  Tom Hochstein
-  Trevor Gamblin
-  Ulrich Ölmann
-  Valeria Petrov
-  Victor J. Hansen
-  Victor Kamensky
-  Vijay Anusuri
-  Vince Chang
-  Vivek Puar
-  Vyacheslav Yurkov
-  Walter Schweizer
-  Wang Mingyu
-  Weisser, Pascal
-  Xiangyu Chen
-  Xiaotian Wu
-  Yash Shinde
-  Yi Zhao
-  Yoann Congal
-  Yogita Urade
-  Zoltán Böszörményi

Repositories / Downloads for Yocto-|yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
