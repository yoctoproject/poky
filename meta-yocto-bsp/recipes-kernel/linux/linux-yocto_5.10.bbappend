KBRANCH_genericx86  = "v5.10/standard/base"
KBRANCH_genericx86-64  = "v5.10/standard/base"
KBRANCH_edgerouter = "v5.10/standard/edgerouter"
KBRANCH_beaglebone-yocto = "v5.10/standard/beaglebone"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"
KMACHINE_beaglebone-yocto ?= "beaglebone"

SRCREV_machine_genericx86 ?= "c274623910704eefcc98380a17649889ac7e9408"
SRCREV_machine_genericx86-64 ?= "c274623910704eefcc98380a17649889ac7e9408"
SRCREV_machine_edgerouter ?= "ac089d661362ba857e235c5630242039b150ae26"
SRCREV_machine_beaglebone-yocto ?= "a6df693a45f5787d4254e0998f52b4465b2a5efe"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_edgerouter = "edgerouter"
COMPATIBLE_MACHINE_beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION_genericx86 = "5.10.55"
LINUX_VERSION_genericx86-64 = "5.10.55"
LINUX_VERSION_edgerouter = "5.10.55"
LINUX_VERSION_beaglebone-yocto = "5.10.55"
