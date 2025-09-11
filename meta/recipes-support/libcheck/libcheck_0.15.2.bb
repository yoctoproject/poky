SUMMARY  = "Check - unit testing framework for C code"
DESCRIPTION = "It features a simple interface for defining unit tests, \
putting little in the way of the developer. Tests are run in a separate \
address space, so both assertion failures and code errors that cause \
segmentation faults or other signals can be caught. Test results are \
reportable in the following: Subunit, TAP, XML, and a generic logging format."
HOMEPAGE = "https://libcheck.github.io/check/"
SECTION = "devel"

LICENSE  = "LGPL-2.1-or-later"
LIC_FILES_CHKSUM = "file://COPYING.LESSER;md5=2d5025d4aa3495befef8f17206a5b0a1"

SRC_URI = "${GITHUB_BASE_URI}/download/${PV}/check-${PV}.tar.gz \
           file://automake-output.patch \
           file://subunit.patch \
           file://0001-Fix-texinfo-errors-and-warnings.patch \
"

SRC_URI[sha256sum] = "a8de4e0bacfb4d76dd1c618ded263523b53b85d92a146d8835eb1a52932fa20a"
GITHUB_BASE_URI = "https://github.com/libcheck/check/releases/"

S = "${UNPACKDIR}/check-${PV}"

inherit cmake pkgconfig texinfo github-releases

RREPLACES:${PN} = "check (<= 0.9.5)"

EXTRA_OECMAKE:append:class-target = " -DAWK_PATH=${bindir}/awk"
EXTRA_OECMAKE = "-DENABLE_SUBUNIT_EXT=OFF"

do_install:append:class-native() {
    create_cmdline_shebang_wrapper ${D}${bindir}/checkmk
}

BBCLASSEXTEND = "native nativesdk"

PACKAGES =+ "checkmk"

FILES:checkmk = "${bindir}/checkmk"

RDEPENDS:checkmk = "gawk"
