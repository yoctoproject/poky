.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

.. |yocto-codename| replace:: whinlatter
.. |yocto-ver| replace:: 5.3
.. Note: anchors id below cannot contain substitutions so replace them with the
   value of |yocto-ver| above.

Release |yocto-ver| (|yocto-codename|)
======================================

Migration notes for |yocto-ver| (|yocto-codename|)
--------------------------------------------------

This section provides migration information for moving to the Yocto
Project |yocto-ver| Release (codename "|yocto-codename|") from the prior release.

:term:`WORKDIR` changes
~~~~~~~~~~~~~~~~~~~~~~~

``S = ${WORKDIR}/something`` no longer supported
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

If a recipe has :term:`S` set to be ``${``\ :term:`WORKDIR`\ ``}/something``,
this is no longer supported, and an error will be issued. The recipe should be
changed to::

   S = "${UNPACKDIR}/something"

``S = ${WORKDIR}/git`` and ``S = ${UNPACKDIR}/git`` should be removed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The Git fetcher now unpacks into the :term:`BB_GIT_DEFAULT_DESTSUFFIX` directory
rather than the ``git/`` directory under :term:`UNPACKDIR`.
:term:`BB_GIT_DEFAULT_DESTSUFFIX` is set in :term:`OpenEmbedded-Core
(OE-Core)`'s :oe_git:`bitbake.conf
</openembedded-core/tree/meta/conf/bitbake.conf>` to :term:`BP`.

This location matches the default value of :term:`S` set by bitbake.conf, so :term:`S`
setting in recipes can and should be removed.

Note that when :term:`S` is set to a subdirectory of the git checkout, then it
should be instead adjusted according to the previous point::

   S = "${UNPACKDIR}/${BP}/something"

Note that "git" as the source checkout location can be hardcoded
in other places in recipes; when it's in :term:`SRC_URI`, replace with
:term:`BB_GIT_DEFAULT_DESTSUFFIX`, otherwise replace with :term:`BP`.

How to make those adjustments without tedious manual editing
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

The following sed command can be used to remove S = "${WORKDIR}/git
across a whole layer::

   sed -i "/^S = \"\${WORKDIR}\/git\"/d" `find . -name *.bb -o -name *.inc -o -name *.bbclass`

Then, the following command can tweak the remaining :term:`S` assignments to
refer to :term:`UNPACKDIR` instead of :term:`WORKDIR`::

   sed -i "s/^S = \"\${WORKDIR}\//S = \"\${UNPACKDIR}\//g" `find . -name *.bb -o -name *.inc -o -name *.bbclass`

The first change can introduce a lot of consecutive empty lines, so those can be removed with::

   sed -i -z -E 's/([ \t\f\v\r]*\n){3,}/\n\n/g' `find . -name *.bb -o -name *.inc`


BitBake Git fetcher ``tag`` parameter
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``tag=`` parameter of the Git fetcher (``git://``) was updated. The tag
commit SHA will be compared against the value supplied by the :term:`SRCREV`
variable or the ``rev=`` parameter in the URI in :term:`SRC_URI`. This is
strongly recommended to add to the URIs when using the Git fetcher for
repositories using tag releases.

Space around equal assignment
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

A new warning is now printed when there are no whitespaces around an ``=``
assignment in recipes::

   <filename>:<line number> has a lack of whitespace around the assignment: '<assignment>'

For example, the following assignments would print a warning::

   FOO="bar"
   FOO= "bar"
   FOO ="bar"

These should be replaced by::

   FOO = "bar"

Wic plugins containing dashes should be renamed
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

After a Python upgrade, :ref:`Wic <dev-manual/wic:creating partitioned images
using wic>` plugins containing dashes (``-``) for their filenames are **no
longer supported**. One must rename the plugin file and convert the dashes to
underscores (``_``).

It is also recommended to update any WKS file to convert dashes to underscores.
For example, the ``bootimg-partition.py`` plugin was renamed to
``bootimg_partition.py``. This means that any WKS file using this plugin must
change each ``--source bootimg-partition`` to ``--source bootimg_partition``.

However, the current WIC code automatically converts dashes to underscore for
any ``--source`` call, so existing WKS files will not break if they use upstream
plugins from :term:`OpenEmbedded-Core (OE-Core)`.

``fitImage`` no longer supporter for :term:`KERNEL_IMAGETYPE`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

The ``fitImage`` type for :term:`KERNEL_IMAGETYPE` is no longer supported. The
logic for creating a FIT image was moved out of the :ref:`ref-classes-kernel`
class. Instead, one should create a new recipe to build this FIT image, as
described in the :ref:`Removed Classes <migration-guides/migration-5.3:Removed
Classes>` section of the Migration notes for |yocto-ver| (|yocto-codename|).

Supported kernel versions
~~~~~~~~~~~~~~~~~~~~~~~~~

The :term:`OLDEST_KERNEL` setting is XXX in this release, meaning that
out the box, older kernels are not supported. See :ref:`4.3 migration notes
<migration-4.3-supported-kernel-versions>` for details.

Supported distributions
~~~~~~~~~~~~~~~~~~~~~~~

Compared to the previous releases, running BitBake is supported on new
GNU/Linux distributions:

-  XXX

On the other hand, some earlier distributions are no longer supported:

-  XXX

See :ref:`all supported distributions <system-requirements-supported-distros>`.

Rust language changes
~~~~~~~~~~~~~~~~~~~~~

systemd changes
~~~~~~~~~~~~~~~

Recipe changes
~~~~~~~~~~~~~~

Removed variables
~~~~~~~~~~~~~~~~~

The following variables have been removed:

-  ``BUILDHISTORY_RESET``: Setting this to non-empty used to remove the old
   content of the :ref:`ref-classes-buildhistory` as part of the current
   :term:`BitBake` invocation and replace it with information about what was
   built during the build. This was partly broken and hard to maintain.

Removed recipes
~~~~~~~~~~~~~~~

The following recipes have been removed in this release:

-  ``libsoup``: The last user in :term:`OpenEmbedded-Core (OE-Core)` was
   ``gst-examples``, which has been upgraded with its ``libsoup`` dependency
   dropped.

-  ``glibc-y2038-tests``: removed as the recipe only provides tests which are
   now provided by ``glibc-testsuite``.

-  ``python3-ndg-httpsclient``: The last dependency in core on this recipe was
   removed in May 2024 with dfa482f1998 ("python3-requests: cleanup RDEPENDS"),
   and there is no other user of this variable.

Removed :term:`PACKAGECONFIG` entries
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

-  ``dropbear``: ``enable-x11-forwarding`` (renamed to ``x11``)

-  ``libxml2``: ``ipv6``

-  ``squashfs-tools``: ``reproducible``

-  ``mesa``: ``kmsro``, ``osmesa``, ``xa``

Removed classes
~~~~~~~~~~~~~~~

The following classes have been removed in this release:

-  ``kernel-fitimage.bbclass``: the class has been replaced by the
   :ref:`ref-classes-kernel-fit-image` class. The new implementation resolves
   the long-standing :yocto_bugs:`bug 12912</show_bug.cgi?id=12912>`.

   If you are using the kernel FIT image support, you will need to:

   #. Make sure to include ``kernel-fit-extra-artifacts`` in your :term:`KERNEL_CLASSES`
      variable to ensure the required files are exposed to the :term:`DEPLOY_DIR_IMAGE`
      directory::

         KERNEL_CLASSES += "kernel-fit-extra-artifacts"

   #. Use the specific FIT image recipe rather than the base kernel recipe.
      For example, instead of::

         bitbake linux-yocto

      the FIT image is now build by::

         bitbake linux-yocto-fitimage

      For custom kernel recipes, creating a corresponding custom FIT image recipe
      is usually a good approach.

   #. If a FIT image is used as a replacement for the kernel image in the root
      filesystem, add the following configuration to your machine configuration
      file::

         # Create and deploy the vmlinux artifact which gets included into the FIT image
         KERNEL_CLASSES += "kernel-fit-extra-artifacts"

         # Do not install the kernel image package
         RRECOMMENDS:${KERNEL_PACKAGE_NAME}-base = ""
         # Install the FIT image package
         MACHINE_ESSENTIAL_EXTRA_RDEPENDS += "linux-yocto-fitimage"

         # Configure the image.bbclass to depend on the FIT image instead of only
         # the kernel to ensure the FIT image is built and deployed with the image
         KERNEL_DEPLOY_DEPEND = "linux-yocto-fitimage:do_deploy"

   See the :ref:`ref-classes-kernel-fit-image` section for more information.

-  ``icecc.bbclass``: Reports show that this class has been broken since Yocto
   Mickledore which suggests there are limited numbers of users. It doesn't have
   any automated testing and it would be hard to setup and maintain a testing
   environment for it. The original users/maintainers aren't using it now.

Removed features
~~~~~~~~~~~~~~~~

The following features have been removed in this release:

Miscellaneous changes
~~~~~~~~~~~~~~~~~~~~~

-  ``xserver-xorg``: remove sub-package ``${PN}-xwayland``, as ``xwayland`` is
   now its own recipe.
