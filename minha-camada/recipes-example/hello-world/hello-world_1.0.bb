SUMMARY = "Hello World - Simple test package"
DESCRIPTION = "A simple test package that prints Hello World"
LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/LICENSE;md5=3b83ef96387f14655fc854ddc3c6bd27"

# Copy the source file from files directory
SRC_URI = "file://helloworld.c"
S = "${WORKDIR}"

# Inherit autotools for compilation
inherit autotools

# Custom compilation
do_compile() {
    ${CC} ${CFLAGS} -o ${WORKDIR}/hello-world ${WORKDIR}/helloworld.c
}

do_install() {
    install -d ${D}${bindir}
    install -m 0755 ${WORKDIR}/hello-world ${D}${bindir}/hello-world
}

FILES_${PN} = "${bindir}/hello-world"

