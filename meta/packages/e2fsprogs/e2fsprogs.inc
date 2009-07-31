DESCRIPTION = "EXT2 Filesystem Utilities"
HOMEPAGE = "http://e2fsprogs.sf.net"
LICENSE = "GPL"
SECTION = "base"
DEPENDS = "gettext"

SRC_URI = "${SOURCEFORGE_MIRROR}/e2fsprogs/e2fsprogs-${PV}.tar.gz \
           file://ubuntu904.patch;patch=1"

inherit autotools

EXTRA_OECONF = " --enable-dynamic-e2fsck"


