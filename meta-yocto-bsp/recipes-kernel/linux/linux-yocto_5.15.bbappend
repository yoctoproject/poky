KBRANCH:genericx86  = "v5.15/standard/base"
KBRANCH:genericx86-64  = "v5.15/standard/base"
KBRANCH:edgerouter = "v5.15/standard/edgerouter"
KBRANCH:beaglebone-yocto = "v5.15/standard/beaglebone"

KMACHINE:genericx86 ?= "common-pc"
KMACHINE:genericx86-64 ?= "common-pc-64"
KMACHINE:beaglebone-yocto ?= "beaglebone"

SRCREV_machine:genericx86 ?= "8cd3f1c8dc13e8fa2d9a25ce0285d3526705eea7"
SRCREV_machine:genericx86-64 ?= "8cd3f1c8dc13e8fa2d9a25ce0285d3526705eea7"
SRCREV_machine:edgerouter ?= "7d45a6cb45c174d33daf3c2af544861a6c1ece53"
SRCREV_machine:beaglebone-yocto ?= "d3780eabef136a2129ee69249512abd0d69ccd04"

COMPATIBLE_MACHINE:genericx86 = "genericx86"
COMPATIBLE_MACHINE:genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE:edgerouter = "edgerouter"
COMPATIBLE_MACHINE:beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION:genericx86 = "5.15.78"
LINUX_VERSION:genericx86-64 = "5.15.78"
LINUX_VERSION:edgerouter = "5.15.78"
LINUX_VERSION:beaglebone-yocto = "5.15.78"
