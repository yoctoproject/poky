require libxt_${PV}.bb

DEPENDS = "libx11-native libsm-native kbproto-native"
PROVIDES = "xt-native"

inherit native

XORG_PN = "libXt"
