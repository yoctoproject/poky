COMPATIBLE_MACHINE:genericarm64 = "genericarm64"
COMPATIBLE_MACHINE:beaglebone-yocto = "beaglebone-yocto"

KMACHINE:beaglebone-yocto ?= "beaglebone"

# Incorporate fixes post 6.12.3
SRCREV_meta:genericarm64 = "9ee4baec963b10d213c060622fce6d2b34166f40"
