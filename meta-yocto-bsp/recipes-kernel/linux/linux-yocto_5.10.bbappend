KBRANCH:genericx86  = "v5.10/standard/base"
KBRANCH:genericx86-64  = "v5.10/standard/base"
KBRANCH:edgerouter = "v5.10/standard/edgerouter"
KBRANCH:beaglebone-yocto = "v5.10/standard/beaglebone"

KMACHINE:genericx86 ?= "common-pc"
KMACHINE:genericx86-64 ?= "common-pc-64"
KMACHINE:beaglebone-yocto ?= "beaglebone"

SRCREV_machine:genericx86 ?= "4d201ec392f149ecce321186ea5494a6e25e28f4"
SRCREV_machine:genericx86-64 ?= "4d201ec392f149ecce321186ea5494a6e25e28f4"
SRCREV_machine:edgerouter ?= "58eb61187e8c78dc0241b2b85cb7d2c958f0e1fd"
SRCREV_machine:beaglebone-yocto ?= "aab4d3436476d643c68ac2efccb887a4386a35bb"

COMPATIBLE_MACHINE:genericx86 = "genericx86"
COMPATIBLE_MACHINE:genericx86-64 = "genericx86-64"
COMPATIBLE_MACHINE:edgerouter = "edgerouter"
COMPATIBLE_MACHINE:beaglebone-yocto = "beaglebone-yocto"

LINUX_VERSION:genericx86 = "5.10.128"
LINUX_VERSION:genericx86-64 = "5.10.128"
LINUX_VERSION:edgerouter = "5.10.128"
LINUX_VERSION:beaglebone-yocto = "5.10.128"
