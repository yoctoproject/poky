KBRANCH_genericx86  = "standard/common-pc/base"
KBRANCH_genericx86-64  = "standard/common-pc-64/base"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"

SRCREV_machine_genericx86 ?= "3e0a296fae952d8d93eb0f96566bf6d4a978c8ee"
SRCREV_machine_genericx86-64 ?= "3e0a296fae952d8d93eb0f96566bf6d4a978c8ee"
SRCREV_machine_routerstationpro ?= "c951f46b196f287d90d016d2441c91a3b86669f1"
SRCREV_machine_mpc8315e-rdb ?= "74ed53110138055ff6b87e2af28a2fd31a8bf9c6"
SRCREV_machine_beagleboard ?= "97c2adb38b76e0b1d6319986818d4b536e244dd6"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_routerstationpro = "16777216"
