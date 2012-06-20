require recipes-kernel/linux-libc-headers/linux-libc-headers.inc
include recipes-kernel/linux/linux-yocto.inc

B = "${S}"

INHIBIT_DEFAULT_DEPS = "1"
DEPENDS += "unifdef-native"
PROVIDES = "linux-libc-headers"
RPROVIDES_${PN}-dev = "linux-libc-headers-dev"
RPROVIDES_${PN}-dbg = "linux-libc-headers-dbg"
SRCREV = "21ab5dca134a6bf1316aa59f69f9ee9e091d5702"
KBRANCH ?= "standard/base"
KMETA ?= "meta"
PV = "3.2+git-${SRCPV}"
PR = "r5"

SRC_URI = "git://git.yoctoproject.org/linux-yocto-3.2;protocol=git;nocheckout=1;branch=${KBRANCH},meta;name=machine,meta"

# force this to empty to prevent installation failures, we aren't
# building a device tree as part of kern headers
KERNEL_DEVICETREE = ""

inherit kernel-arch

do_configure() {
	oe_runmake allnoconfig
}

do_install() {
	oe_runmake headers_install INSTALL_HDR_PATH=${D}${exec_prefix}

        # The ..install.cmd conflicts between various configure runs
        find ${D}${includedir} -name ..install.cmd | xargs rm -f
}

# The following tasks are not required when we just want
# headers. So we override and stub them out.
do_kernel_configme() {
}

do_patch () {
}

do_compile () {
}

do_validate_branches () {
}

do_kernel_configcheck () {
}

BBCLASSEXTEND = "nativesdk"
