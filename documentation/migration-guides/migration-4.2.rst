.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Release 4.2 (mickledore)
========================

Migration notes for 4.2 (mickledore)
------------------------------------

This section provides migration information for moving to the Yocto
Project 4.2 Release (codename "mickledore") from the prior release.

.. _migration-4.2-python-3.8:

Python 3.8 is now the minimum required Python version version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

BitBake and OpenEmbedded-Core are now relying on Python 3.8,
making it a requirement to use a distribution providing at least this
version, or to use :term:`buildtools`.

.. _migration-4.2-gcc-8.0:

gcc 8.0 is now the minumum required GNU C compiler version
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This version, released in 2018, is a minimum requirement
to build the ``mesa-native`` recipe.

.. _migration-4.2-new-nvd-api:

Fetching the NVD vulnerability database through the 2.0 API
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This new version adds a new fetcher for the NVD database using the 2.0 API,
as the 1.0 API will be retired in 2023.

The implementation changes as little as possible, keeping the current
database format (but using a different database file for the transition
period), with a notable exception of not using the META table.

Here are minor changes that you may notice:

-  The database starts in 1999 instead of 2002
-  The complete fetch is longer (30 minutes typically)

.. _migration-4.2-rust-crate-checksums:

Rust: mandatory checksums for crates
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

This release now supports checksums for Rust crates and make
them mandatory for each crate in a recipe. See :yocto_git:`python3_bcrypt recipe changes
</poky/commit/?h=mickledore&id=0dcb5ab3462fdaaf1646b05a00c7150eea711a9a>`
for example.

The ``cargo-update-recipe-crates`` utility
:yocto_git:`has been extended </poky/commit/?h=mickledore&id=eef7fbea2c5bf59369390be4d5efa915591b7b22>`
to include such checksums. So, in case you need to add the list of checksums
to a recipe just inheriting the :ref:`ref-classes-cargo` class so far, you can
follow these steps:

#.  Make the recipe inherit :ref:`ref-classes-cargo-update-recipe-crates`
#.  Remove all ``crate://`` lines from the recipe
#.  Create an empty ``${BPN}-crates.inc`` file and make your recipe require it
#.  Execute ``bitbake -c update_crates your_recipe``
#.  Copy and paste the output of BitBake about the missing checksums into the
    ``${BPN}-crates.inc`` file.

.. _migration-4.2-supported-distributions:

Supported distributions
~~~~~~~~~~~~~~~~~~~~~~~

This release supports running BitBake on new GNU/Linux distributions:

-  Fedora 36 and 37
-  AlmaLinux 8.7 and 9.1
-  OpenSuse 15.4

On the other hand, some earlier distributions are no longer supported:

-  Debian 10.x
-  Fedora 34 and 35
-  AlmaLinux 8.5

See :ref:`all supported distributions <system-requirements-supported-distros>`.

.. _migration-4.2-misc-changes:

Miscellaneous changes
~~~~~~~~~~~~~~~~~~~~~

-  The ``OEBasic`` signature handler (see :term:`BB_SIGNATURE_HANDLER`) has been
   removed.
  

.. _migration-4.2-removed-variables:

Removed variables
~~~~~~~~~~~~~~~~~

The following variables have been removed:

-  ``SERIAL_CONSOLE``, deprecated since version 2.6, replaced by :term:`SERIAL_CONSOLES`.

.. _migration-4.2-removed-recipes:

Removed recipes
~~~~~~~~~~~~~~~

The following recipes have been removed in this release:

-  ``python3-picobuild``: after switching to ``python3-build``
-  ``python3-strict-rfc3339``: unmaintained and not needed by anything in
   :oe_git:`openembedded-core </openembedded-core>`
   or :oe_git:`meta-openembedded </meta-openembedded>`.

.. _migration-4.2-removed-classes:

Removed classes
~~~~~~~~~~~~~~~

The following classes have been removed in this release:

-  ``rust-bin``: no longer used in Poky

