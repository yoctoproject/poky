SUMMARY = "XML C Parser Library and Toolkit"
DESCRIPTION = "The XML Parser Library allows for manipulation of XML files.  Libxml2 exports Push and Pull type parser interfaces for both XML and HTML.  It can do DTD validation at parse time, on a parsed document instance or with an arbitrary DTD.  Libxml2 includes complete XPath, XPointer and Xinclude implementations.  It also has a SAX like interface, which is designed to be compatible with Expat."
HOMEPAGE = "https://gitlab.gnome.org/GNOME/libxml2"
BUGTRACKER = "http://bugzilla.gnome.org/buglist.cgi?product=libxml2"
SECTION = "libs"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://Copyright;md5=5873615e8a9ecbf5c8857c4312ee05d6 \
                    file://dict.c;beginline=6;endline=15;md5=2b4b7b827d2d8b080372433c4c9c85b6 \
                    file://list.c;beginline=4;endline=13;md5=b9c25b021ccaf287e50060602d20f3a7 \
                    "

DEPENDS = "zlib virtual/libiconv"

GNOMEBASEBUILDCLASS = "autotools"
inherit gnomebase

SRC_URI += "http://www.w3.org/XML/Test/xmlts20130923.tar;subdir=${BP};name=testtar \
           file://run-ptest \
           file://install-tests.patch \
           file://0001-Revert-cmake-Fix-installation-directories-in-libxml2.patch \
           file://CVE-2025-6021.patch \
           "

SRC_URI[archive.sha256sum] = "7ce458a0affeb83f0b55f1f4f9e0e55735dbfc1a9de124ee86fb4a66b597203a"
SRC_URI[testtar.sha256sum] = "c6b2d42ee50b8b236e711a97d68e6c4b5c8d83e69a2be4722379f08702ea7273"

CVE_STATUS[CVE-2025-6170] = "fixed-version: fixed in version 2.14.5"

BINCONFIG = "${bindir}/xml2-config"

PACKAGECONFIG ??= "python"
PACKAGECONFIG[python] = "--with-python=${PYTHON},--without-python,python3"

inherit autotools pkgconfig binconfig-disabled ptest

inherit_defer ${@bb.utils.contains('PACKAGECONFIG', 'python', 'python3targetconfig', '', d)}

LDFLAGS:append:riscv64 = "${@bb.utils.contains('DISTRO_FEATURES', 'ld-is-lld ptest', ' -fuse-ld=bfd', '', d)}"

RDEPENDS:${PN}-ptest += "bash make locale-base-en-us ${@bb.utils.contains('PACKAGECONFIG', 'python', 'libgcc python3-core python3-logging python3-shell python3-stringold python3-threading python3-unittest ${PN}-python', '', d)}"

RDEPENDS:${PN}-python += "${@bb.utils.contains('PACKAGECONFIG', 'python', 'python3-core', '', d)}"

RDEPENDS:${PN}-ptest:append:libc-musl = " musl-locales"
RDEPENDS:${PN}-ptest:append:libc-glibc = " glibc-gconv-ebcdic-us \
                                           glibc-gconv-ibm1141 \
                                           glibc-gconv-iso8859-5 \
                                           glibc-gconv-euc-jp \
                                         "

# WARNING: zlib is required for RPM use
EXTRA_OECONF = "--without-debug --without-legacy --with-catalog --with-c14n --without-lzma"
EXTRA_OECONF:class-native = "--without-legacy --with-c14n --without-lzma --with-zlib"
EXTRA_OECONF:class-nativesdk = "--without-legacy --with-c14n --without-lzma --with-zlib"
EXTRA_OECONF:linuxstdbase = "--with-debug --with-legacy --with-c14n --without-lzma --with-zlib"

python populate_packages:prepend () {
    # autonamer would call this libxml2-2, but we don't want that
    if d.getVar('DEBIAN_NAMES'):
        d.setVar('PKG:libxml2', '${MLPREFIX}libxml2')
}

PACKAGE_BEFORE_PN += "${PN}-utils"
PACKAGES += "${PN}-python"

FILES:${PN}-staticdev += "${PYTHON_SITEPACKAGES_DIR}/*.a"
FILES:${PN}-utils = "${bindir}/*"
FILES:${PN}-python = "${PYTHON_SITEPACKAGES_DIR}"

do_configure:prepend () {
	# executables take longer to package: these should not be executable
	find ${S}/xmlconf/ -type f -exec chmod -x {} \+
}

do_install_ptest () {
    oe_runmake DESTDIR=${D} ptestdir=${PTEST_PATH} install-test-data

	cp -r ${S}/xmlconf ${D}${PTEST_PATH}

    if ! ${@bb.utils.contains('PACKAGECONFIG', 'python', 'true', 'false', d)}; then
        rm -rf ${D}${PTEST_DIR}/python
    fi
}

# with musl we need to enable icu support explicitly for these tests
do_install_ptest:append:libc-musl () {
	rm -rf ${D}/${PTEST_PATH}/test/icu_parse_test.xml
}

do_install:append:class-native () {
	# Docs are not needed in the native case
	rm ${D}${datadir}/gtk-doc -rf

	create_wrapper ${D}${bindir}/xmllint 'XML_CATALOG_FILES=${XML_CATALOG_FILES:-${sysconfdir}/xml/catalog}'
}
do_install[vardepsexclude] += "XML_CATALOG_FILES:-${sysconfdir}/xml/catalog"

BBCLASSEXTEND = "native nativesdk"
