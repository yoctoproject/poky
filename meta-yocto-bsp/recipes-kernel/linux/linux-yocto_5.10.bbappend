KBRANCH_genericx86  = "v5.10/standard/base"
KBRANCH_genericx86-64  = "v5.10/standard/base"
KBRANCH_edgerouter = "v5.10/standard/edgerouter"
KBRANCH_beaglebone-yocto = "v5.10/standard/beaglebone"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"
KMACHINE_beaglebone-yocto ?= "beaglebone"

SRCREV_machine_genericx86 ?= "84f6a75f64961e59d61bf3d70ab17e8bb430386b"
SRCREV_machine_genericx86-64 ?= "84f6a75f64961e59d61bf3d70ab17e8bb430386b"
SRCREV_machine_edgerouter ?= "4ab94e777d8b41ee1ee4c279259e9733bc8049b1"
SRCREV_machine_beaglebone-yocto ?= "941cc9c3849f96f7eaf109b1e35e05ba366aca56"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_edgerouter = "edgerouter"
COMPATIBLE_MACHINE_beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION_genericx86 = "5.10.99"
LINUX_VERSION_genericx86-64 = "5.10.99"
LINUX_VERSION_edgerouter = "5.10.63"
LINUX_VERSION_beaglebone-yocto = "5.10.63"
