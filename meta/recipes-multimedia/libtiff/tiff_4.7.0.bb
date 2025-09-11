SUMMARY = "Provides support for the Tag Image File Format (TIFF)"
DESCRIPTION = "Library provides support for the Tag Image File Format \
(TIFF), a widely used format for storing image data.  This library \
provide means to easily access and create TIFF image files."
HOMEPAGE = "http://www.libtiff.org/"
LICENSE = "libtiff"
LIC_FILES_CHKSUM = "file://LICENSE.md;md5=a3e32d664d6db1386b4689c8121531c3"

CVE_PRODUCT = "libtiff"

SRC_URI = "http://download.osgeo.org/libtiff/tiff-${PV}.tar.gz \
	   file://CVE-2024-13978_1.patch \
	   file://CVE-2024-13978_2.patch \
	   file://CVE-2025-8176_1.patch \
	   file://CVE-2025-8176_2.patch \
	   file://CVE-2025-8176_3.patch \
	   file://CVE-2025-8177_1.patch \
	   file://CVE-2025-8177_2.patch \
           file://CVE-2025-8534.patch \
	   "

SRC_URI[sha256sum] = "67160e3457365ab96c5b3286a0903aa6e78bdc44c4bc737d2e486bcecb6ba976"

# exclude betas
UPSTREAM_CHECK_REGEX = "tiff-(?P<pver>\d+(\.\d+)+).tar"

CVE_STATUS[CVE-2015-7313] = "fixed-version: Tested with check from https://security-tracker.debian.org/tracker/CVE-2015-7313 and already 4.3.0 doesn't have the issue"
CVE_STATUS[CVE-2023-52356] = "fixed-version: Fixed since 4.7.0, NVD tracks this as version-less vulnerability"
CVE_STATUS[CVE-2023-6228] = "fixed-version: Fixed since 4.7.0, NVD tracks this as version-less vulnerability"
CVE_STATUS[CVE-2023-6277] = "fixed-version: Fixed since 4.7.0, NVD tracks this as version-less vulnerability"

inherit autotools multilib_header

CACHED_CONFIGUREVARS = "ax_cv_check_gl_libgl=no"

PACKAGECONFIG ?= "cxx jpeg zlib lzma \
                  strip-chopping extrasample-as-alpha check-ycbcr-subsampling"

PACKAGECONFIG[cxx] = "--enable-cxx,--disable-cxx,,"
PACKAGECONFIG[jbig] = "--enable-jbig,--disable-jbig,jbig,"
PACKAGECONFIG[jpeg] = "--enable-jpeg,--disable-jpeg,jpeg,"
PACKAGECONFIG[lerc] = "--enable-lerc,--disable-lerc,liblerc,"
PACKAGECONFIG[zlib] = "--enable-zlib,--disable-zlib,zlib,"
PACKAGECONFIG[lzma] = "--enable-lzma,--disable-lzma,xz,"
PACKAGECONFIG[webp] = "--enable-webp,--disable-webp,libwebp,"
PACKAGECONFIG[zstd] = "--enable-zstd,--disable-zstd,zstd,"
PACKAGECONFIG[libdeflate] = "--enable-libdeflate,--disable-libdeflate,libdeflate,"

# Convert single-strip uncompressed images to multiple strips of specified
# size (default: 8192) to reduce memory usage
PACKAGECONFIG[strip-chopping] = "--enable-strip-chopping,--disable-strip-chopping,,"

# Treat a fourth sample with no EXTRASAMPLE_ value as being ASSOCALPHA
PACKAGECONFIG[extrasample-as-alpha] = "--enable-extrasample-as-alpha,--disable-extrasample-as-alpha,,"

# Control picking up YCbCr subsample info. Disable to support files lacking
# the tag
PACKAGECONFIG[check-ycbcr-subsampling] = "--enable-check-ycbcr-subsampling,--disable-check-ycbcr-subsampling,,"

# Support a mechanism allowing reading large strips (usually one strip files)
# in chunks when using TIFFReadScanline. Experimental 4.0+ feature
PACKAGECONFIG[chunky-strip-read] = "--enable-chunky-strip-read,--disable-chunky-strip-read,,"

PACKAGES =+ "tiffxx tiff-utils"
FILES:tiffxx = "${libdir}/libtiffxx.so.*"
FILES:tiff-utils = "${bindir}/*"

do_install:append() {
    oe_multilib_header tiffconf.h
}

BBCLASSEXTEND = "native nativesdk"
