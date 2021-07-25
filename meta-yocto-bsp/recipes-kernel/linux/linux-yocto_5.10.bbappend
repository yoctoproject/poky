KBRANCH:genericx86  = "v5.10/standard/base"
KBRANCH:genericx86-64  = "v5.10/standard/base"
KBRANCH:edgerouter = "v5.10/standard/edgerouter"
KBRANCH:beaglebone-yocto = "v5.10/standard/beaglebone"

KMACHINE:genericx86 ?= "common-pc"
KMACHINE:genericx86-64 ?= "common-pc-64"
KMACHINE:beaglebone-yocto ?= "beaglebone"

SRCREV_machine:genericx86 ?= "ab49d2db98bdee2c8c6e17fb59ded9e5292b0f41"
SRCREV_machine:genericx86-64 ?= "ab49d2db98bdee2c8c6e17fb59ded9e5292b0f41"
SRCREV_machine:edgerouter ?= "274d63799465eebfd201b3e8251f16d29e93a978"
SRCREV_machine:beaglebone-yocto ?= "ab49d2db98bdee2c8c6e17fb59ded9e5292b0f41"

COMPATIBLE_MACHINE:genericx86 = "genericx86"
COMPATIBLE_MACHINE:genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE:edgerouter = "edgerouter"
COMPATIBLE_MACHINE:beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION:genericx86 = "5.10.43"
LINUX_VERSION:genericx86-64 = "5.10.43"
LINUX_VERSION:edgerouter = "5.10.43"
LINUX_VERSION:beaglebone-yocto = "5.10.43"
