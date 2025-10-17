KBRANCH ?= "v6.16/standard/base"

require recipes-kernel/linux/linux-yocto.inc

# CVE exclusions
include recipes-kernel/linux/cve-exclusion.inc
include recipes-kernel/linux/cve-exclusion_6.16.inc

# board specific branches
KBRANCH:qemuarm  ?= "v6.16/standard/arm-versatile-926ejs"
KBRANCH:qemuarm64 ?= "v6.16/standard/base"
KBRANCH:qemumips ?= "v6.16/standard/mti-malta32"
KBRANCH:qemuppc  ?= "v6.16/standard/qemuppc"
KBRANCH:qemuriscv64  ?= "v6.16/standard/base"
KBRANCH:qemuriscv32  ?= "v6.16/standard/base"
KBRANCH:qemux86  ?= "v6.16/standard/base"
KBRANCH:qemux86-64 ?= "v6.16/standard/base"
KBRANCH:qemuloongarch64  ?= "v6.16/standard/base"
KBRANCH:qemumips64 ?= "v6.16/standard/mti-malta64"

SRCREV_machine:qemuarm ?= "cdb5121dcb8fbde2d7616011e8e84623914d17a4"
SRCREV_machine:qemuarm64 ?= "42ddd61a7bcedefc5eaedb89e91dcec7061e78ce"
SRCREV_machine:qemuloongarch64 ?= "42ddd61a7bcedefc5eaedb89e91dcec7061e78ce"
SRCREV_machine:qemumips ?= "62ea92a539f58803a222be98b81118403074206e"
SRCREV_machine:qemuppc ?= "42ddd61a7bcedefc5eaedb89e91dcec7061e78ce"
SRCREV_machine:qemuriscv64 ?= "42ddd61a7bcedefc5eaedb89e91dcec7061e78ce"
SRCREV_machine:qemuriscv32 ?= "42ddd61a7bcedefc5eaedb89e91dcec7061e78ce"
SRCREV_machine:qemux86 ?= "42ddd61a7bcedefc5eaedb89e91dcec7061e78ce"
SRCREV_machine:qemux86-64 ?= "42ddd61a7bcedefc5eaedb89e91dcec7061e78ce"
SRCREV_machine:qemumips64 ?= "9fb4ff0187c85426f21fd40d4c61b742800f65c4"
SRCREV_machine ?= "42ddd61a7bcedefc5eaedb89e91dcec7061e78ce"
SRCREV_meta ?= "9e0a3e81b40db2b35e060ef001b3902a6a0996ac"

# set your preferred provider of linux-yocto to 'linux-yocto-upstream', and you'll
# get the <version>/base branch, which is pure upstream -stable, and the same
# meta SRCREV as the linux-yocto-standard builds. Select your version using the
# normal PREFERRED_VERSION settings.
BBCLASSEXTEND = "devupstream:target"
SRCREV_machine:class-devupstream ?= "683320aeb0e83deac1b6c6794b0567969de09548"
PN:class-devupstream = "linux-yocto-upstream"
KBRANCH:class-devupstream = "v6.16/base"

SRC_URI = "git://git.yoctoproject.org/linux-yocto.git;name=machine;branch=${KBRANCH};protocol=https \
           git://git.yoctoproject.org/yocto-kernel-cache;type=kmeta;name=meta;branch=yocto-6.16;destsuffix=${KMETA};protocol=https"

LIC_FILES_CHKSUM = "file://COPYING;md5=6bc538ed5bd9a7fc9398086aedcd7e46"
LINUX_VERSION ?= "6.16.11"

PV = "${LINUX_VERSION}+git"

KMETA = "kernel-meta"
KCONF_BSP_AUDIT_LEVEL = "1"

KERNEL_DEVICETREE:qemuarmv5 = "arm/versatile-pb.dtb"

COMPATIBLE_MACHINE = "^(qemuarm|qemuarmv5|qemuarm64|qemux86|qemuppc|qemuppc64|qemumips|qemumips64|qemux86-64|qemuriscv64|qemuriscv32|qemuloongarch64)$"

# Functionality flags
KERNEL_EXTRA_FEATURES ?= "features/netfilter/netfilter.scc"
KERNEL_FEATURES:append = " ${KERNEL_EXTRA_FEATURES}"
KERNEL_FEATURES:append:qemuall = " cfg/virtio.scc features/drm-bochs/drm-bochs.scc cfg/net/mdio.scc"
KERNEL_FEATURES:append:qemux86 = " cfg/sound.scc cfg/paravirt_kvm.scc"
KERNEL_FEATURES:append:qemux86-64 = " cfg/sound.scc cfg/paravirt_kvm.scc"
KERNEL_FEATURES:append = " ${@bb.utils.contains("TUNE_FEATURES", "mx32", " cfg/x32.scc", "", d)}"
KERNEL_FEATURES:append = " ${@bb.utils.contains("DISTRO_FEATURES", "ptest", " features/scsi/scsi-debug.scc features/nf_tables/nft_test.scc", "", d)}"
KERNEL_FEATURES:append = " ${@bb.utils.contains("DISTRO_FEATURES", "ptest", " features/gpio/mockup.scc features/gpio/sim.scc", "", d)}"
KERNEL_FEATURES:append = " ${@bb.utils.contains("KERNEL_DEBUG", "True", " features/reproducibility/reproducibility.scc features/debug/debug-btf.scc", "", d)}"
# libteam ptests from meta-oe needs it
KERNEL_FEATURES:append = " ${@bb.utils.contains("DISTRO_FEATURES", "ptest", " features/net/team/team.scc", "", d)}"
# openl2tp tests from meta-networking needs it
KERNEL_FEATURES:append = " ${@bb.utils.contains("DISTRO_FEATURES", "ptest", " cgl/cfg/net/l2tp.scc", "", d)}"
KERNEL_FEATURES:append:powerpc = " arch/powerpc/powerpc-debug.scc"
KERNEL_FEATURES:append:powerpc64 = " arch/powerpc/powerpc-debug.scc"
KERNEL_FEATURES:append:powerpc64le = " arch/powerpc/powerpc-debug.scc"
# Do not add debug info for riscv32, it fails during depmod
# ERROR: modpost: __ex_table+0x17a4 references non-executable section '.debug_loclists'
# Check again during next major version upgrade
KERNEL_FEATURES:remove:riscv32 = "features/debug/debug-kernel.scc"
INSANE_SKIP:kernel-vmlinux:qemuppc64 = "textrel"
