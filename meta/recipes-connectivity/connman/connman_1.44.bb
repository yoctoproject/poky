SUMMARY = "A daemon for managing internet connections within embedded devices"
DESCRIPTION = "The ConnMan project provides a daemon for managing \
internet connections within embedded devices running the Linux \
operating system.  The Connection Manager is designed to be slim and \
to use as few resources as possible, so it can be easily integrated. \
It is a fully modular system that can be extended, through plug-ins, \
to support all kinds of wired or wireless technologies. Also, \
configuration methods, like DHCP and domain name resolving, are \
implemented using plug-ins."
HOMEPAGE = "https://web.git.kernel.org/pub/scm/network/connman/connman.git/about/"
LICENSE  = "GPL-2.0-only"
LIC_FILES_CHKSUM = "file://COPYING;md5=12f884d2ae1ff87c09e5b7ccc2c4ca7e \
                    file://src/main.c;beginline=1;endline=20;md5=486a279a6ab0c8d152bcda3a5b5edc36"

CVE_PRODUCT = "connman connection_manager"

DEPENDS  = "dbus glib-2.0"

SRC_URI = "${KERNELORG_MIRROR}/linux/network/${BPN}/${BP}.tar.xz \
           file://connman \
           file://0002-resolve-musl-does-not-implement-res_ninit.patch \
"

SRC_URI[sha256sum] = "2be2b00321632b775f9eff713acd04ef21e31fbf388f6ebf45512ff4289574ff"

inherit autotools pkgconfig systemd update-rc.d update-alternatives

RDEPENDS:${PN} = "${@bb.utils.contains('PACKAGECONFIG', 'wifi', '${WIRELESS_DAEMON}', '', d)}"
RRECOMMENDS:${PN} = "connman-conf"

EXTRA_OECONF += "\
    --enable-datafiles \
    --enable-tools \
    --runstatedir='${runtimedir}' \
    --with-dns-backend='${@bb.utils.contains("DISTRO_FEATURES", "systemd-resolved", "systemd-resolved", "internal", d)}' \
    ac_cv_path_IP6TABLES_SAVE=${sbindir}/ip6tables-save \
    ac_cv_path_IPTABLES_SAVE=${sbindir}/iptables-save \
    ac_cv_path_PPPD=${sbindir}/pppd \
    ac_cv_path_WPASUPPLICANT=${sbindir}/wpa_supplicant \
"

# For smooth operation it would be best to start only one wireless daemon at a time.
# If wpa-supplicant is running, connman will use it preferentially.
# Select either wpa-supplicant or iwd
WIRELESS_DAEMON ??= "wpa-supplicant"

# Choose "iptables" or "nftables"
CONNMAN_FIREWALL ??= "iptables"

# Default is 16kB
CONNMAN_STATS_MAX_FILE_SIZE = "16384"

PACKAGECONFIG ??= "client ethernet loopback wispr ${CONNMAN_FIREWALL} \
                   ${@bb.utils.filter('DISTRO_FEATURES', '3g bluetooth nfc polkit selinux systemd usbgadget wifi', d)} \
                   ${@bb.utils.filter('WIRELESS_DAEMON', 'iwd', d)} \
"

PACKAGECONFIG[3g] = "--enable-ofono,--disable-ofono,ofono"
PACKAGECONFIG[bluetooth] = "--enable-bluetooth,--disable-bluetooth,bluez5,bluez5"
PACKAGECONFIG[client] = "--enable-client,--disable-client,readline"
PACKAGECONFIG[dundee] = "--enable-dundee,--disable-dundee"
PACKAGECONFIG[ethernet] = "--enable-ethernet,--disable-ethernet"
PACKAGECONFIG[hh2serial-gps] = "--enable-hh2serial-gps,--disable-hh2serial-gps"
PACKAGECONFIG[iospm] = "--enable-iospm,--disable-iospm"
PACKAGECONFIG[iptables] = ",,iptables,iptables,nftables"
PACKAGECONFIG[iwd] = "--enable-iwd,--disable-iwd"
PACKAGECONFIG[loopback] = "--enable-loopback,--disable-loopback"
PACKAGECONFIG[nfc] = "--enable-neard,--disable-neard,neard"
PACKAGECONFIG[nftables] = ",,libmnl libnftnl,,kernel-module-nf-tables kernel-module-nft-chain-nat-ipv4 kernel-module-nft-chain-route-ipv4 kernel-module-nft-masq-ipv4 kernel-module-nft-nat,iptables"
PACKAGECONFIG[nmcompat] = "--enable-nmcompat,--disable-nmcompat"
PACKAGECONFIG[pacrunner] = "--enable-pacrunner,--disable-pacrunner"
PACKAGECONFIG[polkit] = "--enable-polkit,--disable-polkit,polkit"
PACKAGECONFIG[selinux] = "--enable-selinux,--disable-selinux,libselinux"
PACKAGECONFIG[session-policy-local] = "--enable-session-policy-local,--disable-session-policy-local"
PACKAGECONFIG[stats] = "--enable-stats --with-stats-max-file-size=${CONNMAN_STATS_MAX_FILE_SIZE},--disable-stats"
PACKAGECONFIG[systemd] = "--with-systemdunitdir=${systemd_system_unitdir}/ --with-tmpfilesdir=${nonarch_libdir}/tmpfiles.d/,--with-systemdunitdir='' --with-tmpfilesdir=''"
PACKAGECONFIG[test] = "--enable-test,--disable-test"
PACKAGECONFIG[tist] = "--enable-tist,--disable-tist"
PACKAGECONFIG[usbgadget] = "--enable-gadget,--disable-gadget"
PACKAGECONFIG[wifi] = "--enable-wifi,--disable-wifi"
PACKAGECONFIG[wispr] = "--enable-wispr,--disable-wispr,gnutls"

PACKAGECONFIG[l2tp] = "--enable-l2tp --with-l2tp=${sbindir}/xl2tpd,--disable-l2tp,ppp,xl2tpd"
PACKAGECONFIG[openconnect] = "--enable-openconnect --with-openconnect=${sbindir}/openconnect,--disable-openconnect,openconnect,openconnect"
PACKAGECONFIG[openvpn] = "--enable-openvpn --with-openvpn=${sbindir}/openvpn,--disable-openvpn,,openvpn"
PACKAGECONFIG[pptp] = "--enable-pptp --with-pptp=${sbindir}/pptp,--disable-pptp,ppp,pptp-linux"
PACKAGECONFIG[vpnc] = "--enable-vpnc --with-vpnc=${sbindir}/vpnc,--disable-vpnc,,vpnc"
PACKAGECONFIG[wireguard] = "--enable-wireguard,--disable-wireguard,libmnl"

INITSCRIPT_NAME = "connman"
INITSCRIPT_PARAMS = "start 05 5 2 3 . stop 22 0 1 6 ."

SYSTEMD_SERVICE:${PN} = "\
    connman.service \
    connman-wait-online.service \
    ${@bb.utils.contains_any('PACKAGECONFIG', ['openconnect', 'openvpn', 'vpnc', 'l2tp', 'pptp', 'wireguard'], 'connman-vpn.service', '', d)} \
"

ALTERNATIVE_PRIORITY = "100"
ALTERNATIVE:${PN} = "${@bb.utils.contains('DISTRO_FEATURES','systemd','resolv-conf','',d)}"
ALTERNATIVE_TARGET[resolv-conf] = "${@bb.utils.contains('DISTRO_FEATURES','systemd','${sysconfdir}/resolv-conf.connman','',d)}"
ALTERNATIVE_LINK_NAME[resolv-conf] = "${@bb.utils.contains('DISTRO_FEATURES','systemd','${sysconfdir}/resolv.conf','',d)}"

do_install:append() {
	if ${@bb.utils.contains('DISTRO_FEATURES','sysvinit','true','false',d)}; then
		install -d ${D}${sysconfdir}/init.d
		install -m 0755 ${UNPACKDIR}/connman ${D}${sysconfdir}/init.d/connman
		sed -i s%@DATADIR@%${datadir}% ${D}${sysconfdir}/init.d/connman
	fi

	for noinst_program in ${NOINST_TESTS} ${NOINST_TOOLS}; do
		if [ -r "${B}/$noinst_program" ]; then
			install -d ${D}${bindir}
			install -m 0755 "${B}/$noinst_program" ${D}${bindir}
		fi
	done

	# We don't need to package an empty directory
	rmdir --ignore-fail-on-non-empty ${D}${libdir}/connman/scripts ${D}${libdir}/connman

	# For read-only filesystem, do not create links during bootup
	if ${@bb.utils.contains('DISTRO_FEATURES','systemd','true','false',d)}; then
		install -d ${D}${sysconfdir}
		ln -sf ../run/connman/resolv.conf ${D}${sysconfdir}/resolv-conf.connman
	fi
}

NOINST_TESTS = "tools/supplicant-test tools/dhcp-test tools/dhcp-server-test \
		tools/addr-test tools/web-test tools/resolv-test tools/dbus-test \
		tools/polkit-test tools/wpad-test tools/private-network-test \
		tools/session-test tools/dnsproxy-test tools/iptables-test tools/ip6tables-test \
		tools/iptables-unit tools/dnsproxy-standalone \
		unit/test-ippool unit/test-iptables \
"
NOINST_TOOLS = "tools/stats-tool tools/wispr"

PACKAGE_BEFORE_PN = "${PN}-client ${PN}-tests ${PN}-tools"

FILES:${PN} += " \
    ${datadir}/dbus-1/system-services \
    ${datadir}/dbus-1/system.d \
    ${datadir}/polkit-1 \
    ${nonarch_libdir}/tmpfiles.d/*.conf \
"

FILES:${PN}-client = "${bindir}/connmanctl"
RDEPENDS:${PN}-client = "${PN}"

FILES:${PN}-tests = "${@ ' '.join([os.path.join('${bindir}', os.path.basename(noinst_program)) for noinst_program in NOINST_TESTS.split()]) }"
RDEPENDS:${PN}-tests = "${PN}"
ALLOW_EMPTY:${PN}-tests = "1"

FILES:${PN}-tools = "${@ ' '.join([os.path.join('${bindir}', os.path.basename(noinst_program)) for noinst_program in NOINST_TOOLS.split()]) }"
RDEPENDS:${PN}-tools = "${PN}"
ALLOW_EMPTY:${PN}-tools = "1"
