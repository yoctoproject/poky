.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Creating a Custom Template Configuration Directory
**************************************************

If you are producing your own customized version of the build system for
use by other users, you might want to customize the message shown by the
setup script or you might want to change the template configuration
files (i.e. ``local.conf`` and ``bblayers.conf``) that are created in a
new build directory.

The OpenEmbedded build system uses the environment variable
``TEMPLATECONF`` to locate the directory from which it gathers
configuration information that ultimately ends up in the
:term:`Build Directory` ``conf`` directory.
By default, ``TEMPLATECONF`` is set as follows in the ``poky``
repository::

   TEMPLATECONF=${TEMPLATECONF:-meta-poky/conf}

This is the
directory used by the build system to find templates from which to build
some key configuration files. If you look at this directory, you will
see the ``bblayers.conf.sample``, ``local.conf.sample``, and
``conf-notes.txt`` files. The build system uses these files to form the
respective ``bblayers.conf`` file, ``local.conf`` file, and display the
list of BitBake targets when running the setup script.

To override these default configuration files with configurations you
want used within every new Build Directory, simply set the
``TEMPLATECONF`` variable to your directory. The ``TEMPLATECONF``
variable is set in the ``.templateconf`` file, which is in the top-level
:term:`Source Directory` folder
(e.g. ``poky``). Edit the ``.templateconf`` so that it can locate your
directory.

Best practices dictate that you should keep your template configuration
directory in your custom distribution layer. For example, suppose you
have a layer named ``meta-mylayer`` located in your home directory and
you want your template configuration directory named ``myconf``.
Changing the ``.templateconf`` as follows causes the OpenEmbedded build
system to look in your directory and base its configuration files on the
``*.sample`` configuration files it finds. The final configuration files
(i.e. ``local.conf`` and ``bblayers.conf`` ultimately still end up in
your Build Directory, but they are based on your ``*.sample`` files.
::

   TEMPLATECONF=${TEMPLATECONF:-meta-mylayer/myconf}

Aside from the ``*.sample`` configuration files, the ``conf-notes.txt``
also resides in the default ``meta-poky/conf`` directory. The script
that sets up the build environment (i.e.
:ref:`structure-core-script`) uses this file to
display BitBake targets as part of the script output. Customizing this
``conf-notes.txt`` file is a good way to make sure your list of custom
targets appears as part of the script's output.

Here is the default list of targets displayed as a result of running
either of the setup scripts::

   You can now run 'bitbake <target>'

   Common targets are:
       core-image-minimal
       core-image-sato
       meta-toolchain
       meta-ide-support

Changing the listed common targets is as easy as editing your version of
``conf-notes.txt`` in your custom template configuration directory and
making sure you have ``TEMPLATECONF`` set to your directory.

