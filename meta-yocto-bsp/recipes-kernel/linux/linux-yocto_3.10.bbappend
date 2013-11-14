KBRANCH_genericx86  = "standard/common-pc/base"
KBRANCH_genericx86-64  = "standard/common-pc-64/base"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"

SRCREV_machine_genericx86 ?= "c03195ed6e3066494e3fb4be69154a57066e845b"
SRCREV_machine_genericx86-64 ?= "c03195ed6e3066494e3fb4be69154a57066e845b"
SRCREV_machine_routerstationpro ?= "2d91e201018c15e24fb83336dcb4029b8569eb9d"
SRCREV_machine_mpc8315e-rdb ?= "ac071526ffac37c907532933b628e4f64070f155"
SRCREV_machine_beagleboard ?= "3d9b0d130a00dd32e6061ac708eaaaed69e35c3d"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_routerstationpro = "16777216"
