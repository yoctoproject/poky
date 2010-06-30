require xorg-font-common.inc
PE = "1"
PR = "${INC_PR}.1"

DEPENDS = "mkfontscale-native font-util-native"

EXTRA_OECONF += "--with-encodingsdir=${datadir}/fonts/X11/encodings"
