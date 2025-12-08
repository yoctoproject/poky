SUMMARY = "Minimal image with hello-world package"
DESCRIPTION = "Custom minimal image that includes hello-world"
LICENSE = "MIT"

inherit image

# Define image packages - minimal set
IMAGE_INSTALL = "base-files base-passwd hello-world"

IMAGE_LINGUAS = ""
IMAGE_ROOTFS_SIZE ?= "65536"

# Disable SDK and debugfs
IMAGE_GEN_DEBUGFS = "0"
IMAGE_GEN_SSTATE_PKGSPEC = ""

