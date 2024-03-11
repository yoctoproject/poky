KBRANCH:genericx86  = "v5.15/standard/base"
KBRANCH:genericx86-64  = "v5.15/standard/base"
KBRANCH:edgerouter = "v5.15/standard/edgerouter"
KBRANCH:beaglebone-yocto = "v5.15/standard/beaglebone"

KMACHINE:genericx86 ?= "common-pc"
KMACHINE:genericx86-64 ?= "common-pc-64"
KMACHINE:beaglebone-yocto ?= "beaglebone"

SRCREV_machine:genericx86 ?= "7c82dac028864e8a608e70d3ac2dbc05b3cd1e14"
SRCREV_machine:genericx86-64 ?= "7c82dac028864e8a608e70d3ac2dbc05b3cd1e14"
SRCREV_machine:edgerouter ?= "23b867c1a618572a36b6283f55746a5162e08cc7"
SRCREV_machine:beaglebone-yocto ?= "4fca0c437367cf4d4fe158d74e0ae880a3f99d3c"

COMPATIBLE_MACHINE:genericx86 = "genericx86"
COMPATIBLE_MACHINE:genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE:edgerouter = "edgerouter"
COMPATIBLE_MACHINE:beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION:genericx86 = "5.15.150"
LINUX_VERSION:genericx86-64 = "5.15.150"
LINUX_VERSION:edgerouter = "5.15.150"
LINUX_VERSION:beaglebone-yocto = "5.15.150"
