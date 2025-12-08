# Kernel customization for minha-camada
# This bbappend file customizes kernel configuration options

FILESEXTRAPATHS_prepend := "${THISDIR}:"

# SRC_URI additions for custom patches and configs
SRC_URI += "file://minha-camada-kernel.cfg"

# Merge custom kernel configuration
do_configure_prepend() {
    cat ${WORKDIR}/minha-camada-kernel.cfg >> ${B}/.config
    oe_runmake oldconfig
}

# Kernel command line customization
APPEND += "quiet loglevel=3"

# Additional kernel options
KERNEL_MODULE_AUTOLOAD += "ext4"
