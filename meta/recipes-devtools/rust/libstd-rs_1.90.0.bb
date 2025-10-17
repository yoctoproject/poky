SUMMARY = "Rust standard libaries"
HOMEPAGE = "http://www.rust-lang.org"
SECTION = "devel"
LICENSE = "(MIT | Apache-2.0) & Unicode-3.0"
LIC_FILES_CHKSUM = "file://../../COPYRIGHT;md5=11a3899825f4376896e438c8c753f8dc"

require rust-source.inc

# The dummy crate named `sysroot` represents the standard library target.
#
# See fd4c81f4c19e ("Add a `sysroot` crate to represent the standard library crates")
# https://github.com/rust-lang/rust/pull/108865/
S = "${RUSTSRC}/library/sysroot"

RUSTLIB_DEP = ""
inherit cargo

CVE_PRODUCT = "rust"

DEPENDS:append:libc-musl = " libunwind"
# rv32 does not have libunwind ported yet
DEPENDS:remove:riscv32 = "libunwind"
DEPENDS:remove:riscv64 = "libunwind"

# Embed bitcode in order to allow compiling both with and without LTO
RUSTFLAGS += "-Cembed-bitcode=yes"
# Ensure that user code can't access the dependencies of the standard library
RUSTFLAGS += "-Zforce-unstable-if-unmarked"
# Needed so cargo can find libbacktrace
RUSTFLAGS += "-L ${STAGING_LIBDIR} -C link-arg=-Wl,-soname,libstd.so"

CARGO_FEATURES ?= "panic-unwind backtrace"
CARGO_BUILD_FLAGS += "--features '${CARGO_FEATURES}'"
CARGO_VENDORING_DIRECTORY = "${RUSTSRC}/vendor"

do_compile:prepend () {
    # For Rust 1.13.0 and newer
    export RUSTC_BOOTSTRAP="1"
}

do_install () {
    mkdir -p ${D}${rustlibdir}

    # With the incremental build support added in 1.24, the libstd deps directory also includes dependency
    # files that get installed. Those are really only needed to incrementally rebuild the libstd library
    # itself and don't need to be installed.
    rm -f ${B}/target/${RUST_TARGET_SYS}/${BUILD_DIR}/deps/*.d
    cp ${B}/target/${RUST_TARGET_SYS}/${BUILD_DIR}/deps/* ${D}${rustlibdir}
}

BBCLASSEXTEND = "nativesdk"
