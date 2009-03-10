require libice_${PV}.bb

DEPENDS = "libx11-native xproto-native xtrans-native"
PROVIDES = "ice-native"

inherit native

XORG_PN = "libICE"
