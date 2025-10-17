SUMMARY = "An image containing the build system itself"
DESCRIPTION = "An image containing the build system that you can boot and run using either VirtualBox, VMware Player or VMware Workstation."
HOMEPAGE = "https://docs.yoctoproject.org/overview-manual/yp-intro.html#archived-components"

LICENSE = "MIT"
LIC_FILES_CHKSUM = "file://${COREBASE}/meta/COPYING.MIT;md5=3da9cfbcb788c80a0384361b4de20420"

IMAGE_INSTALL = "packagegroup-core-boot packagegroup-core-ssh-openssh packagegroup-self-hosted \
                 kernel-dev kernel-devsrc connman connman-plugin-ethernet dhcpcd \
                 tzdata python3-pip perl-misc"

IMAGE_FEATURES += "x11-base package-management splash"

QB_MEM ?= '${@bb.utils.contains("DISTRO_FEATURES", "opengl", "-m 512", "-m 256", d)}'

# Ensure there's enough space to do a core-image-sato build, with rm_work enabled
IMAGE_ROOTFS_EXTRA_SPACE = "41943040"

# Do a quiet boot with limited console messages
APPEND += "rootfstype=ext4 quiet"

DEPENDS = "zip-native python3-pip-native"
IMAGE_FSTYPES = "wic.vmdk wic.vhd wic.vhdx"

inherit core-image setuptools3 features_check

REQUIRED_DISTRO_FEATURES += "xattr"

SRCREV_bitbake ?= "8b582ef8dd0cef0192d4c0104bcd9b5d642d132c"
SRCREV_oe-core ?= "5298d01663f897e38380116edf23973d2a156cbc"
SRCREV_yocto ?= "fe65e142d0d9ba0e51ff9175ffa82e902f982a20"
SRCREV_FORMAT = "bitbake_oe-core_yocto"

SRC_URI = "git://git.openembedded.org/bitbake;name=bitbake;branch=master;destsuffix=bitbake \
           git://git.openembedded.org/openembedded-core;name=oe-core;branch=master;destsuffix=openembedded-core \
           git://git.yoctoproject.org/meta-yocto;name=yocto;branch=master;destsuffix=meta-yocto \
           file://Yocto_Build_Appliance.vmx \
           file://Yocto_Build_Appliance.vmxf \
           file://README_VirtualBox_Guest_Additions.txt \
           file://README_VirtualBox_Toaster.txt \
          "
RECIPE_NO_UPDATE_REASON = "Recipe is recursive and handled as part of the release process"
BA_INCLUDE_SOURCES ??= "0"

IMAGE_CMD:ext4:append () {
	# We don't need to reserve much space for root, 0.5% is more than enough
	tune2fs -m 0.5 ${IMGDEPLOYDIR}/${IMAGE_NAME}.rootfs.ext4
}

fakeroot do_populate_poky_src () {
	# Because fetch2's git's unpack uses -s cloneflag, the unpacked git repo
	# will become invalid in the target.
	for d in bitbake openembedded-core meta-yocto; do
		rm -rf ${UNPACKDIR}/$d/.git
		rm -f ${UNPACKDIR}/$d/.gitignore
		cp -R ${UNPACKDIR}/$d ${IMAGE_ROOTFS}/home/builder/
	done

	mkdir -p ${IMAGE_ROOTFS}/home/builder/openembedded-core/build/conf
	echo "INHERIT += \"rm_work\"" >> ${IMAGE_ROOTFS}/home/builder/openembedded-core/build/conf/auto.conf

	if [ ${BA_INCLUDE_SOURCES} != 0 ]; then
		mkdir -p ${IMAGE_ROOTFS}/home/builder/openembedded-core/build/downloads
		cp -RpL ${DL_DIR}/* ${IMAGE_ROOTFS}/home/builder/openembedded-core/build/downloads/
		# Remove the git2_* tarballs -- this is ok since we still have the git2/.
		rm -rf ${IMAGE_ROOTFS}/home/builder/openembedded-core/build/downloads/git2_*
	fi

	# Place the README_VirtualBox_Guest_Additions file in builders home folder.
	cp ${UNPACKDIR}/README_VirtualBox_Guest_Additions.txt ${IMAGE_ROOTFS}/home/builder/

	# Place the README_VirtualBox_Toaster file in builders home folder.
	cp ${UNPACKDIR}/README_VirtualBox_Toaster.txt ${IMAGE_ROOTFS}/home/builder/

	echo "export LC_ALL=en_US.utf8" >> ${IMAGE_ROOTFS}/home/builder/.bashrc
	echo "export TERM=xterm-color" >> ${IMAGE_ROOTFS}/home/builder/.bashrc

	# Also save (for reference only) the actual SRCREV used to create this image
	echo "export BA_SRCREV=${SRCREV}" >> ${IMAGE_ROOTFS}/home/builder/.bashrc
	echo "" >> ${IMAGE_ROOTFS}/home/builder/.bashrc
	echo 'export PATH=$PATH:/sbin' >> ${IMAGE_ROOTFS}/home/builder/.bashrc
	echo "" >> ${IMAGE_ROOTFS}/home/builder/.bashrc

	echo "# If working behind a proxy and using the provided oe-git-proxy script" >> ${IMAGE_ROOTFS}/home/builder/.bashrc
	echo "# you need to set ALL_PROXY based on your proxy settings." >> ${IMAGE_ROOTFS}/home/builder/.bashrc
	echo "# Example ALL_PROXY values:" >> ${IMAGE_ROOTFS}/home/builder/.bashrc
	echo "# export ALL_PROXY=https://proxy.example.com:8080" >> ${IMAGE_ROOTFS}/home/builder/.bashrc
	echo "# export ALL_PROXY=socks://socks.example.com:1080" >> ${IMAGE_ROOTFS}/home/builder/.bashrc

	chown -R builder:builder ${IMAGE_ROOTFS}/home/builder/
	chmod -R ug+rw ${IMAGE_ROOTFS}/home/builder/

	# Assume we will need CDROM to install guest additions
	mkdir -p ${IMAGE_ROOTFS}/media/cdrom

	# Allow builder to use sudo
	echo "builder ALL=(ALL) NOPASSWD: ALL" >> ${IMAGE_ROOTFS}/etc/sudoers

	# Load tap/tun at startup
	rm -f ${IMAGE_ROOTFS}/sbin/iptables
	ln -rs ${IMAGE_ROOTFS}/usr/sbin/iptables ${IMAGE_ROOTFS}/sbin/iptables
	echo "tun" >> ${IMAGE_ROOTFS}/etc/modules

	# Use Clearlooks GTK+ theme
	mkdir -p ${IMAGE_ROOTFS}/etc/gtk-2.0
	echo 'gtk-theme-name = "Clearlooks"' > ${IMAGE_ROOTFS}/etc/gtk-2.0/gtkrc

	# Install modules needed for toaster
	export STAGING_LIBDIR=${STAGING_LIBDIR_NATIVE}
	export STAGING_INCDIR=${STAGING_INCDIR_NATIVE}
	export HOME=${IMAGE_ROOTFS}/home/builder
	mkdir -p ${IMAGE_ROOTFS}/home/builder/.cache/pip
	pip3_install_params="--user -I -U -v -r ${IMAGE_ROOTFS}/home/builder/bitbake/toaster-requirements.txt"
	if [ -n "${http_proxy}" ]; then
	   pip3_install_params="${pip3_install_params} --proxy ${http_proxy}"
	fi
	pip3 install ${pip3_install_params}
	chown -R builder:builder ${IMAGE_ROOTFS}/home/builder/.local
	chown -R builder:builder ${IMAGE_ROOTFS}/home/builder/.cache
}

fakeroot do_tweak_image () {
	# add a /lib64 symlink
	# this is needed for building rust-native on a 64-bit build appliance
	ln -rs ${IMAGE_ROOTFS}/lib ${IMAGE_ROOTFS}/lib64
}

IMAGE_PREPROCESS_COMMAND += "do_populate_poky_src do_tweak_image"
# For pip usage above
do_image[network] = "1"

addtask rootfs after do_unpack

python () {
    # Ensure we run these usually noexec tasks
    d.delVarFlag("do_fetch", "noexec")
    d.delVarFlag("do_unpack", "noexec")
}

# ${S} doesn't exist for us
do_qa_unpack() {
    return
}

create_bundle_files () {
	cd ${WORKDIR}
	mkdir -p Yocto_Build_Appliance
	cp ${UNPACKDIR}/*.vmx* Yocto_Build_Appliance
	ln -sf ${IMGDEPLOYDIR}/${IMAGE_NAME}.wic.vmdk Yocto_Build_Appliance/Yocto_Build_Appliance.vmdk
	ln -sf ${IMGDEPLOYDIR}/${IMAGE_NAME}.wic.vhdx Yocto_Build_Appliance/Yocto_Build_Appliance.vhdx
	ln -sf ${IMGDEPLOYDIR}/${IMAGE_NAME}.wic.vhd Yocto_Build_Appliance/Yocto_Build_Appliance.vhd
	zip -r ${IMGDEPLOYDIR}/Yocto_Build_Appliance-${DATETIME}.zip Yocto_Build_Appliance
	ln -sf Yocto_Build_Appliance-${DATETIME}.zip ${IMGDEPLOYDIR}/Yocto_Build_Appliance.zip
}
create_bundle_files[vardepsexclude] = "DATETIME"

python do_bundle_files() {
    bb.build.exec_func('create_bundle_files', d)
}

addtask bundle_files after do_image_wic before do_image_complete
