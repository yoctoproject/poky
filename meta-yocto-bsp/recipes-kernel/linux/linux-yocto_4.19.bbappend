KBRANCH_genericx86  = "v4.19/standard/base"
KBRANCH_genericx86-64  = "v4.19/standard/base"
KBRANCH_edgerouter = "v4.19/standard/edgerouter"
KBRANCH_beaglebone-yocto = "v4.19/standard/beaglebone"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"
KMACHINE_beaglebone-yocto ?= "beaglebone"

SRCREV_machine_genericx86    ?= "5664dc14399edcaad210bbeb6343d84561fb3ea8"
SRCREV_machine_genericx86-64 ?= "5664dc14399edcaad210bbeb6343d84561fb3ea8"
SRCREV_machine_edgerouter ?= "5664dc14399edcaad210bbeb6343d84561fb3ea8"
SRCREV_machine_beaglebone-yocto ?= "5664dc14399edcaad210bbeb6343d84561fb3ea8"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_edgerouter = "edgerouter"
COMPATIBLE_MACHINE_beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION_genericx86 = "4.19.34"
LINUX_VERSION_genericx86-64 = "4.19.34"
LINUX_VERSION_edgerouter = "4.19.34"
LINUX_VERSION_beaglebone-yocto = "4.19.34"
