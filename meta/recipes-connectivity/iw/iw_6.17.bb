SUMMARY = "nl80211 based CLI configuration utility for wireless devices"
DESCRIPTION = "iw is a new nl80211 based CLI configuration utility for \
wireless devices. It supports almost all new drivers that have been added \
to the kernel recently. "
HOMEPAGE = "https://wireless.wiki.kernel.org/en/users/documentation/iw"
SECTION = "base"
LICENSE = "ISC"
LIC_FILES_CHKSUM = "file://COPYING;md5=878618a5c4af25e9b93ef0be1a93f774"

DEPENDS = "libnl"

SRC_URI = "http://www.kernel.org/pub/software/network/iw/${BP}.tar.gz \
           file://0001-iw-version.sh-don-t-use-git-describe-for-versioning.patch \
           file://separate-objdir.patch \
"

SRC_URI[sha256sum] = "aebdcfa3691aa5065a9b0d7def66c761c8b01a59dd81bc315d0305e05c3b04de"

inherit pkgconfig

EXTRA_OEMAKE = "\
    -f '${S}/Makefile' \
    \
    'PREFIX=${prefix}' \
    'SBINDIR=${sbindir}' \
    'MANDIR=${mandir}' \
"

do_install() {
    oe_runmake 'DESTDIR=${D}' install
}
