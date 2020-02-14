KBRANCH_genericx86  = "v5.4/standard/base"
KBRANCH_genericx86-64  = "v5.4/standard/base"
KBRANCH_edgerouter = "v5.4/standard/edgerouter"
KBRANCH_beaglebone-yocto = "v5.4/standard/beaglebone"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"
KMACHINE_beaglebone-yocto ?= "beaglebone"

SRCREV_machine_genericx86    ?= "cdda35317561d2741b396efa623ace0bd2212c16"
SRCREV_machine_genericx86-64 ?= "cdda35317561d2741b396efa623ace0bd2212c16"
SRCREV_machine_edgerouter ?= "cdda35317561d2741b396efa623ace0bd2212c16"
SRCREV_machine_beaglebone-yocto ?= "cdda35317561d2741b396efa623ace0bd2212c16"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_edgerouter = "edgerouter"
COMPATIBLE_MACHINE_beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION_genericx86 = "5.4.15"
LINUX_VERSION_genericx86-64 = "5.4.15"
LINUX_VERSION_edgerouter = "5.4.15"
LINUX_VERSION_beaglebone-yocto = "5.4.15"
