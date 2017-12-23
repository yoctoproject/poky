KBRANCH_genericx86  = "standard/base"
KBRANCH_genericx86-64  = "standard/base"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"
KBRANCH_edgerouter = "standard/edgerouter"
KBRANCH_beaglebone = "standard/beaglebone"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"

SRCREV_machine_genericx86    ?= "16de0149674ed12d983b77a453852ac2e64584b4"
SRCREV_machine_genericx86-64 ?= "16de0149674ed12d983b77a453852ac2e64584b4"
SRCREV_machine_edgerouter ?= "558fe84d691abbb8c8f5e149aa29ef4a478d0128"
SRCREV_machine_beaglebone-yocto ?= "558fe84d691abbb8c8f5e149aa29ef4a478d0128"
SRCREV_machine_mpc8315e-rdb ?= "f3c9a151c503869e39cea788b504b26b21e83ea4"


COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_edgerouter = "edgerouter"
COMPATIBLE_MACHINE_beaglebone = "beaglebone"
COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"

LINUX_VERSION_genericx86 = "4.12.12"
LINUX_VERSION_genericx86-64 = "4.12.12"
LINUX_VERSION_edgerouter = "4.12.18"
LINUX_VERSION_beaglebone-yocto = "4.12.18"
LINUX_VERSION_mpc8315e-rdb = "4.12.18"
