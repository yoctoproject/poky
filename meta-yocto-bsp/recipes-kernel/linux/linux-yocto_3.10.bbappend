KBRANCH_genericx86  = "standard/common-pc/base"
KBRANCH_genericx86-64  = "standard/common-pc-64/base"
KBRANCH_routerstationpro = "standard/routerstationpro"
KBRANCH_mpc8315e-rdb = "standard/fsl-mpc8315e-rdb"
KBRANCH_beagleboard = "standard/beagleboard"

KMACHINE_genericx86 ?= "common-pc"
KMACHINE_genericx86-64 ?= "common-pc-64"

SRCREV_machine_genericx86 ?= "79af968f2f26378798aec7a6d729ff5a371aae5f"
SRCREV_machine_genericx86-64 ?= "79af968f2f26378798aec7a6d729ff5a371aae5f"
SRCREV_machine_routerstationpro ?= "db4e91193fe3077fd6e822a88b9601731f27d397"
SRCREV_machine_mpc8315e-rdb ?= "10de7036a4ba156c44de2de720fd1495f747919c"
SRCREV_machine_beagleboard ?= "30cb7dc2c05815be5233f1a010f52ecdc4d97b01"

COMPATIBLE_MACHINE_genericx86 = "genericx86"
COMPATIBLE_MACHINE_genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE_mpc8315e-rdb = "mpc8315e-rdb"
COMPATIBLE_MACHINE_routerstationpro = "routerstationpro"
COMPATIBLE_MACHINE_beagleboard = "beagleboard"

# routerstationpro has a flash size of 16mb
KERNEL_IMAGE_MAXSIZE_routerstationpro = "16777216"
