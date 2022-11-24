.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Optionally Using an External Toolchain
**************************************

You might want to use an external toolchain as part of your development.
If this is the case, the fundamental steps you need to accomplish are as
follows:

-  Understand where the installed toolchain resides. For cases where you
   need to build the external toolchain, you would need to take separate
   steps to build and install the toolchain.

-  Make sure you add the layer that contains the toolchain to your
   ``bblayers.conf`` file through the
   :term:`BBLAYERS` variable.

-  Set the ``EXTERNAL_TOOLCHAIN`` variable in your ``local.conf`` file
   to the location in which you installed the toolchain.

A good example of an external toolchain used with the Yocto Project is
Mentor Graphics Sourcery G++ Toolchain. You can see information on how
to use that particular layer in the ``README`` file at
https://github.com/MentorEmbedded/meta-sourcery/. You can find
further information by reading about the
:term:`TCMODE` variable in the Yocto
Project Reference Manual's variable glossary.

