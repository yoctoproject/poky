KBRANCH_genericx86  = "standard/common-pc/base"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

SRCREV_machine_genericx86 ?= "f20047520a57322f05d95a18a5fbd082fb15cb87"
SRCREV_machine_routerstationpro ?= "4a94f39d429fa284ce69b13bb635b29b1319e372"
SRCREV_machine_mpc8315e-rdb ?= "f467c72937de0e4a2a66e21b9855c4aee844f936"
SRCREV_machine_beagleboard ?= "f20047520a57322f05d95a18a5fbd082fb15cb87"

COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"
COMPATIBLE_MACHINE_genericx86 = "genericx86"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_routerstationpro = "16777216"

KMACHINE_genericx86 = "common-pc"
