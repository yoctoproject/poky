require recipes-kernel/linux-libc-headers/linux-libc-headers.inc

B = "${S}"

PROVIDES = "linux-libc-headers"
RPROVIDES_${PN}-dev = "linux-libc-headers-dev"
RPROVIDES_${PN}-dbg = "linux-libc-headers-dbg"

KBRANCH = "standard/base"
SRCREV = "a1cdb60720c452c3965eaec3ec2cd10f06261cc5"

PV = "3.4+git-${SRCPV}"
PR = "r6"

SRCREV_FORMAT ?= "meta_machine"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-3.4.git;protocol=git;nocheckout=1;branch=${KBRANCH},meta;name=machine,meta"

# force this to empty to prevent installation failures, we aren't
# building a device tree as part of kern headers
KERNEL_DEVICETREE = ""

inherit kernel-arch

# The following tasks are not required when we just want
# headers. So we override and stub them out.
do_kernel_configme() {
}

do_patch () {
}

do_kernel_configcheck () {
}

BBCLASSEXTEND = "nativesdk"
