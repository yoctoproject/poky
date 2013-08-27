KBRANCH_genericx86  = "standard/common-pc/base"
KBRANCH_genericx86-64  = "standard/common-pc-64/base"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"

SRCREV_machine_genericx86 ?= "6c1528b2b78d1ec7e75bb7a9880074ec35aa1aa0"
SRCREV_machine_genericx86-64 ?= "6c1528b2b78d1ec7e75bb7a9880074ec35aa1aa0"
SRCREV_machine_routerstationpro ?= "3991d03bd450e9363d5b6e97ede0628ba073db79"
SRCREV_machine_mpc8315e-rdb ?= "8d8339af518104db03f9c36b82f4372569e55b0a"
SRCREV_machine_beagleboard ?= "6c1528b2b78d1ec7e75bb7a9880074ec35aa1aa0"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_routerstationpro = "16777216"
