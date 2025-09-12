DESCRIPTION = "SDK type target for building a standalone tarball containing python3, chrpath, make, git and tar. The \
               tarball can be used to run bitbake builds on systems which don't meet the usual version requirements."
SUMMARY = "Standalone tarball for running builds on systems with inadequate software"
LICENSE = "MIT"

TOOLCHAIN_TARGET_TASK ?= ""

TOOLCHAIN_HOST_TASK ?= "\
    nativesdk-sdk-provides-dummy \
    nativesdk-python3 \
    nativesdk-python3-git \
    nativesdk-python3-jinja2 \
    nativesdk-python3-testtools \
    nativesdk-python3-pip \
    nativesdk-python3-setuptools \
    nativesdk-python3-subunit \
    nativesdk-python3-pyyaml \
    nativesdk-python3-websockets \
    nativesdk-ncurses-terminfo-base \
    nativesdk-chrpath \
    nativesdk-tar \
    nativesdk-buildtools-perl-dummy \
    nativesdk-git \
    nativesdk-git-perltools \
    nativesdk-pigz \
    nativesdk-make \
    nativesdk-wget \
    nativesdk-ca-certificates \
    nativesdk-texinfo \
    nativesdk-libnss-nis \
    nativesdk-rpcsvc-proto \
    nativesdk-patch \
    nativesdk-mtools \
    nativesdk-zstd \
    nativesdk-lz4 \
    nativesdk-libacl \
    "

MULTIMACH_TARGET_SYS = "${SDK_ARCH}-nativesdk${SDK_VENDOR}-${SDK_OS}"
PACKAGE_ARCH = "${SDK_ARCH}_${SDK_OS}"
PACKAGE_ARCHS = ""
TARGET_ARCH = "none"
TARGET_OS = "none"

SDK_PACKAGE_ARCHS += "buildtools-dummy-${SDKPKGSUFFIX}"

TOOLCHAIN_OUTPUTNAME ?= "${SDK_ARCH}-buildtools-nativesdk-standalone-${DISTRO_VERSION}"

SDK_TITLE = "Build tools"

RDEPENDS = "${TOOLCHAIN_HOST_TASK}"

EXCLUDE_FROM_WORLD = "1"

inherit populate_sdk
inherit toolchain-scripts-base
inherit nopackages

deltask install
deltask populate_sysroot

do_populate_sdk[stamp-extra-info] = "${PACKAGE_ARCH}"

REAL_MULTIMACH_TARGET_SYS = "none"

create_sdk_files:append () {
	rm -f ${SDK_OUTPUT}/${SDKPATH}/site-config-*
	rm -f ${SDK_OUTPUT}/${SDKPATH}/environment-setup-*
	rm -f ${SDK_OUTPUT}/${SDKPATH}/version-*

	# Generate new (mini) sdk-environment-setup file
	script=${1:-${SDK_OUTPUT}/${SDKPATH}/environment-setup-${SDK_SYS}}
	touch $script
	echo 'export PATH="${SDKPATHNATIVE}${bindir_nativesdk}:${SDKPATHNATIVE}${sbindir_nativesdk}:${SDKPATHNATIVE}${base_bindir_nativesdk}:${SDKPATHNATIVE}${base_sbindir_nativesdk}:$PATH"' >> $script
	echo 'export OECORE_NATIVE_SYSROOT="${SDKPATHNATIVE}"' >> $script
	echo 'HOST_PKG_PATH=$(command -p pkg-config --variable=pc_path pkg-config 2>/dev/null || true)' >>$script
	echo 'export PKG_CONFIG_LIBDIR=${SDKPATHNATIVE}/${libdir}/pkgconfig:${SDKPATHNATIVE}/${datadir}/pkgconfig:${HOST_PKG_PATH:-/usr/lib/pkgconfig:/usr/share/pkgconfig}' >>$script
	echo 'unset HOST_PKG_PATH'

	toolchain_create_sdk_version ${SDK_OUTPUT}/${SDKPATH}/version-${SDK_SYS}

	cat >> $script <<EOF
# Detect host ca file/path, export for envfile to use
# /etc/ssl/certs/ca-certificates.crt Debian systems
# /etc/pki/tls/certs/ca-bundle.crt Fedora systems
# /etc/ssl/ca-bundle.pem Suse systems
export CAFILE
export CAPATH
for a in /etc/ssl/certs/ca-certificates.crt \
    /etc/pki/tls/certs/ca-bundle.crt \
    /etc/ssl/ca-bundle.pem ; do
    if test -f "\$a"; then
        CAFILE="\$a"
        break
    fi
done

a="/etc/ssl/certs"
if test -d "\$a" && ls "\$a"/[0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f][0-9a-f].0 >/dev/null 2>/dev/null; then
    CAPATH="\$a"
fi

if [ -d "\$OECORE_NATIVE_SYSROOT/environment-setup.d" ]; then
	for envfile in \$OECORE_NATIVE_SYSROOT/environment-setup.d/*.sh; do
		. \$envfile
	done
fi

# We have to unset this else it can confuse oe-selftest and other tools
# which may also use the overlapping namespace.
unset OECORE_NATIVE_SYSROOT CAFILE CAPATH
EOF

	if [ "${SDKMACHINE}" = "i686" ]; then
		echo 'export NO32LIBS="0"' >>$script
		echo 'echo "$BB_ENV_PASSTHROUGH_ADDITIONS" | grep -q "NO32LIBS"' >>$script
		echo '[ $? != 0 ] && export BB_ENV_PASSTHROUGH_ADDITIONS="NO32LIBS $BB_ENV_PASSTHROUGH_ADDITIONS"' >>$script
	fi
}

# buildtools-tarball doesn't need config site
TOOLCHAIN_NEED_CONFIGSITE_CACHE = ""

# The recipe doesn't need any default deps
INHIBIT_DEFAULT_DEPS = "1"

inherit testsdk

# Directory that contains testcases
TESTSDK_CASE_DIRS = "buildtools"