KBRANCH_genericx86  = "standard/common-pc/base"
KBRANCH_genericx86-64  = "standard/common-pc-64/base"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"

SRCREV_machine_genericx86 ?= "a86e2b1eadd1f607d0d6ac5c4ab20a902714ddb1"
SRCREV_machine_genericx86-64 ?= "a86e2b1eadd1f607d0d6ac5c4ab20a902714ddb1"
SRCREV_machine_routerstationpro ?= "e2c76467906116a42a020ed0c76a06af720e5cf1"
SRCREV_machine_mpc8315e-rdb ?= "1ac2906d6d672f33e36c5add9b7d0e6277e34aaf"
SRCREV_machine_beagleboard ?= "e231c6220163d3c2a41cb380e1f759e8b222303c"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_routerstationpro = "16777216"
