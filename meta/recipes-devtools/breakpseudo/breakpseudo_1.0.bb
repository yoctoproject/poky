
LICENSE = "MIT"
SUMMARY = "test to break psuedo"
DESCRIPTION = "test to break psuedo"
SRC_URI = "file://run.sh"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"
FILES:${PN} = "/file*"

inherit allarch

do_install () {
	touch ${D}/file

	${UNPACKDIR}/run.sh ${D}

	sleep 2
}