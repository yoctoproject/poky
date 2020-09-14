.. SPDX-License-Identifier: CC-BY-2.0-UK

******************************************
Migrating to a Newer Yocto Project Release
******************************************

This chapter provides information you can use to migrate work to a newer
Yocto Project release. You can find the same information in the release
notes for a given release.

General Migration Considerations
================================

Some considerations are not tied to a specific Yocto Project release.
This section presents information you should consider when migrating to
any new Yocto Project release.

-  *Dealing with Customized Recipes*:

   Issues could arise if you take
   older recipes that contain customizations and simply copy them
   forward expecting them to work after you migrate to new Yocto Project
   metadata. For example, suppose you have a recipe in your layer that
   is a customized version of a core recipe copied from the earlier
   release, rather than through the use of an append file. When you
   migrate to a newer version of Yocto Project, the metadata (e.g.
   perhaps an include file used by the recipe) could have changed in a
   way that would break the build. Say, for example, a function is
   removed from an include file and the customized recipe tries to call
   that function.

   You could "forward-port" all your customizations in your recipe so
   that everything works for the new release. However, this is not the
   optimal solution as you would have to repeat this process with each
   new release if changes occur that give rise to problems.

   The better solution (where practical) is to use append files
   (``*.bbappend``) to capture any customizations you want to make to a
   recipe. Doing so, isolates your changes from the main recipe making
   them much more manageable. However, sometimes it is not practical to
   use an append file. A good example of this is when introducing a
   newer or older version of a recipe in another layer.

-  *Updating Append Files*:

   Since append files generally only contain
   your customizations, they often do not need to be adjusted for new
   releases. However, if the ``.bbappend`` file is specific to a
   particular version of the recipe (i.e. its name does not use the %
   wildcard) and the version of the recipe to which it is appending has
   changed, then you will at a minimum need to rename the append file to
   match the name of the recipe file. A mismatch between an append file
   and its corresponding recipe file (``.bb``) will trigger an error
   during parsing.

   Depending on the type of customization the append file applies, other
   incompatibilities might occur when you upgrade. For example, if your
   append file applies a patch and the recipe to which it is appending
   is updated to a newer version, the patch might no longer apply. If
   this is the case and assuming the patch is still needed, you must
   modify the patch file so that it does apply.

Moving to the Yocto Project 1.3 Release
=======================================

This section provides migration information for moving to the Yocto
Project 1.3 Release from the prior release.

.. _1.3-local-configuration:

Local Configuration
-------------------

Differences include changes for
:term:`SSTATE_MIRRORS` and ``bblayers.conf``.

.. _migration-1.3-sstate-mirrors:

SSTATE_MIRRORS
~~~~~~~~~~~~~~

The shared state cache (sstate-cache), as pointed to by
:term:`SSTATE_DIR`, by default now has two-character
subdirectories to prevent issues arising from too many files in the same
directory. Also, native sstate-cache packages, which are built to run on
the host system, will go into a subdirectory named using the distro ID
string. If you copy the newly structured sstate-cache to a mirror
location (either local or remote) and then point to it in
:term:`SSTATE_MIRRORS`, you need to append "PATH"
to the end of the mirror URL so that the path used by BitBake before the
mirror substitution is appended to the path used to access the mirror.
Here is an example: ::

   SSTATE_MIRRORS = "file://.* http://someserver.tld/share/sstate/PATH"

.. _migration-1.3-bblayers-conf:

bblayers.conf
~~~~~~~~~~~~~

The ``meta-yocto`` layer consists of two parts that correspond to the
Poky reference distribution and the reference hardware Board Support
Packages (BSPs), respectively: ``meta-yocto`` and ``meta-yocto-bsp``.
When running BitBake for the first time after upgrading, your
``conf/bblayers.conf`` file will be updated to handle this change and
you will be asked to re-run or restart for the changes to take effect.

.. _1.3-recipes:

Recipes
-------

Differences include changes for the following:

.. _migration-1.3-python-function-whitespace:

Python Function Whitespace
~~~~~~~~~~~~~~~~~~~~~~~~~~

All Python functions must now use four spaces for indentation.
Previously, an inconsistent mix of spaces and tabs existed, which made
extending these functions using ``_append`` or ``_prepend`` complicated
given that Python treats whitespace as syntactically significant. If you
are defining or extending any Python functions (e.g.
``populate_packages``, ``do_unpack``, ``do_patch`` and so forth) in
custom recipes or classes, you need to ensure you are using consistent
four-space indentation.

.. _migration-1.3-proto=-in-src-uri:

proto= in SRC_URI
~~~~~~~~~~~~~~~~~

Any use of ``proto=`` in :term:`SRC_URI` needs to be
changed to ``protocol=``. In particular, this applies to the following
URIs:

-  ``svn://``

-  ``bzr://``

-  ``hg://``

-  ``osc://``

Other URIs were already using ``protocol=``. This change improves
consistency.

.. _migration-1.3-nativesdk:

nativesdk
~~~~~~~~~

The suffix ``nativesdk`` is now implemented as a prefix, which
simplifies a lot of the packaging code for ``nativesdk`` recipes. All
custom ``nativesdk`` recipes, which are relocatable packages that are
native to :term:`SDK_ARCH`, and any references need to
be updated to use ``nativesdk-*`` instead of ``*-nativesdk``.

.. _migration-1.3-task-recipes:

Task Recipes
~~~~~~~~~~~~

"Task" recipes are now known as "Package groups" and have been renamed
from ``task-*.bb`` to ``packagegroup-*.bb``. Existing references to the
previous ``task-*`` names should work in most cases as there is an
automatic upgrade path for most packages. However, you should update
references in your own recipes and configurations as they could be
removed in future releases. You should also rename any custom ``task-*``
recipes to ``packagegroup-*``, and change them to inherit
``packagegroup`` instead of ``task``, as well as taking the opportunity
to remove anything now handled by ``packagegroup.bbclass``, such as
providing ``-dev`` and ``-dbg`` packages, setting
:term:`LIC_FILES_CHKSUM`, and so forth. See the
":ref:`packagegroup.bbclass <ref-classes-packagegroup>`" section for
further details.

.. _migration-1.3-image-features:

IMAGE_FEATURES
~~~~~~~~~~~~~~

Image recipes that previously included "apps-console-core" in
:term:`IMAGE_FEATURES` should now include "splash"
instead to enable the boot-up splash screen. Retaining
"apps-console-core" will still include the splash screen but generates a
warning. The "apps-x11-core" and "apps-x11-games" ``IMAGE_FEATURES``
features have been removed.

.. _migration-1.3-removed-recipes:

Removed Recipes
~~~~~~~~~~~~~~~

The following recipes have been removed. For most of them, it is
unlikely that you would have any references to them in your own
:term:`Metadata`. However, you should check your metadata
against this list to be sure:

-  ``libx11-trim``: Replaced by ``libx11``, which has a negligible
   size difference with modern Xorg.

-  ``xserver-xorg-lite``: Use ``xserver-xorg``, which has a negligible
   size difference when DRI and GLX modules are not installed.

-  ``xserver-kdrive``: Effectively unmaintained for many years.

-  ``mesa-xlib``: No longer serves any purpose.

-  ``galago``: Replaced by telepathy.

-  ``gail``: Functionality was integrated into GTK+ 2.13.

-  ``eggdbus``: No longer needed.

-  ``gcc-*-intermediate``: The build has been restructured to avoid
   the need for this step.

-  ``libgsmd``: Unmaintained for many years. Functionality now
   provided by ``ofono`` instead.

-  *contacts, dates, tasks, eds-tools*: Largely unmaintained PIM
   application suite. It has been moved to ``meta-gnome`` in
   ``meta-openembedded``.

In addition to the previously listed changes, the ``meta-demoapps``
directory has also been removed because the recipes in it were not being
maintained and many had become obsolete or broken. Additionally, these
recipes were not parsed in the default configuration. Many of these
recipes are already provided in an updated and maintained form within
the OpenEmbedded community layers such as ``meta-oe`` and
``meta-gnome``. For the remainder, you can now find them in the
``meta-extras`` repository, which is in the
:yocto_git:`Source Repositories <>` at
http://git.yoctoproject.org/cgit/cgit.cgi/meta-extras/.

.. _1.3-linux-kernel-naming:

Linux Kernel Naming
-------------------

The naming scheme for kernel output binaries has been changed to now
include :term:`PE` as part of the filename:
::

   KERNEL_IMAGE_BASE_NAME ?= "${KERNEL_IMAGETYPE}-${PE}-${PV}-${PR}-${MACHINE}-${DATETIME}"

Because the ``PE`` variable is not set by default, these binary files
could result with names that include two dash characters. Here is an
example: ::

   bzImage--3.10.9+git0+cd502a8814_7144bcc4b8-r0-qemux86-64-20130830085431.bin

Moving to the Yocto Project 1.4 Release
=======================================

This section provides migration information for moving to the Yocto
Project 1.4 Release from the prior release.

.. _migration-1.4-bitbake:

BitBake
-------

Differences include the following:

-  *Comment Continuation:* If a comment ends with a line continuation
   (\) character, then the next line must also be a comment. Any
   instance where this is not the case, now triggers a warning. You must
   either remove the continuation character, or be sure the next line is
   a comment.

-  *Package Name Overrides:* The runtime package specific variables
   :term:`RDEPENDS`,
   :term:`RRECOMMENDS`,
   :term:`RSUGGESTS`,
   :term:`RPROVIDES`,
   :term:`RCONFLICTS`,
   :term:`RREPLACES`, :term:`FILES`,
   :term:`ALLOW_EMPTY`, and the pre, post, install,
   and uninstall script functions ``pkg_preinst``, ``pkg_postinst``,
   ``pkg_prerm``, and ``pkg_postrm`` should always have a package name
   override. For example, use ``RDEPENDS_${PN}`` for the main package
   instead of ``RDEPENDS``. BitBake uses more strict checks when it
   parses recipes.

.. _migration-1.4-build-behavior:

Build Behavior
--------------

Differences include the following:

-  *Shared State Code:* The shared state code has been optimized to
   avoid running unnecessary tasks. For example, the following no longer
   populates the target sysroot since that is not necessary:
   ::

      $ bitbake -c rootfs some-image

   Instead, the system just needs to extract the
   output package contents, re-create the packages, and construct the
   root filesystem. This change is unlikely to cause any problems unless
   you have missing declared dependencies.

-  *Scanning Directory Names:* When scanning for files in
   :term:`SRC_URI`, the build system now uses
   :term:`FILESOVERRIDES` instead of
   :term:`OVERRIDES` for the directory names. In
   general, the values previously in ``OVERRIDES`` are now in
   ``FILESOVERRIDES`` as well. However, if you relied upon an additional
   value you previously added to ``OVERRIDES``, you might now need to
   add it to ``FILESOVERRIDES`` unless you are already adding it through
   the :term:`MACHINEOVERRIDES` or
   :term:`DISTROOVERRIDES` variables, as
   appropriate. For more related changes, see the
   "`Variables <#migration-1.4-variables>`__" section.

.. _migration-1.4-proxies-and-fetching-source:

Proxies and Fetching Source
---------------------------

A new ``oe-git-proxy`` script has been added to replace previous methods
of handling proxies and fetching source from Git. See the
``meta-yocto/conf/site.conf.sample`` file for information on how to use
this script.

.. _migration-1.4-custom-interfaces-file-netbase-change:

Custom Interfaces File (netbase change)
---------------------------------------

If you have created your own custom ``etc/network/interfaces`` file by
creating an append file for the ``netbase`` recipe, you now need to
create an append file for the ``init-ifupdown`` recipe instead, which
you can find in the :term:`Source Directory` at
``meta/recipes-core/init-ifupdown``. For information on how to use
append files, see the
":ref:`dev-manual/dev-manual-common-tasks:using .bbappend files in your layer`"
section in the Yocto Project Development Tasks Manual.

.. _migration-1.4-remote-debugging:

Remote Debugging
----------------

Support for remote debugging with the Eclipse IDE is now separated into
an image feature (``eclipse-debug``) that corresponds to the
``packagegroup-core-eclipse-debug`` package group. Previously, the
debugging feature was included through the ``tools-debug`` image
feature, which corresponds to the ``packagegroup-core-tools-debug``
package group.

.. _migration-1.4-variables:

Variables
---------

The following variables have changed:

-  ``SANITY_TESTED_DISTROS``: This variable now uses a distribution
   ID, which is composed of the host distributor ID followed by the
   release. Previously,
   :term:`SANITY_TESTED_DISTROS` was
   composed of the description field. For example, "Ubuntu 12.10"
   becomes "Ubuntu-12.10". You do not need to worry about this change if
   you are not specifically setting this variable, or if you are
   specifically setting it to "".

-  ``SRC_URI``: The ``${``\ :term:`PN`\ ``}``,
   ``${``\ :term:`PF`\ ``}``,
   ``${``\ :term:`P`\ ``}``, and ``FILE_DIRNAME`` directories
   have been dropped from the default value of the
   :term:`FILESPATH` variable, which is used as the
   search path for finding files referred to in
   :term:`SRC_URI`. If you have a recipe that relied upon
   these directories, which would be unusual, then you will need to add
   the appropriate paths within the recipe or, alternatively, rearrange
   the files. The most common locations are still covered by ``${BP}``,
   ``${BPN}``, and "files", which all remain in the default value of
   :term:`FILESPATH`.

.. _migration-target-package-management-with-rpm:

Target Package Management with RPM
----------------------------------

If runtime package management is enabled and the RPM backend is
selected, Smart is now installed for package download, dependency
resolution, and upgrades instead of Zypper. For more information on how
to use Smart, run the following command on the target:
::

   smart --help

.. _migration-1.4-recipes-moved:

Recipes Moved
-------------

The following recipes were moved from their previous locations because
they are no longer used by anything in the OpenEmbedded-Core:

-  ``clutter-box2d``: Now resides in the ``meta-oe`` layer.

-  ``evolution-data-server``: Now resides in the ``meta-gnome`` layer.

-  ``gthumb``: Now resides in the ``meta-gnome`` layer.

-  ``gtkhtml2``: Now resides in the ``meta-oe`` layer.

-  ``gupnp``: Now resides in the ``meta-multimedia`` layer.

-  ``gypsy``: Now resides in the ``meta-oe`` layer.

-  ``libcanberra``: Now resides in the ``meta-gnome`` layer.

-  ``libgdata``: Now resides in the ``meta-gnome`` layer.

-  ``libmusicbrainz``: Now resides in the ``meta-multimedia`` layer.

-  ``metacity``: Now resides in the ``meta-gnome`` layer.

-  ``polkit``: Now resides in the ``meta-oe`` layer.

-  ``zeroconf``: Now resides in the ``meta-networking`` layer.

.. _migration-1.4-removals-and-renames:

Removals and Renames
--------------------

The following list shows what has been removed or renamed:

-  ``evieext``: Removed because it has been removed from ``xserver``
   since 2008.

-  *Gtk+ DirectFB:* Removed support because upstream Gtk+ no longer
   supports it as of version 2.18.

-  ``libxfontcache / xfontcacheproto``: Removed because they were
   removed from the Xorg server in 2008.

-  ``libxp / libxprintapputil / libxprintutil / printproto``: Removed
   because the XPrint server was removed from Xorg in 2008.

-  ``libxtrap / xtrapproto``: Removed because their functionality was
   broken upstream.

-  *linux-yocto 3.0 kernel:* Removed with linux-yocto 3.8 kernel being
   added. The linux-yocto 3.2 and linux-yocto 3.4 kernels remain as part
   of the release.

-  ``lsbsetup``: Removed with functionality now provided by
   ``lsbtest``.

-  ``matchbox-stroke``: Removed because it was never more than a
   proof-of-concept.

-  ``matchbox-wm-2 / matchbox-theme-sato-2``: Removed because they are
   not maintained. However, ``matchbox-wm`` and ``matchbox-theme-sato``
   are still provided.

-  ``mesa-dri``: Renamed to ``mesa``.

-  ``mesa-xlib``: Removed because it was no longer useful.

-  ``mutter``: Removed because nothing ever uses it and the recipe is
   very old.

-  ``orinoco-conf``: Removed because it has become obsolete.

-  ``update-modules``: Removed because it is no longer used. The
   kernel module ``postinstall`` and ``postrm`` scripts can now do the
   same task without the use of this script.

-  ``web``: Removed because it is not maintained. Superseded by
   ``web-webkit``.

-  ``xf86bigfontproto``: Removed because upstream it has been disabled
   by default since 2007. Nothing uses ``xf86bigfontproto``.

-  ``xf86rushproto``: Removed because its dependency in ``xserver``
   was spurious and it was removed in 2005.

-  ``zypper / libzypp / sat-solver``: Removed and been functionally
   replaced with Smart (``python-smartpm``) when RPM packaging is used
   and package management is enabled on the target.

Moving to the Yocto Project 1.5 Release
=======================================

This section provides migration information for moving to the Yocto
Project 1.5 Release from the prior release.

.. _migration-1.5-host-dependency-changes:

Host Dependency Changes
-----------------------

The OpenEmbedded build system now has some additional requirements on
the host system:

-  Python 2.7.3+

-  Tar 1.24+

-  Git 1.7.8+

-  Patched version of Make if you are using 3.82. Most distributions
   that provide Make 3.82 use the patched version.

If the Linux distribution you are using on your build host does not
provide packages for these, you can install and use the Buildtools
tarball, which provides an SDK-like environment containing them.

For more information on this requirement, see the "`Required Git, tar,
Python and gcc Versions <#required-git-tar-python-and-gcc-versions>`__"
section.

.. _migration-1.5-atom-pc-bsp:

``atom-pc`` Board Support Package (BSP)
---------------------------------------

The ``atom-pc`` hardware reference BSP has been replaced by a
``genericx86`` BSP. This BSP is not necessarily guaranteed to work on
all x86 hardware, but it will run on a wider range of systems than the
``atom-pc`` did.

.. note::

   Additionally, a
   genericx86-64
   BSP has been added for 64-bit Atom systems.

.. _migration-1.5-bitbake:

BitBake
-------

The following changes have been made that relate to BitBake:

-  BitBake now supports a ``_remove`` operator. The addition of this
   operator means you will have to rename any items in recipe space
   (functions, variables) whose names currently contain ``_remove_`` or
   end with ``_remove`` to avoid unexpected behavior.

-  BitBake's global method pool has been removed. This method is not
   particularly useful and led to clashes between recipes containing
   functions that had the same name.

-  The "none" server backend has been removed. The "process" server
   backend has been serving well as the default for a long time now.

-  The ``bitbake-runtask`` script has been removed.

-  ``${``\ :term:`P`\ ``}`` and
   ``${``\ :term:`PF`\ ``}`` are no longer added to
   :term:`PROVIDES` by default in ``bitbake.conf``.
   These version-specific ``PROVIDES`` items were seldom used.
   Attempting to use them could result in two versions being built
   simultaneously rather than just one version due to the way BitBake
   resolves dependencies.

.. _migration-1.5-qa-warnings:

QA Warnings
-----------

The following changes have been made to the package QA checks:

-  If you have customized :term:`ERROR_QA` or
   :term:`WARN_QA` values in your configuration, check
   that they contain all of the issues that you wish to be reported.
   Previous Yocto Project versions contained a bug that meant that any
   item not mentioned in ``ERROR_QA`` or ``WARN_QA`` would be treated as
   a warning. Consequently, several important items were not already in
   the default value of ``WARN_QA``. All of the possible QA checks are
   now documented in the ":ref:`insane.bbclass <ref-classes-insane>`"
   section.

-  An additional QA check has been added to check if
   ``/usr/share/info/dir`` is being installed. Your recipe should delete
   this file within :ref:`ref-tasks-install` if "make
   install" is installing it.

-  If you are using the buildhistory class, the check for the package
   version going backwards is now controlled using a standard QA check.
   Thus, if you have customized your ``ERROR_QA`` or ``WARN_QA`` values
   and still wish to have this check performed, you should add
   "version-going-backwards" to your value for one or the other
   variables depending on how you wish it to be handled. See the
   documented QA checks in the
   ":ref:`insane.bbclass <ref-classes-insane>`" section.

.. _migration-1.5-directory-layout-changes:

Directory Layout Changes
------------------------

The following directory changes exist:

-  Output SDK installer files are now named to include the image name
   and tuning architecture through the :term:`SDK_NAME`
   variable.

-  Images and related files are now installed into a directory that is
   specific to the machine, instead of a parent directory containing
   output files for multiple machines. The
   :term:`DEPLOY_DIR_IMAGE` variable continues
   to point to the directory containing images for the current
   :term:`MACHINE` and should be used anywhere there is a
   need to refer to this directory. The ``runqemu`` script now uses this
   variable to find images and kernel binaries and will use BitBake to
   determine the directory. Alternatively, you can set the
   ``DEPLOY_DIR_IMAGE`` variable in the external environment.

-  When buildhistory is enabled, its output is now written under the
   :term:`Build Directory` rather than
   :term:`TMPDIR`. Doing so makes it easier to delete
   ``TMPDIR`` and preserve the build history. Additionally, data for
   produced SDKs is now split by :term:`IMAGE_NAME`.

-  The ``pkgdata`` directory produced as part of the packaging process
   has been collapsed into a single machine-specific directory. This
   directory is located under ``sysroots`` and uses a machine-specific
   name (i.e. ``tmp/sysroots/machine/pkgdata``).

.. _migration-1.5-shortened-git-srcrev-values:

Shortened Git ``SRCREV`` Values
-------------------------------

BitBake will now shorten revisions from Git repositories from the normal
40 characters down to 10 characters within :term:`SRCPV`
for improved usability in path and file names. This change should be
safe within contexts where these revisions are used because the chances
of spatially close collisions is very low. Distant collisions are not a
major issue in the way the values are used.

.. _migration-1.5-image-features:

``IMAGE_FEATURES``
------------------

The following changes have been made that relate to
:term:`IMAGE_FEATURES`:

-  The value of ``IMAGE_FEATURES`` is now validated to ensure invalid
   feature items are not added. Some users mistakenly add package names
   to this variable instead of using
   :term:`IMAGE_INSTALL` in order to have the
   package added to the image, which does not work. This change is
   intended to catch those kinds of situations. Valid ``IMAGE_FEATURES``
   are drawn from ``PACKAGE_GROUP`` definitions,
   :term:`COMPLEMENTARY_GLOB` and a new
   "validitems" varflag on ``IMAGE_FEATURES``. The "validitems" varflag
   change allows additional features to be added if they are not
   provided using the previous two mechanisms.

-  The previously deprecated "apps-console-core" ``IMAGE_FEATURES`` item
   is no longer supported. Add "splash" to ``IMAGE_FEATURES`` if you
   wish to have the splash screen enabled, since this is all that
   apps-console-core was doing.

.. _migration-1.5-run:

``/run``
--------

The ``/run`` directory from the Filesystem Hierarchy Standard 3.0 has
been introduced. You can find some of the implications for this change
`here <http://cgit.openembedded.org/openembedded-core/commit/?id=0e326280a15b0f2c4ef2ef4ec441f63f55b75873>`__.
The change also means that recipes that install files to ``/var/run``
must be changed. You can find a guide on how to make these changes
`here <http://permalink.gmane.org/gmane.comp.handhelds.openembedded/58530>`__.

.. _migration-1.5-removal-of-package-manager-database-within-image-recipes:

Removal of Package Manager Database Within Image Recipes
--------------------------------------------------------

The image ``core-image-minimal`` no longer adds
``remove_packaging_data_files`` to
:term:`ROOTFS_POSTPROCESS_COMMAND`.
This addition is now handled automatically when "package-management" is
not in :term:`IMAGE_FEATURES`. If you have custom
image recipes that make this addition, you should remove the lines, as
they are not needed and might interfere with correct operation of
postinstall scripts.

.. _migration-1.5-images-now-rebuild-only-on-changes-instead-of-every-time:

Images Now Rebuild Only on Changes Instead of Every Time
--------------------------------------------------------

The :ref:`ref-tasks-rootfs` and other related image
construction tasks are no longer marked as "nostamp". Consequently, they
will only be re-executed when their inputs have changed. Previous
versions of the OpenEmbedded build system always rebuilt the image when
requested rather when necessary.

.. _migration-1.5-task-recipes:

Task Recipes
------------

The previously deprecated ``task.bbclass`` has now been dropped. For
recipes that previously inherited from this class, you should rename
them from ``task-*`` to ``packagegroup-*`` and inherit packagegroup
instead.

For more information, see the
":ref:`packagegroup.bbclass <ref-classes-packagegroup>`" section.

.. _migration-1.5-busybox:

BusyBox
-------

By default, we now split BusyBox into two binaries: one that is suid
root for those components that need it, and another for the rest of the
components. Splitting BusyBox allows for optimization that eliminates
the ``tinylogin`` recipe as recommended by upstream. You can disable
this split by setting
:term:`BUSYBOX_SPLIT_SUID` to "0".

.. _migration-1.5-automated-image-testing:

Automated Image Testing
-----------------------

A new automated image testing framework has been added through the
:ref:`testimage.bbclass <ref-classes-testimage*>` class. This
framework replaces the older ``imagetest-qemu`` framework.

You can learn more about performing automated image tests in the
":ref:`dev-manual/dev-manual-common-tasks:performing automated runtime testing`"
section in the Yocto Project Development Tasks Manual.

.. _migration-1.5-build-history:

Build History
-------------

Following are changes to Build History:

-  Installed package sizes: ``installed-package-sizes.txt`` for an image
   now records the size of the files installed by each package instead
   of the size of each compressed package archive file.

-  The dependency graphs (``depends*.dot``) now use the actual package
   names instead of replacing dashes, dots and plus signs with
   underscores.

-  The ``buildhistory-diff`` and ``buildhistory-collect-srcrevs``
   utilities have improved command-line handling. Use the ``--help``
   option for each utility for more information on the new syntax.

For more information on Build History, see the
":ref:`dev-manual/dev-manual-common-tasks:maintaining build output quality`"
section in the Yocto Project Development Tasks Manual.

.. _migration-1.5-udev:

``udev``
--------

Following are changes to ``udev``:

-  ``udev`` no longer brings in ``udev-extraconf`` automatically through
   :term:`RRECOMMENDS`, since this was originally
   intended to be optional. If you need the extra rules, then add
   ``udev-extraconf`` to your image.

-  ``udev`` no longer brings in ``pciutils-ids`` or ``usbutils-ids``
   through ``RRECOMMENDS``. These are not needed by ``udev`` itself and
   removing them saves around 350KB.

.. _migration-1.5-removed-renamed-recipes:

Removed and Renamed Recipes
---------------------------

-  The ``linux-yocto`` 3.2 kernel has been removed.

-  ``libtool-nativesdk`` has been renamed to ``nativesdk-libtool``.

-  ``tinylogin`` has been removed. It has been replaced by a suid
   portion of Busybox. See the "`BusyBox <#migration-1.5-busybox>`__"
   section for more information.

-  ``external-python-tarball`` has been renamed to
   ``buildtools-tarball``.

-  ``web-webkit`` has been removed. It has been functionally replaced by
   ``midori``.

-  ``imake`` has been removed. It is no longer needed by any other
   recipe.

-  ``transfig-native`` has been removed. It is no longer needed by any
   other recipe.

-  ``anjuta-remote-run`` has been removed. Anjuta IDE integration has
   not been officially supported for several releases.

.. _migration-1.5-other-changes:

Other Changes
-------------

Following is a list of short entries describing other changes:

-  ``run-postinsts``: Make this generic.

-  ``base-files``: Remove the unnecessary ``media/``\ xxx directories.

-  ``alsa-state``: Provide an empty ``asound.conf`` by default.

-  ``classes/image``: Ensure
   :term:`BAD_RECOMMENDATIONS` supports
   pre-renamed package names.

-  ``classes/rootfs_rpm``: Implement ``BAD_RECOMMENDATIONS`` for RPM.

-  ``systemd``: Remove ``systemd_unitdir`` if ``systemd`` is not in
   :term:`DISTRO_FEATURES`.

-  ``systemd``: Remove ``init.d`` dir if ``systemd`` unit file is
   present and ``sysvinit`` is not a distro feature.

-  ``libpam``: Deny all services for the ``OTHER`` entries.

-  ``image.bbclass``: Move ``runtime_mapping_rename`` to avoid conflict
   with ``multilib``. See
   `YOCTO #4993 <https://bugzilla.yoctoproject.org/show_bug.cgi?id=4993>`_
   in Bugzilla for more information.

-  ``linux-dtb``: Use kernel build system to generate the ``dtb`` files.

-  ``kern-tools``: Switch from guilt to new ``kgit-s2q`` tool.

Moving to the Yocto Project 1.6 Release
=======================================

This section provides migration information for moving to the Yocto
Project 1.6 Release from the prior release.

.. _migration-1.6-archiver-class:

``archiver`` Class
------------------

The :ref:`archiver <ref-classes-archiver>` class has been rewritten
and its configuration has been simplified. For more details on the
source archiver, see the
":ref:`dev-manual/dev-manual-common-tasks:maintaining open source license compliance during your product's lifecycle`"
section in the Yocto Project Development Tasks Manual.

.. _migration-1.6-packaging-changes:

Packaging Changes
-----------------

The following packaging changes have been made:

-  The ``binutils`` recipe no longer produces a ``binutils-symlinks``
   package. ``update-alternatives`` is now used to handle the preferred
   ``binutils`` variant on the target instead.

-  The tc (traffic control) utilities have been split out of the main
   ``iproute2`` package and put into the ``iproute2-tc`` package.

-  The ``gtk-engines`` schemas have been moved to a dedicated
   ``gtk-engines-schemas`` package.

-  The ``armv7a`` with thumb package architecture suffix has changed.
   The suffix for these packages with the thumb optimization enabled is
   "t2" as it should be. Use of this suffix was not the case in the 1.5
   release. Architecture names will change within package feeds as a
   result.

.. _migration-1.6-bitbake:

BitBake
-------

The following changes have been made to :term:`BitBake`.

.. _migration-1.6-matching-branch-requirement-for-git-fetching:

Matching Branch Requirement for Git Fetching
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

When fetching source from a Git repository using
:term:`SRC_URI`, BitBake will now validate the
:term:`SRCREV` value against the branch. You can specify
the branch using the following form: SRC_URI =
"git://server.name/repository;branch=branchname" If you do not specify a
branch, BitBake looks in the default "master" branch.

Alternatively, if you need to bypass this check (e.g. if you are
fetching a revision corresponding to a tag that is not on any branch),
you can add ";nobranch=1" to the end of the URL within ``SRC_URI``.

.. _migration-1.6-bitbake-deps:

Python Definition substitutions
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BitBake had some previously deprecated Python definitions within its
``bb`` module removed. You should use their sub-module counterparts
instead:

-  ``bb.MalformedUrl``: Use ``bb.fetch.MalformedUrl``.

-  ``bb.encodeurl``: Use ``bb.fetch.encodeurl``.

-  ``bb.decodeurl``: Use ``bb.fetch.decodeurl``

-  ``bb.mkdirhier``: Use ``bb.utils.mkdirhier``.

-  ``bb.movefile``: Use ``bb.utils.movefile``.

-  ``bb.copyfile``: Use ``bb.utils.copyfile``.

-  ``bb.which``: Use ``bb.utils.which``.

-  ``bb.vercmp_string``: Use ``bb.utils.vercmp_string``.

-  ``bb.vercmp``: Use ``bb.utils.vercmp``.

.. _migration-1.6-bitbake-fetcher:

SVK Fetcher
~~~~~~~~~~~

The SVK fetcher has been removed from BitBake.

.. _migration-1.6-bitbake-console-output:

Console Output Error Redirection
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The BitBake console UI will now output errors to ``stderr`` instead of
``stdout``. Consequently, if you are piping or redirecting the output of
``bitbake`` to somewhere else, and you wish to retain the errors, you
will need to add ``2>&1`` (or something similar) to the end of your
``bitbake`` command line.

.. _migration-1.6-task-taskname-overrides:

``task-``\ taskname Overrides
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``task-``\ taskname overrides have been adjusted so that tasks whose
names contain underscores have the underscores replaced by hyphens for
the override so that they now function properly. For example, the task
override for :ref:`ref-tasks-populate_sdk` is
``task-populate-sdk``.

.. _migration-1.6-variable-changes:

Changes to Variables
--------------------

The following variables have changed. For information on the
OpenEmbedded build system variables, see the "`Variables
Glossary <#ref-variables-glos>`__" Chapter.

.. _migration-1.6-variable-changes-TMPDIR:

``TMPDIR``
~~~~~~~~~~

:term:`TMPDIR` can no longer be on an NFS mount. NFS does
not offer full POSIX locking and inode consistency and can cause
unexpected issues if used to store ``TMPDIR``.

The check for this occurs on startup. If ``TMPDIR`` is detected on an
NFS mount, an error occurs.

.. _migration-1.6-variable-changes-PRINC:

``PRINC``
~~~~~~~~~

The ``PRINC`` variable has been deprecated and triggers a warning if
detected during a build. For :term:`PR` increments on changes,
use the PR service instead. You can find out more about this service in
the ":ref:`dev-manual/dev-manual-common-tasks:working with a pr service`"
section in the Yocto Project Development Tasks Manual.

.. _migration-1.6-variable-changes-IMAGE_TYPES:

``IMAGE_TYPES``
~~~~~~~~~~~~~~~

The "sum.jffs2" option for :term:`IMAGE_TYPES` has
been replaced by the "jffs2.sum" option, which fits the processing
order.

.. _migration-1.6-variable-changes-COPY_LIC_MANIFEST:

``COPY_LIC_MANIFEST``
~~~~~~~~~~~~~~~~~~~~~

The :term:`COPY_LIC_MANIFEST` variable must now
be set to "1" rather than any value in order to enable it.

.. _migration-1.6-variable-changes-COPY_LIC_DIRS:

``COPY_LIC_DIRS``
~~~~~~~~~~~~~~~~~

The :term:`COPY_LIC_DIRS` variable must now be set
to "1" rather than any value in order to enable it.

.. _migration-1.6-variable-changes-PACKAGE_GROUP:

``PACKAGE_GROUP``
~~~~~~~~~~~~~~~~~

The ``PACKAGE_GROUP`` variable has been renamed to
:term:`FEATURE_PACKAGES` to more accurately
reflect its purpose. You can still use ``PACKAGE_GROUP`` but the
OpenEmbedded build system produces a warning message when it encounters
the variable.

.. _migration-1.6-variable-changes-variable-entry-behavior:

Preprocess and Post Process Command Variable Behavior
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The following variables now expect a semicolon separated list of
functions to call and not arbitrary shell commands:

  - :term:`ROOTFS_PREPROCESS_COMMAND`
  - :term:`ROOTFS_POSTPROCESS_COMMAND`
  - :term:`SDK_POSTPROCESS_COMMAND`
  - :term:`POPULATE_SDK_POST_TARGET_COMMAND`
  - :term:`POPULATE_SDK_POST_HOST_COMMAND`
  - :term:`IMAGE_POSTPROCESS_COMMAND`
  - :term:`IMAGE_PREPROCESS_COMMAND`
  - :term:`ROOTFS_POSTUNINSTALL_COMMAND`
  - :term:`ROOTFS_POSTINSTALL_COMMAND`

For
migration purposes, you can simply wrap shell commands in a shell
function and then call the function. Here is an example: ::

   my_postprocess_function() {
      echo "hello" > ${IMAGE_ROOTFS}/hello.txt
   }
   ROOTFS_POSTPROCESS_COMMAND += "my_postprocess_function; "

.. _migration-1.6-package-test-ptest:

Package Test (ptest)
--------------------

Package Tests (ptest) are built but not installed by default. For
information on using Package Tests, see the
":ref:`dev-manual/dev-manual-common-tasks:testing packages with ptest`"
section in the Yocto Project Development Tasks Manual. For information on the
``ptest`` class, see the ":ref:`ptest.bbclass <ref-classes-ptest>`"
section.

.. _migration-1.6-build-changes:

Build Changes
-------------

Separate build and source directories have been enabled by default for
selected recipes where it is known to work (a whitelist) and for all
recipes that inherit the :ref:`cmake <ref-classes-cmake>` class. In
future releases the :ref:`autotools <ref-classes-autotools>` class
will enable a separate build directory by default as well. Recipes
building Autotools-based software that fails to build with a separate
build directory should be changed to inherit from the
:ref:`autotools-brokensep <ref-classes-autotools>` class instead of
the ``autotools`` or ``autotools_stage``\ classes.

.. _migration-1.6-building-qemu-native:

``qemu-native``
---------------

``qemu-native`` now builds without SDL-based graphical output support by
default. The following additional lines are needed in your
``local.conf`` to enable it:
::

   PACKAGECONFIG_pn-qemu-native = "sdl"
   ASSUME_PROVIDED += "libsdl-native"

.. note::

   The default
   local.conf
   contains these statements. Consequently, if you are building a
   headless system and using a default
   local.conf
   file, you will need comment these two lines out.

.. _migration-1.6-core-image-basic:

``core-image-basic``
--------------------

``core-image-basic`` has been renamed to ``core-image-full-cmdline``.

In addition to ``core-image-basic`` being renamed,
``packagegroup-core-basic`` has been renamed to
``packagegroup-core-full-cmdline`` to match.

.. _migration-1.6-licensing:

Licensing
---------

The top-level ``LICENSE`` file has been changed to better describe the
license of the various components of :term:`OpenEmbedded-Core (OE-Core)`. However,
the licensing itself remains unchanged.

Normally, this change would not cause any side-effects. However, some
recipes point to this file within
:term:`LIC_FILES_CHKSUM` (as
``${COREBASE}/LICENSE``) and thus the accompanying checksum must be
changed from 3f40d7994397109285ec7b81fdeb3b58 to
4d92cd373abda3937c2bc47fbc49d690. A better alternative is to have
``LIC_FILES_CHKSUM`` point to a file describing the license that is
distributed with the source that the recipe is building, if possible,
rather than pointing to ``${COREBASE}/LICENSE``.

.. _migration-1.6-cflags-options:

``CFLAGS`` Options
------------------

The "-fpermissive" option has been removed from the default
:term:`CFLAGS` value. You need to take action on
individual recipes that fail when building with this option. You need to
either patch the recipes to fix the issues reported by the compiler, or
you need to add "-fpermissive" to ``CFLAGS`` in the recipes.

.. _migration-1.6-custom-images:

Custom Image Output Types
-------------------------

Custom image output types, as selected using
:term:`IMAGE_FSTYPES`, must declare their
dependencies on other image types (if any) using a new
:term:`IMAGE_TYPEDEP` variable.

.. _migration-1.6-do-package-write-task:

Tasks
-----

The ``do_package_write`` task has been removed. The task is no longer
needed.

.. _migration-1.6-update-alternatives-provider:

``update-alternative`` Provider
-------------------------------

The default ``update-alternatives`` provider has been changed from
``opkg`` to ``opkg-utils``. This change resolves some troublesome
circular dependencies. The runtime package has also been renamed from
``update-alternatives-cworth`` to ``update-alternatives-opkg``.

.. _migration-1.6-virtclass-overrides:

``virtclass`` Overrides
-----------------------

The ``virtclass`` overrides are now deprecated. Use the equivalent class
overrides instead (e.g. ``virtclass-native`` becomes ``class-native``.)

.. _migration-1.6-removed-renamed-recipes:

Removed and Renamed Recipes
---------------------------

The following recipes have been removed:

-  ``packagegroup-toolset-native`` - This recipe is largely unused.

-  ``linux-yocto-3.8`` - Support for the Linux yocto 3.8 kernel has been
   dropped. Support for the 3.10 and 3.14 kernels have been added with
   the ``linux-yocto-3.10`` and ``linux-yocto-3.14`` recipes.

-  ``ocf-linux`` - This recipe has been functionally replaced using
   ``cryptodev-linux``.

-  ``genext2fs`` - ``genext2fs`` is no longer used by the build system
   and is unmaintained upstream.

-  ``js`` - This provided an ancient version of Mozilla's javascript
   engine that is no longer needed.

-  ``zaurusd`` - The recipe has been moved to the ``meta-handheld``
   layer.

-  ``eglibc 2.17`` - Replaced by the ``eglibc 2.19`` recipe.

-  ``gcc 4.7.2`` - Replaced by the now stable ``gcc 4.8.2``.

-  ``external-sourcery-toolchain`` - this recipe is now maintained in
   the ``meta-sourcery`` layer.

-  ``linux-libc-headers-yocto 3.4+git`` - Now using version 3.10 of the
   ``linux-libc-headers`` by default.

-  ``meta-toolchain-gmae`` - This recipe is obsolete.

-  ``packagegroup-core-sdk-gmae`` - This recipe is obsolete.

-  ``packagegroup-core-standalone-gmae-sdk-target`` - This recipe is
   obsolete.

.. _migration-1.6-removed-classes:

Removed Classes
---------------

The following classes have become obsolete and have been removed:

-  ``module_strip``

-  ``pkg_metainfo``

-  ``pkg_distribute``

-  ``image-empty``

.. _migration-1.6-reference-bsps:

Reference Board Support Packages (BSPs)
---------------------------------------

The following reference BSPs changes occurred:

-  The BeagleBoard (``beagleboard``) ARM reference hardware has been
   replaced by the BeagleBone (``beaglebone``) hardware.

-  The RouterStation Pro (``routerstationpro``) MIPS reference hardware
   has been replaced by the EdgeRouter Lite (``edgerouter``) hardware.

The previous reference BSPs for the ``beagleboard`` and
``routerstationpro`` machines are still available in a new
``meta-yocto-bsp-old`` layer in the
:yocto_git:`Source Repositories <>` at
http://git.yoctoproject.org/cgit/cgit.cgi/meta-yocto-bsp-old/.

Moving to the Yocto Project 1.7 Release
=======================================

This section provides migration information for moving to the Yocto
Project 1.7 Release from the prior release.

.. _migration-1.7-changes-to-setting-qemu-packageconfig-options:

Changes to Setting QEMU ``PACKAGECONFIG`` Options in ``local.conf``
-------------------------------------------------------------------

The QEMU recipe now uses a number of
:term:`PACKAGECONFIG` options to enable various
optional features. The method used to set defaults for these options
means that existing ``local.conf`` files will need to be be modified to
append to ``PACKAGECONFIG`` for ``qemu-native`` and ``nativesdk-qemu``
instead of setting it. In other words, to enable graphical output for
QEMU, you should now have these lines in ``local.conf``:
::

   PACKAGECONFIG_append_pn-qemu-native = " sdl"
   PACKAGECONFIG_append_pn-nativesdk-qemu = " sdl"

.. _migration-1.7-minimum-git-version:

Minimum Git version
-------------------

The minimum :ref:`overview-manual/overview-manual-development-environment:git`
version required on the
build host is now 1.7.8 because the ``--list`` option is now required by
BitBake's Git fetcher. As always, if your host distribution does not
provide a version of Git that meets this requirement, you can use the
``buildtools-tarball`` that does. See the "`Required Git, tar, Python
and gcc Versions <#required-git-tar-python-and-gcc-versions>`__" section
for more information.

.. _migration-1.7-autotools-class-changes:

Autotools Class Changes
-----------------------

The following :ref:`autotools <ref-classes-autotools>` class changes
occurred:

-  *A separate build directory is now used by default:* The
   ``autotools`` class has been changed to use a directory for building
   (:term:`B`), which is separate from the source directory
   (:term:`S`). This is commonly referred to as ``B != S``, or
   an out-of-tree build.

   If the software being built is already capable of building in a
   directory separate from the source, you do not need to do anything.
   However, if the software is not capable of being built in this
   manner, you will need to either patch the software so that it can
   build separately, or you will need to change the recipe to inherit
   the :ref:`autotools-brokensep <ref-classes-autotools>` class
   instead of the ``autotools`` or ``autotools_stage`` classes.

-  The ``--foreign`` option is no longer passed to ``automake`` when
   running ``autoconf``: This option tells ``automake`` that a
   particular software package does not follow the GNU standards and
   therefore should not be expected to distribute certain files such as
   ``ChangeLog``, ``AUTHORS``, and so forth. Because the majority of
   upstream software packages already tell ``automake`` to enable
   foreign mode themselves, the option is mostly superfluous. However,
   some recipes will need patches for this change. You can easily make
   the change by patching ``configure.ac`` so that it passes "foreign"
   to ``AM_INIT_AUTOMAKE()``. See `this
   commit <http://cgit.openembedded.org/openembedded-core/commit/?id=01943188f85ce6411717fb5bf702d609f55813f2>`__
   for an example showing how to make the patch.

.. _migration-1.7-binary-configuration-scripts-disabled:

Binary Configuration Scripts Disabled
-------------------------------------

Some of the core recipes that package binary configuration scripts now
disable the scripts due to the scripts previously requiring error-prone
path substitution. Software that links against these libraries using
these scripts should use the much more robust ``pkg-config`` instead.
The list of recipes changed in this version (and their configuration
scripts) is as follows:
::

   directfb (directfb-config)
   freetype (freetype-config)
   gpgme (gpgme-config)
   libassuan (libassuan-config)
   libcroco (croco-6.0-config)
   libgcrypt (libgcrypt-config)
   libgpg-error (gpg-error-config)
   libksba (ksba-config)
   libpcap (pcap-config)
   libpcre (pcre-config)
   libpng (libpng-config, libpng16-config)
   libsdl (sdl-config)
   libusb-compat (libusb-config)
   libxml2 (xml2-config)
   libxslt (xslt-config)
   ncurses (ncurses-config)
   neon (neon-config)
   npth (npth-config)
   pth (pth-config)
   taglib (taglib-config)

Additionally, support for ``pkg-config`` has been added to some recipes in the
previous list in the rare cases where the upstream software package does
not already provide it.

.. _migration-1.7-glibc-replaces-eglibc:

``eglibc 2.19`` Replaced with ``glibc 2.20``
--------------------------------------------

Because ``eglibc`` and ``glibc`` were already fairly close, this
replacement should not require any significant changes to other software
that links to ``eglibc``. However, there were a number of minor changes
in ``glibc 2.20`` upstream that could require patching some software
(e.g. the removal of the ``_BSD_SOURCE`` feature test macro).

``glibc 2.20`` requires version 2.6.32 or greater of the Linux kernel.
Thus, older kernels will no longer be usable in conjunction with it.

For full details on the changes in ``glibc 2.20``, see the upstream
release notes
`here <https://sourceware.org/ml/libc-alpha/2014-09/msg00088.html>`__.

.. _migration-1.7-kernel-module-autoloading:

Kernel Module Autoloading
-------------------------

The :term:`module_autoload_* <module_autoload>` variable is now
deprecated and a new
:term:`KERNEL_MODULE_AUTOLOAD` variable
should be used instead. Also, :term:`module_conf_* <module_conf>`
must now be used in conjunction with a new
:term:`KERNEL_MODULE_PROBECONF` variable.
The new variables no longer require you to specify the module name as
part of the variable name. This change not only simplifies usage but
also allows the values of these variables to be appropriately
incorporated into task signatures and thus trigger the appropriate tasks
to re-execute when changed. You should replace any references to
``module_autoload_*`` with ``KERNEL_MODULE_AUTOLOAD``, and add any
modules for which ``module_conf_*`` is specified to
``KERNEL_MODULE_PROBECONF``.

.. _migration-1.7-qa-check-changes:

QA Check Changes
----------------

The following changes have occurred to the QA check process:

-  Additional QA checks ``file-rdeps`` and ``build-deps`` have been
   added in order to verify that file dependencies are satisfied (e.g.
   package contains a script requiring ``/bin/bash``) and build-time
   dependencies are declared, respectively. For more information, please
   see the "`QA Error and Warning Messages <#ref-qa-checks>`__" chapter.

-  Package QA checks are now performed during a new
   :ref:`ref-tasks-package_qa` task rather than being
   part of the :ref:`ref-tasks-package` task. This allows
   more parallel execution. This change is unlikely to be an issue
   except for highly customized recipes that disable packaging tasks
   themselves by marking them as ``noexec``. For those packages, you
   will need to disable the ``do_package_qa`` task as well.

-  Files being overwritten during the
   :ref:`ref-tasks-populate_sysroot` task now
   trigger an error instead of a warning. Recipes should not be
   overwriting files written to the sysroot by other recipes. If you
   have these types of recipes, you need to alter them so that they do
   not overwrite these files.

   You might now receive this error after changes in configuration or
   metadata resulting in orphaned files being left in the sysroot. If
   you do receive this error, the way to resolve the issue is to delete
   your :term:`TMPDIR` or to move it out of the way and
   then re-start the build. Anything that has been fully built up to
   that point and does not need rebuilding will be restored from the
   shared state cache and the rest of the build will be able to proceed
   as normal.

.. _migration-1.7-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed:

-  ``x-load``: This recipe has been superseded by U-boot SPL for all
   Cortex-based TI SoCs. For legacy boards, the ``meta-ti`` layer, which
   contains a maintained recipe, should be used instead.

-  ``ubootchart``: This recipe is obsolete. A ``bootchart2`` recipe has
   been added to functionally replace it.

-  ``linux-yocto 3.4``: Support for the linux-yocto 3.4 kernel has been
   dropped. Support for the 3.10 and 3.14 kernels remains, while support
   for version 3.17 has been added.

-  ``eglibc`` has been removed in favor of ``glibc``. See the
   "```eglibc 2.19`` Replaced with
   ``glibc 2.20`` <#migration-1.7-glibc-replaces-eglibc>`__" section for
   more information.

.. _migration-1.7-miscellaneous-changes:

Miscellaneous Changes
---------------------

The following miscellaneous change occurred:

-  The build history feature now writes ``build-id.txt`` instead of
   ``build-id``. Additionally, ``build-id.txt`` now contains the full
   build header as printed by BitBake upon starting the build. You
   should manually remove old "build-id" files from your existing build
   history repositories to avoid confusion. For information on the build
   history feature, see the
   ":ref:`dev-manual/dev-manual-common-tasks:maintaining build output quality`"
   section in the Yocto Project Development Tasks Manual.

Moving to the Yocto Project 1.8 Release
=======================================

This section provides migration information for moving to the Yocto
Project 1.8 Release from the prior release.

.. _migration-1.8-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed:

-  ``owl-video``: Functionality replaced by ``gst-player``.

-  ``gaku``: Functionality replaced by ``gst-player``.

-  ``gnome-desktop``: This recipe is now available in ``meta-gnome`` and
   is no longer needed.

-  ``gsettings-desktop-schemas``: This recipe is now available in
   ``meta-gnome`` and is no longer needed.

-  ``python-argparse``: The ``argparse`` module is already provided in
   the default Python distribution in a package named
   ``python-argparse``. Consequently, the separate ``python-argparse``
   recipe is no longer needed.

-  ``telepathy-python, libtelepathy, telepathy-glib, telepathy-idle, telepathy-mission-control``:
   All these recipes have moved to ``meta-oe`` and are consequently no
   longer needed by any recipes in OpenEmbedded-Core.

-  ``linux-yocto_3.10`` and ``linux-yocto_3.17``: Support for the
   linux-yocto 3.10 and 3.17 kernels has been dropped. Support for the
   3.14 kernel remains, while support for 3.19 kernel has been added.

-  ``poky-feed-config-opkg``: This recipe has become obsolete and is no
   longer needed. Use ``distro-feed-config`` from ``meta-oe`` instead.

-  ``libav 0.8.x``: ``libav 9.x`` is now used.

-  ``sed-native``: No longer needed. A working version of ``sed`` is
   expected to be provided by the host distribution.

.. _migration-1.8-bluez:

BlueZ 4.x / 5.x Selection
-------------------------

Proper built-in support for selecting BlueZ 5.x in preference to the
default of 4.x now exists. To use BlueZ 5.x, simply add "bluez5" to your
:term:`DISTRO_FEATURES` value. If you had
previously added append files (``*.bbappend``) to make this selection,
you can now remove them.

Additionally, a ``bluetooth`` class has been added to make selection of
the appropriate bluetooth support within a recipe a little easier. If
you wish to make use of this class in a recipe, add something such as
the following: ::

   inherit bluetooth
   PACKAGECONFIG ??= "${@bb.utils.contains('DISTRO_FEATURES', 'bluetooth', '${BLUEZ}', '', d)}"
   PACKAGECONFIG[bluez4] = "--enable-bluetooth,--disable-bluetooth,bluez4"
   PACKAGECONFIG[bluez5] = "--enable-bluez5,--disable-bluez5,bluez5"

.. _migration-1.8-kernel-build-changes:

Kernel Build Changes
--------------------

The kernel build process was changed to place the source in a common
shared work area and to place build artifacts separately in the source
code tree. In theory, migration paths have been provided for most common
usages in kernel recipes but this might not work in all cases. In
particular, users need to ensure that ``${S}`` (source files) and
``${B}`` (build artifacts) are used correctly in functions such as
:ref:`ref-tasks-configure` and
:ref:`ref-tasks-install`. For kernel recipes that do not
inherit from ``kernel-yocto`` or include ``linux-yocto.inc``, you might
wish to refer to the ``linux.inc`` file in the ``meta-oe`` layer for the
kinds of changes you need to make. For reference, here is the
`commit <http://cgit.openembedded.org/meta-openembedded/commit/meta-oe/recipes-kernel/linux/linux.inc?id=fc7132ede27ac67669448d3d2845ce7d46c6a1ee>`__
where the ``linux.inc`` file in ``meta-oe`` was updated.

Recipes that rely on the kernel source code and do not inherit the
module classes might need to add explicit dependencies on the
``do_shared_workdir`` kernel task, for example: ::

   do_configure[depends] += "virtual/kernel:do_shared_workdir"

.. _migration-1.8-ssl:

SSL 3.0 is Now Disabled in OpenSSL
----------------------------------

SSL 3.0 is now disabled when building OpenSSL. Disabling SSL 3.0 avoids
any lingering instances of the POODLE vulnerability. If you feel you
must re-enable SSL 3.0, then you can add an append file (``*.bbappend``)
for the ``openssl`` recipe to remove "-no-ssl3" from
:term:`EXTRA_OECONF`.

.. _migration-1.8-default-sysroot-poisoning:

Default Sysroot Poisoning
-------------------------

``gcc's`` default sysroot and include directories are now "poisoned". In
other words, the sysroot and include directories are being redirected to
a non-existent location in order to catch when host directories are
being used due to the correct options not being passed. This poisoning
applies both to the cross-compiler used within the build and to the
cross-compiler produced in the SDK.

If this change causes something in the build to fail, it almost
certainly means the various compiler flags and commands are not being
passed correctly to the underlying piece of software. In such cases, you
need to take corrective steps.

.. _migration-1.8-rebuild-improvements:

Rebuild Improvements
--------------------

Changes have been made to the :ref:`base <ref-classes-base>`,
:ref:`autotools <ref-classes-autotools>`, and
:ref:`cmake <ref-classes-cmake>` classes to clean out generated files
when the :ref:`ref-tasks-configure` task needs to be
re-executed.

One of the improvements is to attempt to run "make clean" during the
``do_configure`` task if a ``Makefile`` exists. Some software packages
do not provide a working clean target within their make files. If you
have such recipes, you need to set
:term:`CLEANBROKEN` to "1" within the recipe, for example: ::

   CLEANBROKEN = "1"

.. _migration-1.8-qa-check-and-validation-changes:

QA Check and Validation Changes
-------------------------------

The following QA Check and Validation Changes have occurred:

-  Usage of ``PRINC`` previously triggered a warning. It now triggers an
   error. You should remove any remaining usage of ``PRINC`` in any
   recipe or append file.

-  An additional QA check has been added to detect usage of ``${D}`` in
   :term:`FILES` values where :term:`D` values
   should not be used at all. The same check ensures that ``$D`` is used
   in ``pkg_preinst/pkg_postinst/pkg_prerm/pkg_postrm`` functions
   instead of ``${D}``.

-  :term:`S` now needs to be set to a valid value within a
   recipe. If ``S`` is not set in the recipe, the directory is not
   automatically created. If ``S`` does not point to a directory that
   exists at the time the :ref:`ref-tasks-unpack` task
   finishes, a warning will be shown.

-  :term:`LICENSE` is now validated for correct
   formatting of multiple licenses. If the format is invalid (e.g.
   multiple licenses are specified with no operators to specify how the
   multiple licenses interact), then a warning will be shown.

.. _migration-1.8-miscellaneous-changes:

Miscellaneous Changes
---------------------

The following miscellaneous changes have occurred:

-  The ``send-error-report`` script now expects a "-s" option to be
   specified before the server address. This assumes a server address is
   being specified.

-  The ``oe-pkgdata-util`` script now expects a "-p" option to be
   specified before the ``pkgdata`` directory, which is now optional. If
   the ``pkgdata`` directory is not specified, the script will run
   BitBake to query :term:`PKGDATA_DIR` from the
   build environment.

Moving to the Yocto Project 2.0 Release
=======================================

This section provides migration information for moving to the Yocto
Project 2.0 Release from the prior release.

.. _migration-2.0-gcc-5:

GCC 5
-----

The default compiler is now GCC 5.2. This change has required fixes for
compilation errors in a number of other recipes.

One important example is a fix for when the Linux kernel freezes at boot
time on ARM when built with GCC 5. If you are using your own kernel
recipe or source tree and building for ARM, you will likely need to
apply this
`patch <https://git.kernel.org/cgit/linux/kernel/git/torvalds/linux.git/commit?id=a077224fd35b2f7fbc93f14cf67074fc792fbac2>`__.
The standard ``linux-yocto`` kernel source tree already has a workaround
for the same issue.

For further details, see https://gcc.gnu.org/gcc-5/changes.html
and the porting guide at
https://gcc.gnu.org/gcc-5/porting_to.html.

Alternatively, you can switch back to GCC 4.9 or 4.8 by setting
``GCCVERSION`` in your configuration, as follows:
::

   GCCVERSION = "4.9%"

.. _migration-2.0-Gstreamer-0.10-removed:

Gstreamer 0.10 Removed
----------------------

Gstreamer 0.10 has been removed in favor of Gstreamer 1.x. As part of
the change, recipes for Gstreamer 0.10 and related software are now
located in ``meta-multimedia``. This change results in Qt4 having Phonon
and Gstreamer support in QtWebkit disabled by default.

.. _migration-2.0-removed-recipes:

Removed Recipes
---------------

The following recipes have been moved or removed:

-  ``bluez4``: The recipe is obsolete and has been moved due to
   ``bluez5`` becoming fully integrated. The ``bluez4`` recipe now
   resides in ``meta-oe``.

-  ``gamin``: The recipe is obsolete and has been removed.

-  ``gnome-icon-theme``: The recipe's functionally has been replaced by
   ``adwaita-icon-theme``.

-  Gstreamer 0.10 Recipes: Recipes for Gstreamer 0.10 have been removed
   in favor of the recipes for Gstreamer 1.x.

-  ``insserv``: The recipe is obsolete and has been removed.

-  ``libunique``: The recipe is no longer used and has been moved to
   ``meta-oe``.

-  ``midori``: The recipe's functionally has been replaced by
   ``epiphany``.

-  ``python-gst``: The recipe is obsolete and has been removed since it
   only contains bindings for Gstreamer 0.10.

-  ``qt-mobility``: The recipe is obsolete and has been removed since it
   requires ``Gstreamer 0.10``, which has been replaced.

-  ``subversion``: All 1.6.x versions of this recipe have been removed.

-  ``webkit-gtk``: The older 1.8.3 version of this recipe has been
   removed in favor of ``webkitgtk``.

.. _migration-2.0-bitbake-datastore-improvements:

BitBake datastore improvements
------------------------------

The method by which BitBake's datastore handles overrides has changed.
Overrides are now applied dynamically and ``bb.data.update_data()`` is
now a no-op. Thus, ``bb.data.update_data()`` is no longer required in
order to apply the correct overrides. In practice, this change is
unlikely to require any changes to Metadata. However, these minor
changes in behavior exist:

-  All potential overrides are now visible in the variable history as
   seen when you run the following:
   ::

      $ bitbake -e

-  ``d.delVar('``\ VARNAME\ ``')`` and
   ``d.setVar('``\ VARNAME\ ``', None)`` result in the variable and all
   of its overrides being cleared out. Before the change, only the
   non-overridden values were cleared.

.. _migration-2.0-shell-message-function-changes:

Shell Message Function Changes
------------------------------

The shell versions of the BitBake message functions (i.e. ``bbdebug``,
``bbnote``, ``bbwarn``, ``bbplain``, ``bberror``, and ``bbfatal``) are
now connected through to their BitBake equivalents ``bb.debug()``,
``bb.note()``, ``bb.warn()``, ``bb.plain()``, ``bb.error()``, and
``bb.fatal()``, respectively. Thus, those message functions that you
would expect to be printed by the BitBake UI are now actually printed.
In practice, this change means two things:

-  If you now see messages on the console that you did not previously
   see as a result of this change, you might need to clean up the calls
   to ``bbwarn``, ``bberror``, and so forth. Or, you might want to
   simply remove the calls.

-  The ``bbfatal`` message function now suppresses the full error log in
   the UI, which means any calls to ``bbfatal`` where you still wish to
   see the full error log should be replaced by ``die`` or
   ``bbfatal_log``.

.. _migration-2.0-extra-development-debug-package-cleanup:

Extra Development/Debug Package Cleanup
---------------------------------------

The following recipes have had extra ``dev/dbg`` packages removed:

-  ``acl``

-  ``apmd``

-  ``aspell``

-  ``attr``

-  ``augeas``

-  ``bzip2``

-  ``cogl``

-  ``curl``

-  ``elfutils``

-  ``gcc-target``

-  ``libgcc``

-  ``libtool``

-  ``libxmu``

-  ``opkg``

-  ``pciutils``

-  ``rpm``

-  ``sysfsutils``

-  ``tiff``

-  ``xz``

All of the above recipes now conform to the standard packaging scheme
where a single ``-dev``, ``-dbg``, and ``-staticdev`` package exists per
recipe.

.. _migration-2.0-recipe-maintenance-tracking-data-moved-to-oe-core:

Recipe Maintenance Tracking Data Moved to OE-Core
-------------------------------------------------

Maintenance tracking data for recipes that was previously part of
``meta-yocto`` has been moved to :term:`OpenEmbedded-Core (OE-Core)`. The change
includes ``package_regex.inc`` and ``distro_alias.inc``, which are
typically enabled when using the ``distrodata`` class. Additionally, the
contents of ``upstream_tracking.inc`` has now been split out to the
relevant recipes.

.. _migration-2.0-automatic-stale-sysroot-file-cleanup:

Automatic Stale Sysroot File Cleanup
------------------------------------

Stale files from recipes that no longer exist in the current
configuration are now automatically removed from sysroot as well as
removed from any other place managed by shared state. This automatic
cleanup means that the build system now properly handles situations such
as renaming the build system side of recipes, removal of layers from
``bblayers.conf``, and :term:`DISTRO_FEATURES`
changes.

Additionally, work directories for old versions of recipes are now
pruned. If you wish to disable pruning old work directories, you can set
the following variable in your configuration:
::

   SSTATE_PRUNE_OBSOLETEWORKDIR = "0"

.. _migration-2.0-linux-yocto-kernel-metadata-repository-now-split-from-source:

``linux-yocto`` Kernel Metadata Repository Now Split from Source
----------------------------------------------------------------

The ``linux-yocto`` tree has up to now been a combined set of kernel
changes and configuration (meta) data carried in a single tree. While
this format is effective at keeping kernel configuration and source
modifications synchronized, it is not always obvious to developers how
to manipulate the Metadata as compared to the source.

Metadata processing has now been removed from the
:ref:`kernel-yocto <ref-classes-kernel-yocto>` class and the external
Metadata repository ``yocto-kernel-cache``, which has always been used
to seed the ``linux-yocto`` "meta" branch. This separate ``linux-yocto``
cache repository is now the primary location for this data. Due to this
change, ``linux-yocto`` is no longer able to process combined trees.
Thus, if you need to have your own combined kernel repository, you must
do the split there as well and update your recipes accordingly. See the
``meta/recipes-kernel/linux/linux-yocto_4.1.bb`` recipe for an example.

.. _migration-2.0-additional-qa-checks:

Additional QA checks
--------------------

The following QA checks have been added:

-  Added a "host-user-contaminated" check for ownership issues for
   packaged files outside of ``/home``. The check looks for files that
   are incorrectly owned by the user that ran BitBake instead of owned
   by a valid user in the target system.

-  Added an "invalid-chars" check for invalid (non-UTF8) characters in
   recipe metadata variable values (i.e.
   :term:`DESCRIPTION`,
   :term:`SUMMARY`, :term:`LICENSE`, and
   :term:`SECTION`). Some package managers do not support
   these characters.

-  Added an "invalid-packageconfig" check for any options specified in
   :term:`PACKAGECONFIG` that do not match any
   ``PACKAGECONFIG`` option defined for the recipe.

.. _migration-2.0-miscellaneous:

Miscellaneous Changes
---------------------

These additional changes exist:

-  ``gtk-update-icon-cache`` has been renamed to ``gtk-icon-utils``.

-  The ``tools-profile`` :term:`IMAGE_FEATURES`
   item as well as its corresponding packagegroup and
   ``packagegroup-core-tools-profile`` no longer bring in ``oprofile``.
   Bringing in ``oprofile`` was originally added to aid compilation on
   resource-constrained targets. However, this aid has not been widely
   used and is not likely to be used going forward due to the more
   powerful target platforms and the existence of better
   cross-compilation tools.

-  The :term:`IMAGE_FSTYPES` variable's default
   value now specifies ``ext4`` instead of ``ext3``.

-  All support for the ``PRINC`` variable has been removed.

-  The ``packagegroup-core-full-cmdline`` packagegroup no longer brings
   in ``lighttpd`` due to the fact that bringing in ``lighttpd`` is not
   really in line with the packagegroup's purpose, which is to add full
   versions of command-line tools that by default are provided by
   ``busybox``.

Moving to the Yocto Project 2.1 Release
=======================================

This section provides migration information for moving to the Yocto
Project 2.1 Release from the prior release.

.. _migration-2.1-variable-expansion-in-python-functions:

Variable Expansion in Python Functions
--------------------------------------

Variable expressions, such as ``${``\ VARNAME\ ``}`` no longer expand
automatically within Python functions. Suppressing expansion was done to
allow Python functions to construct shell scripts or other code for
situations in which you do not want such expressions expanded. For any
existing code that relies on these expansions, you need to change the
expansions to expand the value of individual variables through
``d.getVar()``. To alternatively expand more complex expressions, use
``d.expand()``.

.. _migration-2.1-overrides-must-now-be-lower-case:

Overrides Must Now be Lower-Case
--------------------------------

The convention for overrides has always been for them to be lower-case
characters. This practice is now a requirement as BitBake's datastore
now assumes lower-case characters in order to give a slight performance
boost during parsing. In practical terms, this requirement means that
anything that ends up in :term:`OVERRIDES` must now
appear in lower-case characters (e.g. values for ``MACHINE``,
``TARGET_ARCH``, ``DISTRO``, and also recipe names if
``_pn-``\ recipename overrides are to be effective).

.. _migration-2.1-expand-parameter-to-getvar-and-getvarflag-now-mandatory:

Expand Parameter to ``getVar()`` and ``getVarFlag()`` is Now Mandatory
----------------------------------------------------------------------

The expand parameter to ``getVar()`` and ``getVarFlag()`` previously
defaulted to False if not specified. Now, however, no default exists so
one must be specified. You must change any ``getVar()`` calls that do
not specify the final expand parameter to calls that do specify the
parameter. You can run the following ``sed`` command at the base of a
layer to make this change:
::

   sed -e 's:\(\.getVar([^,()]*\)):\1, False):g' -i `grep -ril getVar *`
   sed -e 's:\(\.getVarFlag([^,()]*,[^,()]*\)):\1, False):g' -i `grep -ril getVarFlag *`

.. note::

   The reason for this change is that it prepares the way for changing
   the default to True in a future Yocto Project release. This future
   change is a much more sensible default than False. However, the
   change needs to be made gradually as a sudden change of the default
   would potentially cause side-effects that would be difficult to
   detect.

.. _migration-2.1-makefile-environment-changes:

Makefile Environment Changes
----------------------------

:term:`EXTRA_OEMAKE` now defaults to "" instead of
"-e MAKEFLAGS=". Setting ``EXTRA_OEMAKE`` to "-e MAKEFLAGS=" by default
was a historical accident that has required many classes (e.g.
``autotools``, ``module``) and recipes to override this default in order
to work with sensible build systems. When upgrading to the release, you
must edit any recipe that relies upon this old default by either setting
``EXTRA_OEMAKE`` back to "-e MAKEFLAGS=" or by explicitly setting any
required variable value overrides using ``EXTRA_OEMAKE``, which is
typically only needed when a Makefile sets a default value for a
variable that is inappropriate for cross-compilation using the "="
operator rather than the "?=" operator.

.. _migration-2.1-libexecdir-reverted-to-prefix-libexec:

``libexecdir`` Reverted to ``${prefix}/libexec``
------------------------------------------------

The use of ``${libdir}/${BPN}`` as ``libexecdir`` is different as
compared to all other mainstream distributions, which either uses
``${prefix}/libexec`` or ``${libdir}``. The use is also contrary to the
GNU Coding Standards (i.e.
https://www.gnu.org/prep/standards/html_node/Directory-Variables.html)
that suggest ``${prefix}/libexec`` and also notes that any
package-specific nesting should be done by the package itself. Finally,
having ``libexecdir`` change between recipes makes it very difficult for
different recipes to invoke binaries that have been installed into
``libexecdir``. The Filesystem Hierarchy Standard (i.e.
http://refspecs.linuxfoundation.org/FHS_3.0/fhs/ch04s07.html) now
recognizes the use of ``${prefix}/libexec/``, giving distributions the
choice between ``${prefix}/lib`` or ``${prefix}/libexec`` without
breaking FHS.

.. _migration-2.1-ac-cv-sizeof-off-t-no-longer-cached-in-site-files:

``ac_cv_sizeof_off_t`` is No Longer Cached in Site Files
--------------------------------------------------------

For recipes inheriting the :ref:`autotools <ref-classes-autotools>`
class, ``ac_cv_sizeof_off_t`` is no longer cached in the site files for
``autoconf``. The reason for this change is because the
``ac_cv_sizeof_off_t`` value is not necessarily static per architecture
as was previously assumed. Rather, the value changes based on whether
large file support is enabled. For most software that uses ``autoconf``,
this change should not be a problem. However, if you have a recipe that
bypasses the standard :ref:`ref-tasks-configure` task
from the ``autotools`` class and the software the recipe is building
uses a very old version of ``autoconf``, the recipe might be incapable
of determining the correct size of ``off_t`` during ``do_configure``.

The best course of action is to patch the software as necessary to allow
the default implementation from the ``autotools`` class to work such
that ``autoreconf`` succeeds and produces a working configure script,
and to remove the overridden ``do_configure`` task such that the default
implementation does get used.

.. _migration-2.1-image-generation-split-out-from-filesystem-generation:

Image Generation is Now Split Out from Filesystem Generation
------------------------------------------------------------

Previously, for image recipes the :ref:`ref-tasks-rootfs`
task assembled the filesystem and then from that filesystem generated
images. With this Yocto Project release, image generation is split into
separate ```do_image_*`` <#ref-tasks-image>`__ tasks for clarity both in
operation and in the code.

For most cases, this change does not present any problems. However, if
you have made customizations that directly modify the ``do_rootfs`` task
or that mention ``do_rootfs``, you might need to update those changes.
In particular, if you had added any tasks after ``do_rootfs``, you
should make edits so that those tasks are after the
```do_image_complete`` <#ref-tasks-image-complete>`__ task rather than
after ``do_rootfs`` so that the your added tasks run at the correct
time.

A minor part of this restructuring is that the post-processing
definitions and functions have been moved from the
:ref:`image <ref-classes-image>` class to the
:ref:`rootfs-postcommands <ref-classes-rootfs*>` class. Functionally,
however, they remain unchanged.

.. _migration-2.1-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed in the 2.1 release:

-  ``gcc`` version 4.8: Versions 4.9 and 5.3 remain.

-  ``qt4``: All support for Qt 4.x has been moved out to a separate
   ``meta-qt4`` layer because Qt 4 is no longer supported upstream.

-  ``x11vnc``: Moved to the ``meta-oe`` layer.

-  ``linux-yocto-3.14``: No longer supported.

-  ``linux-yocto-3.19``: No longer supported.

-  ``libjpeg``: Replaced by the ``libjpeg-turbo`` recipe.

-  ``pth``: Became obsolete.

-  ``liboil``: Recipe is no longer needed and has been moved to the
   ``meta-multimedia`` layer.

-  ``gtk-theme-torturer``: Recipe is no longer needed and has been moved
   to the ``meta-gnome`` layer.

-  ``gnome-mime-data``: Recipe is no longer needed and has been moved to
   the ``meta-gnome`` layer.

-  ``udev``: Replaced by the ``eudev`` recipe for compatibility when
   using ``sysvinit`` with newer kernels.

-  ``python-pygtk``: Recipe became obsolete.

-  ``adt-installer``: Recipe became obsolete. See the "`ADT
   Removed <#migration-2.1-adt-removed>`__" section for more
   information.

.. _migration-2.1-class-changes:

Class Changes
-------------

The following classes have changed:

-  ``autotools_stage``: Removed because the
   :ref:`autotools <ref-classes-autotools>` class now provides its
   functionality. Recipes that inherited from ``autotools_stage`` should
   now inherit from ``autotools`` instead.

-  ``boot-directdisk``: Merged into the ``image-vm`` class. The
   ``boot-directdisk`` class was rarely directly used. Consequently,
   this change should not cause any issues.

-  ``bootimg``: Merged into the
   :ref:`image-live <ref-classes-image-live>` class. The ``bootimg``
   class was rarely directly used. Consequently, this change should not
   cause any issues.

-  ``packageinfo``: Removed due to its limited use by the Hob UI, which
   has itself been removed.

.. _migration-2.1-build-system-ui-changes:

Build System User Interface Changes
-----------------------------------

The following changes have been made to the build system user interface:

-  *Hob GTK+-based UI*: Removed because it is unmaintained and based on
   the outdated GTK+ 2 library. The Toaster web-based UI is much more
   capable and is actively maintained. See the
   ":ref:`toaster-manual/toaster-manual-setup-and-use:using the toaster web interface`"
   section in the Toaster User Manual for more information on this
   interface.

-  *"puccho" BitBake UI*: Removed because is unmaintained and no longer
   useful.

.. _migration-2.1-adt-removed:

ADT Removed
-----------

The Application Development Toolkit (ADT) has been removed because its
functionality almost completely overlapped with the :ref:`standard
SDK <sdk-manual/sdk-using:using the standard sdk>` and the
:ref:`extensible SDK <sdk-manual/sdk-extensible:using the extensible sdk>`. For
information on these SDKs and how to build and use them, see the
:doc:`../sdk-manual/sdk-manual` manual.

.. note::

   The Yocto Project Eclipse IDE Plug-in is still supported and is not
   affected by this change.

.. _migration-2.1-poky-reference-distribution-changes:

Poky Reference Distribution Changes
-----------------------------------

The following changes have been made for the Poky distribution:

-  The ``meta-yocto`` layer has been renamed to ``meta-poky`` to better
   match its purpose, which is to provide the Poky reference
   distribution. The ``meta-yocto-bsp`` layer retains its original name
   since it provides reference machines for the Yocto Project and it is
   otherwise unrelated to Poky. References to ``meta-yocto`` in your
   ``conf/bblayers.conf`` should automatically be updated, so you should
   not need to change anything unless you are relying on this naming
   elsewhere.

-  The :ref:`uninative <ref-classes-uninative>` class is now enabled
   by default in Poky. This class attempts to isolate the build system
   from the host distribution's C library and makes re-use of native
   shared state artifacts across different host distributions practical.
   With this class enabled, a tarball containing a pre-built C library
   is downloaded at the start of the build.

   The ``uninative`` class is enabled through the
   ``meta/conf/distro/include/yocto-uninative.inc`` file, which for
   those not using the Poky distribution, can include to easily enable
   the same functionality.

   Alternatively, if you wish to build your own ``uninative`` tarball,
   you can do so by building the ``uninative-tarball`` recipe, making it
   available to your build machines (e.g. over HTTP/HTTPS) and setting a
   similar configuration as the one set by ``yocto-uninative.inc``.

-  Static library generation, for most cases, is now disabled by default
   in the Poky distribution. Disabling this generation saves some build
   time as well as the size used for build output artifacts.

   Disabling this library generation is accomplished through a
   ``meta/conf/distro/include/no-static-libs.inc``, which for those not
   using the Poky distribution can easily include to enable the same
   functionality.

   Any recipe that needs to opt-out of having the "--disable-static"
   option specified on the configure command line either because it is
   not a supported option for the configure script or because static
   libraries are needed should set the following variable:
   DISABLE_STATIC = ""

-  The separate ``poky-tiny`` distribution now uses the musl C library
   instead of a heavily pared down ``glibc``. Using musl results in a
   smaller distribution and facilitates much greater maintainability
   because musl is designed to have a small footprint.

   If you have used ``poky-tiny`` and have customized the ``glibc``
   configuration you will need to redo those customizations with musl
   when upgrading to the new release.

.. _migration-2.1-packaging-changes:

Packaging Changes
-----------------

The following changes have been made to packaging:

-  The ``runuser`` and ``mountpoint`` binaries, which were previously in
   the main ``util-linux`` package, have been split out into the
   ``util-linux-runuser`` and ``util-linux-mountpoint`` packages,
   respectively.

-  The ``python-elementtree`` package has been merged into the
   ``python-xml`` package.

.. _migration-2.1-tuning-file-changes:

Tuning File Changes
-------------------

The following changes have been made to the tuning files:

-  The "no-thumb-interwork" tuning feature has been dropped from the ARM
   tune include files. Because interworking is required for ARM EABI,
   attempting to disable it through a tuning feature no longer makes
   sense.

   .. note::

      Support for ARM OABI was deprecated in gcc 4.7.

-  The ``tune-cortexm*.inc`` and ``tune-cortexr4.inc`` files have been
   removed because they are poorly tested. Until the OpenEmbedded build
   system officially gains support for CPUs without an MMU, these tuning
   files would probably be better maintained in a separate layer if
   needed.

.. _migration-2.1-supporting-gobject-introspection:

Supporting GObject Introspection
--------------------------------

This release supports generation of GLib Introspective Repository (GIR)
files through GObject introspection, which is the standard mechanism for
accessing GObject-based software from runtime environments. You can
enable, disable, and test the generation of this data. See the
":ref:`dev-manual/dev-manual-common-tasks:enabling gobject introspection support`"
section in the Yocto Project Development Tasks Manual for more
information.

.. _migration-2.1-miscellaneous-changes:

Miscellaneous Changes
---------------------

These additional changes exist:

-  The minimum Git version has been increased to 1.8.3.1. If your host
   distribution does not provide a sufficiently recent version, you can
   install the buildtools, which will provide it. See the "`Required
   Git, tar, Python and gcc
   Versions <#required-git-tar-python-and-gcc-versions>`__" section for
   more information on the buildtools tarball.

-  The buggy and incomplete support for the RPM version 4 package
   manager has been removed. The well-tested and maintained support for
   RPM version 5 remains.

-  Previously, the following list of packages were removed if
   package-management was not in
   :term:`IMAGE_FEATURES`, regardless of any
   dependencies:
   ::

      update-rc.d
      base-passwd
      shadow
      update-alternatives

   run-postinsts With the Yocto Project 2.1 release, these packages are
   only removed if "read-only-rootfs" is in ``IMAGE_FEATURES``, since
   they might still be needed for a read-write image even in the absence
   of a package manager (e.g. if users need to be added, modified, or
   removed at runtime).

-  The
   :ref:`devtool modify <sdk-manual/sdk-extensible:use \`\`devtool modify\`\` to modify the source of an existing component>`
   command now defaults to extracting the source since that is most
   commonly expected. The "-x" or "--extract" options are now no-ops. If
   you wish to provide your own existing source tree, you will now need
   to specify either the "-n" or "--no-extract" options when running
   ``devtool modify``.

-  If the formfactor for a machine is either not supplied or does not
   specify whether a keyboard is attached, then the default is to assume
   a keyboard is attached rather than assume no keyboard. This change
   primarily affects the Sato UI.

-  The ``.debug`` directory packaging is now automatic. If your recipe
   builds software that installs binaries into directories other than
   the standard ones, you no longer need to take care of setting
   ``FILES_${PN}-dbg`` to pick up the resulting ``.debug`` directories
   as these directories are automatically found and added.

-  Inaccurate disk and CPU percentage data has been dropped from
   ``buildstats`` output. This data has been replaced with
   ``getrusage()`` data and corrected IO statistics. You will probably
   need to update any custom code that reads the ``buildstats`` data.

-  The ``meta/conf/distro/include/package_regex.inc`` is now deprecated.
   The contents of this file have been moved to individual recipes.

   .. note::

      Because this file will likely be removed in a future Yocto Project
      release, it is suggested that you remove any references to the
      file that might be in your configuration.

-  The ``v86d/uvesafb`` has been removed from the ``genericx86`` and
   ``genericx86-64`` reference machines, which are provided by the
   ``meta-yocto-bsp`` layer. Most modern x86 boards do not rely on this
   file and it only adds kernel error messages during startup. If you do
   still need to support ``uvesafb``, you can simply add ``v86d`` to
   your image.

-  Build sysroot paths are now removed from debug symbol files. Removing
   these paths means that remote GDB using an unstripped build system
   sysroot will no longer work (although this was never documented to
   work). The supported method to accomplish something similar is to set
   ``IMAGE_GEN_DEBUGFS`` to "1", which will generate a companion debug
   image containing unstripped binaries and associated debug sources
   alongside the image.

Moving to the Yocto Project 2.2 Release
=======================================

This section provides migration information for moving to the Yocto
Project 2.2 Release from the prior release.

.. _migration-2.2-minimum-kernel-version:

Minimum Kernel Version
----------------------

The minimum kernel version for the target system and for SDK is now
3.2.0, due to the upgrade to ``glibc 2.24``. Specifically, for
AArch64-based targets the version is 3.14. For Nios II-based targets,
the minimum kernel version is 3.19.

.. note::

   For x86 and x86_64, you can reset
   OLDEST_KERNEL
   to anything down to 2.6.32 if desired.

.. _migration-2.2-staging-directories-in-sysroot-simplified:

Staging Directories in Sysroot Has Been Simplified
--------------------------------------------------

The way directories are staged in sysroot has been simplified and
introduces the new :term:`SYSROOT_DIRS`,
:term:`SYSROOT_DIRS_NATIVE`, and
:term:`SYSROOT_DIRS_BLACKLIST`. See the
`v2 patch series on the OE-Core Mailing
List <http://lists.openembedded.org/pipermail/openembedded-core/2016-May/121365.html>`__
for additional information.

.. _migration-2.2-removal-of-old-images-from-tmp-deploy-now-enabled:

Removal of Old Images and Other Files in ``tmp/deploy`` Now Enabled
-------------------------------------------------------------------

Removal of old images and other files in ``tmp/deploy/`` is now enabled
by default due to a new staging method used for those files. As a result
of this change, the ``RM_OLD_IMAGE`` variable is now redundant.

.. _migration-2.2-python-changes:

Python Changes
--------------

The following changes for Python occurred:

.. _migration-2.2-bitbake-now-requires-python-3.4:

BitBake Now Requires Python 3.4+
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BitBake requires Python 3.4 or greater.

.. _migration-2.2-utf-8-locale-required-on-build-host:

UTF-8 Locale Required on Build Host
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A UTF-8 locale is required on the build host due to Python 3. Since
C.UTF-8 is not a standard, the default is en_US.UTF-8.

.. _migration-2.2-metadata-now-must-use-python-3-syntax:

Metadata Must Now Use Python 3 Syntax
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The metadata is now required to use Python 3 syntax. For help preparing
metadata, see any of the many Python 3 porting guides available.
Alternatively, you can reference the conversion commits for Bitbake and
you can use :term:`OpenEmbedded-Core (OE-Core)` as a guide for changes. Following are
particular areas of interest:

  - subprocess command-line pipes needing locale decoding

  - the syntax for octal values changed

  - the ``iter*()`` functions changed name \* iterators now return views, not lists

  - changed names for Python modules

.. _migration-2.2-target-python-recipes-switched-to-python-3:

Target Python Recipes Switched to Python 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Most target Python recipes have now been switched to Python 3.
Unfortunately, systems using RPM as a package manager and providing
online package-manager support through SMART still require Python 2.

.. note::

   Python 2 and recipes that use it can still be built for the target as
   with previous versions.

.. _migration-2.2-buildtools-tarball-includes-python-3:

``buildtools-tarball`` Includes Python 3
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

``buildtools-tarball`` now includes Python 3.

.. _migration-2.2-uclibc-replaced-by-musl:

uClibc Replaced by musl
-----------------------

uClibc has been removed in favor of musl. Musl has matured, is better
maintained, and is compatible with a wider range of applications as
compared to uClibc.

.. _migration-2.2-B-no-longer-default-working-directory-for-tasks:

``${B}`` No Longer Default Working Directory for Tasks
------------------------------------------------------

``${``\ :term:`B`\ ``}`` is no longer the default working
directory for tasks. Consequently, any custom tasks you define now need
to either have the
``[``\ :ref:`dirs <bitbake:bitbake-user-manual/bitbake-user-manual-metadata:variable flags>`\ ``]`` flag
set, or the task needs to change into the appropriate working directory
manually (e.g using ``cd`` for a shell task).

.. note::

   The preferred method is to use the
   [dirs]
   flag.

.. _migration-2.2-runqemu-ported-to-python:

``runqemu`` Ported to Python
----------------------------

``runqemu`` has been ported to Python and has changed behavior in some
cases. Previous usage patterns continue to be supported.

The new ``runqemu`` is a Python script. Machine knowledge is no longer
hardcoded into ``runqemu``. You can choose to use the ``qemuboot``
configuration file to define the BSP's own arguments and to make it
bootable with ``runqemu``. If you use a configuration file, use the
following form:
::

   image-name-machine.qemuboot.conf

The configuration file
enables fine-grained tuning of options passed to QEMU without the
``runqemu`` script hard-coding any knowledge about different machines.
Using a configuration file is particularly convenient when trying to use
QEMU with machines other than the ``qemu*`` machines in
:term:`OpenEmbedded-Core (OE-Core)`. The ``qemuboot.conf`` file is generated by the
``qemuboot`` class when the root filesystem is being build (i.e. build
rootfs). QEMU boot arguments can be set in BSP's configuration file and
the ``qemuboot`` class will save them to ``qemuboot.conf``.

If you want to use ``runqemu`` without a configuration file, use the
following command form:
::

   $ runqemu machine rootfs kernel [options]

Supported machines are as follows:

  - qemuarm
  - qemuarm64
  - qemux86
  - qemux86-64
  - qemuppc
  - qemumips
  - qemumips64
  - qemumipsel
  - qemumips64el

Consider the
following example, which uses the ``qemux86-64`` machine, provides a
root filesystem, provides an image, and uses the ``nographic`` option: ::

   $ runqemu qemux86-64 tmp/deploy/images/qemux86-64/core-image-minimal-qemux86-64.ext4 tmp/deploy/images/qemux86-64/bzImage nographic

Following is a list of variables that can be set in configuration files
such as ``bsp.conf`` to enable the BSP to be booted by ``runqemu``:

.. note::

   "QB" means "QEMU Boot".

::

   QB_SYSTEM_NAME: QEMU name (e.g. "qemu-system-i386")
   QB_OPT_APPEND: Options to append to QEMU (e.g. "-show-cursor")
   QB_DEFAULT_KERNEL: Default kernel to boot (e.g. "bzImage")
   QB_DEFAULT_FSTYPE: Default FSTYPE to boot (e.g. "ext4")
   QB_MEM: Memory (e.g. "-m 512")
   QB_MACHINE: QEMU machine (e.g. "-machine virt")
   QB_CPU: QEMU cpu (e.g. "-cpu qemu32")
   QB_CPU_KVM: Similar to QB_CPU except used for kvm support (e.g. "-cpu kvm64")
   QB_KERNEL_CMDLINE_APPEND: Options to append to the kernel's -append
                             option (e.g. "console=ttyS0 console=tty")
   QB_DTB: QEMU dtb name
   QB_AUDIO_DRV: QEMU audio driver (e.g. "alsa", set it when support audio)
   QB_AUDIO_OPT: QEMU audio option (e.g. "-soundhw ac97,es1370"), which is used
                 when QB_AUDIO_DRV is set.
   QB_KERNEL_ROOT: Kernel's root (e.g. /dev/vda)
   QB_TAP_OPT: Network option for 'tap' mode (e.g.
               "-netdev tap,id=net0,ifname=@TAP@,script=no,downscript=no -device virtio-net-device,netdev=net0").
                runqemu will replace "@TAP@" with the one that is used, such as tap0, tap1 ...
   QB_SLIRP_OPT: Network option for SLIRP mode (e.g. "-netdev user,id=net0 -device virtio-net-device,netdev=net0")
   QB_ROOTFS_OPT: Used as rootfs (e.g.
                  "-drive id=disk0,file=@ROOTFS@,if=none,format=raw -device virtio-blk-device,drive=disk0").
                  runqemu will replace "@ROOTFS@" with the one which is used, such as
                  core-image-minimal-qemuarm64.ext4.
   QB_SERIAL_OPT: Serial port (e.g. "-serial mon:stdio")
   QB_TCPSERIAL_OPT: tcp serial port option (e.g.
                     " -device virtio-serial-device -chardev socket,id=virtcon,port=@PORT@,host=127.0.0.1 -device      virtconsole,chardev=virtcon"
                     runqemu will replace "@PORT@" with the port number which is used.

To use ``runqemu``, set :term:`IMAGE_CLASSES` as
follows and run ``runqemu``:

.. note::

   For command-line syntax, use
   runqemu help
   .

::

   IMAGE_CLASSES += "qemuboot"

.. _migration-2.2-default-linker-hash-style-changed:

Default Linker Hash Style Changed
---------------------------------

The default linker hash style for ``gcc-cross`` is now "sysv" in order
to catch recipes that are building software without using the
OpenEmbedded :term:`LDFLAGS`. This change could result in
seeing some "No GNU_HASH in the elf binary" QA issues when building such
recipes. You need to fix these recipes so that they use the expected
``LDFLAGS``. Depending on how the software is built, the build system
used by the software (e.g. a Makefile) might need to be patched.
However, sometimes making this fix is as simple as adding the following
to the recipe:
::

   TARGET_CC_ARCH += "${LDFLAGS}"

.. _migration-2.2-kernel-image-base-name-no-longer-uses-kernel-imagetype:

``KERNEL_IMAGE_BASE_NAME`` no Longer Uses ``KERNEL_IMAGETYPE``
--------------------------------------------------------------

The ``KERNEL_IMAGE_BASE_NAME`` variable no longer uses the
:term:`KERNEL_IMAGETYPE` variable to create the
image's base name. Because the OpenEmbedded build system can now build
multiple kernel image types, this part of the kernel image base name as
been removed leaving only the following:
::

   KERNEL_IMAGE_BASE_NAME ?= "${PKGE}-${PKGV}-${PKGR}-${MACHINE}-${DATETIME}"

If you have recipes or
classes that use ``KERNEL_IMAGE_BASE_NAME`` directly, you might need to
update the references to ensure they continue to work.

.. _migration-2.2-bitbake-changes:

BitBake Changes
---------------

The following changes took place for BitBake:

-  The "goggle" UI and standalone image-writer tool have been removed as
   they both require GTK+ 2.0 and were not being maintained.

-  The Perforce fetcher now supports :term:`SRCREV` for
   specifying the source revision to use, be it
   ``${``\ :term:`AUTOREV`\ ``}``, changelist number,
   p4date, or label, in preference to separate
   :term:`SRC_URI` parameters to specify these. This
   change is more in-line with how the other fetchers work for source
   control systems. Recipes that fetch from Perforce will need to be
   updated to use ``SRCREV`` in place of specifying the source revision
   within ``SRC_URI``.

-  Some of BitBake's internal code structures for accessing the recipe
   cache needed to be changed to support the new multi-configuration
   functionality. These changes will affect external tools that use
   BitBake's tinfoil module. For information on these changes, see the
   changes made to the scripts supplied with OpenEmbedded-Core:
   `1 <http://git.yoctoproject.org/cgit/cgit.cgi/poky/commit/?id=189371f8393971d00bca0fceffd67cc07784f6ee>`__
   and
   `2 <http://git.yoctoproject.org/cgit/cgit.cgi/poky/commit/?id=4a5aa7ea4d07c2c90a1654b174873abb018acc67>`__.

-  The task management code has been rewritten to avoid using ID
   indirection in order to improve performance. This change is unlikely
   to cause any problems for most users. However, the setscene
   verification function as pointed to by
   ``BB_SETSCENE_VERIFY_FUNCTION`` needed to change signature.
   Consequently, a new variable named ``BB_SETSCENE_VERIFY_FUNCTION2``
   has been added allowing multiple versions of BitBake to work with
   suitably written metadata, which includes OpenEmbedded-Core and Poky.
   Anyone with custom BitBake task scheduler code might also need to
   update the code to handle the new structure.

.. _migration-2.2-swabber-has-been-removed:

Swabber has Been Removed
------------------------

Swabber, a tool that was intended to detect host contamination in the
build process, has been removed, as it has been unmaintained and unused
for some time and was never particularly effective. The OpenEmbedded
build system has since incorporated a number of mechanisms including
enhanced QA checks that mean that there is less of a need for such a
tool.

.. _migration-2.2-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed:

-  ``augeas``: No longer needed and has been moved to ``meta-oe``.

-  ``directfb``: Unmaintained and has been moved to ``meta-oe``.

-  ``gcc``: Removed 4.9 version. Versions 5.4 and 6.2 are still present.

-  ``gnome-doc-utils``: No longer needed.

-  ``gtk-doc-stub``: Replaced by ``gtk-doc``.

-  ``gtk-engines``: No longer needed and has been moved to
   ``meta-gnome``.

-  ``gtk-sato-engine``: Became obsolete.

-  ``libglade``: No longer needed and has been moved to ``meta-oe``.

-  ``libmad``: Unmaintained and functionally replaced by ``libmpg123``.
   ``libmad`` has been moved to ``meta-oe``.

-  ``libowl``: Became obsolete.

-  ``libxsettings-client``: No longer needed.

-  ``oh-puzzles``: Functionally replaced by ``puzzles``.

-  ``oprofileui``: Became obsolete. OProfile has been largely supplanted
   by perf.

-  ``packagegroup-core-directfb.bb``: Removed.

-  ``core-image-directfb.bb``: Removed.

-  ``pointercal``: No longer needed and has been moved to ``meta-oe``.

-  ``python-imaging``: No longer needed and moved to ``meta-python``

-  ``python-pyrex``: No longer needed and moved to ``meta-python``.

-  ``sato-icon-theme``: Became obsolete.

-  ``swabber-native``: Swabber has been removed. See the `entry on
   Swabber <#migration-2.2-swabber-has-been-removed>`__.

-  ``tslib``: No longer needed and has been moved to ``meta-oe``.

-  ``uclibc``: Removed in favor of musl.

-  ``xtscal``: No longer needed and moved to ``meta-oe``

.. _migration-2.2-removed-classes:

Removed Classes
---------------

The following classes have been removed:

-  ``distutils-native-base``: No longer needed.

-  ``distutils3-native-base``: No longer needed.

-  ``sdl``: Only set :term:`DEPENDS` and
   :term:`SECTION`, which are better set within the
   recipe instead.

-  ``sip``: Mostly unused.

-  ``swabber``: See the `entry on
   Swabber <#migration-2.2-swabber-has-been-removed>`__.

.. _migration-2.2-minor-packaging-changes:

Minor Packaging Changes
-----------------------

The following minor packaging changes have occurred:

-  ``grub``: Split ``grub-editenv`` into its own package.

-  ``systemd``: Split container and vm related units into a new package,
   systemd-container.

-  ``util-linux``: Moved ``prlimit`` to a separate
   ``util-linux-prlimit`` package.

.. _migration-2.2-miscellaneous-changes:

Miscellaneous Changes
---------------------

The following miscellaneous changes have occurred:

-  ``package_regex.inc``: Removed because the definitions
   ``package_regex.inc`` previously contained have been moved to their
   respective recipes.

-  Both ``devtool add`` and ``recipetool create`` now use a fixed
   :term:`SRCREV` by default when fetching from a Git
   repository. You can override this in either case to use
   ``${``\ :term:`AUTOREV`\ ``}`` instead by using the
   ``-a`` or ``DASHDASHautorev`` command-line option

-  ``distcc``: GTK+ UI is now disabled by default.

-  ``packagegroup-core-tools-testapps``: Removed Piglit.

-  ``image.bbclass``: Renamed COMPRESS(ION) to CONVERSION. This change
   means that ``COMPRESSIONTYPES``, ``COMPRESS_DEPENDS`` and
   ``COMPRESS_CMD`` are deprecated in favor of ``CONVERSIONTYPES``,
   ``CONVERSION_DEPENDS`` and ``CONVERSION_CMD``. The ``COMPRESS*``
   variable names will still work in the 2.2 release but metadata that
   does not need to be backwards-compatible should be changed to use the
   new names as the ``COMPRESS*`` ones will be removed in a future
   release.

-  ``gtk-doc``: A full version of ``gtk-doc`` is now made available.
   However, some old software might not be capable of using the current
   version of ``gtk-doc`` to build documentation. You need to change
   recipes that build such software so that they explicitly disable
   building documentation with ``gtk-doc``.

Moving to the Yocto Project 2.3 Release
=======================================

This section provides migration information for moving to the Yocto
Project 2.3 Release from the prior release.

.. _migration-2.3-recipe-specific-sysroots:

Recipe-specific Sysroots
------------------------

The OpenEmbedded build system now uses one sysroot per recipe to resolve
long-standing issues with configuration script auto-detection of
undeclared dependencies. Consequently, you might find that some of your
previously written custom recipes are missing declared dependencies,
particularly those dependencies that are incidentally built earlier in a
typical build process and thus are already likely to be present in the
shared sysroot in previous releases.

Consider the following:

-  *Declare Build-Time Dependencies:* Because of this new feature, you
   must explicitly declare all build-time dependencies for your recipe.
   If you do not declare these dependencies, they are not populated into
   the sysroot for the recipe.

-  *Specify Pre-Installation and Post-Installation Native Tool
   Dependencies:* You must specifically specify any special native tool
   dependencies of ``pkg_preinst`` and ``pkg_postinst`` scripts by using
   the :term:`PACKAGE_WRITE_DEPS` variable.
   Specifying these dependencies ensures that these tools are available
   if these scripts need to be run on the build host during the
   :ref:`ref-tasks-rootfs` task.

   As an example, see the ``dbus`` recipe. You will see that this recipe
   has a ``pkg_postinst`` that calls ``systemctl`` if "systemd" is in
   :term:`DISTRO_FEATURES`. In the example,
   ``systemd-systemctl-native`` is added to ``PACKAGE_WRITE_DEPS``,
   which is also conditional on "systemd" being in ``DISTRO_FEATURES``.

-  Examine Recipes that Use ``SSTATEPOSTINSTFUNCS``: You need to
   examine any recipe that uses ``SSTATEPOSTINSTFUNCS`` and determine
   steps to take.

   Functions added to ``SSTATEPOSTINSTFUNCS`` are still called as they
   were in previous Yocto Project releases. However, since a separate
   sysroot is now being populated for every recipe and if existing
   functions being called through ``SSTATEPOSTINSTFUNCS`` are doing
   relocation, then you will need to change these to use a
   post-installation script that is installed by a function added to
   :term:`SYSROOT_PREPROCESS_FUNCS`.

   For an example, see the ``pixbufcache`` class in ``meta/classes/`` in
   the :ref:`overview-manual/overview-manual-development-environment:yocto project source repositories`.

   .. note::

      The
      SSTATEPOSTINSTFUNCS
      variable itself is now deprecated in favor of the
      do_populate_sysroot[postfuncs]
      task. Consequently, if you do still have any function or functions
      that need to be called after the sysroot component is created for
      a recipe, then you would be well advised to take steps to use a
      post installation script as described previously. Taking these
      steps prepares your code for when
      SSTATEPOSTINSTFUNCS
      is removed in a future Yocto Project release.

-  *Specify the Sysroot when Using Certain External Scripts:* Because
   the shared sysroot is now gone, the scripts
   ``oe-find-native-sysroot`` and ``oe-run-native`` have been changed
   such that you need to specify which recipe's
   :term:`STAGING_DIR_NATIVE` is used.

.. note::

   You can find more information on how recipe-specific sysroots work in
   the "
   staging.bbclass
   " section.

.. _migration-2.3-path-variable:

``PATH`` Variable
-----------------

Within the environment used to run build tasks, the environment variable
``PATH`` is now sanitized such that the normal native binary paths
(``/bin``, ``/sbin``, ``/usr/bin`` and so forth) are removed and a
directory containing symbolic links linking only to the binaries from
the host mentioned in the :term:`HOSTTOOLS` and
:term:`HOSTTOOLS_NONFATAL` variables is added
to ``PATH``.

Consequently, any native binaries provided by the host that you need to
call needs to be in one of these two variables at the configuration
level.

Alternatively, you can add a native recipe (i.e. ``-native``) that
provides the binary to the recipe's :term:`DEPENDS`
value.

.. note::

   PATH
   is not sanitized in the same way within
   devshell
   . If it were, you would have difficulty running host tools for
   development and debugging within the shell.

.. _migration-2.3-scripts:

Changes to Scripts
------------------

The following changes to scripts took place:

-  ``oe-find-native-sysroot``: The usage for the
   ``oe-find-native-sysroot`` script has changed to the following:
   ::

      $ . oe-find-native-sysroot recipe

   You must now supply a recipe for recipe
   as part of the command. Prior to the Yocto Project &DISTRO; release, it
   was not necessary to provide the script with the command.

-  ``oe-run-native``: The usage for the ``oe-run-native`` script has
   changed to the following:
   ::

      $ oe-run-native native_recipe tool

   You must
   supply the name of the native recipe and the tool you want to run as
   part of the command. Prior to the Yocto Project DISTRO release, it
   was not necessary to provide the native recipe with the command.

-  ``cleanup-workdir``: The ``cleanup-workdir`` script has been
   removed because the script was found to be deleting files it should
   not have, which lead to broken build trees. Rather than trying to
   delete portions of :term:`TMPDIR` and getting it wrong,
   it is recommended that you delete ``TMPDIR`` and have it restored
   from shared state (sstate) on subsequent builds.

-  ``wipe-sysroot``: The ``wipe-sysroot`` script has been removed as
   it is no longer needed with recipe-specific sysroots.

.. _migration-2.3-functions:

Changes to Functions
--------------------

The previously deprecated ``bb.data.getVar()``, ``bb.data.setVar()``,
and related functions have been removed in favor of ``d.getVar()``,
``d.setVar()``, and so forth.

You need to fix any references to these old functions.

.. _migration-2.3-bitbake-changes:

BitBake Changes
---------------

The following changes took place for BitBake:

-  *BitBake's Graphical Dependency Explorer UI Replaced:* BitBake's
   graphical dependency explorer UI ``depexp`` was replaced by
   ``taskexp`` ("Task Explorer"), which provides a graphical way of
   exploring the ``task-depends.dot`` file. The data presented by Task
   Explorer is much more accurate than the data that was presented by
   ``depexp``. Being able to visualize the data is an often requested
   feature as standard ``*.dot`` file viewers cannot usual cope with the
   size of the ``task-depends.dot`` file.

-  *BitBake "-g" Output Changes:* The ``package-depends.dot`` and
   ``pn-depends.dot`` files as previously generated using the
   ``bitbake -g`` command have been removed. A ``recipe-depends.dot``
   file is now generated as a collapsed version of ``task-depends.dot``
   instead.

   The reason for this change is because ``package-depends.dot`` and
   ``pn-depends.dot`` largely date back to a time before task-based
   execution and do not take into account task-level dependencies
   between recipes, which could be misleading.

-  *Mirror Variable Splitting Changes:* Mirror variables including
   :term:`MIRRORS`, :term:`PREMIRRORS`,
   and :term:`SSTATE_MIRRORS` can now separate
   values entirely with spaces. Consequently, you no longer need "\\n".
   BitBake looks for pairs of values, which simplifies usage. There
   should be no change required to existing mirror variable values
   themselves.

-  *The Subversion (SVN) Fetcher Uses an "ssh" Parameter and Not an
   "rsh" Parameter:* The SVN fetcher now takes an "ssh" parameter
   instead of an "rsh" parameter. This new optional parameter is used
   when the "protocol" parameter is set to "svn+ssh". You can only use
   the new parameter to specify the ``ssh`` program used by SVN. The SVN
   fetcher passes the new parameter through the ``SVN_SSH`` environment
   variable during the :ref:`ref-tasks-fetch` task.

   See the ":ref:`bitbake:svn-fetcher`"
   section in the BitBake
   User Manual for additional information.

-  ``BB_SETSCENE_VERIFY_FUNCTION`` and ``BB_SETSCENE_VERIFY_FUNCTION2``
   Removed: Because the mechanism they were part of is no longer
   necessary with recipe-specific sysroots, the
   ``BB_SETSCENE_VERIFY_FUNCTION`` and ``BB_SETSCENE_VERIFY_FUNCTION2``
   variables have been removed.

.. _migration-2.3-absolute-symlinks:

Absolute Symbolic Links
-----------------------

Absolute symbolic links (symlinks) within staged files are no longer
permitted and now trigger an error. Any explicit creation of symlinks
can use the ``lnr`` script, which is a replacement for ``ln -r``.

If the build scripts in the software that the recipe is building are
creating a number of absolute symlinks that need to be corrected, you
can inherit ``relative_symlinks`` within the recipe to turn those
absolute symlinks into relative symlinks.

.. _migration-2.3-gplv2-and-gplv3-moves:

GPLv2 Versions of GPLv3 Recipes Moved
-------------------------------------

Older GPLv2 versions of GPLv3 recipes have moved to a separate
``meta-gplv2`` layer.

If you use :term:`INCOMPATIBLE_LICENSE` to
exclude GPLv3 or set :term:`PREFERRED_VERSION`
to substitute a GPLv2 version of a GPLv3 recipe, then you must add the
``meta-gplv2`` layer to your configuration.

.. note::

   You can find
   meta-gplv2
   layer in the OpenEmbedded layer index at
   .

These relocated GPLv2 recipes do not receive the same level of
maintenance as other core recipes. The recipes do not get security fixes
and upstream no longer maintains them. In fact, the upstream community
is actively hostile towards people that use the old versions of the
recipes. Moving these recipes into a separate layer both makes the
different needs of the recipes clearer and clearly identifies the number
of these recipes.

.. note::

   The long-term solution might be to move to BSD-licensed replacements
   of the GPLv3 components for those that need to exclude GPLv3-licensed
   components from the target system. This solution will be investigated
   for future Yocto Project releases.

.. _migration-2.3-package-management-changes:

Package Management Changes
--------------------------

The following package management changes took place:

-  Smart package manager is replaced by DNF package manager. Smart has
   become unmaintained upstream, is not ported to Python 3.x.
   Consequently, Smart needed to be replaced. DNF is the only feasible
   candidate.

   The change in functionality is that the on-target runtime package
   management from remote package feeds is now done with a different
   tool that has a different set of command-line options. If you have
   scripts that call the tool directly, or use its API, they need to be
   fixed.

   For more information, see the `DNF
   Documentation <http://dnf.readthedocs.io/en/latest/>`__.

-  Rpm 5.x is replaced with Rpm 4.x. This is done for two major reasons:

   -  DNF is API-incompatible with Rpm 5.x and porting it and
      maintaining the port is non-trivial.

   -  Rpm 5.x itself has limited maintenance upstream, and the Yocto
      Project is one of the very few remaining users.

-  Berkeley DB 6.x is removed and Berkeley DB 5.x becomes the default:

   -  Version 6.x of Berkeley DB has largely been rejected by the open
      source community due to its AGPLv3 license. As a result, most
      mainstream open source projects that require DB are still
      developed and tested with DB 5.x.

   -  In OE-core, the only thing that was requiring DB 6.x was Rpm 5.x.
      Thus, no reason exists to continue carrying DB 6.x in OE-core.

-  ``createrepo`` is replaced with ``createrepo_c``.

   ``createrepo_c`` is the current incarnation of the tool that
   generates remote repository metadata. It is written in C as compared
   to ``createrepo``, which is written in Python. ``createrepo_c`` is
   faster and is maintained.

-  Architecture-independent RPM packages are "noarch" instead of "all".

   This change was made because too many places in DNF/RPM4 stack
   already make that assumption. Only the filenames and the architecture
   tag has changed. Nothing else has changed in OE-core system,
   particularly in the :ref:`allarch.bbclass <ref-classes-allarch>`
   class.

-  Signing of remote package feeds using ``PACKAGE_FEED_SIGN`` is not
   currently supported. This issue will be fully addressed in a future
   Yocto Project release. See `defect
   11209 <https://bugzilla.yoctoproject.org/show_bug.cgi?id=11209>`__
   for more information on a solution to package feed signing with RPM
   in the Yocto Project 2.3 release.

-  OPKG now uses the libsolv backend for resolving package dependencies
   by default. This is vastly superior to OPKG's internal ad-hoc solver
   that was previously used. This change does have a small impact on
   disk (around 500 KB) and memory footprint.

   .. note::

      For further details on this change, see the
      commit message
      .

.. _migration-2.3-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed:

-  ``linux-yocto 4.8``: Version 4.8 has been removed. Versions 4.1
   (LTSI), 4.4 (LTS), 4.9 (LTS/LTSI) and 4.10 are now present.

-  ``python-smartpm``: Functionally replaced by ``dnf``.

-  ``createrepo``: Replaced by the ``createrepo-c`` recipe.

-  ``rpmresolve``: No longer needed with the move to RPM 4 as RPM
   itself is used instead.

-  ``gstreamer``: Removed the GStreamer Git version recipes as they
   have been stale. ``1.10.``\ x recipes are still present.

-  ``alsa-conf-base``: Merged into ``alsa-conf`` since ``libasound``
   depended on both. Essentially, no way existed to install only one of
   these.

-  ``tremor``: Moved to ``meta-multimedia``. Fixed-integer Vorbis
   decoding is not needed by current hardware. Thus, GStreamer's ivorbis
   plugin has been disabled by default eliminating the need for the
   ``tremor`` recipe in :term:`OpenEmbedded-Core (OE-Core)`.

-  ``gummiboot``: Replaced by ``systemd-boot``.

.. _migration-2.3-wic-changes:

Wic Changes
-----------

The following changes have been made to Wic:

.. note::

   For more information on Wic, see the "
   Creating Partitioned Images Using Wic
   " section in the Yocto Project Development Tasks Manual.

-  *Default Output Directory Changed:* Wic's default output directory is
   now the current directory by default instead of the unusual
   ``/var/tmp/wic``.

   The "-o" and "--outdir" options remain unchanged and are used to
   specify your preferred output directory if you do not want to use the
   default directory.

-  *fsimage Plug-in Removed:* The Wic fsimage plugin has been removed as
   it duplicates functionality of the rawcopy plugin.

.. _migration-2.3-qa-changes:

QA Changes
----------

The following QA checks have changed:

-  ``unsafe-references-in-binaries``: The
   ``unsafe-references-in-binaries`` QA check, which was disabled by
   default, has now been removed. This check was intended to detect
   binaries in ``/bin`` that link to libraries in ``/usr/lib`` and have
   the case where the user has ``/usr`` on a separate filesystem to
   ``/``.

   The removed QA check was buggy. Additionally, ``/usr`` residing on a
   separate partition from ``/`` is now a rare configuration.
   Consequently, ``unsafe-references-in-binaries`` was removed.

-  ``file-rdeps``: The ``file-rdeps`` QA check is now an error by
   default instead of a warning. Because it is an error instead of a
   warning, you need to address missing runtime dependencies.

   For additional information, see the
   :ref:`insane <ref-classes-insane>` class and the "`Errors and
   Warnings <#qa-errors-and-warnings>`__" section.

.. _migration-2.3-miscellaneous-changes:

Miscellaneous Changes
---------------------

The following miscellaneous changes have occurred:

-  In this release, a number of recipes have been changed to ignore the
   ``largefile`` :term:`DISTRO_FEATURES` item,
   enabling large file support unconditionally. This feature has always
   been enabled by default. Disabling the feature has not been widely
   tested.

   .. note::

      Future releases of the Yocto Project will remove entirely the
      ability to disable the
      largefile
      feature, which would make it unconditionally enabled everywhere.

-  If the :term:`DISTRO_VERSION` value contains
   the value of the :term:`DATE` variable, which is the
   default between Poky releases, the ``DATE`` value is explicitly
   excluded from ``/etc/issue`` and ``/etc/issue.net``, which is
   displayed at the login prompt, in order to avoid conflicts with
   Multilib enabled. Regardless, the ``DATE`` value is inaccurate if the
   ``base-files`` recipe is restored from shared state (sstate) rather
   than rebuilt.

   If you need the build date recorded in ``/etc/issue*`` or anywhere
   else in your image, a better method is to define a post-processing
   function to do it and have the function called from
   :term:`ROOTFS_POSTPROCESS_COMMAND`.
   Doing so ensures the value is always up-to-date with the created
   image.

-  Dropbear's ``init`` script now disables DSA host keys by default.
   This change is in line with the systemd service file, which supports
   RSA keys only, and with recent versions of OpenSSH, which deprecates
   DSA host keys.

-  The :ref:`buildhistory <ref-classes-buildhistory>` class now
   correctly uses tabs as separators between all columns in
   ``installed-package-sizes.txt`` in order to aid import into other
   tools.

-  The ``USE_LDCONFIG`` variable has been replaced with the "ldconfig"
   ``DISTRO_FEATURES`` feature. Distributions that previously set:
   ::

      USE_LDCONFIG = "0"

   should now instead use the following:

   ::

      DISTRO_FEATURES_BACKFILL_CONSIDERED_append = " ldconfig"

-  The default value of
   :term:`COPYLEFT_LICENSE_INCLUDE` now
   includes all versions of AGPL licenses in addition to GPL and LGPL.

   .. note::

      The default list is not intended to be guaranteed as a complete
      safe list. You should seek legal advice based on what you are
      distributing if you are unsure.

-  Kernel module packages are now suffixed with the kernel version in
   order to allow module packages from multiple kernel versions to
   co-exist on a target system. If you wish to return to the previous
   naming scheme that does not include the version suffix, use the
   following:
   ::

      KERNEL_MODULE_PACKAGE_SUFFIX to ""

-  Removal of ``libtool`` ``*.la`` files is now enabled by default. The
   ``*.la`` files are not actually needed on Linux and relocating them
   is an unnecessary burden.

   If you need to preserve these ``.la`` files (e.g. in a custom
   distribution), you must change
   :term:`INHERIT_DISTRO` such that
   "remove-libtool" is not included in the value.

-  Extensible SDKs built for GCC 5+ now refuse to install on a
   distribution where the host GCC version is 4.8 or 4.9. This change
   resulted from the fact that the installation is known to fail due to
   the way the ``uninative`` shared state (sstate) package is built. See
   the :ref:`uninative <ref-classes-uninative>` class for additional
   information.

-  All native and nativesdk recipes now use a separate
   ``DISTRO_FEATURES`` value instead of sharing the value used by
   recipes for the target, in order to avoid unnecessary rebuilds.

   The ``DISTRO_FEATURES`` for ``native`` recipes is
   :term:`DISTRO_FEATURES_NATIVE` added to
   an intersection of ``DISTRO_FEATURES`` and
   :term:`DISTRO_FEATURES_FILTER_NATIVE`.

   For nativesdk recipes, the corresponding variables are
   :term:`DISTRO_FEATURES_NATIVESDK`
   and
   :term:`DISTRO_FEATURES_FILTER_NATIVESDK`.

-  The ``FILESDIR`` variable, which was previously deprecated and rarely
   used, has now been removed. You should change any recipes that set
   ``FILESDIR`` to set :term:`FILESPATH` instead.

-  The ``MULTIMACH_HOST_SYS`` variable has been removed as it is no
   longer needed with recipe-specific sysroots.

Moving to the Yocto Project 2.4 Release
=======================================

This section provides migration information for moving to the Yocto
Project 2.4 Release from the prior release.

.. _migration-2.4-memory-resident-mode:

Memory Resident Mode
--------------------

A persistent mode is now available in BitBake's default operation,
replacing its previous "memory resident mode" (i.e.
``oe-init-build-env-memres``). Now you only need to set
:term:`BB_SERVER_TIMEOUT` to a timeout (in
seconds) and BitBake's server stays resident for that amount of time
between invocations. The ``oe-init-build-env-memres`` script has been
removed since a separate environment setup script is no longer needed.

.. _migration-2.4-packaging-changes:

Packaging Changes
-----------------

This section provides information about packaging changes that have
occurred:

-  ``python3`` Changes:

   -  The main "python3" package now brings in all of the standard
      Python 3 distribution rather than a subset. This behavior matches
      what is expected based on traditional Linux distributions. If you
      wish to install a subset of Python 3, specify ``python-core`` plus
      one or more of the individual packages that are still produced.

   -  ``python3``: The ``bz2.py``, ``lzma.py``, and
      ``_compression.py`` scripts have been moved from the
      ``python3-misc`` package to the ``python3-compression`` package.

-  ``binutils``: The ``libbfd`` library is now packaged in a separate
   "libbfd" package. This packaging saves space when certain tools (e.g.
   ``perf``) are installed. In such cases, the tools only need
   ``libbfd`` rather than all the packages in ``binutils``.

-  ``util-linux`` Changes:

   -  The ``su`` program is now packaged in a separate "util-linux-su"
      package, which is only built when "pam" is listed in the
      :term:`DISTRO_FEATURES` variable.
      ``util-linux`` should not be installed unless it is needed because
      ``su`` is normally provided through the shadow file format. The
      main ``util-linux`` package has runtime dependencies (i.e.
      :term:`RDEPENDS`) on the ``util-linux-su`` package
      when "pam" is in ``DISTRO_FEATURES``.

   -  The ``switch_root`` program is now packaged in a separate
      "util-linux-switch-root" package for small initramfs images that
      do not need the whole ``util-linux`` package or the busybox
      binary, which are both much larger than ``switch_root``. The main
      ``util-linux`` package has a recommended runtime dependency (i.e.
      :term:`RRECOMMENDS`) on the
      ``util-linux-switch-root`` package.

   -  The ``ionice`` program is now packaged in a separate
      "util-linux-ionice" package. The main ``util-linux`` package has a
      recommended runtime dependency (i.e. ``RRECOMMENDS``) on the
      ``util-linux-ionice`` package.

-  ``initscripts``: The ``sushell`` program is now packaged in a
   separate "initscripts-sushell" package. This packaging change allows
   systems to pull ``sushell`` in when ``selinux`` is enabled. The
   change also eliminates needing to pull in the entire ``initscripts``
   package. The main ``initscripts`` package has a runtime dependency
   (i.e. ``RDEPENDS``) on the ``sushell`` package when "selinux" is in
   ``DISTRO_FEATURES``.

-  ``glib-2.0``: The ``glib-2.0`` package now has a recommended
   runtime dependency (i.e. ``RRECOMMENDS``) on the ``shared-mime-info``
   package, since large portions of GIO are not useful without the MIME
   database. You can remove the dependency by using the
   :term:`BAD_RECOMMENDATIONS` variable if
   ``shared-mime-info`` is too large and is not required.

-  *Go Standard Runtime:* The Go standard runtime has been split out
   from the main ``go`` recipe into a separate ``go-runtime`` recipe.

.. _migration-2.4-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed:

-  ``acpitests``: This recipe is not maintained.

-  ``autogen-native``: No longer required by Grub, oe-core, or
   meta-oe.

-  ``bdwgc``: Nothing in OpenEmbedded-Core requires this recipe. It
   has moved to meta-oe.

-  ``byacc``: This recipe was only needed by rpm 5.x and has moved to
   meta-oe.

-  ``gcc (5.4)``: The 5.4 series dropped the recipe in favor of 6.3 /
   7.2.

-  ``gnome-common``: Deprecated upstream and no longer needed.

-  ``go-bootstrap-native``: Go 1.9 does its own bootstrapping so this
   recipe has been removed.

-  ``guile``: This recipe was only needed by ``autogen-native`` and
   ``remake``. The recipe is no longer needed by either of these
   programs.

-  ``libclass-isa-perl``: This recipe was previously needed for LSB 4,
   no longer needed.

-  ``libdumpvalue-perl``: This recipe was previously needed for LSB 4,
   no longer needed.

-  ``libenv-perl``: This recipe was previously needed for LSB 4, no
   longer needed.

-  ``libfile-checktree-perl``: This recipe was previously needed for
   LSB 4, no longer needed.

-  ``libi18n-collate-perl``: This recipe was previously needed for LSB
   4, no longer needed.

-  ``libiconv``: This recipe was only needed for ``uclibc``, which was
   removed in the previous release. ``glibc`` and ``musl`` have their
   own implementations. ``meta-mingw`` still needs ``libiconv``, so it
   has been moved to ``meta-mingw``.

-  ``libpng12``: This recipe was previously needed for LSB. The
   current ``libpng`` is 1.6.x.

-  ``libpod-plainer-perl``: This recipe was previously needed for LSB
   4, no longer needed.

-  ``linux-yocto (4.1)``: This recipe was removed in favor of 4.4,
   4.9, 4.10 and 4.12.

-  ``mailx``: This recipe was previously only needed for LSB
   compatibility, and upstream is defunct.

-  ``mesa (git version only)``: The git version recipe was stale with
   respect to the release version.

-  ``ofono (git version only)``: The git version recipe was stale with
   respect to the release version.

-  ``portmap``: This recipe is obsolete and is superseded by
   ``rpcbind``.

-  ``python3-pygpgme``: This recipe is old and unmaintained. It was
   previously required by ``dnf``, which has switched to official
   ``gpgme`` Python bindings.

-  ``python-async``: This recipe has been removed in favor of the
   Python 3 version.

-  ``python-gitdb``: This recipe has been removed in favor of the
   Python 3 version.

-  ``python-git``: This recipe was removed in favor of the Python 3
   version.

-  ``python-mako``: This recipe was removed in favor of the Python 3
   version.

-  ``python-pexpect``: This recipe was removed in favor of the Python
   3 version.

-  ``python-ptyprocess``: This recipe was removed in favor of Python
   the 3 version.

-  ``python-pycurl``: Nothing is using this recipe in
   OpenEmbedded-Core (i.e. ``meta-oe``).

-  ``python-six``: This recipe was removed in favor of the Python 3
   version.

-  ``python-smmap``: This recipe was removed in favor of the Python 3
   version.

-  ``remake``: Using ``remake`` as the provider of ``virtual/make`` is
   broken. Consequently, this recipe is not needed in OpenEmbedded-Core.

.. _migration-2.4-kernel-device-tree-move:

Kernel Device Tree Move
-----------------------

Kernel Device Tree support is now easier to enable in a kernel recipe.
The Device Tree code has moved to a
:ref:`kernel-devicetree <ref-classes-kernel-devicetree>` class.
Functionality is automatically enabled for any recipe that inherits the
:ref:`kernel <ref-classes-kernel>` class and sets the
:term:`KERNEL_DEVICETREE` variable. The
previous mechanism for doing this,
``meta/recipes-kernel/linux/linux-dtb.inc``, is still available to avoid
breakage, but triggers a deprecation warning. Future releases of the
Yocto Project will remove ``meta/recipes-kernel/linux/linux-dtb.inc``.
It is advisable to remove any ``require`` statements that request
``meta/recipes-kernel/linux/linux-dtb.inc`` from any custom kernel
recipes you might have. This will avoid breakage in post 2.4 releases.

.. _migration-2.4-package-qa-changes:

Package QA Changes
------------------

The following package QA changes took place:

-  The "unsafe-references-in-scripts" QA check has been removed.

-  If you refer to ``${COREBASE}/LICENSE`` within
   :term:`LIC_FILES_CHKSUM` you receive a
   warning because this file is a description of the license for
   OE-Core. Use ``${COMMON_LICENSE_DIR}/MIT`` if your recipe is
   MIT-licensed and you cannot use the preferred method of referring to
   a file within the source tree.

.. _migration-2.4-readme-changes:

``README`` File Changes
-----------------------

The following are changes to ``README`` files:

-  The main Poky ``README`` file has been moved to the ``meta-poky``
   layer and has been renamed ``README.poky``. A symlink has been
   created so that references to the old location work.

-  The ``README.hardware`` file has been moved to ``meta-yocto-bsp``. A
   symlink has been created so that references to the old location work.

-  A ``README.qemu`` file has been created with coverage of the
   ``qemu*`` machines.

.. _migration-2.4-miscellaneous-changes:

Miscellaneous Changes
---------------------

The following are additional changes:

-  The ``ROOTFS_PKGMANAGE_BOOTSTRAP`` variable and any references to it
   have been removed. You should remove this variable from any custom
   recipes.

-  The ``meta-yocto`` directory has been removed.

   .. note::

      In the Yocto Project 2.1 release
      meta-yocto
      was renamed to
      meta-poky
      and the
      meta-yocto
      subdirectory remained to avoid breaking existing configurations.

-  The ``maintainers.inc`` file, which tracks maintainers by listing a
   primary person responsible for each recipe in OE-Core, has been moved
   from ``meta-poky`` to OE-Core (i.e. from
   ``meta-poky/conf/distro/include`` to ``meta/conf/distro/include``).

-  The :ref:`buildhistory <ref-classes-buildhistory>` class now makes
   a single commit per build rather than one commit per subdirectory in
   the repository. This behavior assumes the commits are enabled with
   :term:`BUILDHISTORY_COMMIT` = "1", which
   is typical. Previously, the ``buildhistory`` class made one commit
   per subdirectory in the repository in order to make it easier to see
   the changes for a particular subdirectory. To view a particular
   change, specify that subdirectory as the last parameter on the
   ``git show`` or ``git diff`` commands.

-  The ``x86-base.inc`` file, which is included by all x86-based machine
   configurations, now sets :term:`IMAGE_FSTYPES`
   using ``?=`` to "live" rather than appending with ``+=``. This change
   makes the default easier to override.

-  BitBake fires multiple "BuildStarted" events when multiconfig is
   enabled (one per configuration). For more information, see the
   ":ref:`Events <bitbake:bitbake-user-manual/bitbake-user-manual-metadata:events>`" section in the BitBake User
   Manual.

-  By default, the ``security_flags.inc`` file sets a
   :term:`GCCPIE` variable with an option to enable
   Position Independent Executables (PIE) within ``gcc``. Enabling PIE
   in the GNU C Compiler (GCC), makes Return Oriented Programming (ROP)
   attacks much more difficult to execute.

-  OE-Core now provides a ``bitbake-layers`` plugin that implements a
   "create-layer" subcommand. The implementation of this subcommand has
   resulted in the ``yocto-layer`` script being deprecated and will
   likely be removed in the next Yocto Project release.

-  The ``vmdk``, ``vdi``, and ``qcow2`` image file types are now used in
   conjunction with the "wic" image type through ``CONVERSION_CMD``.
   Consequently, the equivalent image types are now ``wic.vmdk``,
   ``wic.vdi``, and ``wic.qcow2``, respectively.

-  ``do_image_<type>[depends]`` has replaced ``IMAGE_DEPENDS_<type>``.
   If you have your own classes that implement custom image types, then
   you need to update them.

-  OpenSSL 1.1 has been introduced. However, the default is still 1.0.x
   through the :term:`PREFERRED_VERSION`
   variable. This preference is set is due to the remaining
   compatibility issues with other software. The
   :term:`PROVIDES` variable in the openssl 1.0 recipe
   now includes "openssl10" as a marker that can be used in
   :term:`DEPENDS` within recipes that build software
   that still depend on OpenSSL 1.0.

-  To ensure consistent behavior, BitBake's "-r" and "-R" options (i.e.
   prefile and postfile), which are used to read or post-read additional
   configuration files from the command line, now only affect the
   current BitBake command. Before these BitBake changes, these options
   would "stick" for future executions.

Moving to the Yocto Project 2.5 Release
=======================================

This section provides migration information for moving to the Yocto
Project 2.5 Release from the prior release.

.. _migration-2.5-packaging-changes:

Packaging Changes
-----------------

This section provides information about packaging changes that have
occurred:

-  ``bind-libs``: The libraries packaged by the bind recipe are in a
   separate ``bind-libs`` package.

-  ``libfm-gtk``: The ``libfm`` GTK+ bindings are split into a
   separate ``libfm-gtk`` package.

-  ``flex-libfl``: The flex recipe splits out libfl into a separate
   ``flex-libfl`` package to avoid too many dependencies being pulled in
   where only the library is needed.

-  ``grub-efi``: The ``grub-efi`` configuration is split into a
   separate ``grub-bootconf`` recipe. However, the dependency
   relationship from ``grub-efi`` is through a virtual/grub-bootconf
   provider making it possible to have your own recipe provide the
   dependency. Alternatively, you can use a BitBake append file to bring
   the configuration back into the ``grub-efi`` recipe.

-  *armv7a Legacy Package Feed Support:* Legacy support is removed for
   transitioning from ``armv7a`` to ``armv7a-vfp-neon`` in package
   feeds, which was previously enabled by setting
   ``PKGARCHCOMPAT_ARMV7A``. This transition occurred in 2011 and active
   package feeds should by now be updated to the new naming.

.. _migration-2.5-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed:

-  ``gcc``: The version 6.4 recipes are replaced by 7.x.

-  ``gst-player``: Renamed to ``gst-examples`` as per upstream.

-  ``hostap-utils``: This software package is obsolete.

-  ``latencytop``: This recipe is no longer maintained upstream. The
   last release was in 2009.

-  ``libpfm4``: The only file that requires this recipe is
   ``oprofile``, which has been removed.

-  ``linux-yocto``: The version 4.4, 4.9, and 4.10 recipes have been
   removed. Versions 4.12, 4.14, and 4.15 remain.

-  ``man``: This recipe has been replaced by modern ``man-db``

-  ``mkelfimage``: This tool has been removed in the upstream coreboot
   project, and is no longer needed with the removal of the ELF image
   type.

-  ``nativesdk-postinst-intercept``: This recipe is not maintained.

-  ``neon``: This software package is no longer maintained upstream
   and is no longer needed by anything in OpenEmbedded-Core.

-  ``oprofile``: The functionality of this recipe is replaced by
   ``perf`` and keeping compatibility on an ongoing basis with ``musl``
   is difficult.

-  ``pax``: This software package is obsolete.

-  ``stat``: This software package is not maintained upstream.
   ``coreutils`` provides a modern stat binary.

-  ``zisofs-tools-native``: This recipe is no longer needed because
   the compressed ISO image feature has been removed.

.. _migration-2.5-scripts-and-tools-changes:

Scripts and Tools Changes
-------------------------

The following are changes to scripts and tools:

-  ``yocto-bsp``, ``yocto-kernel``, and ``yocto-layer``: The
   ``yocto-bsp``, ``yocto-kernel``, and ``yocto-layer`` scripts
   previously shipped with poky but not in OpenEmbedded-Core have been
   removed. These scripts are not maintained and are outdated. In many
   cases, they are also limited in scope. The
   ``bitbake-layers create-layer`` command is a direct replacement for
   ``yocto-layer``. See the documentation to create a BSP or kernel
   recipe in the ":ref:`bsp-guide/bsp:bsp kernel recipe example`" section.

-  ``devtool finish``: ``devtool finish`` now exits with an error if
   there are uncommitted changes or a rebase/am in progress in the
   recipe's source repository. If this error occurs, there might be
   uncommitted changes that will not be included in updates to the
   patches applied by the recipe. A -f/--force option is provided for
   situations that the uncommitted changes are inconsequential and you
   want to proceed regardless.

-  ``scripts/oe-setup-rpmrepo`` script: The functionality of
   ``scripts/oe-setup-rpmrepo`` is replaced by
   ``bitbake package-index``.

-  ``scripts/test-dependencies.sh`` script: The script is largely made
   obsolete by the recipe-specific sysroots functionality introduced in
   the previous release.

.. _migration-2.5-bitbake-changes:

BitBake Changes
---------------

The following are BitBake changes:

-  The ``--runall`` option has changed. There are two different
   behaviors people might want:

   -  *Behavior A:* For a given target (or set of targets) look through
      the task graph and run task X only if it is present and will be
      built.

   -  *Behavior B:* For a given target (or set of targets) look through
      the task graph and run task X if any recipe in the taskgraph has
      such a target, even if it is not in the original task graph.

   The ``--runall`` option now performs "Behavior B". Previously
   ``--runall`` behaved like "Behavior A". A ``--runonly`` option has
   been added to retain the ability to perform "Behavior A".

-  Several explicit "run this task for all recipes in the dependency
   tree" tasks have been removed (e.g. ``fetchall``, ``checkuriall``,
   and the ``*all`` tasks provided by the ``distrodata`` and
   ``archiver`` classes). There is a BitBake option to complete this for
   any arbitrary task. For example:
   ::

      bitbake <target> -c fetchall

   should now be replaced with:
   ::

      bitbake <target> --runall=fetch

.. _migration-2.5-python-and-python3-changes:

Python and Python 3 Changes
---------------------------

The following are auto-packaging changes to Python and Python 3:

The script-managed ``python-*-manifest.inc`` files that were previously
used to generate Python and Python 3 packages have been replaced with a
JSON-based file that is easier to read and maintain. A new task is
available for maintainers of the Python recipes to update the JSON file
when upgrading to new Python versions. You can now edit the file
directly instead of having to edit a script and run it to update the
file.

One particular change to note is that the Python recipes no longer have
build-time provides for their packages. This assumes ``python-foo`` is
one of the packages provided by the Python recipe. You can no longer run
``bitbake python-foo`` or have a
:term:`DEPENDS` on ``python-foo``,
but doing either of the following causes the package to work as
expected: ::

   IMAGE_INSTALL_append = " python-foo"

or ::

   RDEPENDS_${PN} = "python-foo"

The earlier build-time provides behavior was a quirk of the
way the Python manifest file was created. For more information on this
change please see `this
commit <http://git.yoctoproject.org/cgit/cgit.cgi/poky/commit/?id=8d94b9db221d1def42f091b991903faa2d1651ce>`__.

.. _migration-2.5-miscellaneous-changes:

Miscellaneous Changes
---------------------

The following are additional changes:

-  The ``kernel`` class supports building packages for multiple kernels.
   If your kernel recipe or ``.bbappend`` file mentions packaging at
   all, you should replace references to the kernel in package names
   with ``${KERNEL_PACKAGE_NAME}``. For example, if you disable
   automatic installation of the kernel image using
   ``RDEPENDS_kernel-base = ""`` you can avoid warnings using
   ``RDEPENDS_${KERNEL_PACKAGE_NAME}-base = ""`` instead.

-  The ``buildhistory`` class commits changes to the repository by
   default so you no longer need to set ``BUILDHISTORY_COMMIT = "1"``.
   If you want to disable commits you need to set
   ``BUILDHISTORY_COMMIT = "0"`` in your configuration.

-  The ``beaglebone`` reference machine has been renamed to
   ``beaglebone-yocto``. The ``beaglebone-yocto`` BSP is a reference
   implementation using only mainline components available in
   OpenEmbedded-Core and ``meta-yocto-bsp``, whereas Texas Instruments
   maintains a full-featured BSP in the ``meta-ti`` layer. This rename
   avoids the previous name clash that existed between the two BSPs.

-  The ``update-alternatives`` class no longer works with SysV ``init``
   scripts because this usage has been problematic. Also, the
   ``sysklogd`` recipe no longer uses ``update-alternatives`` because it
   is incompatible with other implementations.

-  By default, the :ref:`cmake <ref-classes-cmake>` class uses
   ``ninja`` instead of ``make`` for building. This improves build
   performance. If a recipe is broken with ``ninja``, then the recipe
   can set ``OECMAKE_GENERATOR = "Unix Makefiles"`` to change back to
   ``make``.

-  The previously deprecated ``base_*`` functions have been removed in
   favor of their replacements in ``meta/lib/oe`` and
   ``bitbake/lib/bb``. These are typically used from recipes and
   classes. Any references to the old functions must be updated. The
   following table shows the removed functions and their replacements:

   +------------------------------+----------------------------------------------------------+
   | *Removed*                    | *Replacement*                                            |
   +==============================+==========================================================+
   | base_path_join()             | oe.path.join()                                           |
   +------------------------------+----------------------------------------------------------+
   | base_path_relative()         | oe.path.relative()                                       |
   +------------------------------+----------------------------------------------------------+
   | base_path_out()              | oe.path.format_display()                                 |
   +------------------------------+----------------------------------------------------------+
   | base_read_file()             | oe.utils.read_file()                                     |
   +------------------------------+----------------------------------------------------------+
   | base_ifelse()                | oe.utils.ifelse()                                        |
   +------------------------------+----------------------------------------------------------+
   | base_conditional()           | oe.utils.conditional()                                   |
   +------------------------------+----------------------------------------------------------+
   | base_less_or_equal()         | oe.utils.less_or_equal()                                 |
   +------------------------------+----------------------------------------------------------+
   | base_version_less_or_equal() | oe.utils.version_less_or_equal()                         |
   +------------------------------+----------------------------------------------------------+
   | base_contains()              | bb.utils.contains()                                      |
   +------------------------------+----------------------------------------------------------+
   | base_both_contain()          | oe.utils.both_contain()                                  |
   +------------------------------+----------------------------------------------------------+
   | base_prune_suffix()          | oe.utils.prune_suffix()                                  |
   +------------------------------+----------------------------------------------------------+
   | oe_filter()                  | oe.utils.str_filter()                                    |
   +------------------------------+----------------------------------------------------------+
   | oe_filter_out()              | oe.utils.str_filter_out() (or use the \_remove operator) |
   +------------------------------+----------------------------------------------------------+

-  Using ``exit 1`` to explicitly defer a postinstall script until first
   boot is now deprecated since it is not an obvious mechanism and can
   mask actual errors. If you want to explicitly defer a postinstall to
   first boot on the target rather than at ``rootfs`` creation time, use
   ``pkg_postinst_ontarget()`` or call
   ``postinst_intercept delay_to_first_boot`` from ``pkg_postinst()``.
   Any failure of a ``pkg_postinst()`` script (including ``exit 1``)
   will trigger a warning during ``do_rootfs``.

   For more information, see the
   ":ref:`dev-manual/dev-manual-common-tasks:post-installation scripts`"
   section in the Yocto Project Development Tasks Manual.

-  The ``elf`` image type has been removed. This image type was removed
   because the ``mkelfimage`` tool that was required to create it is no
   longer provided by coreboot upstream and required updating every time
   ``binutils`` updated.

-  Support for .iso image compression (previously enabled through
   ``COMPRESSISO = "1"``) has been removed. The userspace tools
   (``zisofs-tools``) are unmaintained and ``squashfs`` provides better
   performance and compression. In order to build a live image with
   squashfs+lz4 compression enabled you should now set
   ``LIVE_ROOTFS_TYPE = "squashfs-lz4"`` and ensure that ``live`` is in
   ``IMAGE_FSTYPES``.

-  Recipes with an unconditional dependency on ``libpam`` are only
   buildable with ``pam`` in ``DISTRO_FEATURES``. If the dependency is
   truly optional then it is recommended that the dependency be
   conditional upon ``pam`` being in ``DISTRO_FEATURES``.

-  For EFI-based machines, the bootloader (``grub-efi`` by default) is
   installed into the image at /boot. Wic can be used to split the
   bootloader into separate boot and rootfs partitions if necessary.

-  Patches whose context does not match exactly (i.e. where patch
   reports "fuzz" when applying) will generate a warning. For an example
   of this see `this
   commit <http://git.yoctoproject.org/cgit/cgit.cgi/poky/commit/?id=cc97bc08125b63821ce3f616771830f77c456f57>`__.

-  Layers are expected to set ``LAYERSERIES_COMPAT_layername`` to match
   the version(s) of OpenEmbedded-Core they are compatible with. This is
   specified as codenames using spaces to separate multiple values (e.g.
   "rocko sumo"). If a layer does not set
   ``LAYERSERIES_COMPAT_layername``, a warning will is shown. If a layer
   sets a value that does not include the current version ("sumo" for
   the 2.5 release), then an error will be produced.

-  The ``TZ`` environment variable is set to "UTC" within the build
   environment in order to fix reproducibility problems in some recipes.

Moving to the Yocto Project 2.6 Release
=======================================

This section provides migration information for moving to the Yocto
Project 2.6 Release from the prior release.

.. _migration-2.6-gcc-changes:

GCC 8.2 is Now Used by Default
------------------------------

The GNU Compiler Collection version 8.2 is now used by default for
compilation. For more information on what has changed in the GCC 8.x
release, see https://gcc.gnu.org/gcc-8/changes.html.

If you still need to compile with version 7.x, GCC 7.3 is also provided.
You can select this version by setting the and can be selected by
setting the :term:`GCCVERSION` variable to "7.%" in
your configuration.

.. _migration-2.6-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed:

- *beecrypt*: No longer needed since moving to RPM 4.
- *bigreqsproto*: Replaced by ``xorgproto``.
- *calibrateproto*: Removed in favor of ``xinput``.
- *compositeproto*: Replaced by ``xorgproto``.
- *damageproto*: Replaced by ``xorgproto``.
- *dmxproto*: Replaced by ``xorgproto``.
- *dri2proto*: Replaced by ``xorgproto``.
- *dri3proto*: Replaced by ``xorgproto``.
- *eee-acpi-scripts*: Became obsolete.
- *fixesproto*: Replaced by ``xorgproto``.
- *fontsproto*: Replaced by ``xorgproto``.
- *fstests*: Became obsolete.
- *gccmakedep*: No longer used.
- *glproto*: Replaced by ``xorgproto``.
- *gnome-desktop3*: No longer needed. This recipe has moved to ``meta-oe``.
- *icon-naming-utils*: No longer used since the Sato theme was removed in 2016.
- *inputproto*: Replaced by ``xorgproto``.
- *kbproto*: Replaced by ``xorgproto``.
- *libusb-compat*: Became obsolete.
- *libuser*: Became obsolete.
- *libnfsidmap*: No longer an external requirement since ``nfs-utils`` 2.2.1. ``libnfsidmap`` is now integrated.
- *libxcalibrate*: No longer needed with ``xinput``
- *mktemp*: Became obsolete. The ``mktemp`` command is provided by both ``busybox`` and ``coreutils``.
- *ossp-uuid*: Is not being maintained and has mostly been replaced by ``uuid.h`` in ``util-linux``.
- *pax-utils*: No longer needed. Previous QA tests that did use this recipe are now done at build time.
- *pcmciautils*: Became obsolete.
- *pixz*: No longer needed. ``xz`` now supports multi-threaded compression.
- *presentproto*: Replaced by ``xorgproto``.
- *randrproto*: Replaced by ``xorgproto``.
- *recordproto*: Replaced by ``xorgproto``.
- *renderproto*: Replaced by ``xorgproto``.
- *resourceproto*: Replaced by ``xorgproto``.
- *scrnsaverproto*: Replaced by ``xorgproto``.
- *trace-cmd*: Became obsolete. ``perf`` replaced this recipe's functionally.
- *videoproto*: Replaced by ``xorgproto``.
- *wireless-tools*: Became obsolete. Superseded by ``iw``.
- *xcmiscproto*: Replaced by ``xorgproto``.
- *xextproto*: Replaced by ``xorgproto``.
- *xf86dgaproto*: Replaced by ``xorgproto``.
- *xf86driproto*: Replaced by ``xorgproto``.
- *xf86miscproto*: Replaced by ``xorgproto``.
- *xf86-video-omapfb*: Became obsolete. Use kernel modesetting driver instead.
- *xf86-video-omap*: Became obsolete. Use kernel modesetting driver instead.
- *xf86vidmodeproto*: Replaced by ``xorgproto``.
- *xineramaproto*: Replaced by ``xorgproto``.
- *xproto*: Replaced by ``xorgproto``.
- *yasm*: No longer needed since previous usages are now satisfied by ``nasm``.

.. _migration-2.6-packaging-changes:

Packaging Changes
-----------------

The following packaging changes have been made:

-  *cmake*: ``cmake.m4`` and ``toolchain`` files have been moved to
   the main package.

-  *iptables*: The ``iptables`` modules have been split into
   separate packages.

-  *alsa-lib*: ``libasound`` is now in the main ``alsa-lib`` package
   instead of ``libasound``.

-  *glibc*: ``libnss-db`` is now in its own package along with a
   ``/var/db/makedbs.sh`` script to update databases.

-  *python and python3*: The main package has been removed from
   the recipe. You must install specific packages or ``python-modules``
   / ``python3-modules`` for everything.

-  *systemtap*: Moved ``systemtap-exporter`` into its own package.

.. _migration-2.6-xorg-protocol-dependencies:

XOrg Protocol dependencies
--------------------------

The ``*proto`` upstream repositories have been combined into one
"xorgproto" repository. Thus, the corresponding recipes have also been
combined into a single ``xorgproto`` recipe. Any recipes that depend
upon the older ``*proto`` recipes need to be changed to depend on the
newer ``xorgproto`` recipe instead.

For names of recipes removed because of this repository change, see the
`Removed Recipes <#migration-2.6-removed-recipes>`__ section.

.. _migration-2.6-distutils-distutils3-fetching-dependencies:

``distutils`` and ``distutils3`` Now Prevent Fetching Dependencies During the ``do_configure`` Task
---------------------------------------------------------------------------------------------------

Previously, it was possible for Python recipes that inherited the
:ref:`distutils <ref-classes-distutils>` and
:ref:`distutils3 <ref-classes-distutils3>` classes to fetch code
during the :ref:`ref-tasks-configure` task to satisfy
dependencies mentioned in ``setup.py`` if those dependencies were not
provided in the sysroot (i.e. recipes providing the dependencies were
missing from :term:`DEPENDS`).

.. note::

   This change affects classes beyond just the two mentioned (i.e.
   distutils
   and
   distutils3
   ). Any recipe that inherits
   distutils\*
   classes are affected. For example, the
   setuptools
   and
   setuptools3
   recipes are affected since they inherit the
   distutils\*
   classes.

Fetching these types of dependencies that are not provided in the
sysroot negatively affects the ability to reproduce builds. This type of
fetching is now explicitly disabled. Consequently, any missing
dependencies in Python recipes that use these classes now result in an
error during the ``do_configure`` task.

.. _migration-2.6-linux-yocto-configuration-audit-issues-now-correctly-reported:

``linux-yocto`` Configuration Audit Issues Now Correctly Reported
-----------------------------------------------------------------

Due to a bug, the kernel configuration audit functionality was not
writing out any resulting warnings during the build. This issue is now
corrected. You might notice these warnings now if you have a custom
kernel configuration with a ``linux-yocto`` style kernel recipe.

.. _migration-2.6-image-kernel-artifact-naming-changes:

Image/Kernel Artifact Naming Changes
------------------------------------

The following changes have been made:

-  Name variables (e.g. :term:`IMAGE_NAME`) use a new
   ``IMAGE_VERSION_SUFFIX`` variable instead of
   :term:`DATETIME`. Using ``IMAGE_VERSION_SUFFIX``
   allows easier and more direct changes.

   The ``IMAGE_VERSION_SUFFIX`` variable is set in the ``bitbake.conf``
   configuration file as follows:
   ::

      IMAGE_VERSION_SUFFIX = "-${DATETIME}"

-  Several variables have changed names for consistency:
   ::

      Old Variable                  Name New Variable Name
      ========================================================
      KERNEL_IMAGE_BASE_NAME        :term:`KERNEL_IMAGE_NAME`
      KERNEL_IMAGE_SYMLINK_NAME     :term:`KERNEL_IMAGE_LINK_NAME`
      MODULE_TARBALL_BASE_NAME      :term:`MODULE_TARBALL_NAME`
      MODULE_TARBALL_SYMLINK_NAME   :term:`MODULE_TARBALL_LINK_NAME`
      INITRAMFS_BASE_NAME           :term:`INITRAMFS_NAME`

-  The ``MODULE_IMAGE_BASE_NAME`` variable has been removed. The module
   tarball name is now controlled directly with the
   :term:`MODULE_TARBALL_NAME` variable.

-  The :term:`KERNEL_DTB_NAME` and
   :term:`KERNEL_DTB_LINK_NAME` variables
   have been introduced to control kernel Device Tree Binary (DTB)
   artifact names instead of mangling ``KERNEL_IMAGE_*`` variables.

-  The :term:`KERNEL_FIT_NAME` and
   :term:`KERNEL_FIT_LINK_NAME` variables
   have been introduced to specify the name of flattened image tree
   (FIT) kernel images similar to other deployed artifacts.

-  The :term:`MODULE_TARBALL_NAME` and
   :term:`MODULE_TARBALL_LINK_NAME`
   variable values no longer include the "module-" prefix or ".tgz"
   suffix. These parts are now hardcoded so that the values are
   consistent with other artifact naming variables.

-  Added the :term:`INITRAMFS_LINK_NAME`
   variable so that the symlink can be controlled similarly to other
   artifact types.

-  :term:`INITRAMFS_NAME` now uses
   "${PKGE}-${PKGV}-${PKGR}-${MACHINE}${IMAGE_VERSION_SUFFIX}" instead
   of "${PV}-${PR}-${MACHINE}-${DATETIME}", which makes it consistent
   with other variables.

.. _migration-2.6-serial-console-deprecated:

``SERIAL_CONSOLE`` Deprecated
-----------------------------

The :term:`SERIAL_CONSOLE` variable has been
functionally replaced by the
:term:`SERIAL_CONSOLES` variable for some time.
With the Yocto Project 2.6 release, ``SERIAL_CONSOLE`` has been
officially deprecated.

``SERIAL_CONSOLE`` will continue to work as before for the 2.6 release.
However, for the sake of future compatibility, it is recommended that
you replace all instances of ``SERIAL_CONSOLE`` with
``SERIAL_CONSOLES``.

.. note::

   The only difference in usage is that
   SERIAL_CONSOLES
   expects entries to be separated using semicolons as compared to
   SERIAL_CONSOLE
   , which expects spaces.

.. _migration-2.6-poky-sets-unknown-configure-option-to-qa-error:

Configure Script Reports Unknown Options as Errors
--------------------------------------------------

If the configure script reports an unknown option, this now triggers a
QA error instead of a warning. Any recipes that previously got away with
specifying such unknown options now need to be fixed.

.. _migration-2.6-override-changes:

Override Changes
----------------

The following changes have occurred:

-  The ``virtclass-native`` and ``virtclass-nativesdk`` Overrides Have
   Been Removed: The ``virtclass-native`` and ``virtclass-nativesdk``
   overrides have been deprecated since 2012 in favor of
   ``class-native`` and ``class-nativesdk``, respectively. Both
   ``virtclass-native`` and ``virtclass-nativesdk`` are now dropped.

   .. note::

      The
      virtclass-multilib-
      overrides for multilib are still valid.

-  The ``forcevariable`` Override Now Has a Higher Priority Than
   ``libc`` Overrides: The ``forcevariable`` override is documented to
   be the highest priority override. However, due to a long-standing
   quirk of how :term:`OVERRIDES` is set, the ``libc``
   overrides (e.g. ``libc-glibc``, ``libc-musl``, and so forth)
   erroneously had a higher priority. This issue is now corrected.

   It is likely this change will not cause any problems. However, it is
   possible with some unusual configurations that you might see a change
   in behavior if you were relying on the previous behavior. Be sure to
   check how you use ``forcevariable`` and ``libc-*`` overrides in your
   custom layers and configuration files to ensure they make sense.

-  The ``build-${BUILD_OS}`` Override Has Been Removed: The
   ``build-${BUILD_OS}``, which is typically ``build-linux``, override
   has been removed because building on a host operating system other
   than a recent version of Linux is neither supported nor recommended.
   Dropping the override avoids giving the impression that other host
   operating systems might be supported.

-  The "_remove" operator now preserves whitespace. Consequently, when
   specifying list items to remove, be aware that leading and trailing
   whitespace resulting from the removal is retained.

   See the ":ref:`bitbake:removing-override-style-syntax`"
   section in the BitBake User Manual for a detailed example.

.. _migration-2.6-systemd-configuration-now-split-out-to-system-conf:

``systemd`` Configuration is Now Split Into ``systemd-conf``
------------------------------------------------------------

The configuration for the ``systemd`` recipe has been moved into a
``system-conf`` recipe. Moving this configuration to a separate recipe
avoids the ``systemd`` recipe from becoming machine-specific for cases
where machine-specific configurations need to be applied (e.g. for
``qemu*`` machines).

Currently, the new recipe packages the following files:
::

   ${sysconfdir}/machine-id
   ${sysconfdir}/systemd/coredump.conf
   ${sysconfdir}/systemd/journald.conf
   ${sysconfdir}/systemd/logind.conf
   ${sysconfdir}/systemd/system.conf
   ${sysconfdir}/systemd/user.conf

If you previously used bbappend files to append the ``systemd`` recipe to
change any of the listed files, you must do so for the ``systemd-conf``
recipe instead.

.. _migration-2.6-automatic-testing-changes:

Automatic Testing Changes
-------------------------

This section provides information about automatic testing changes:

-  ``TEST_IMAGE`` Variable Removed: Prior to this release, you set the
   ``TEST_IMAGE`` variable to "1" to enable automatic testing for
   successfully built images. The ``TEST_IMAGE`` variable no longer
   exists and has been replaced by the
   :term:`TESTIMAGE_AUTO` variable.

-  Inheriting the ``testimage`` and ``testsdk`` Classes: Best
   practices now dictate that you use the
   :term:`IMAGE_CLASSES` variable rather than the
   :term:`INHERIT` variable when you inherit the
   :ref:`testimage <ref-classes-testimage*>` and
   :ref:`testsdk <ref-classes-testsdk>` classes used for automatic
   testing.

.. _migration-2.6-openssl-changes:

OpenSSL Changes
---------------

`OpenSSL <https://www.openssl.org/>`__ has been upgraded from 1.0 to
1.1. By default, this upgrade could cause problems for recipes that have
both versions in their dependency chains. The problem is that both
versions cannot be installed together at build time.

.. note::

   It is possible to have both versions of the library at runtime.

.. _migration-2.6-bitbake-changes:

BitBake Changes
---------------

The server logfile ``bitbake-cookerdaemon.log`` is now always placed in
the :term:`Build Directory` instead of the current
directory.

.. _migration-2.6-security-changes:

Security Changes
----------------

The Poky distribution now uses security compiler flags by default.
Inclusion of these flags could cause new failures due to stricter
checking for various potential security issues in code.

.. _migration-2.6-post-installation-changes:

Post Installation Changes
-------------------------

You must explicitly mark post installs to defer to the target. If you
want to explicitly defer a postinstall to first boot on the target
rather than at rootfs creation time, use ``pkg_postinst_ontarget()`` or
call ``postinst_intercept delay_to_first_boot`` from ``pkg_postinst()``.
Any failure of a ``pkg_postinst()`` script (including exit 1) triggers
an error during the :ref:`ref-tasks-rootfs` task.

For more information on post-installation behavior, see the
":ref:`dev-manual/dev-manual-common-tasks:post-installation scripts`"
section in the Yocto Project Development Tasks Manual.

.. _migration-2.6-python-3-profile-guided-optimizations:

Python 3 Profile-Guided Optimization
------------------------------------

The ``python3`` recipe now enables profile-guided optimization. Using
this optimization requires a little extra build time in exchange for
improved performance on the target at runtime. Additionally, the
optimization is only enabled if the current
:term:`MACHINE` has support for user-mode emulation in
QEMU (i.e. "qemu-usermode" is in
:term:`MACHINE_FEATURES`, which it is by
default).

If you wish to disable Python profile-guided optimization regardless of
the value of ``MACHINE_FEATURES``, then ensure that
:term:`PACKAGECONFIG` for the ``python3`` recipe
does not contain "pgo". You could accomplish the latter using the
following at the configuration level:
::

   PACKAGECONFIG_remove_pn-python3 = "pgo"

Alternatively, you can set ``PACKAGECONFIG`` using an append file
for the ``python3`` recipe.

.. _migration-2.6-miscellaneous-changes:

Miscellaneous Changes
---------------------

The following miscellaneous changes occurred:

-  Default to using the Thumb-2 instruction set for armv7a and above. If
   you have any custom recipes that build software that needs to be
   built with the ARM instruction set, change the recipe to set the
   instruction set as follows:
   ::

      ARM_INSTRUCTION_SET = "arm"

-  ``run-postinsts`` no longer uses ``/etc/*-postinsts`` for
   ``dpkg/opkg`` in favor of built-in postinst support. RPM behavior
   remains unchanged.

-  The ``NOISO`` and ``NOHDD`` variables are no longer used. You now
   control building ``*.iso`` and ``*.hddimg`` image types directly by
   using the :term:`IMAGE_FSTYPES` variable.

-  The ``scripts/contrib/mkefidisk.sh`` has been removed in favor of
   Wic.

-  ``kernel-modules`` has been removed from
   :term:`RRECOMMENDS` for ``qemumips`` and
   ``qemumips64`` machines. Removal also impacts the ``x86-base.inc``
   file.

   .. note::

      genericx86
      and
      genericx86-64
      retain
      kernel-modules
      as part of the
      RRECOMMENDS
      variable setting.

-  The ``LGPLv2_WHITELIST_GPL-3.0`` variable has been removed. If you
   are setting this variable in your configuration, set or append it to
   the ``WHITELIST_GPL-3.0`` variable instead.

-  ``${ASNEEDED}`` is now included in the
   :term:`TARGET_LDFLAGS` variable directly. The
   remaining definitions from ``meta/conf/distro/include/as-needed.inc``
   have been moved to corresponding recipes.

-  Support for DSA host keys has been dropped from the OpenSSH recipes.
   If you are still using DSA keys, you must switch over to a more
   secure algorithm as recommended by OpenSSH upstream.

-  The ``dhcp`` recipe now uses the ``dhcpd6.conf`` configuration file
   in ``dhcpd6.service`` for IPv6 DHCP rather than re-using
   ``dhcpd.conf``, which is now reserved for IPv4.

Moving to the Yocto Project 2.7 Release
=======================================

This section provides migration information for moving to the Yocto
Project 2.7 Release from the prior release.

.. _migration-2.7-bitbake-changes:

BitBake Changes
---------------

The following changes have been made to BitBake:

-  BitBake now checks anonymous Python functions and pure Python
   functions (e.g. ``def funcname:``) in the metadata for tab
   indentation. If found, BitBake produces a warning.

-  Bitbake now checks
   :term:`BBFILE_COLLECTIONS` for duplicate
   entries and triggers an error if any are found.

.. _migration-2.7-eclipse-support-dropped:

Eclipse Support Removed
-----------------------

Support for the Eclipse IDE has been removed. Support continues for
those releases prior to 2.7 that did include support. The 2.7 release
does not include the Eclipse Yocto plugin.

.. _migration-2.7-qemu-native-splits-system-and-user-mode-parts:

``qemu-native`` Splits the System and User-Mode Parts
-----------------------------------------------------

The system and user-mode parts of ``qemu-native`` are now split.
``qemu-native`` provides the user-mode components and
``qemu-system-native`` provides the system components. If you have
recipes that depend on QEMU's system emulation functionality at build
time, they should now depend upon ``qemu-system-native`` instead of
``qemu-native``.

.. _migration-2.7-upstream-tracking.inc-removed:

The ``upstream-tracking.inc`` File Has Been Removed
---------------------------------------------------

The previously deprecated ``upstream-tracking.inc`` file is now removed.
Any ``UPSTREAM_TRACKING*`` variables are now set in the corresponding
recipes instead.

Remove any references you have to the ``upstream-tracking.inc`` file in
your configuration.

.. _migration-2.7-distro-features-libc-removed:

The ``DISTRO_FEATURES_LIBC`` Variable Has Been Removed
------------------------------------------------------

The ``DISTRO_FEATURES_LIBC`` variable is no longer used. The ability to
configure glibc using kconfig has been removed for quite some time
making the ``libc-*`` features set no longer effective.

Remove any references you have to ``DISTRO_FEATURES_LIBC`` in your own
layers.

.. _migration-2.7-license-values:

License Value Corrections
-------------------------

The following corrections have been made to the
:term:`LICENSE` values set by recipes:

- *socat*: Corrected ``LICENSE`` to be "GPLv2" rather than "GPLv2+".
- *libgfortran*: Set license to "GPL-3.0-with-GCC-exception".
- *elfutils*: Removed "Elfutils-Exception" and set to "GPLv2" for shared libraries

.. _migration-2.7-packaging-changes:

Packaging Changes
-----------------

This section provides information about packaging changes.

-  ``bind``: The ``nsupdate`` binary has been moved to the
   ``bind-utils`` package.

-  Debug split: The default debug split has been changed to create
   separate source packages (i.e. package_name\ ``-dbg`` and
   package_name\ ``-src``). If you are currently using ``dbg-pkgs`` in
   :term:`IMAGE_FEATURES` to bring in debug
   symbols and you still need the sources, you must now also add
   ``src-pkgs`` to ``IMAGE_FEATURES``. Source packages remain in the
   target portion of the SDK by default, unless you have set your own
   value for :term:`SDKIMAGE_FEATURES` that
   does not include ``src-pkgs``.

-  Mount all using ``util-linux``: ``/etc/default/mountall`` has moved
   into the -mount sub-package.

-  Splitting binaries using ``util-linux``: ``util-linux`` now splits
   each binary into its own package for fine-grained control. The main
   ``util-linux`` package pulls in the individual binary packages using
   the :term:`RRECOMMENDS` and
   :term:`RDEPENDS` variables. As a result, existing
   images should not see any changes assuming
   :term:`NO_RECOMMENDATIONS` is not set.

-  ``netbase/base-files``: ``/etc/hosts`` has moved from ``netbase`` to
   ``base-files``.

-  ``tzdata``: The main package has been converted to an empty meta
   package that pulls in all ``tzdata`` packages by default.

-  ``lrzsz``: This package has been removed from
   ``packagegroup-self-hosted`` and
   ``packagegroup-core-tools-testapps``. The X/Y/ZModem support is less
   likely to be needed on modern systems. If you are relying on these
   packagegroups to include the ``lrzsz`` package in your image, you now
   need to explicitly add the package.

.. _migration-2.7-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed:

- *gcc*: Drop version 7.3 recipes. Version 8.3 now remains.
- *linux-yocto*: Drop versions 4.14 and 4.18 recipes. Versions 4.19 and 5.0 remain.
- *go*: Drop version 1.9 recipes. Versions 1.11 and 1.12 remain.
- *xvideo-tests*: Became obsolete.
- *libart-lgpl*: Became obsolete.
- *gtk-icon-utils-native*: These tools are now provided by gtk+3-native
- *gcc-cross-initial*: No longer needed. gcc-cross/gcc-crosssdk is now used instead.
- *gcc-crosssdk-initial*: No longer needed. gcc-cross/gcc-crosssdk is now used instead.
- *glibc-initial*: Removed because the benefits of having it for site_config are currently outweighed by the cost of building the recipe.

.. _migration-2.7-removed-classes:

Removed Classes
---------------

The following classes have been removed:

- *distutils-tools*: This class was never used.
- *bugzilla.bbclass*: Became obsolete.
- *distrodata*: This functionally has been replaced by a more modern tinfoil-based implementation.

.. _migration-2.7-miscellaneous-changes:

Miscellaneous Changes
---------------------

The following miscellaneous changes occurred:

-  The ``distro`` subdirectory of the Poky repository has been removed
   from the top-level ``scripts`` directory.

-  Perl now builds for the target using
   `perl-cross <http://arsv.github.io/perl-cross/>`_ for better
   maintainability and improved build performance. This change should
   not present any problems unless you have heavily customized your Perl
   recipe.

-  ``arm-tunes``: Removed the "-march" option if mcpu is already added.

-  ``update-alternatives``: Convert file renames to
   :term:`PACKAGE_PREPROCESS_FUNCS`

-  ``base/pixbufcache``: Obsolete ``sstatecompletions`` code has been
   removed.

-  :ref:`native <ref-classes-native>` class:
   :term:`RDEPENDS` handling has been enabled.

-  ``inetutils``: This recipe has rsh disabled.

Moving to the Yocto Project 3.0 Release
=======================================

This section provides migration information for moving to the Yocto
Project 3.0 Release from the prior release.

.. _migration-3.0-init-system-selection:

Init System Selection
---------------------

Changing the init system manager previously required setting a number of
different variables. You can now change the manager by setting the
``INIT_MANAGER`` variable and the corresponding include files (i.e.
``conf/distro/include/init-manager-*.conf``). Include files are provided
for four values: "none", "sysvinit", "systemd", and "mdev-busybox". The
default value, "none", for ``INIT_MANAGER`` should allow your current
settings to continue working. However, it is advisable to explicitly set
``INIT_MANAGER``.

.. _migration-3.0-lsb-support-removed:

LSB Support Removed
-------------------

Linux Standard Base (LSB) as a standard is not current, and is not well
suited for embedded applications. Support can be continued in a separate
layer if needed. However, presently LSB support has been removed from
the core.

As a result of this change, the ``poky-lsb`` derivative distribution
configuration that was also used for testing alternative configurations
has been replaced with a ``poky-altcfg`` distribution that has LSB parts
removed.

.. _migration-3.0-removed-recipes:

Removed Recipes
---------------

The following recipes have been removed.

-  ``core-image-lsb-dev``: Part of removed LSB support.

-  ``core-image-lsb``: Part of removed LSB support.

-  ``core-image-lsb-sdk``: Part of removed LSB support.

-  ``cve-check-tool``: Functionally replaced by the ``cve-update-db``
   recipe and ``cve-check`` class.

-  ``eglinfo``: No longer maintained. ``eglinfo`` from ``mesa-demos`` is
   an adequate and maintained alternative.

-  ``gcc-8.3``: Version 8.3 removed. Replaced by 9.2.

-  ``gnome-themes-standard``: Only needed by gtk+ 2.x, which has been
   removed.

-  ``gtk+``: GTK+ 2 is obsolete and has been replaced by gtk+3.

-  ``irda-utils``: Has become obsolete. IrDA support has been removed
   from the Linux kernel in version 4.17 and later.

-  ``libnewt-python``: ``libnewt`` Python support merged into main
   ``libnewt`` recipe.

-  ``libsdl``: Replaced by newer ``libsdl2``.

-  ``libx11-diet``: Became obsolete.

-  ``libxx86dga``: Removed obsolete client library.

-  ``libxx86misc``: Removed. Library is redundant.

-  ``linux-yocto``: Version 5.0 removed, which is now redundant (5.2 /
   4.19 present).

-  ``lsbinitscripts``: Part of removed LSB support.

-  ``lsb``: Part of removed LSB support.

-  ``lsbtest``: Part of removed LSB support.

-  ``openssl10``: Replaced by newer ``openssl`` version 1.1.

-  ``packagegroup-core-lsb``: Part of removed LSB support.

-  ``python-nose``: Removed the Python 2.x version of the recipe.

-  ``python-numpy``: Removed the Python 2.x version of the recipe.

-  ``python-scons``: Removed the Python 2.x version of the recipe.

-  ``source-highlight``: No longer needed.

-  ``stress``: Replaced by ``stress-ng``.

-  ``vulkan``: Split into ``vulkan-loader``, ``vulkan-headers``, and
   ``vulkan-tools``.

-  ``weston-conf``: Functionality moved to ``weston-init``.

.. _migration-3.0-packaging-changes:

Packaging Changes
-----------------

The following packaging changes have occurred.

-  The `Epiphany <https://en.wikipedia.org/wiki/GNOME_Web>`__ browser
   has been dropped from ``packagegroup-self-hosted`` as it has not been
   needed inside ``build-appliance-image`` for quite some time and was
   causing resource problems.

-  ``libcap-ng`` Python support has been moved to a separate
   ``libcap-ng-python`` recipe to streamline the build process when the
   Python bindings are not needed.

-  ``libdrm`` now packages the file ``amdgpu.ids`` into a separate
   ``libdrm-amdgpu`` package.

-  ``python3``: The ``runpy`` module is now in the ``python3-core``
   package as it is required to support the common "python3 -m" command
   usage.

-  ``distcc`` now provides separate ``distcc-client`` and
   ``distcc-server`` packages as typically one or the other are needed,
   rather than both.

-  ``python*-setuptools`` recipes now separately package the
   ``pkg_resources`` module in a ``python-pkg-resources`` /
   ``python3-pkg-resources`` package as the module is useful independent
   of the rest of the setuptools package. The main ``python-setuptools``
   / ``python3-setuptools`` package depends on this new package so you
   should only need to update dependencies unless you want to take
   advantage of the increased granularity.

.. _migration-3.0-cve-checking:

CVE Checking
------------

``cve-check-tool`` has been functionally replaced by a new
``cve-update-db`` recipe and functionality built into the ``cve-check``
class. The result uses NVD JSON data feeds rather than the deprecated
XML feeds that ``cve-check-tool`` was using, supports CVSSv3 scoring,
and makes other improvements.

Additionally, the ``CVE_CHECK_CVE_WHITELIST`` variable has been replaced
by ``CVE_CHECK_WHITELIST``.

.. _migration-3.0-bitbake-changes:

Bitbake Changes
---------------

The following BitBake changes have occurred.

-  ``addtask`` statements now properly validate dependent tasks.
   Previously, an invalid task was silently ignored. With this change,
   the invalid task generates a warning.

-  Other invalid ``addtask`` and ``deltask`` usages now trigger these
   warnings: "multiple target tasks arguments with addtask / deltask",
   and "multiple before/after clauses".

-  The "multiconfig" prefix is now shortened to "mc". "multiconfig" will
   continue to work, however it may be removed in a future release.

-  The ``bitbake -g`` command no longer generates a
   ``recipe-depends.dot`` file as the contents (i.e. a reprocessed
   version of ``task-depends.dot``) were confusing.

-  The ``bb.build.FuncFailed`` exception, previously raised by
   ``bb.build.exec_func()`` when certain other exceptions have occurred,
   has been removed. The real underlying exceptions will be raised
   instead. If you have calls to ``bb.build.exec_func()`` in custom
   classes or ``tinfoil-using`` scripts, any references to
   ``bb.build.FuncFailed`` should be cleaned up.

-  Additionally, the ``bb.build.exec_func()`` no longer accepts the
   "pythonexception" parameter. The function now always raises
   exceptions. Remove this argument in any calls to
   ``bb.build.exec_func()`` in custom classes or scripts.

-  The
   :term:`bitbake:BB_SETSCENE_VERIFY_FUNCTION2`
   is no longer used. In the unlikely event that you have any references
   to it, they should be removed.

-  The ``RunQueueExecuteScenequeue`` and ``RunQueueExecuteTasks`` events
   have been removed since setscene tasks are now executed as part of
   the normal runqueue. Any event handling code in custom classes or
   scripts that handles these two events need to be updated.

-  The arguments passed to functions used with
   :term:`bitbake:BB_HASHCHECK_FUNCTION`
   have changed. If you are using your own custom hash check function,
   see
   http://git.yoctoproject.org/cgit/cgit.cgi/poky/commit/?id=40a5e193c4ba45c928fccd899415ea56b5417725
   for details.

-  Task specifications in ``BB_TASKDEPDATA`` and class implementations
   used in signature generator classes now use "<fn>:<task>" everywhere
   rather than the "." delimiter that was being used in some places.
   This change makes it consistent with all areas in the code. Custom
   signature generator classes and code that reads ``BB_TASKDEPDATA``
   need to be updated to use ':' as a separator rather than '.'.

.. _migration-3.0-sanity-checks:

Sanity Checks
-------------

The following sanity check changes occurred.

-  :term:`SRC_URI` is now checked for usage of two
   problematic items:

   -  "${PN}" prefix/suffix use - Warnings always appear if ${PN} is
      used. You must fix the issue regardless of whether multiconfig or
      anything else that would cause prefixing/suffixing to happen.

   -  Github archive tarballs - these are not guaranteed to be stable.
      Consequently, it is likely that the tarballs will be refreshed and
      thus the SRC_URI checksums will fail to apply. It is recommended
      that you fetch either an official release tarball or a specific
      revision from the actual Git repository instead.

   Either one of these items now trigger a warning by default. If you
   wish to disable this check, remove ``src-uri-bad`` from
   :term:`WARN_QA`.

-  The ``file-rdeps`` runtime dependency check no longer expands
   :term:`RDEPENDS` recursively as there is no mechanism
   to ensure they can be fully computed, and thus races sometimes result
   in errors either showing up or not. Thus, you might now see errors
   for missing runtime dependencies that were previously satisfied
   recursively. Here is an example: package A contains a shell script
   starting with ``#!/bin/bash`` but has no dependency on bash. However,
   package A depends on package B, which does depend on bash. You need
   to add the missing dependency or dependencies to resolve the warning.

-  Setting ``DEPENDS_${PN}`` anywhere (i.e. typically in a recipe) now
   triggers an error. The error is triggered because
   :term:`DEPENDS` is not a package-specific variable
   unlike RDEPENDS. You should set ``DEPENDS`` instead.

-  systemd currently does not work well with the musl C library because
   only upstream officially supports linking the library with glibc.
   Thus, a warning is shown when building systemd in conjunction with
   musl.

.. _migration-3.0-miscellaneous-changes:

Miscellaneous Changes
---------------------

The following miscellaneous changes have occurred.

-  The ``gnome`` class has been removed because it now does very little.
   You should update recipes that previously inherited this class to do
   the following: inherit gnomebase gtk-icon-cache gconf mime

-  The ``meta/recipes-kernel/linux/linux-dtb.inc`` file has been
   removed. This file was previously deprecated in favor of setting
   :term:`KERNEL_DEVICETREE` in any kernel
   recipe and only produced a warning. Remove any ``include`` or
   ``require`` statements pointing to this file.

-  :term:`TARGET_CFLAGS`,
   :term:`TARGET_CPPFLAGS`,
   :term:`TARGET_CXXFLAGS`, and
   :term:`TARGET_LDFLAGS` are no longer exported
   to the external environment. This change did not require any changes
   to core recipes, which is a good indicator that no changes will be
   required. However, if for some reason the software being built by one
   of your recipes is expecting these variables to be set, then building
   the recipe will fail. In such cases, you must either export the
   variable or variables in the recipe or change the scripts so that
   exporting is not necessary.

-  You must change the host distro identifier used in
   :term:`NATIVELSBSTRING` to use all lowercase
   characters even if it does not contain a version number. This change
   is necessary only if you are not using ``uninative`` and
   :term:`SANITY_TESTED_DISTROS`.

-  In the ``base-files`` recipe, writing the hostname into
   ``/etc/hosts`` and ``/etc/hostname`` is now done within the main
   :ref:`ref-tasks-install` function rather than in the
   ``do_install_basefilesissue`` function. The reason for the change is
   because ``do_install_basefilesissue`` is more easily overridden
   without having to duplicate the hostname functionality. If you have
   done the latter (e.g. in a ``base-files`` bbappend), then you should
   remove it from your customized ``do_install_basefilesissue``
   function.

-  The ``wic --expand`` command now uses commas to separate "key:value"
   pairs rather than hyphens.

   .. note::

      The wic command-line help is not updated.

   You must update any scripts or commands where you use
   ``wic --expand`` with multiple "key:value" pairs.

-  UEFI image variable settings have been moved from various places to a
   central ``conf/image-uefi.conf``. This change should not influence
   any existing configuration as the ``meta/conf/image-uefi.conf`` in
   the core metadata sets defaults that can be overridden in the same
   manner as before.

-  ``conf/distro/include/world-broken.inc`` has been removed. For cases
   where certain recipes need to be disabled when using the musl C
   library, these recipes now have ``COMPATIBLE_HOST_libc-musl`` set
   with a comment that explains why.

Moving to the Yocto Project 3.1 Release
=======================================

This section provides migration information for moving to the Yocto
Project 3.1 Release from the prior release.

.. _migration-3.1-minimum-system-requirements:

Minimum system requirements
---------------------------

The following versions / requirements of build host components have been
updated:

-  gcc 5.0

-  python 3.5

-  tar 1.28

-  ``rpcgen`` is now required on the host (part of the ``libc-dev-bin``
   package on Ubuntu, Debian and related distributions, and the
   ``glibc`` package on RPM-based distributions).

Additionally, the ``makeinfo`` and ``pod2man`` tools are *no longer*
required on the host.

.. _migration-3.1-mpc8315e-rdb-removed:

mpc8315e-rdb machine removed
----------------------------

The MPC8315E-RDB machine is old/obsolete and unobtainable, thus given
the maintenance burden the ``mpc8315e-rdb`` machine configuration that
supported it has been removed in this release. The removal does leave a
gap in official PowerPC reference hardware support; this may change in
future if a suitable machine with accompanying support resources is
found.

.. _migration-3.1-python-2-removed:

Python 2 removed
----------------

Due to the expiration of upstream support in January 2020, support for
Python 2 has now been removed; it is recommended that you use Python 3
instead. If absolutely needed there is a meta-python2 community layer
containing Python 2, related classes and various Python 2-based modules,
however it should not be considered as supported.

.. _migration-3.1-reproducible-builds:

Reproducible builds now enabled by default
------------------------------------------

In order to avoid unnecessary differences in output files (aiding binary
reproducibility), the Poky distribution configuration
(``DISTRO = "poky"``) now inherits the ``reproducible_build`` class by
default.

.. _migration-3.1-ptest-feature-impact:

Impact of ptest feature is now more significant
-----------------------------------------------

The Poky distribution configuration (``DISTRO = "poky"``) enables ptests
by default to enable runtime testing of various components. In this
release, a dependency needed to be added that has resulted in a
significant increase in the number of components that will be built just
when building a simple image such as core-image-minimal. If you do not
need runtime tests enabled for core components, then it is recommended
that you remove "ptest" from
:term:`DISTRO_FEATURES` to save a significant
amount of build time e.g. by adding the following in your configuration:
::

   DISTRO_FEATURES_remove = "ptest"

.. _migration-3.1-removed-recipes:

Removed recipes
---------------

The following recipes have been removed:

-  ``chkconfig``: obsolete

-  ``console-tools``: obsolete

-  ``enchant``: replaced by ``enchant2``

-  ``foomatic-filters``: obsolete

-  ``libidn``: no longer needed, moved to meta-oe

-  ``libmodulemd``: replaced by ``libmodulemd-v1``

-  ``linux-yocto``: drop 4.19, 5.2 version recipes (5.4 now provided)

-  ``nspr``: no longer needed, moved to meta-oe

-  ``nss``: no longer needed, moved to meta-oe

-  ``python``: Python 2 removed (Python 3 preferred)

-  ``python-setuptools``: Python 2 version removed (python3-setuptools
   preferred)

-  ``sysprof``: no longer needed, moved to meta-oe

-  ``texi2html``: obsolete

-  ``u-boot-fw-utils``: functionally replaced by ``libubootenv``

.. _migration-3.1-features-check:

features_check class replaces distro_features_check
---------------------------------------------------

The ``distro_features_check`` class has had its functionality expanded,
now supporting ``ANY_OF_MACHINE_FEATURES``,
``REQUIRED_MACHINE_FEATURES``, ``CONFLICT_MACHINE_FEATURES``,
``ANY_OF_COMBINED_FEATURES``, ``REQUIRED_COMBINED_FEATURES``,
``CONFLICT_COMBINED_FEATURES``. As a result the class has now been
renamed to ``features_check``; the ``distro_features_check`` class still
exists but generates a warning and redirects to the new class. In
preparation for a future removal of the old class it is recommended that
you update recipes currently inheriting ``distro_features_check`` to
inherit ``features_check`` instead.

.. _migration-3.1-removed-classes:

Removed classes
---------------

The following classes have been removed:

-  ``distutils-base``: moved to meta-python2

-  ``distutils``: moved to meta-python2

-  ``libc-common``: merged into the glibc recipe as nothing else used
   it.

-  ``python-dir``: moved to meta-python2

-  ``pythonnative``: moved to meta-python2

-  ``setuptools``: moved to meta-python2

-  ``tinderclient``: dropped as it was obsolete.

.. _migration-3.1-src-uri-checksums:

SRC_URI checksum behaviour
--------------------------

Previously, recipes by tradition included both SHA256 and MD5 checksums
for remotely fetched files in :term:`SRC_URI`, even
though only one is actually mandated. However, the MD5 checksum does not
add much given its inherent weakness; thus when a checksum fails only
the SHA256 sum will now be printed. The md5sum will still be verified if
it is specified.

.. _migration-3.1-npm:

npm fetcher changes
-------------------

The npm fetcher has been completely reworked in this release. The npm
fetcher now only fetches the package source itself and no longer the
dependencies; there is now also an npmsw fetcher which explicitly
fetches the shrinkwrap file and the dependencies. This removes the
slightly awkward ``NPM_LOCKDOWN`` and ``NPM_SHRINKWRAP`` variables which
pointed to local files; the lockdown file is no longer needed at all.
Additionally, the package name in ``npm://`` entries in
:term:`SRC_URI` is now specified using a ``package``
parameter instead of the earlier ``name`` which overlapped with the
generic ``name`` parameter. All recipes using the npm fetcher will need
to be changed as a result.

An example of the new scheme: ::

   SRC_URI = "npm://registry.npmjs.org;package=array-flatten;version=1.1.1 \
              npmsw://${THISDIR}/npm-shrinkwrap.json"

Another example where the sources are fetched from git rather than an npm repository: ::

   SRC_URI = "git://github.com/foo/bar.git;protocol=https \
              npmsw://${THISDIR}/npm-shrinkwrap.json"

devtool and recipetool have also been updated to match with the npm
fetcher changes. Other than producing working and more complete recipes
for npm sources, there is also a minor change to the command line for
devtool: the ``--fetch-dev`` option has been renamed to ``--npm-dev`` as
it is npm-specific.

.. _migration-3.1-packaging-changes:

Packaging changes
-----------------

-  ``intltool`` has been removed from ``packagegroup-core-sdk`` as it is
   rarely needed to build modern software - gettext can do most of the
   things it used to be needed for. ``intltool`` has also been removed
   from ``packagegroup-core-self-hosted`` as it is not needed to for
   standard builds.

-  git: ``git-am``, ``git-difftool``, ``git-submodule``, and
   ``git-request-pull`` are no longer perl-based, so are now installed
   with the main ``git`` package instead of within ``git-perltools``.

-  The ``ldconfig`` binary built as part of glibc has now been moved to
   its own ``ldconfig`` package (note no ``glibc-`` prefix). This
   package is in the :term:`RRECOMMENDS` of the main
   ``glibc`` package if ``ldconfig`` is present in
   :term:`DISTRO_FEATURES`.

-  ``libevent`` now splits each shared library into its own package (as
   Debian does). Since these are shared libraries and will be pulled in
   through the normal shared library dependency handling, there should
   be no impact to existing configurations other than less unnecessary
   libraries being installed in some cases.

-  linux-firmware now has a new package for ``bcm4366c`` and includes
   available NVRAM config files into the ``bcm43340``, ``bcm43362``,
   ``bcm43430`` and ``bcm4356-pcie`` packages.

-  ``harfbuzz`` now splits the new ``libharfbuzz-subset.so`` library
   into its own package to reduce the main package size in cases where
   ``libharfbuzz-subset.so`` is not needed.

.. _migration-3.1-package-qa-warnings:

Additional warnings
-------------------

Warnings will now be shown at ``do_package_qa`` time in the following
circumstances:

-  A recipe installs ``.desktop`` files containing ``MimeType`` keys but
   does not inherit the new ``mime-xdg`` class

-  A recipe installs ``.xml`` files into ``${datadir}/mime/packages``
   but does not inherit the ``mime`` class

.. _migration-3.1-x86-live-wic:

``wic`` image type now used instead of ``live`` by default for x86
------------------------------------------------------------------

``conf/machine/include/x86-base.inc`` (inherited by most x86 machine
configurations) now specifies ``wic`` instead of ``live`` by default in
:term:`IMAGE_FSTYPES`. The ``live`` image type will
likely be removed in a future release so it is recommended that you use
``wic`` instead.

.. _migration-3.1-misc:

Miscellaneous changes
---------------------

-  The undocumented ``SRC_DISTRIBUTE_LICENSES`` variable has now been
   removed in favour of a new ``AVAILABLE_LICENSES`` variable which is
   dynamically set based upon license files found in
   ``${COMMON_LICENSE_DIR}`` and ``${LICENSE_PATH}``.

-  The tune definition for big-endian microblaze machines is now
   ``microblaze`` instead of ``microblazeeb``.

-  ``newlib`` no longer has built-in syscalls. ``libgloss`` should then
   provide the syscalls, ``crt0.o`` and other functions that are no
   longer part of ``newlib`` itself. If you are using
   ``TCLIBC = "newlib"`` this now means that you must link applications
   with both ``newlib`` and ``libgloss``, whereas before ``newlib``
   would run in many configurations by itself.
