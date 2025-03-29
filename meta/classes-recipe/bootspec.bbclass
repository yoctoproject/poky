# Class for adding a basic bootloader specification file to rootfs images
#
# For more information, see:
# https://uapi-group.org/specifications/specs/boot_loader_specification/
#
# To use the class in your image recipe, simply add
#
#   inherit bootspec
#
# This will create a bootspec entry for each devicetree found in
# KERNEL_DEVICETREE and EXTERNAL_KERNEL_DEVICETREE.
# For machines not using devicetree, it will create a single default.conf.
#
# The bootspec lines generated can be customized with the BOOTSPEC_TITLE,
# BOOTSPEC_VERSION, BOOTSPEC_OPTIONS and BOOTSPEC_EXTRALINE variables.

BOOTSPEC_TITLE ?= "${SUMMARY}"
BOOTSPEC_TITLE[doc] = "Content of the boot spec entry 'title' line"

BOOTSPEC_OPTIONS_ext4 = "rootfstype=ext4 rootwait"
BOOTSPEC_OPTIONS_ubi = "rootfstype=ubifs"
BOOTSPEC_OPTIONS_squashfs = "rootfstype=squashfs"
BOOTSPEC_OPTIONS_squashfs-lzo = "rootfstype=squashfs"
BOOTSPEC_OPTIONS_squashfs-xz = "rootfstype=squashfs"

BOOTSPEC_VERSION ?= "${PV}"
BOOTSPEC_VERSION[doc] ?= "Content of the bootspec version entry"

# Search in IMAGE_FSTYPES for a type we have a default for
def bootspec_default_option(d):
    for type in (d.getVar('IMAGE_FSTYPES') or "").split():
        option = d.getVar('BOOTSPEC_OPTIONS_%s' % type)
        if option:
            return option

python () {
    if d.getVar('PREFERRED_PROVIDER_virtual/dtb'):
        d.appendVarFlag('do_rootfs', 'depends', ' virtual/dtb:do_populate_sysroot')
        d.setVar('EXTERNAL_KERNEL_DEVICETREE', '${RECIPE_SYSROOT}/boot/devicetree')
}

BOOTSPEC_OPTIONS ?= "${@bootspec_default_option(d)}"
BOOTSPEC_OPTIONS[doc] = "Content of the boot spec entry 'options' line"

BOOTSPEC_EXTRALINE ?= ""
BOOTSPEC_EXTRALINE[doc] = "Allows to add extra content to bootspec entries, lines must be terminated with a newline"

do_rootfs[vardeps] += "BOOTSPEC_TITLE BOOTSPEC_VERSION BOOTSPEC_OPTIONS BOOTSPEC_EXTRALINE"

python create_bootspec() {
    dtbs = (d.getVar('KERNEL_DEVICETREE') or '').split()
    ext_dtbs = os.listdir(d.getVar('EXTERNAL_KERNEL_DEVICETREE')) if d.getVar('EXTERNAL_KERNEL_DEVICETREE') else []
    ext_dtbs = [x for x in ext_dtbs if x.endswith('.dtb')]
    if not dtbs and not ext_dtbs:
        dtbs = ['default']

    bb.utils.mkdirhier(d.expand("${IMAGE_ROOTFS}/loader/entries/"))

    for x in set(dtbs + ext_dtbs):
        x = os.path.basename(x)
        conf = "/loader/entries/" + x.replace('.dtb', '') + ".conf"

        bb.note("Creating boot spec entry '%s'" % conf)

        try:
            bootspecfile = open(d.expand("${IMAGE_ROOTFS}/%s" % conf), 'w')
        except OSError:
            raise bb.build.FuncFailed('Unable to open boot spec file for writing')

        bootspecfile.write('title      %s\n' % d.getVar('BOOTSPEC_TITLE'))
        bootspecfile.write('version    %s\n' % d.getVar('BOOTSPEC_VERSION'))
        bootspecfile.write('options    %s\n' % d.getVar('BOOTSPEC_OPTIONS'))
        bootspecfile.write(d.getVar('BOOTSPEC_EXTRALINE').replace(r'\n', '\n'))
        bootspecfile.write('linux      %s\n' % d.expand('/boot/${KERNEL_IMAGETYPE}'))
        if x != "default":
            # Prefer BSP dts if BSP and kernel provide the same dts
            dtbpath = '/boot/devicetree/' if x in ext_dtbs else '/boot/'
            bootspecfile.write('devicetree %s\n' % d.expand(dtbpath + x))

        bootspecfile.close()
}

ROOTFS_POSTPROCESS_COMMAND += " create_bootspec; "

IMAGE_INSTALL:append = " kernel-image"
IMAGE_INSTALL:append = '${@ " kernel-devicetree" if d.getVar('KERNEL_DEVICETREE') else ""}'
