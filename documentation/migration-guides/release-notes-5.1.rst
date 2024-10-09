.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Release notes for 5.1 (styhead)
---------------------------------

New Features / Enhancements in 5.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  Linux kernel 6.X, gcc 14.X, glibc 2.X, LLVM 18.X, and over XXX other recipe upgrades

-  New variables:

   -  :term:`CVE_CHECK_MANIFEST_JSON_SUFFIX`: suffix for the CVE JSON manifest file.

   -  :term:`PRSERV_UPSTREAM`: Upstream PR service (``host:port``) for the local
      PR server to connect to.

   -  :term:`RECIPE_UPGRADE_EXTRA_TASKS`: space-delimited list of tasks to run
      after the new sources have been unpacked in the
      ``scripts/lib/devtool/upgrade.py`` upgrade() method.

   -  :term:`UNPACKDIR`: allow change of the :ref:`ref-tasks-unpack` task
      directory.

-  Architecture-specific enhancements:

  -  The default kernel is the current stable (6.10), and there is also support
     for the latest long-term release (6.6).

-  New core recipes:

   -  `fmt <https://fmt.dev>`__: an open-source formatting library for C++
      (imported from meta-oe).

   -  `xcb-util-errors <http://xcb.freedesktop.org/XcbUtil/>`__: gives human
      readable names to error codes and event codes

-  QEMU / ``runqemu`` enhancements:

   -  runqemu: ``QB_DRIVE_TYPE`` now support for sd card (``/dev/mmcblk``)

-  Rust improvements:

-  SDK-related improvements:

   -  included ``nativesdk-python3-pip`` in buildtools.

-  Testing:

   -  oeqa/selftest: Only rewrite envvars paths that absolutely point to builddir

   -  Enable ptests for ``python3-cffi``, ``python3-idna``, ``python3-libarchive-c``,
      ``python3-mako``, ``python3-packaging``, ``python3-uritools`` and ``python3-rpds-py``.
   -  Included ``nativesdk-python3-pip`` in :term:`buildtools` by default.

   -  Enable ptests for ``python3-cffi``, ``python3-idna``,
      ``python3-libarchive-c``, ``python3-mako``, ``python3-packaging``,
      ``python3-uritools`` and ``python3-rpds-py``.

-  Utility script changes:

   -  New ``cve-json-to-text`` script that converts the ``cve-check`` result
      from the JSON format to the TEXT format as ``cve-check`` removed text
      format.

   -  New ``makefile-getvar`` script to extract value from a Makefile.

   -  New ``pull-spdx-licenses`` script to pull SPDX license data, update
      license list JSON data and update license directory.

   -  Several improvements in ``oe-build-perf-report`` report.

   -  ``oe-debuginfod``: add parameter "-d" to store debuginfod files in project
      sub-directory.

   -  ``resulttool``: support test report generation in JUnit XML format.


-  BitBake improvements:

   -  New go module fetcher (``gomod://``) for downloading module dependencies to the
      module cache from a module proxy.

   -  Fetcher for Rust crates: added a check for latest upstream version.

   -  ``syncrpc`` now requires a minimum version of the websockets module depend
      on Python version.

   -  Improve ``bitbake-hashclient`` stress statistics reporting.

   -  ``bitbake-hashserv`` added ``reuseport`` parameter to enable SO_REUSEPORT,
      allowing multiple servers to bind to the same port for load balancing

   -  Improve cloning speed with :term:`BB_GIT_SHALLOW` and
      :term:`BB_GENERATE_MIRROR_TARBALLS`.

   -  `BitBake` UI now includes log paths for failed task.

   -  ``fetcher2``: support for wget and wget2.

   -  ``fetcher2``: support npm package name with '@' character.

   -  ``fetcher2``: remote name for ``git://`` is now ``origin`` by default.

   -  Codeparser now support shell substitution in quotes, for example::

         var1="$(cmd1 ...)"

-  devtool improvements:

   - Fix ``_test_devtool_add_git_url`` test

-  recipetool improvements:

-  Packaging changes:

-  Security improvements:

-  Toaster Web UI improvements:

-  Prominent documentation updates:

-  Miscellaneous changes:

   -  Fix reproducibility for ``spirv-tools``

   -  Allow selection of host key types used by openssh.

   -  New glibc task ``do_symlist`` to list exported symbols.

   -  ``initramfs-framework`` support for force reboot in the case of fatal error.

   -  The :ref:`ref-classes-insane` class now checks for ``patch-status`` and
      ``pep517-backend`` by default.

   -  New ``yocto-space-optimize`` include file to allow turning off debug compiler options
      for a small set of recipes to reduce build on disk footprint and package/sstate sizes.

   -  Image creation tasks inheriting from the :ref:`ref-classes-image` class
      now produce a ``manifest.json`` file listing the images created. The
      output manifest path is defined by the :term:`IMAGE_OUTPUT_MANIFEST`
      variable.

   -  New :ref:`ref-classes-vex` class generates the minimum information that is necessary
      for VEX generation by an external CVE checking tool.

   -  New :ref:`ref-classes-retain` class creates a tarball of the work directory for a recipe
      when one of its tasks fails, or any other nominated directories.

   -  New ``localpkgfeed`` class in meta-selftest to create a subset of the
      package feed that just contain the packages depended on by this recipe.

   -  New :term:`PACKAGECONFIG` options for individual recipes:

      -  ``appstream``: qt6
      -  ``cronie``: inotify
      -  ``gstreamer1``.0-plugins-bad: gtk3
      -  ``libsdl2``: libsamplerate
      -  ``mesa``: tegra
      -  ``openssh``: hostkey-rsa hostkey-ecdsa hostkey-ed25519
      -  ``pciutils``: kmod zlib
      -  ``piglit``: wayland
      -  ``pulseaudio``: oss-output
      -  ``python3``: staticlibpython
      -  ``python3-jsonschema``: format-nongpl (previously "nongpl")
      -  ``systemd``: bpf-framework
      -  ``util-linux``: libmount-mountfd-support

   -  Stop referring :term:`WORKDIR` for :term:`S` and :term:`B` and trigger
      :ref:`ref-classes-insane` errors when :term:`S` or :term:`B` are equal to
      :term:`WORKDIR`.

Known Issues in 5.1
~~~~~~~~~~~~~~~~~~~

Recipe License changes in 5.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following corrections have been made to the :term:`LICENSE` values set by recipes:

-  ``dejagnu``: update :term:`LICENSE` to ``GPL-3.0-only``.
-  ``gcr``: update :term:`LICENSE` to ``LGPL-2.0-only``.
-  ``glibc``: update :term:`LICENSE` to ``GPL-2.0-only & LGPL-2.1-or-later``.
-  ``gpgme``: update :term:`LICENSE` for different packages.
-  ``libgcrypt``: add license ``BSD-3-Clause``.
-  ``linux-firmware``: separate license ``Firmware-linaro`` for linaro-license package.
-  ``iw``: update :term:`LICENSE` to ``ISC``.
-  ``ppp``: add license ``RSA-MD`` .
-  ``tiff``: update :term:`LICENSE` to ``libtiff``.
-  ``unzip``: update :term:`LICENSE` to ``Info-ZIP``.
-  ``xz``: add :term:`LICENSE` ``PD`` for xz, xz-dev and xz-doc package.
-  ``zip``: update :term:`LICENSE` to ``Info-ZIP``.


Security Fixes in 5.1
~~~~~~~~~~~~~~~~~~~~~

Recipe Upgrades in 5.1
~~~~~~~~~~~~~~~~~~~~~~

Contributors to 5.1
~~~~~~~~~~~~~~~~~~~

Thanks to the following people who contributed to this release:

- Adithya Balakumar
- Adriaan Schmidt
- Adrian Freihofer
- Alban Bedel
- Alejandro Hernandez Samaniego
- Aleksandar Nikolic
- Alessandro Pecugi
- Alexander Kanavin
- Alexander Sverdlin
- Alexandre Belloni
- Alexandre Truong
- Alexis Lothoré
- Andrew Fernandes
- Andrew Oppelt
- Andrey Zhizhikin
- Anton Almqvist
- Antonin Godard
- Anuj Mittal
- Archana Polampalli
- Bartosz Golaszewski
- Benjamin Bara
- Benjamin Szőke
- Bruce Ashfield
- Carlos Alberto Lopez Perez
- Changhyeok Bae
- Changqing Li
- Chen Qi
- Chris Laplante
- Chris Spencer
- Christian Bräuner Sørensen
- Christian Lindeberg
- Christian Taedcke
- Clara Kowalsky
- Clément Péron
- Colin McAllister
- Corentin Lévy
- Daniel Klauer
- Daniel Semkowicz
- Daniil Batalov
- Dan McGregor
- Deepesh Varatharajan
- Deepthi Hemraj
- Denys Dmytriyenko
- Divya Chellam
- Dmitry Baryshkov
- Emil Kronborg
- Enguerrand de Ribaucourt
- Enrico Jörns
- Esben Haabendal
- Etienne Cordonnier
- Fabio Estevam
- Felix Nilsson
- Florian Amstutz
- Gassner, Tobias.ext
- Gauthier HADERER
- Guðni Már Gilbert
- Harish Sadineni
- Heiko Thole
- Het Patel
- Hongxu Jia
- Igor Opaniuk
- Intaek Hwang
- Iskander Amara
- Jaeyoon Jung
- Jan Vermaete
- Jasper Orschulko
- Joe Slater
- Johannes Schneider
- John Ripple
- Jonas Gorski
- Jonas Munsin
- Jonathan GUILLOT
- Jon Mason
- Jookia
- Jordan Crouse
- Jörg Sommer
- Jose Quaresma
- Joshua Watt
- Julien Stephan
- Kai Kang
- Kari Sivonen
- Khem Raj
- Kirill Yatsenko
- Konrad Weihmann
- Lee Chee Yang
- Lei Maohui
- Leon Anavi
- Leonard Göhrs
- Louis Rannou
- Marc Ferland
- Marcus Folkesson
- Marek Vasut
- Mark Hatle
- Markus Volk
- Marlon Rodriguez Garcia
- Marta Rybczynska
- Martin Hundebøll
- Martin Jansa
- Matthew Bullock
- Matthias Pritschet
- Maxin B. John
- Michael Glembotzki
- Michael Haener
- Michael Halstead
- Michael Opdenacker
- Michal Sieron
- Mikko Rapeli
- Mingli Yu
- Naveen Saini
- Niko Mauno
- Ninette Adhikari
- Noe Galea
- Ola x Nilsson
- Oleksandr Hnatiuk
- Otavio Salvador
- Patrick Wicki
- Paul Barker
- Paul Eggleton
- Paul Gerber
- Pedro Ferreira
- Peter Kjellerstedt
- Peter Marko
- Philip Lorenz
- Poonam Jadhav
- Primoz Fiser
- Quentin Schulz
- Ralph Siemsen
- Rasmus Villemoes
- Ricardo Simoes
- Richard Purdie
- Robert Joslyn
- Robert Kovacsics
- Robert Yang
- Ross Burton
- Rudolf J Streif
- Ryan Eatmon
- Sabeeh Khan
- Sakib Sajal
- Samantha Jalabert
- Siddharth Doshi
- simit.ghane
- Simone Weiß
- Soumya Sambu
- Sreejith Ravi
- Stefan Mueller-Klieser
- Sundeep KOKKONDA
- Sven Schwermer
- Teresa Remmet
- Theodore A. Roth
- Thomas Perrot
- Tim Orling
- Tom Hochstein
- Trevor Gamblin
- Troels Dalsgaard Hoffmeyer
- Tronje Krabbe
- Ulrich Ölmann
- Victor Kamensky
- Vijay Anusuri
- Vincent Kriek
- Vivek Puar
- Wadim Egorov
- Wang Mingyu
- Weisser, Pascal.ext
- Willy Tu
- Xiangyu Chen
- Yang-Mark Zhang
- Yash Shinde
- Yi Zhao
- Yoann Congal
- Yogita Urade
- Yuri D'Elia
- Zahir Hussain
- Zev Weiss
- Zoltan Boszormenyi


Repositories / Downloads for Yocto-5.1
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
