KBRANCH_genericx86  = "v5.10/standard/base"
KBRANCH_genericx86-64  = "v5.10/standard/base"
KBRANCH_edgerouter = "v5.10/standard/edgerouter"
KBRANCH_beaglebone-yocto = "v5.10/standard/beaglebone"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"
KMACHINE_beaglebone-yocto ?= "beaglebone"

SRCREV_machine_genericx86 ?= "f08df324ccdbc73b9f0c2de2826a2843bcdf651b"
SRCREV_machine_genericx86-64 ?= "f08df324ccdbc73b9f0c2de2826a2843bcdf651b"
SRCREV_machine_edgerouter ?= "1f3d7b6a85e98317771367e70824f7803ff9ca30"
SRCREV_machine_beaglebone-yocto ?= "f08df324ccdbc73b9f0c2de2826a2843bcdf651b"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_edgerouter = "edgerouter"
COMPATIBLE_MACHINE_beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION_genericx86 = "5.10.5"
LINUX_VERSION_genericx86-64 = "5.10.5"
LINUX_VERSION_edgerouter = "5.10.5"
LINUX_VERSION_beaglebone-yocto = "5.10.5"
