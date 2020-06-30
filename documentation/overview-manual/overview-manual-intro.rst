.. SPDX-License-Identifier: CC-BY-2.0-UK

**********************************************
The Yocto Project Overview and Concepts Manual
**********************************************

.. _overview-manual-welcome:

Welcome
=======

Welcome to the Yocto Project Overview and Concepts Manual! This manual
introduces the Yocto Project by providing concepts, software overviews,
best-known-methods (BKMs), and any other high-level introductory
information suitable for a new Yocto Project user.

The following list describes what you can get from this manual:

-  `Introducing the Yocto Project <#overview-yp>`__\ *:* This chapter
   provides an introduction to the Yocto Project. You will learn about
   features and challenges of the Yocto Project, the layer model,
   components and tools, development methods, the
   `Poky <&YOCTO_DOCS_REF_URL;#poky>`__ reference distribution, the
   OpenEmbedded build system workflow, and some basic Yocto terms.

-  `The Yocto Project Development
   Environment <#overview-development-environment>`__\ *:* This chapter
   helps you get started understanding the Yocto Project development
   environment. You will learn about open source, development hosts,
   Yocto Project source repositories, workflows using Git and the Yocto
   Project, a Git primer, and information about licensing.

-  `Yocto Project Concepts <#overview-manual-concepts>`__\ *:* This
   chapter presents various concepts regarding the Yocto Project. You
   can find conceptual information about components, development,
   cross-toolchains, and so forth.

This manual does not give you the following:

-  *Step-by-step Instructions for Development Tasks:* Instructional
   procedures reside in other manuals within the Yocto Project
   documentation set. For example, the `Yocto Project Development Tasks
   Manual <&YOCTO_DOCS_DEV_URL;>`__ provides examples on how to perform
   various development tasks. As another example, the `Yocto Project
   Application Development and the Extensible Software Development Kit
   (eSDK) <&YOCTO_DOCS_SDK_URL;>`__ manual contains detailed
   instructions on how to install an SDK, which is used to develop
   applications for target hardware.

-  *Reference Material:* This type of material resides in an appropriate
   reference manual. For example, system variables are documented in the
   `Yocto Project Reference Manual <&YOCTO_DOCS_REF_URL;>`__. As another
   example, the `Yocto Project Board Support Package (BSP) Developer's
   Guide <&YOCTO_DOCS_BSP_URL;>`__ contains reference information on
   BSPs.

-  *Detailed Public Information Not Specific to the Yocto Project:* For
   example, exhaustive information on how to use the Source Control
   Manager Git is better covered with Internet searches and official Git
   Documentation than through the Yocto Project documentation.

.. _overview-manual-other-information:

Other Information
=================

Because this manual presents information for many different topics,
supplemental information is recommended for full comprehension. For
additional introductory information on the Yocto Project, see the `Yocto
Project Website <&YOCTO_HOME_URL;>`__. If you want to build an image
with no knowledge of Yocto Project as a way of quickly testing it out,
see the `Yocto Project Quick Build <&YOCTO_DOCS_BRIEF_URL;>`__ document.
For a comprehensive list of links and other documentation, see the
"`Links and Related
Documentation <&YOCTO_DOCS_REF_URL;#resources-links-and-related-documentation>`__"
section in the Yocto Project Reference Manual.
