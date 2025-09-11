SUMMARY = "Provides cryptographic recipes and primitives to python developers"
HOMEPAGE = "https://cryptography.io/"
SECTION = "devel/python"
LICENSE = "Apache-2.0 | BSD-3-Clause"
LIC_FILES_CHKSUM = "file://LICENSE;md5=8c3617db4fb6fae01f1d253ab91511e4 \
                    file://LICENSE.APACHE;md5=4e168cce331e5c827d4c2b68a6200e1b \
                    file://LICENSE.BSD;md5=5ae30ba4123bc4f2fa49aa0b0dce887b \
                   "
LDSHARED += "-pthread"

# NOTE: Make sure to keep this recipe at the same version as python3-cryptography-vectors
#       Upgrade both recipes at the same time
require python3-cryptography-common.inc
SRC_URI[sha256sum] = "4b1654dfc64ea479c242508eb8c724044f1e964a47d1d1cacc5132292d851971"

SRC_URI += "file://0001-pyproject.toml-remove-benchmark-disable-option.patch \
            file://check-memfree.py \
            file://run-ptest \
           "

require ${BPN}-crates.inc

inherit pypi python_maturin cargo-update-recipe-crates pkgconfig

DEPENDS += " \
    python3-cffi-native \
    openssl \
"

RDEPENDS:${PN} += " \
    python3-cffi \
"

RDEPENDS:${PN}:append:class-target = " \
    python3-numbers \
    python3-threading \
"

RDEPENDS:${PN}-ptest += " \
    python3-bcrypt \
    python3-cryptography-vectors (= ${PV}) \
    python3-hypothesis \
    python3-iso8601 \
    python3-mmap \
    python3-pretend \
    python3-psutil \
    python3-pytest \
    python3-unittest-automake-output \
    python3-pytest-subtests \
    python3-pytz \
"

inherit ptest

do_install_ptest() {
    install -D ${UNPACKDIR}/check-memfree.py ${D}${PTEST_PATH}/
    install -d ${D}${PTEST_PATH}/tests
    cp -rf ${S}/tests/* ${D}${PTEST_PATH}/tests/
    # remove test_x509.py as it needs benchmark and we don't
    # want to introduce the benchmark dependency
    rm -rf ${D}${PTEST_PATH}/tests/bench/test_x509.py
    install -d ${D}${PTEST_PATH}/tests/hazmat
    cp -rf ${S}/tests/hazmat/* ${D}${PTEST_PATH}/tests/hazmat/
    cp -r ${S}/pyproject.toml ${D}${PTEST_PATH}/
}

FILES:${PN}-dbg += " \
    ${PYTHON_SITEPACKAGES_DIR}/${SRCNAME}/hazmat/bindings/.debug \
"

BBCLASSEXTEND = "native nativesdk"
