KBRANCH_atom-pc  = "standard/common-pc/atom-pc"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

SRCREV_machine_atom-pc ?= "59c2a9eb334c2def405c9d93ed6d8d4e822d1945"
SRCREV_machine_routerstationpro ?= "85c72b6f0775fb3f4babe266fc00b7e8e5305f01"
SRCREV_machine_mpc8315e-rdb ?= "dd6f6f7ca0d56fce2942509024647264ff9c9caa"
SRCREV_machine_beagleboard ?= "59c2a9eb334c2def405c9d93ed6d8d4e822d1945"


COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"
COMPATIBLE_MACHINE_atom-pc = "atom-pc"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_append_routerstationpro = "16777216"
