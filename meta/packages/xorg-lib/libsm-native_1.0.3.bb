require libsm_${PV}.bb

inherit native

DEPENDS = "libx11-native libice-native xproto-native xtrans-native"

XORG_PN = "libSM"
