KBRANCH:genericx86  = "v5.15/standard/base"
KBRANCH:genericx86-64  = "v5.15/standard/base"
KBRANCH:edgerouter = "v5.15/standard/edgerouter"
KBRANCH:beaglebone-yocto = "v5.15/standard/beaglebone"

KMACHINE:genericx86 ?= "common-pc"
KMACHINE:genericx86-64 ?= "common-pc-64"
KMACHINE:beaglebone-yocto ?= "beaglebone"

SRCREV_machine:genericx86 ?= "2fca0fd719812ea2ff67630b01355aa80481623e"
SRCREV_machine:genericx86-64 ?= "2fca0fd719812ea2ff67630b01355aa80481623e"
SRCREV_machine:edgerouter ?= "26de0a7a59c56b63833a55dc33dbf70a7984d140"
SRCREV_machine:beaglebone-yocto ?= "3ec00e9ee0e41e4c402396425337c42da58c4d6f"

COMPATIBLE_MACHINE:genericx86 = "genericx86"
COMPATIBLE_MACHINE:genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE:edgerouter = "edgerouter"
COMPATIBLE_MACHINE:beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION:genericx86 = "5.15.52"
LINUX_VERSION:genericx86-64 = "5.15.52"
LINUX_VERSION:edgerouter = "5.15.52"
LINUX_VERSION:beaglebone-yocto = "5.15.52"
