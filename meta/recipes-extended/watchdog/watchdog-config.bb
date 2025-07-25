SUMMARY = "Software watchdog"
DESCRIPTION = "Watchdog is a daemon that checks if your system is still \
working. If programs in user space are not longer executed it will reboot \
the system."
HOMEPAGE = "http://watchdog.sourceforge.net/"
BUGTRACKER = "http://sourceforge.net/tracker/?group_id=172030&atid=860194"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

SRC_URI = " \
    file://watchdog.default \
    file://watchdog.conf \
"

S = "${UNPACKDIR}"

# The default value is 60 seconds when null.
WATCHDOG_TIMEOUT ??= ""

do_install() {
    install -Dm 0644 ${UNPACKDIR}/watchdog.default ${D}${sysconfdir}/default/watchdog
    install -Dm 0644 ${UNPACKDIR}/watchdog.conf ${D}${sysconfdir}/watchdog.conf

    if [ -n "${WATCHDOG_TIMEOUT}" ]; then
        echo "watchdog-timeout = ${WATCHDOG_TIMEOUT}" >> ${D}/etc/watchdog.conf
    fi
}

