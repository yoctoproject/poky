# COMPATIBLE_MACHINE:beaglebone-yocto = "beaglebone-yocto"
COMPATIBLE_MACHINE:genericarm64 = "genericarm64"
# COMPATIBLE_MACHINE:genericx86 = "genericx86"
# COMPATIBLE_MACHINE:genericx86-64 = "genericx86-64"

KMACHINE:beaglebone-yocto ?= "beaglebone"
KMACHINE:genericarm64 ?= "genericarm64"
KMACHINE:genericx86 ?= "common-pc"
KMACHINE:genericx86-64 ?= "common-pc-64"

SRCREV_machine:beaglebone-yocto = "1025debfd0d40f7f8d0547328bbf50ac543bdeba"
SRCREV_machine:genericarm64 = "1025debfd0d40f7f8d0547328bbf50ac543bdeba"
SRCREV_machine:genericx86 = "1025debfd0d40f7f8d0547328bbf50ac543bdeba"
SRCREV_machine:genericx86-64 = "1025debfd0d40f7f8d0547328bbf50ac543bdeba"

LINUX_VERSION:beaglebone-yocto = "6.10.8"
LINUX_VERSION:genericarm64 = "6.10.8"
LINUX_VERSION:genericx86 = "6.10.8"
LINUX_VERSION:genericx86-64 = "6.10.8"
