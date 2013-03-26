KBRANCH_atom-pc  = "standard/common-pc/atom-pc"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

SRCREV_machine_atom-pc ?= "c994390cfa28339cbc1ec3b56eeec83a5fa75bb7"
SRCREV_machine_routerstationpro ?= "a45e1fb8bd549cbec860980f71dd0012449418e4"
SRCREV_machine_mpc8315e-rdb ?= "3663df787956385df7c6a9c964bb834a6106ac8b"
SRCREV_machine_beagleboard ?= "c994390cfa28339cbc1ec3b56eeec83a5fa75bb7"

COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"
COMPATIBLE_MACHINE_atom-pc = "atom-pc"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_append_routerstationpro = "16777216"
