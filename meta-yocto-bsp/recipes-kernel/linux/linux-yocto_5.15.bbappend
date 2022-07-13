KBRANCH:genericx86  = "v5.15/standard/base"
KBRANCH:genericx86-64  = "v5.15/standard/base"
KBRANCH:edgerouter = "v5.15/standard/edgerouter"
KBRANCH:beaglebone-yocto = "v5.15/standard/beaglebone"

KMACHINE:genericx86 ?= "common-pc"
KMACHINE:genericx86-64 ?= "common-pc-64"
KMACHINE:beaglebone-yocto ?= "beaglebone"

SRCREV_machine:genericx86 ?= "6c085baf183868ed45d8c1d44408d7b24724cde5"
SRCREV_machine:genericx86-64 ?= "6c085baf183868ed45d8c1d44408d7b24724cde5"
SRCREV_machine:edgerouter ?= "e90573857c176458965737d77b1747be83fe7edc"
SRCREV_machine:beaglebone-yocto ?= "d91bb88e58c575e7c3b9fb111b6711a206eba64b"

COMPATIBLE_MACHINE:genericx86 = "genericx86"
COMPATIBLE_MACHINE:genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE:edgerouter = "edgerouter"
COMPATIBLE_MACHINE:beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION:genericx86 = "5.15.52"
LINUX_VERSION:genericx86-64 = "5.15.52"
LINUX_VERSION:edgerouter = "5.15.52"
LINUX_VERSION:beaglebone-yocto = "5.15.52"
