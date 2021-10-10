Release 3.4 (honister)
======================

This section provides migration information for moving to the Yocto
Project 3.4 Release (codename "honister") from the prior release.

Override syntax changes
-----------------------

In this release, the ``:`` character replaces the use of ``_`` to
refer to an override, most commonly when making a conditional assignment
of a variable. This means that an entry like::

   SRC_URI_qemux86 = "file://somefile"

now becomes::

   SRC_URI:qemux86 = "file://somefile"

since ``qemux86`` is an override. This applies to any use of override
syntax, so the following::

   SRC_URI_append = " file://somefile"
   SRC_URI_append_qemux86 = " file://somefile2"
   SRC_URI_remove_qemux86-64 = " file://somefile3"
   SRC_URI_prepend_qemuarm = "file://somefile4 "
   FILES_${PN}-ptest = "${bindir}/xyz"
   IMAGE_CMD_tar = "tar"
   BASE_LIB_tune-cortexa76 = "lib"
   SRCREV_pn-bash = "abc"
   BB_TASK_NICE_LEVEL_task-testimage = '0'

would now become::

   SRC_URI:append = " file://somefile"
   SRC_URI:append:qemux86 = " file://somefile2"
   SRC_URI:remove:qemux86-64 = " file://somefile3"
   SRC_URI:prepend:qemuarm = "file://somefile4 "
   FILES:${PN}-ptest = "${bindir}/xyz"
   IMAGE_CMD:tar = "tar"
   BASE_LIB:tune-cortexa76 = "lib"
   SRCREV:pn-bash = "abc"
   BB_TASK_NICE_LEVEL:task-testimage = '0'

This also applies to
:ref:`variable queries to the datastore <bitbake:bitbake-user-manual/bitbake-user-manual-metadata:functions for accessing datastore variables>`,
for example using ``getVar`` and similar so ``d.getVar("RDEPENDS_${PN}")``
becomes ``d.getVar("RDEPENDS:${PN}")``.

Whilst some of these are fairly obvious such as :term:`MACHINE` and :term:`DISTRO`
overrides, some are less obvious, for example the packaging variables such as
:term:`RDEPENDS`, :term:`FILES` and so on taking package names (e.g. ``${PN}``,
``${PN}-ptest``) as overrides. These overrides are not always in
:term:`OVERRIDES` but applied conditionally in specific contexts
such as packaging. ``task-<taskname>`` is another context specific override, the
context being specific tasks in that case. Tune overrides are another special
case where some code does use them as overrides but some does not. We plan to try
and make the tune code use overrides more consistently in the future.

There are some variables which do not use override syntax which include the
suffix to variables in ``layer.conf`` files such as :term:`BBFILE_PATTERN`,
:term:`SRCREV`\ ``_xxx`` where ``xxx`` is a name from :term:`SRC_URI` and
:term:`PREFERRED_VERSION`\ ``_xxx``. In particular, ``layer.conf`` suffixes
may be the same as a :term:`DISTRO` override causing some confusion. We do
plan to try and improve consistency as these issues are identified.

To help with migration of layers, a script has been provided in OE-Core.
Once configured with the overrides used by a layer, this can be run as::

   <oe-core>/scripts/contrib/convert-overrides.py <layerdir>

.. note::

   Please read the notes in the script as it isn't entirely automatic and it isn't
   expected to handle every case. In particular, it needs to be told which overrides
   the layer uses (usually machine and distro names/overrides) and the result should
   be carefully checked since it can be a little enthusiastic and will convert
   references to ``_append``, ``_remove`` and ``_prepend`` in function and variable
   names.

For reference, this conversion is important as it allows BitBake to more reliably
determine what is an override and what is not, as underscores are also used in
variable names without intending to be overrides. This should allow us to proceed
with other syntax improvements and simplifications for usability. It also means
BitBake no longer has to guess and maintain large lookup lists just in case
e.g. ``functionname`` in ``my_functionname`` is an override, and thus should improve
efficiency.
