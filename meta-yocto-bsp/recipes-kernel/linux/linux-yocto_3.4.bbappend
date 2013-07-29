KBRANCH_atom-pc  = "standard/common-pc/atom-pc"
KBRANCH_genericx86  = "standard/common-pc/atom-pc"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

SRCREV_machine_atom-pc ?= "cdd7a546922ca1c46c94adeec3b9c90dc9aaad2d"
SRCREV_machine_genericx86 ?= "cdd7a546922ca1c46c94adeec3b9c90dc9aaad2d"
SRCREV_machine_routerstationpro ?= "62b86dc8ac794cd97c61a99418d7429e6a83ec1a"
SRCREV_machine_mpc8315e-rdb ?= "b2f78892b3ff6cc940e4661f7b2017a73b289c73"
SRCREV_machine_beagleboard ?= "cdd7a546922ca1c46c94adeec3b9c90dc9aaad2d"

COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"
COMPATIBLE_MACHINE_atom-pc = "atom-pc"
COMPATIBLE_MACHINE_genericx86 = "genericx86"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_append_routerstationpro = "16777216"
