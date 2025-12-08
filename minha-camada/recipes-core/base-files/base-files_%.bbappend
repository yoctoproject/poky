# Customization of base-files for minha-camada
# This appends additional configuration to the base filesystem

FILESEXTRAPATHS_prepend := "${THISDIR}/files:"

SRC_URI += "file://minha-camada-banner.txt"

# Add custom banner/motd
do_install_append() {
    install -d ${D}${sysconfdir}
    install -m 0644 ${WORKDIR}/minha-camada-banner.txt ${D}${sysconfdir}/issue.net
    install -m 0644 ${WORKDIR}/minha-camada-banner.txt ${D}${sysconfdir}/issue
}
