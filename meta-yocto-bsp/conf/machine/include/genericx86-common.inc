include conf/machine/include/ia32-base.inc
MACHINE_FEATURES += "wifi efi pcbios"

PREFERRED_PROVIDER_virtual/kernel ?= "linux-yocto"
PREFERRED_VERSION_linux-yocto ?= "3.10%"
PREFERRED_PROVIDER_virtual/xserver ?= "xserver-xorg"
XSERVER ?= "${XSERVER_IA32_BASE} \
            ${XSERVER_IA32_EXT} \
            ${XSERVER_IA32_I915} \
            ${XSERVER_IA32_I965} \
            ${XSERVER_IA32_FBDEV} \
            ${XSERVER_IA32_VESA} \
            ${XSERVER_IA32_MODESETTING} \
           "

MACHINE_EXTRA_RRECOMMENDS += "linux-firmware v86d"

GLIBC_ADDONS = "nptl"

EXTRA_OECONF_append_pn-matchbox-panel-2 = " --with-battery=acpi"
