SUMMARY = "Theora Video Codec"
DESCRIPTION = "The libtheora reference implementation provides the standard encoder and decoder under a BSD license."
HOMEPAGE = "http://xiph.org/"
BUGTRACKER = "https://trac.xiph.org/newticket"
SECTION = "libs"
LICENSE = "BSD-3-Clause"
LIC_FILES_CHKSUM = "file://COPYING;md5=cf91718f59eb6a83d06dc7bcaf411132"
DEPENDS = "libogg"


SRC_URI = "http://downloads.xiph.org/releases/theora/libtheora-${PV}.tar.bz2 \
           file://autoreconf.patch \
           file://no-docs.patch"

SRC_URI[sha256sum] = "b6ae1ee2fa3d42ac489287d3ec34c5885730b1296f0801ae577a35193d3affbc"

UPSTREAM_CHECK_REGEX = "libtheora-(?P<pver>\d+(\.\d)+)\.(tar\.gz|tgz)"

inherit autotools pkgconfig

EXTRA_OECONF = "--disable-examples"
