.. SPDX-License-Identifier: CC-BY-SA-2.0-UK

Contributing Changes to a Component
************************************

Contributions to the Yocto Project and OpenEmbedded are very welcome.
Because the system is extremely configurable and flexible, we recognize
that developers will want to extend, configure or optimize it for their
specific uses.

.. _ref-why-mailing-lists:

Contributing through mailing lists --- Why not using web-based workflows?
=========================================================================

Both Yocto Project and OpenEmbedded have many key components that are
maintained by patches being submitted on mailing lists. We appreciate this
approach does look a little old fashioned when other workflows are available
through web technology such as GitHub, GitLab and others. Since we are often
asked this question, we’ve decided to document the reasons for using mailing
lists.

One significant factor is that we value peer review. When a change is proposed
to many of the core pieces of the project, it helps to have many eyes of review
go over them. Whilst there is ultimately one maintainer who needs to make the
final call on accepting or rejecting a patch, the review is made by many eyes
and the exact people reviewing it are likely unknown to the maintainer. It is
often the surprise reviewer that catches the most interesting issues!

This is in contrast to the "GitHub" style workflow where either just a
maintainer makes that review, or review is specifically requested from
nominated people. We believe there is significant value added to the codebase
by this peer review and that moving away from mailing lists would be to the
detriment of our code.

We also need to acknowledge that many of our developers are used to this
mailing list workflow and have worked with it for years, with tools and
processes built around it. Changing away from this would result in a loss
of key people from the project, which would again be to its detriment.

The projects are acutely aware that potential new contributors find the
mailing list approach off-putting and would prefer a web-based GUI.
Since we don’t believe that can work for us, the project is aiming to ensure
`patchwork <https://patchwork.yoctoproject.org/>`__ is available to help track
patch status and also looking at how tooling can provide more feedback to users
about patch status. We are looking at improving tools such as ``patchtest`` to
test user contributions before they hit the mailing lists and also at better
documenting how to use such workflows since we recognise that whilst this was
common knowledge a decade ago, it might not be as familiar now.

Finding a Suitable Mailing List
===============================

The Yocto Project and OpenEmbedded use a mailing list and a patch-based
workflow that is similar to the Linux kernel but contains important
differences. In general, there is a mailing list through which you can submit
patches. You should send patches to the appropriate mailing list so that they
can be reviewed and merged by the appropriate maintainer. The specific mailing
list you need to use depends on the location of the code you are
changing. Each component (e.g. layer) should have a ``README`` file that
indicates where to send the changes and which process to follow.

You can send the patches to the mailing list using whichever approach you
feel comfortable with to generate the patches. Once sent, the patches are
usually reviewed by the community at large. If somebody has concerns
any of the the patches, they will usually voice their concern over the mailing
list. If patches do not receive any negative reviews, the maintainer
of the affected layer typically takes them, tests them, and then
based on successful testing, merges them.

The "poky" repository, which is the Yocto Project's reference build
environment, is a hybrid repository that contains several individual
pieces (e.g. BitBake, Metadata, documentation, and so forth) built using
the combo-layer tool. The upstream location used for submitting changes
varies by component:

-  *Core Metadata:* Send your patches to the
   :oe_lists:`openembedded-core </g/openembedded-core>`
   mailing list. For example, a change to anything under the ``meta`` or
   ``scripts`` directories should be sent to this mailing list.

-  *BitBake:* For changes to BitBake (i.e. anything under the
   ``bitbake`` directory), send your patches to the
   :oe_lists:`bitbake-devel </g/bitbake-devel>`
   mailing list.

-  *"meta-\*" trees:* These trees contain Metadata. Use the
   :yocto_lists:`poky </g/poky>` mailing list.

-  *Documentation*: For changes to the Yocto Project documentation, use the
   :yocto_lists:`docs </g/docs>` mailing list.

For changes to other layers hosted in the Yocto Project source
repositories (i.e. ``yoctoproject.org``) and tools use the
:yocto_lists:`yocto </g/yocto/>` general mailing list.

.. note::

   Sometimes a layer's documentation specifies to use a particular
   mailing list. If so, use that list.

For additional recipes that do not fit into the core Metadata, you
should determine which layer the recipe should go into and submit the
changes in the manner recommended by the documentation (e.g. the
``README`` file) supplied with the layer. If in doubt, please ask on the
:yocto_lists:`yocto </g/yocto/>` general mailing list or on the
:oe_lists:`openembedded-devel </g/openembedded-devel>` mailing list.

You can also push changes upstream and request a maintainer to pull the
changes into the component's upstream repository. You do this by pushing
to a contribution repository that is upstream. See the
":ref:`overview-manual/development-environment:git workflows and the yocto project`"
section in the Yocto Project Overview and Concepts Manual for additional
concepts on working in the Yocto Project development environment.

Maintainers commonly use ``-next`` branches to test submissions prior to
merging patches. Thus, you can get an idea of the status of a patch based on
whether the patch has been merged into one of these branches. The commonly
used testing branches for OpenEmbedded-Core are as follows:

-  *openembedded-core "master-next" branch:* This branch is part of the
   :oe_git:`openembedded-core </openembedded-core/>` repository and contains
   proposed changes to the core metadata.

-  *poky "master-next" branch:* This branch is part of the
   :yocto_git:`poky </poky/>` repository and combines proposed
   changes to BitBake, the core metadata and the poky distro.

Similarly, stable branches maintained by the project may have corresponding
``-next`` branches which collect proposed changes. For example,
``&DISTRO_NAME_NO_CAP;-next`` and ``&DISTRO_NAME_NO_CAP_MINUS_ONE;-next``
branches in both the "openembdedded-core" and "poky" repositories.

Other layers may have similar testing branches but there is no formal
requirement or standard for these so please check the documentation for the
layers you are contributing to.

The following sections provide procedures for submitting changes.

Preparing Changes for Submission
================================

The first thing to do is to create a new branch in your local Git repository
for your changes, starting from the reference branch in the upstream
repository (often called ``master``)::

   $ git checkout <ref-branch>
   $ git checkout -b my-changes

If you have completely unrelated sets of changes to submit, you should even
create one branch for each set.

Then, in each branch, you should group your changes into small, controlled and
isolated ones. Keeping changes small and isolated aids review, makes
merging/rebasing easier and keeps the change history clean should anyone need
to refer to it in future.

To this purpose, you should create *one Git commit per change*,
corresponding to each of the patches you will eventually submit.
So, for each identified change:

#. *Stage Your Change:* Stage your change by using the ``git add``
   command on each file you modified.

#. *Commit Your Change:* Commit the change by using the ``git commit``
   command. Make sure your commit information follows standards by
   following these accepted conventions:

   -  Be sure to include a "Signed-off-by:" line in the same style as
      required by the Linux kernel. This can be done by using the
      ``git commit -s`` command. Adding this line signifies that you,
      the submitter, have agreed to the `Developer's Certificate of Origin 1.1
      <https://www.kernel.org/doc/html/latest/process/submitting-patches.html#sign-your-work-the-developer-s-certificate-of-origin>`__
      as follows:

      .. code-block:: none

         Developer's Certificate of Origin 1.1

         By making a contribution to this project, I certify that:

         (a) The contribution was created in whole or in part by me and I
             have the right to submit it under the open source license
             indicated in the file; or

         (b) The contribution is based upon previous work that, to the best
             of my knowledge, is covered under an appropriate open source
             license and I have the right under that license to submit that
             work with modifications, whether created in whole or in part
             by me, under the same open source license (unless I am
             permitted to submit under a different license), as indicated
             in the file; or

         (c) The contribution was provided directly to me by some other
             person who certified (a), (b) or (c) and I have not modified
             it.

         (d) I understand and agree that this project and the contribution
             are public and that a record of the contribution (including all
             personal information I submit with it, including my sign-off) is
             maintained indefinitely and may be redistributed consistent with
             this project or the open source license(s) involved.

   -  Provide a single-line summary of the change and, if more
      explanation is needed, provide more detail in the body of the
      commit. This summary is typically viewable in the "shortlist" of
      changes. Thus, providing something short and descriptive that
      gives the reader a summary of the change is useful when viewing a
      list of many commits. You should prefix this short description
      with the recipe name (if changing a recipe), or else with the
      short form path to the file being changed.

      .. note::

         To find a suitable prefix for the commit summary, a good idea
         is to look for prefixes used in previous commits touching the
         same files or directories::

            git log --oneline <paths>

   -  For the body of the commit message, provide detailed information
      that describes what you changed, why you made the change, and the
      approach you used. It might also be helpful if you mention how you
      tested the change. Provide as much detail as you can in the body
      of the commit message.

      .. note::

         If the single line summary is enough to describe a simple
         change, the body of the commit message can be left empty.

   -  If the change addresses a specific bug or issue that is associated
      with a bug-tracking ID, include a reference to that ID in your
      detailed description. For example, the Yocto Project uses a
      specific convention for bug references --- any commit that addresses
      a specific bug should use the following form for the detailed
      description. Be sure to use the actual bug-tracking ID from
      Bugzilla for bug-id::

         Fixes [YOCTO #bug-id]

         detailed description of change

Using Email to Submit Patches
=============================

Depending on the components changed, you need to submit the email to a
specific mailing list. For some guidance on which mailing list to use,
see the ":ref:`contributor-guide/submit-changes:finding a suitable mailing list`"
section above.

Here is the general procedure on how to create and submit patches through email:

#. *Generate Patches for your Branch:* The ``git format-patch`` command for
   generate patch files for each of the commits in your branch. You need
   to pass the reference branch your branch starts from::

      $ git format-patch <ref-branch>

   After the command is run, the current directory contains numbered
   ``.patch`` files for the commits in your branch.

   If you have more than one patch, you should also use the ``--cover``
   option with the command, which generates a cover letter as the first
   "patch" in the series. You can then edit the cover letter to provide
   a description for the series of patches. Run ``man git-format-patch``
   for details about this command.

#. *Send the patches via email:* Send the patches to the recipients and
   relevant mailing lists by using the ``git send-email`` command.

   .. note::

      In order to use ``git send-email``, you must have the proper Git packages
      installed on your host.
      For Ubuntu, Debian, and Fedora the package is ``git-email``.

   The ``git send-email`` command sends email by using a local or remote
   Mail Transport Agent (MTA) such as ``msmtp``, ``sendmail``, or
   through a direct ``smtp`` configuration in your Git ``~/.gitconfig``
   file. If you are submitting patches through email only, it is very
   important that you submit them without any whitespace or HTML
   formatting that either you or your mailer introduces. The maintainer
   that receives your patches needs to be able to save and apply them
   directly from your emails. A good way to verify that what you are
   sending will be applicable by the maintainer is to do a dry run and
   send them to yourself and then save and apply them as the maintainer
   would.

   The ``git send-email`` command is the preferred method for sending
   your patches using email since there is no risk of compromising
   whitespace in the body of the message, which can occur when you use
   your own mail client. The command also has several options that let
   you specify recipients and perform further editing of the email
   message. Here's a typical usage of this command::

     git send-email --to <mailing-list-address> *.patch

   Run ``man git-send-email`` for more details about this command.

The Yocto Project uses a `Patchwork instance <https://patchwork.yoctoproject.org/>`__
to track the status of patches submitted to the various mailing lists and to
support automated patch testing. Each submitted patch is checked for common
mistakes and deviations from the expected patch format and submitters are
notified by ``patchtest`` if such mistakes are found. This process helps to
reduce the burden of patch review on maintainers.

.. note::

   This system is imperfect and changes can sometimes get lost in the flow.
   Asking about the status of a patch or change is reasonable if the change
   has been idle for a while with no feedback.

Using Scripts to Push a Change Upstream and Request a Pull
==========================================================

For larger patch series it is preferable to send a pull request which not
only includes the patch but also a pointer to a branch that can be pulled
from. This involves making a local branch for your changes, pushing this
branch to an accessible repository and then using the ``create-pull-request``
and ``send-pull-request`` scripts from openembedded-core to create and send a
patch series with a link to the branch for review.

Follow this procedure to push a change to an upstream "contrib" Git
repository once the steps in
":ref:`contributor-guide/submit-changes:preparing changes for submission`"
have been followed:

.. note::

   You can find general Git information on how to push a change upstream
   in the
   `Git Community Book <https://git-scm.com/book/en/v2/Distributed-Git-Distributed-Workflows>`__.

#. *Push Your Commits to a "Contrib" Upstream:* If you have arranged for
   permissions to push to an upstream contrib repository, push the
   change to that repository::

      $ git push upstream_remote_repo local_branch_name

   For example, suppose you have permissions to push
   into the upstream ``meta-intel-contrib`` repository and you are
   working in a local branch named `your_name`\ ``/README``. The following
   command pushes your local commits to the ``meta-intel-contrib``
   upstream repository and puts the commit in a branch named
   `your_name`\ ``/README``::

      $ git push meta-intel-contrib your_name/README

#. *Determine Who to Notify:* Determine the maintainer or the mailing
   list that you need to notify for the change.

   Before submitting any change, you need to be sure who the maintainer
   is or what mailing list that you need to notify. Use either these
   methods to find out:

   -  *Maintenance File:* Examine the ``maintainers.inc`` file, which is
      located in the :term:`Source Directory` at
      ``meta/conf/distro/include``, to see who is responsible for code.

   -  *Search by File:* Using :ref:`overview-manual/development-environment:git`, you can
      enter the following command to bring up a short list of all
      commits against a specific file::

         git shortlog -- filename

      Just provide the name of the file for which you are interested. The
      information returned is not ordered by history but does include a
      list of everyone who has committed grouped by name. From the list,
      you can see who is responsible for the bulk of the changes against
      the file.

   -  *Find the Mailing List to Use:* See the
      ":ref:`contributor-guide/submit-changes:finding a suitable mailing list`"
      section above.

#. *Make a Pull Request:* Notify the maintainer or the mailing list that
   you have pushed a change by making a pull request.

   The Yocto Project provides two scripts that conveniently let you
   generate and send pull requests to the Yocto Project. These scripts
   are ``create-pull-request`` and ``send-pull-request``. You can find
   these scripts in the ``scripts`` directory within the
   :term:`Source Directory` (e.g.
   ``poky/scripts``).

   Using these scripts correctly formats the requests without
   introducing any whitespace or HTML formatting. The maintainer that
   receives your patches either directly or through the mailing list
   needs to be able to save and apply them directly from your emails.
   Using these scripts is the preferred method for sending patches.

   First, create the pull request. For example, the following command
   runs the script, specifies the upstream repository in the contrib
   directory into which you pushed the change, and provides a subject
   line in the created patch files::

      $ poky/scripts/create-pull-request -u meta-intel-contrib -s "Updated Manual Section Reference in README"

   Running this script forms ``*.patch`` files in a folder named
   ``pull-``\ `PID` in the current directory. One of the patch files is a
   cover letter.

   Before running the ``send-pull-request`` script, you must edit the
   cover letter patch to insert information about your change. After
   editing the cover letter, send the pull request. For example, the
   following command runs the script and specifies the patch directory
   and email address. In this example, the email address is a mailing
   list::

      $ poky/scripts/send-pull-request -p ~/meta-intel/pull-10565 -t meta-intel@lists.yoctoproject.org

   You need to follow the prompts as the script is interactive.

   .. note::

      For help on using these scripts, simply provide the ``-h``
      argument as follows::

              $ poky/scripts/create-pull-request -h
              $ poky/scripts/send-pull-request -h

Responding to Patch Review
==========================

You may get feedback on your submitted patches from other community members
or from the automated patchtest service. If issues are identified in your
patch then it is usually necessary to address these before the patch will be
accepted into the project. In this case you should amend the patch according
to the feedback and submit an updated version to the relevant mailing list,
copying in the reviewers who provided feedback to the previous version of the
patch.

The patch should be amended using ``git commit --amend`` or perhaps ``git
rebase`` for more expert git users. You should also modify the ``[PATCH]``
tag in the email subject line when sending the revised patch to mark the new
iteration as ``[PATCH v2]``, ``[PATCH v3]``, etc as appropriate. This can be
done by passing the ``-v`` argument to ``git format-patch`` with a version
number.

Lastly please ensure that you also test your revised changes. In particular
please don't just edit the patch file written out by ``git format-patch`` and
resend it.

Submitting Changes to Stable Release Branches
=============================================

The process for proposing changes to a Yocto Project stable branch differs
from the steps described above. Changes to a stable branch must address
identified bugs or CVEs and should be made carefully in order to avoid the
risk of introducing new bugs or breaking backwards compatibility. Typically
bug fixes must already be accepted into the master branch before they can be
backported to a stable branch unless the bug in question does not affect the
master branch or the fix on the master branch is unsuitable for backporting.

The list of stable branches along with the status and maintainer for each
branch can be obtained from the
:yocto_wiki:`Releases wiki page </Releases>`.

.. note::

   Changes will not typically be accepted for branches which are marked as
   End-Of-Life (EOL).

With this in mind, the steps to submit a change for a stable branch are as
follows:

#. *Identify the bug or CVE to be fixed:* This information should be
   collected so that it can be included in your submission.

   See :ref:`dev-manual/vulnerabilities:checking for vulnerabilities`
   for details about CVE tracking.

#. *Check if the fix is already present in the master branch:* This will
   result in the most straightforward path into the stable branch for the
   fix.

   #. *If the fix is present in the master branch --- submit a backport request
      by email:* You should send an email to the relevant stable branch
      maintainer and the mailing list with details of the bug or CVE to be
      fixed, the commit hash on the master branch that fixes the issue and
      the stable branches which you would like this fix to be backported to.

   #. *If the fix is not present in the master branch --- submit the fix to the
      master branch first:* This will ensure that the fix passes through the
      project's usual patch review and test processes before being accepted.
      It will also ensure that bugs are not left unresolved in the master
      branch itself. Once the fix is accepted in the master branch a backport
      request can be submitted as above.

   #. *If the fix is unsuitable for the master branch --- submit a patch
      directly for the stable branch:* This method should be considered as a
      last resort. It is typically necessary when the master branch is using
      a newer version of the software which includes an upstream fix for the
      issue or when the issue has been fixed on the master branch in a way
      that introduces backwards incompatible changes. In this case follow the
      steps in ":ref:`contributor-guide/submit-changes:preparing changes for submission`" and
      ":ref:`contributor-guide/submit-changes:using email to submit patches`"
      but modify the subject header of your patch
      email to include the name of the stable branch which you are
      targetting. This can be done using the ``--subject-prefix`` argument to
      ``git format-patch``, for example to submit a patch to the dunfell
      branch use
      ``git format-patch --subject-prefix='&DISTRO_NAME_NO_CAP_MINUS_ONE;][PATCH' ...``.
