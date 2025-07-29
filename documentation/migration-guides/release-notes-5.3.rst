.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

.. |yocto-codename| replace:: whinlatter
.. |yocto-ver| replace:: 5.3
.. Note: anchors id below cannot contain substitutions so replace them with the
   value of |yocto-ver| above.

Release notes for |yocto-ver| (|yocto-codename|)
------------------------------------------------

New Features / Enhancements in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Linux kernel XXX, gcc 15, glibc XXX, LLVM XXX, and over XXX other
   recipe upgrades.

-  Minimum Python version required on the host: XXX.

-  BitBake changes:

   -  ``codeparser``: Add function decorators for ``vardeps``

      Adds ``bb.parse.vardeps`` and ``bb.parse.excludevardeps`` function
      decorators that can be used to explicitly add or exclude variables from a
      Python function parsed by :term:`BitBake`.

      Move ``vardepexclude`` flag entries alongside functions for
      maintainability.

   -  Fetcher:

      -  Check for ``git-lfs`` existence before using it.

      -  Add support for ``.debs`` files containing uncompressed data tarballs.

      -  ``az``: Add sanity check to check that :term:`AZ_SAS` starts with ``?``
         to mark the start of the query parameters.

      -  ``git``: Add the tag to shallow clone tarball name.

   -  ``knotty``: pass failed task logs through the log infrastructure (use
      ``bb.plain()`` instead of ``print()``)

   -  Add support for automatically promoting class inherits to deferred
      inherits by listing them in the :term:`BB_DEFER_BBCLASSES` variable.

   -  "Built-in" fragments support is now added to the :ref:`addfragments
      <bitbake-user-manual/bitbake-user-manual-metadata:\`\`addfragments\`\`
      directive>` directive. This is the fourth parameter to this directive, and
      should be the name of the variable that contains definitions of built-in
      fragments. Refer to the documentation of :ref:`addfragments
      <bitbake-user-manual/bitbake-user-manual-metadata:\`\`addfragments\`\`
      directive>` to learn how to define new built-in fragments.

      Listing these built-in fragments can be done with
      :oe_git:`bitbake-config-build
      list-fragments</bitbake/tree/bin/bitbake-config-build>`, which could
      list::

         Available built-in fragments:
         machine/...     Sets MACHINE = ...
         distro/...      Sets DISTRO = ...

      In the above example, this means that the :term:`MACHINE` of
      :term:`DISTRO` can be overridden with::

         OE_FRAGMENTS += "machine/qemuarm64 distro/poky-bleeding"

      This would set :term:`MACHINE` to ``qemuarm64`` and the :term:`DISTRO` to
      ``poky-bleeding``.

   -  The ``tag-`` parameter in URLs can now be specified alongside the ``rev=``
      parameter and :term:`SRCREV` variable, and will ensure that the
      specified tag matches the specified revision.

      It is **strongly encouraged** to include the ``tag=`` parameter to the
      :term:`SRC_URI` definition when possible.

   -  ``tinfoil``: add a ``wait_for`` decorator to wrap a function that makes an
      asynchronous tinfoil call wait for event to say that the call has been
      successful, or an error has occurred.

   -  New ``bb.utils.to_filemode()`` helper function which is a helper to take a
      variable's content containing a filemode and convert it to the proper
      Python representation of the number.

   -  ``cooker``: Use a shared counter for processing parser jobs. This allows
      the parser processes to run independently of needing to be feed by the
      parent process, and load balances them much better.

   -  ``cooker/process/utils``: Add a ``-P`` (``--profile``) option to
      :term:`BitBake` to specify what to profile. Can be "main", "idle" or
      "parsing". Split the reports in separate files.

-  Toolchain changes:

   -  The Clang/LLVM toolchain can now be used as part of the build.

      The :term:`PREFERRED_TOOLCHAIN_TARGET`, :term:`PREFERRED_TOOLCHAIN_NATIVE`
      and :term:`PREFERRED_TOOLCHAIN_SDK` variables can be used to customize the
      selected toolchain globally.

      There are two supported toolchains: "gcc" and "clang". See the
      documentation of :term:`PREFERRED_TOOLCHAIN_TARGET` for more details.

      The toolchain is also customizable on a per-recipe basis, using the
      :term:`TOOLCHAIN` and :term:`TOOLCHAIN_NATIVE` variables.

   -  Multiple recipes were pinned to use the GCC/Binutils toolchain as they do
      not support being built with Clang/LLVM yet. In these recipes the
      :term:`TOOLCHAIN` variable is set to "gcc".

-  Global configuration changes:

   -  ``bitbake.conf/pseudo``: Switch from exclusion list to inclusion list by
      swapping :term:`PSEUDO_IGNORE_PATHS` for :term:`PSEUDO_INCLUDE_PATHS`
      which should be easier and more explicit to maintain.

   -  ``bitbake.conf``: Drop ``lz4`` from :term:`HOSTTOOLS`, as it is not
      required anymore, and the ``lz4-native`` package is used instead.

   -  ``conf/fragments``: add a fragment for the CDN :ref:`sstate-cache
      <overview-manual/concepts:shared state cache>` mirror.

   -  ``default-distrovars``: set an empty default for :term:`LICENSE_PATH`.

   -  The default definition of :term:`UNPACKDIR` is no longer
      ``sources-unpack`` but ``sources``.

-  New variables:

   -  The ``VIRTUAL-RUNTIME_dbus`` variable, to allow changing the runtime
      implementation of D-Bus. See :term:`VIRTUAL-RUNTIME`.

   -  The ``VIRTUAL-RUNTIME_libsdl2`` variable, to allow changing the runtime
      implementation of `libsdl2 <https://www.libsdl.org/>`__. See
      :term:`VIRTUAL-RUNTIME`.

   -  The :term:`SPDX_PACKAGE_URL` variable can be used in recipes to set the
      output ``software_packageUrl`` field in their associated SPDX 3.0 output
      (default value: empty string).

   -  The :term:`KMETA_CONFIG_FEATURES` variable can be used to control
      :ref:`ref-classes-kernel-yocto` configuration features. For now only
      ``prefer-modules`` is supported for this variable.

   -  The :term:`TESTSDK_SUITES` variable can be used to control the list of
      tests run for the :ref:`ref-classes-testsdk` class.

   -  The :term:`UBOOT_FIT_CONF_FIRMWARE` can be used to specify a ``firmware``
      entry in the configuration node of a FIT image.

   -  The :term:`SPDX_INCLUDE_COMPILED_SOURCES` option allows the same as
      :term:`SPDX_INCLUDE_SOURCES` but including only the sources used to
      compile the host tools and the target packages.

   -  The :term:`UBOOT_VERSION` variable holds the package version
      (:term:`PV`) and revision (:term:`PR`) which are part of the installed and
      deployed filenames. Users can now override :term:`UBOOT_VERSION` to
      changes the output filenames.

-  Kernel-related changes:

   -  ``linux/generate-cve-exclusions``: use data from CVEProject instead of
      the archived https://linuxkernelcves.com.

   -  ``kernel-yocto``: allow annotated options to be modified. For example if
      the following kernel configuration is set::

         CONFIG_INET_TUNNEL=y # OVERRIDE:$MODULE_OR_Y

      And if the :term:`KMETA_CONFIG_FEATURES` variable contains
      ``prefer-modules``, ``CONFIG_INET_TUNNEL`` will be set to ``m`` instead of
      ``y``.

   -  ``kernel-devsrc``: Replace the extra ``System.map`` file with symbolic
      link.

   -  ``kernel-module-split``: Allow for external configuration files being
      assigned to the correct kernel module package.

   -  When built for the RISC-V architecture, ensure that the minimum required
      features set by :term:`TUNE_FEATURES` are set using the
      :ref:`ref-classes-features_check` class.

   -  ``linux-yocto``: when built for RISC-V, enable features in
      :term:`KERNEL_FEATURES` based on features listed in :term:`TUNE_FEATURES`.

-  New core recipes:

   -  ``python3-pdm``, ``python3-pdm-backend`` and ``python3-pdm-build-locked``,
      which are dependencies of ``python3-webcolors``. ``python3-pdm`` itself
      depends on ``python3-pdm-build-locked``

   -  ``bindgen-cli``: a tool to generate Rust bindings.

   -  ``python3-colorama``: Cross-platform colored terminal text, needed by
      ``pytest`` as a dependency.

   -  ``libglvnd``: imported from :oe_git:`meta-oe
      </meta-openembedded/tree/meta-oe>` which provides a vendor neutral
      approach to handling OpenGL / OpenGL ES / EGL / GLX libraries.

   -  ``python3-sphinx-argparse``: A sphinx extension that automatically
      documents ``argparse`` commands and options. It is part of
      ``buildtools-docs-tarball`` for later use in the Yocto Project
      documentation.

   -  ``python3-sphinx-copybutton``: A sphinx extension that adds a copy button
      to code blocks in Sphinx. It is part of ``buildtools-docs-tarball`` for later
      use in the Yocto Project documentation.

   -  LLVM/Clang related recipes:

      -  ``clang``: LLVM based C/C++ compiler.

      -  ``compiler-rt``: LLVM based C/C++ compiler Runtime.

      -  ``libclc``: Implementation of the library requirements of the OpenCL C
         programming language.

      -  ``libcxx``: new implementation of the C++ standard library, targeting
         C++11 and above

      -  ``llvm-tblgen-native``: LLVM TableGen binaries for the build host,
         often used to build LLVM projects.

      -  ``lldb``: LLDB debugger for LLVM projects.

      -  ``llvm-project-source``: canonical git mirror of the LLVM subversion
         repository.

      -  ``openmp``: LLVM OpenMP compiler Runtime.

  -  ``kernel-signing-keys-native``: this recipe is used in the
     :ref:`ref-classes-kernel-fit-image` class to generate a pair of RSA
     public/private key. It replaces the ``do_generate_rsa_keys`` of the
     :ref:`ref-classes-kernel-fit-image` class.

-  New :term:`DISTRO_FEATURES`:

   -  ``glvnd``, which enables OpenGL Vendor Neutral Dispatch Library
      support when using recipes such as ``mesa``.

-  New core classes:

   -  The new :ref:`ref-classes-kernel-fit-image` class replaces the previous
      ``kernel-fitimage`` class. It has been rewritten and improved to fix
      :yocto_bugs:`bug 12912</show_bug.cgi?id=12912>`. See the :ref:`Removed
      Classes <migration-guides/migration-5.3:Removed Classes>` section of the
      Migration notes for |yocto-ver| (|yocto-codename|) for more details on how
      to switch to this new class.

   -  The new :ref:`ref-classes-go-mod-update-modules` class can be used to
      maintain Go recipes that use a ``BPN-go-mods.inc`` and
      ``BPN-licenses.inc`` and update these files automatically.

-  Architecture-specific changes:

   -  Rework the RISC-V :term:`TUNE_FEATURES` to make them based of the RISC-V
      ISA (Instruction Set Architecture) implementation.

      This implements the following base ISAs:

      -  ``rv32i``, ``rv64i``
      -  ``rv32e``, ``rv64i``

      The following ABIs:

      -  ``ilp32``, ``ilp32e``, ``ilp32f``, ``ilp32d``
      -  ``lp64``, ``lp64e``, ``lp64f``, ``lp64d``

      The following ISA extension are also implemented:

      -  M: Integer Multiplication and Division Extension
      -  A: Atomic Memory Extension
      -  F: Single-Precision Floating-Point Extension
      -  D: Double-Precision Floating-Point Extension
      -  C: Compressed Extension
      -  B: Bit Manipulation Extension (implies Zba, Zbb, Zbs)
      -  V: Vector Operations Extension
      -  Zicsr: Control and Status Register Access Extension
      -  Zifencei: Instruction-Fetch Fence Extension
      -  Zba: Address bit manipulation extension
      -  Zbb: Basic bit manipulation extension
      -  Zbc: Carry-less multiplication extension
      -  Zbs: Single-bit manipulation extension
      -  Zicbom: Cache-block management extension

      The existing processors tunes are preserved:

      -  ``riscv64`` (``rv64gc``)
      -  ``riscv32`` (``rv32gc``)
      -  ``riscv64nf`` (``rv64imac_zicsr_zifencei``)
      -  ``riscv32nf`` (``rv32imac_zicsr_zifencei``)
      -  ``riscv64nc`` (``rv64imafd_zicsr_zifencei``)

      See :oe_git:`meta/conf/machine/include/riscv/README
      </openembedded-core/tree/meta/conf/machine/include/riscv/README>` for more
      information.

   -  ``arch-mips.inc``: Use ``-EB``/``-EL`` for denoting Endianness.

   -  Enable ``riscv32`` as supported arch for ``musl`` systems.

   -  Powerpc: Use ``-maltivec`` in compiler flags if ``altivec`` is in
      :term:`TUNE_FEATURES`.

-  QEMU / ``runqemu`` changes:

   -  Refactor :ref:`ref-classes-qemu` functions into library functions (in
      :oe_git:`lib/oe/qemu.py </openembedded-core/tree/meta/lib/oe/qemu.py>`).

-  Documentation changes:

   -  Part of :term:`BitBake` internals are now documented at
      :yocto_docs:`/bitbake/bitbake-user-manual/bitbake-user-manual-library-functions.html`.

   -  A new :doc:`/dev-manual/limiting-resources` guide was created to help
      users limit the host resources used by the :term:`OpenEmbedded Build
      System`.

-  Core library changes:

   -  Add :oe_git:`license_finder.py </openembedded-core/tree/meta/lib/oe/license_finder.py>`,
      which was extracted from ``recipetool`` to be shared for multiple users.
      Improve its functionalities.

-  Go changes:

-  Rust changes:

   -  ``rust-llvm``:

      -  Compile LLVM to use dynamic libraries. This reduces the
         size of ``llvm-rust`` to about a third.

      -  Disable the following feature through configuration
         (:ref:`ref-tasks-configure`): libedit, benchmarks.

-  Wic Image Creator changes:

   -  After a Python upgrade, WIC plugins containing dashes (``-``) for their
      filenames are **no longer supported**. One must convert the dashed to
      underscores (``_``) and update users of the plugins accordingly.

      See the :ref:`migration-guides/migration-5.3:Wic plugins containing dashes
      should be renamed` section of the Yocto Project 5.3 Migration Guide for
      more information.

   -  ``wic``: do not ignore :term:`IMAGE_ROOTFS_SIZE` if the Rootfs is
      modified.

   -  Several improvements in WIC selftests.

   -  ``bootimg_efi.py``: fail build if no binaries are installed.

   -  Add new options to the ``wic`` ``ls``, ``cp``, ``rm``, and ``write``
      commands:

      -  ``--image-name``: name of the image to use the artifacts from.
      -  ``--vars``: directory with ``<image>.env`` files that store
         :term:`BitBake` variables. This directory is usually found in
         :term:`STAGING_DIR`.

-  SDK-related changes:

   -  Include additional information about Meson setting in the SDK environment
      setup script (host system, CPU family, etc.).

-  Testing-related changes:

   -  ``bitbake/tests/fetch``: Add tests for ``gitsm`` with git-lfs.

   -  ``bitbake/lib/bb/tests/fetch``: add a test case to ensure Git shallow
      fetch works for tag containing slashes.

   -  OEQA:

      -  SDK:

         -  Add a test to sanity check that the generated SDK manifest was
            parsed correctly and isn't empty.

         -  Add a test to verify the manifests are generated correctly.

         -  Add helpers to check for and install packages.

         -  Add check that meson has detected the target correctly.

      -  Simplify test specification and discovery:

         -  Introduce the ``TESTSDK_CASE_DIRS`` variable to specify test
            directory types, replacing the need to modify the ``default_cases``
            class member.

         -  Discover tests from configured layers using a common discovery
            pattern (``<LAYER_DIR>/lib/oeqa/<dirname>/cases``) where
            ``<dirname>`` is specified in ``TESTSDK_CASE_DIRS``.

         -  The "buildtools" directories were renamed to follow the common
            discovery pattern (``<LAYER_DIR>/lib/oeqa/<dirname>/cases``) for
            consistency across all SDK configurations.

      -  ``selftest/reproducible``: Limit memory used by ``diffoscope`` to avoid
         triggering OOM kills.

      -  Add tests for the :ref:`ref-classes-devicetree` class.

      -  Tests for the :ref:`ref-classes-kernel-fit-image` class have been
         reworked and improved.

      -  ``data.py``: add ``skipIfNotBuildArch`` decorator, to skip tests if
         :term:`BUILD_ARCH` is not in present in the specified tuple.

      -  ``selftest``: add new test for toolchain switching.

      -  ``utils/command``: add a fast-path ``get_bb_var()`` that uses
         ``bitbake-getvar`` instead of ``bitbake -e`` when there is not
         ``postconfig`` argument passed.

      -  ``core/case``: add file exists assertion test case.

      -  ``context.py``: use :term:`TEST_SUITES` if set.

   -  :ref:`ref-classes-testexport`: capture all tests and data from all layers
      (instead of the :term:`OpenEmbedded-Core (OE-Core)` layer only).

-  Utility script changes:

   -  ``sstate-cache-management``: add a ``--dry-run`` argument

   -  ``yocto-check-layer``:

      -  Expect success for ``test_patches_upstream_status``. This means that
         patch files *must* include an ``Upstream-Status`` to pass with this
         script.

      -  :ref:`ref-classes-yocto-check-layer` class:

         -  Refactor to be extended easily.

         -  Add a ``check_network_flag`` test that checks that no tasks other
            than :ref:`ref-tasks-fetch` can access the network.

   -  ``send-error-report``:

      -  Respect URL scheme in server name if it exists.

      -  Drop ``--no-ssl`` as the server URL specifies it with ``http://`` or
         ``https://``.

   -  ``buildstats.py``:

      -  Extend disk stats support for NVMe and flexible token count.

      -  Add tracking of network I/O per interface.

   -  ``buildstats-diff``: find last two Buildstats files if none are specified.

   -  ``pybootchartgui``: visualize ``/proc/net/dev`` network stats in graphs.

-  Packaging changes:

   -  Export ``debugsources`` in :term:`PKGDESTWORK` as JSON. The source
      information used during packaging can be use from other tasks to have more
      detailed information on the files used during the compilation and improve
      SPDX accuracy.

-  LLVM related changes:

   -  Like ``gcc-source``, the LLVM project sources are part of ``work-shared``
      under :term:`TMPDIR`. The project codebase is large and sharing it offers
      performance improvements.

-  SPDX-related changes:

   -  ``spdx30``: Provide ``software_packageUrl`` field

   -  ``spdx30_tasks``: Change recipe license to "declared" (instead of
      "concluded")

   -  ``create-spdx-2.2``: support to override the version of a package in SPDX
      2 through :term:`SPDX_PACKAGE_VERSION`.

-  ``devtool`` and ``recipetool`` changes:

   -  Use ``lib/oe/license_finder`` to extract the license from source code.

   -  Calculate source paths relative to :term:`UNPACKDIR`.

   -  Allow ``recipe create`` handlers to specify bitbake tasks to run.

   -  ``create_go``: Use :ref:`ref-classes-go-mod` class instead of
      :ref:`ref-classes-go-vendor`.

   -  Go recipes are now generated with help of the new
      :ref:`ref-classes-go-mod-update-modules` class.

   -  Add a new :oe_git:`improve_kernel_cve_report.py
      </openembedded-core/tree/meta/scripts/contrib/improve_kernel_cve_report.py>`
      script in ``scripts/contrib`` for post-processing of kernel CVE data.

   -  Handle workspaces for multiconfig.

-  Patchtest-related changes:

-  Security changes:

   -  ``openssl``: add FIPS support. This can be enabled through the ``fips``
      :term:`PACKAGECONFIG`.

-  :ref:`ref-classes-cve-check` changes:

-  New :term:`PACKAGECONFIG` options for individual recipes:

   -  ``ppp``: ``l2tp``, ``pptp``
   -  ``dropbear``: ``x11`` (renamed from ``enable-x11-forwarding``)
   -  ``gdb``: ``source-highlight``
   -  ``gstreamer1.0-plugins-bad``: ``analytics``
   -  ``mtd-utils``: ``ubihealthd-service``
   -  ``openssl``: ``fips``
   -  ``qemu``: ``sdl-image``, ``pixman``
   -  ``wget``: ``pcre2``
   -  ``mesa``: ``asahi``, ``amd``, ``svga``, ``teflon``, ``nouveau``

-  Systemd related changes:

   -  Enable getty generator by default by adding ``serial-getty-generator`` to
      :term:`PACKAGECONFIG`.

-  :ref:`ref-classes-sanity` class changes:

   -  :ref:`ref-classes-insane`: Move test for invalid :term:`PACKAGECONFIG` to
      :ref:`ref-tasks-recipe-qa`.

   -  Add ``unimplemented-ptest`` detection for cargo-based tests, allowing to
      detect when a cargo package has available tests that could be enable with
      :doc:`Ptest </test-manual/ptest>`.

   -  Add a test for recipe naming/class mismatches.

   -  Add a sanity test for "bad" gcc installs on Ubuntu 24.04. The host should
      install ``libstdc++-14-dev`` instead of ``libgcc-14-dev`` to avoid build
      issues when building :ref:`ref-classes-native` with Clang.

-  U-boot related changes:

   -  :ref:`ref-classes-uboot-sign`: Add support for setting firmware property
      in FIT configuration with :term:`UBOOT_FIT_CONF_FIRMWARE`.

   -  :ref:`ref-classes-uboot-sign`: Add support for signing U-Boot FIT image
      without an SPL. The :term:`SPL_DTB_BINARY` variable can be set to an empty
      string to indicate that no SPL is present.

   -  When built for the RISC-V architecture, read the :term:`TUNE_FEATURES`
      variable to automatically set U-boot configuration options (for example
      ``CONFIG_RISCV_ISA_F``).

-  Miscellaneous changes:

   -  ``dropbear``: The ``dropbearkey.service`` can now take extra arguments for
      key generation, through ``/etc/default/dropbear``.

   -  ``initscripts``: add ``log_success_msg``/``log_failure_msg``/``log_warning_msg``
      functions for logging in initscripts.

   -  ``connman``:

      -  Mark ``iptables`` and ``nftables`` feature of :term:`PACKAGECONFIG`
         mutually incompatible.

      -  Set ``dns-backend`` automatically to ``systemd-resolved``
         when ``systemd-resolved`` is part of :term:`DISTRO_FEATURES`.

   -  ``uninative``: show errors if installing fails.

   -  ``meson``: Allow user to override setup command options by exporting
      ``MESON_SETUP_OPTS`` in a recipe.

   -  :ref:`ref-classes-cmake`: Enhance to emit a native toolchain CMake file.
      This is part of improvements allowing to use ``clang`` in an SDK.

   -  Fix the runtime version of several recipes (they now return the effective
      version instead of a default string like "Unknown").

   -  :ref:`ref-classes-module`: add ``KBUILD_EXTRA_SYMBOLS`` to the install
      command.

   -  ``rpm-sequoia``: add :doc:`Ptest </test-manual/ptest>` support.

   -  ``libunwind``: disable installation of tests directory with
      ``--disable-tests``, which can be installed with the ``libunwind-ptest``
      package instead.

   -  ``boost``: add ``process`` library to the list of built libraries.

   -  ``base-files``: add ``nsswitch-resolved.conf``, only installed if
      ``systemd`` and ``systemd-resolved`` is part of :term:`DISTRO_FEATURES`.

   -  ``nfs-utils``: don't use signals to shut down the NFS server in the
      associated initscript, instead use ``rpc.nfsd 0``.

   -  ``readline``: enable HOME, END, INSERT, and DELETE key bindings in
      ``inputrc``.

   -  Switch to a new :ref:`sstate-cache <overview-manual/concepts:shared state
      cache>` CDN (http://sstate.yoctoproject.org).

   -  :ref:`ref-classes-sstate`: Apply a proper :manpage:`umask` when fetching
      from :term:`SSTATE_MIRRORS`.

   -  ``kernel-devsrc``: make package version consistent with kernel source (by
      inheriting :ref:`ref-classes-kernelsrc`).

   -  :ref:`ref-classes-externalsrc`: Always ask Git for location of ``.git``
      directory (may be different from the default ``${S}/.git``).

   -  :ref:`ref-classes-features_check`: Add support for required
      :term:`TUNE_FEATURES`.

   -  ``openssh``: limit read access to ``sshd_config`` file (set its filemode
      to ``0600``).

Known Issues in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Recipe License changes in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following changes have been made to the :term:`LICENSE` values set by recipes:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Recipe
     - Previous value
     - New value
   * - ``recipe name``
     - Previous value
     - New value

Security Fixes in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following CVEs have been fixed:

.. list-table::
   :widths: 30 70
   :header-rows: 1

   * - Recipe
     - CVE IDs
   * - ``recipe name``
     - :cve_nist:`xxx-xxxx`, ...

Recipe Upgrades in |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following recipes have been upgraded:

.. list-table::
   :widths: 20 40 40
   :header-rows: 1

   * - Recipe
     - Previous version
     - New version
   * - ``recipe name``
     - Previous version
     - New version

Contributors to |yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~

Thanks to the following people who contributed to this release:

Repositories / Downloads for Yocto-|yocto-ver|
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
