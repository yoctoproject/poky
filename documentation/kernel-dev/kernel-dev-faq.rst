.. SPDX-License-Identifier: CC-BY-2.0-UK

**********************
Kernel Development FAQ
**********************

.. _kernel-dev-faq-section:

Common Questions and Solutions
==============================

The following lists some solutions for common questions. How do I use my
own Linux kernel ``.config`` file? Refer to the "`Changing the
Configuration <#changing-the-configuration>`__" section for information.
How do I create configuration fragments? Refer to the "`Creating
Configuration Fragments <#creating-config-fragments>`__" section for
information. How do I use my own Linux kernel sources? Refer to the
"`Working With Your Own Sources <#working-with-your-own-sources>`__"
section for information. How do I install/not-install the kernel image
on the rootfs? The kernel image (e.g. ``vmlinuz``) is provided by the
``kernel-image`` package. Image recipes depend on ``kernel-base``. To
specify whether or not the kernel image is installed in the generated
root filesystem, override ``RDEPENDS_kernel-base`` to include or not
include "kernel-image". See the "`Using .bbappend Files in Your
Layer <&YOCTO_DOCS_DEV_URL;#using-bbappend-files>`__" section in the
Yocto Project Development Tasks Manual for information on how to use an
append file to override metadata. How do I install a specific kernel
module? Linux kernel modules are packaged individually. To ensure a
specific kernel module is included in an image, include it in the
appropriate machine
```RRECOMMENDS`` <&YOCTO_DOCS_REF_URL;#var-RRECOMMENDS>`__ variable.
These other variables are useful for installing specific modules:
```MACHINE_ESSENTIAL_EXTRA_RDEPENDS`` <&YOCTO_DOCS_REF_URL;#var-MACHINE_ESSENTIAL_EXTRA_RDEPENDS>`__
```MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS`` <&YOCTO_DOCS_REF_URL;#var-MACHINE_ESSENTIAL_EXTRA_RRECOMMENDS>`__
```MACHINE_EXTRA_RDEPENDS`` <&YOCTO_DOCS_REF_URL;#var-MACHINE_EXTRA_RDEPENDS>`__
```MACHINE_EXTRA_RRECOMMENDS`` <&YOCTO_DOCS_REF_URL;#var-MACHINE_EXTRA_RRECOMMENDS>`__
For example, set the following in the ``qemux86.conf`` file to include
the ``ab123`` kernel modules with images built for the ``qemux86``
machine: MACHINE_EXTRA_RRECOMMENDS += "kernel-module-ab123" For more
information, see the "`Incorporating Out-of-Tree
Modules <#incorporating-out-of-tree-modules>`__" section. How do I
change the Linux kernel command line? The Linux kernel command line is
typically specified in the machine config using the ``APPEND`` variable.
For example, you can add some helpful debug information doing the
following: APPEND += "printk.time=y initcall_debug debug"
