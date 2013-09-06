KBRANCH_genericx86  = "standard/common-pc/base"
KBRANCH_genericx86-64  = "standard/common-pc-64/base"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"

SRCREV_machine_genericx86 ?= "ebc8428fdd938cfdfcdcadd77c3308ece6a57de1"
SRCREV_machine_genericx86-64 ?= "ebc8428fdd938cfdfcdcadd77c3308ece6a57de1"
SRCREV_machine_routerstationpro ?= "80d9c863208fba7d8af6afe7b9167808635a56c0"
SRCREV_machine_mpc8315e-rdb ?= "b9b4bf71249ac7a24420913aa90f7ba75578d5a5"
SRCREV_machine_beagleboard ?= "ebc8428fdd938cfdfcdcadd77c3308ece6a57de1"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_routerstationpro = "16777216"
