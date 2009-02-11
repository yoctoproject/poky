DESCRIPTION = "An HTTP library implementation in C"
LICENSE = "GPL"
SECTION = "x11/gnome/libs"

DEPENDS = "glib-2.0 gnutls libxml2"
PR = "r2"

SRC_URI = "http://ftp.gnome.org/pub/GNOME/sources/${PN}/2.2/${PN}-${PV}.tar.bz2"

inherit autotools

FILES_${PN} = "${libdir}/lib*.so.*"
FILES_${PN}-dev = "${includedir}/ ${libdir}/"
FILES_${PN}-doc = "${datadir}/"

do_stage() {
	autotools_stage_all
	install -d ${PKG_CONFIG_DIR}
	install -m 0644 ${S}/libsoup.pc ${PKG_CONFIG_DIR}/libsoup-2.2.pc
}
