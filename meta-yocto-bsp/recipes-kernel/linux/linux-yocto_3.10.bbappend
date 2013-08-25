KBRANCH_atom-pc  = "standard/common-pc/atom-pc"
KBRANCH_genericx86  = "standard/common-pc/atom-pc"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

SRCREV_machine_atom-pc ?= "6c1528b2b78d1ec7e75bb7a9880074ec35aa1aa0"
SRCREV_machine_genericx86 ?= "f20047520a57322f05d95a18a5fbd082fb15cb87"
SRCREV_machine_routerstationpro ?= "3991d03bd450e9363d5b6e97ede0628ba073db79"
SRCREV_machine_mpc8315e-rdb ?= "8d8339af518104db03f9c36b82f4372569e55b0a"
SRCREV_machine_beagleboard ?= "6c1528b2b78d1ec7e75bb7a9880074ec35aa1aa0"

COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"
COMPATIBLE_MACHINE_atom-pc = "atom-pc"
COMPATIBLE_MACHINE_genericx86 = "genericx86"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_routerstationpro = "16777216"
