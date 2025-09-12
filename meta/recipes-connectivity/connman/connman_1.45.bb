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

inherit autotools pkgconfig systemd update-rc.d update-alternatives

CVE_PRODUCT = "connman connection_manager"

DEPENDS  = "dbus glib-2.0"

SRC_URI = "${KERNELORG_MIRROR}/linux/network/${BPN}/${BP}.tar.xz \
           file://connman \
           file://no-version-scripts.patch \
           file://0001-connman-vpn-avoid-hiding-implementation-reserved-sym.patch \
           file://0002-resolve-musl-does-not-implement-res_ninit.patch \
           "

SRC_URI[sha256sum] = "77128cce80865455c4f106b5901a575e2dfdb35a7d2e2e2996f16e85cba10913"

RRECOMMENDS:${PN} = "connman-conf"
RCONFLICTS:${PN} = "networkmanager"

EXTRA_OECONF += "\
    ac_cv_path_IP6TABLES_SAVE=${sbindir}/ip6tables-save \
    ac_cv_path_IPTABLES_SAVE=${sbindir}/iptables-save \
    ac_cv_path_PPPD=${sbindir}/pppd \
    ac_cv_path_WPASUPPLICANT=${sbindir}/wpa_supplicant \
    --enable-debug \
    --enable-loopback \
    --enable-ethernet \
    --enable-tools \
    --disable-polkit \
    --runstatedir='${runtimedir}' \
    --with-dns-backend='${@bb.utils.contains("DISTRO_FEATURES", "systemd-resolved", "systemd-resolved", "internal", d)}' \
"
# For smooth operation it would be best to start only one wireless daemon at a time.
# If wpa-supplicant is running, connman will use it preferentially.
# Select either wpa-supplicant or iwd
WIRELESS_DAEMON ??= "wpa-supplicant"

PACKAGECONFIG ??= "wispr iptables client\
                   ${@bb.utils.filter('DISTRO_FEATURES', '3g systemd', d)} \
                   ${@bb.utils.contains('DISTRO_FEATURES', 'bluetooth', 'bluez', '', d)} \
                   ${@bb.utils.contains('DISTRO_FEATURES', 'wifi', 'wifi ${WIRELESS_DAEMON}', '', d)} \
"

# If you want ConnMan to support VPN, add following statement into
# local.conf or distro config
# PACKAGECONFIG:append:pn-connman = " openvpn vpnc l2tp pptp"

PACKAGECONFIG[systemd] = "--with-systemdunitdir=${systemd_system_unitdir}/ --with-tmpfilesdir=${sysconfdir}/tmpfiles.d/,--with-systemdunitdir='' --with-tmpfilesdir=''"
PACKAGECONFIG[wifi] = "--enable-wifi, --disable-wifi"
PACKAGECONFIG[bluez] = "--enable-bluetooth, --disable-bluetooth, bluez5, bluez5"
PACKAGECONFIG[3g] = "--enable-ofono, --disable-ofono, ofono, ofono"
PACKAGECONFIG[wpa-supplicant] = ",,wpa-supplicant,wpa-supplicant"
PACKAGECONFIG[iwd] = "--enable-iwd,--disable-iwd,,iwd"
PACKAGECONFIG[tist] = "--enable-tist,--disable-tist,"
PACKAGECONFIG[openvpn] = "--enable-openvpn --with-openvpn=${sbindir}/openvpn,--disable-openvpn,,openvpn"
PACKAGECONFIG[vpnc] = "--enable-vpnc --with-vpnc=${sbindir}/vpnc,--disable-vpnc,,vpnc"
PACKAGECONFIG[l2tp] = "--enable-l2tp --with-l2tp=${sbindir}/xl2tpd,--disable-l2tp,ppp,xl2tpd"
PACKAGECONFIG[pptp] = "--enable-pptp --with-pptp=${sbindir}/pptp,--disable-pptp,ppp,pptp-linux"
# WISPr support for logging into hotspots, requires TLS
PACKAGECONFIG[wispr] = "--enable-wispr,--disable-wispr,gnutls,"
PACKAGECONFIG[nftables] = "--with-firewall=nftables ,,libmnl libnftnl,,kernel-module-nf-tables kernel-module-nft-chain-nat-ipv4 kernel-module-nft-chain-route-ipv4 kernel-module-nft-masq-ipv4 kernel-module-nft-nat,iptables"
PACKAGECONFIG[iptables] = "--with-firewall=iptables,,iptables,,,nftables"
PACKAGECONFIG[nfc] = "--enable-neard, --disable-neard, neard, neard"
PACKAGECONFIG[client] = "--enable-client,--disable-client,readline"
PACKAGECONFIG[wireguard] = "--enable-wireguard,--disable-wireguard,libmnl"

INITSCRIPT_NAME = "connman"
INITSCRIPT_PARAMS = "start 05 5 2 3 . stop 22 0 1 6 ."

python __anonymous () {
    systemd_packages = "${PN} ${PN}-wait-online"
    pkgconfig = d.getVar('PACKAGECONFIG')
    if ('openvpn' or 'vpnc' or 'l2tp' or 'pptp') in pkgconfig.split():
        systemd_packages += " ${PN}-vpn"
    d.setVar('SYSTEMD_PACKAGES', systemd_packages)
}

SYSTEMD_SERVICE:${PN} = "connman.service"
SYSTEMD_SERVICE:${PN}-vpn = "connman-vpn.service"
SYSTEMD_SERVICE:${PN}-wait-online = "connman-wait-online.service"

ALTERNATIVE_PRIORITY = "${@bb.utils.contains('DISTRO_FEATURES','systemd-resolved','10','100',d)}"
ALTERNATIVE:${PN} = "${@bb.utils.contains('DISTRO_FEATURES','systemd','resolv-conf','',d)}"
ALTERNATIVE_TARGET[resolv-conf] = "${@bb.utils.contains('DISTRO_FEATURES','systemd','${sysconfdir}/resolv-conf.connman','',d)}"
ALTERNATIVE_LINK_NAME[resolv-conf] = "${@bb.utils.contains('DISTRO_FEATURES','systemd','${sysconfdir}/resolv.conf','',d)}"

do_install:append() {
	if ${@bb.utils.contains('DISTRO_FEATURES','sysvinit','true','false',d)}; then
		install -d ${D}${sysconfdir}/init.d
		install -m 0755 ${UNPACKDIR}/connman ${D}${sysconfdir}/init.d/connman
		sed -i s%@DATADIR@%${datadir}% ${D}${sysconfdir}/init.d/connman
	fi

	install -d ${D}${bindir}
	install -m 0755 ${B}/tools/*-test ${D}${bindir}
	if [ -e ${B}/tools/wispr ]; then
		install -m 0755 ${B}/tools/wispr ${D}${bindir}
	fi

	# We don't need to package an empty directory
	rmdir --ignore-fail-on-non-empty ${D}${libdir}/connman/scripts

	# Automake 1.12 won't install empty directories, but we need the
	# plugins directory to be present for ownership
	mkdir -p ${D}${libdir}/connman/plugins

	# For read-only filesystem, do not create links during bootup
	if ${@bb.utils.contains('DISTRO_FEATURES','systemd','true','false',d)}; then
		install -d ${D}${sysconfdir}
		ln -sf ../run/connman/resolv.conf ${D}${sysconfdir}/resolv-conf.connman
	fi
}

# These used to be plugins, but now they are core
RPROVIDES:${PN} = "\
	connman-plugin-loopback \
	connman-plugin-ethernet \
	${@bb.utils.contains('PACKAGECONFIG', 'bluetooth','connman-plugin-bluetooth', '', d)} \
	${@bb.utils.contains('PACKAGECONFIG', 'wifi','connman-plugin-wifi', '', d)} \
	${@bb.utils.contains('PACKAGECONFIG', '3g','connman-plugin-ofono', '', d)} \
	"

PACKAGES_DYNAMIC += "^${PN}-plugin-.*"

def add_rdepends(bb, d, file, pkg, depmap, multilib_prefix, add_insane_skip):
    plugintype = pkg.split( '-' )[-1]
    if plugintype in depmap:
        rdepends = map(lambda x: multilib_prefix + x, \
                       depmap[plugintype].split())
        d.setVar("RDEPENDS:%s" % pkg, " ".join(rdepends))
    if add_insane_skip:
        d.appendVar("INSANE_SKIP:%s" % pkg, "dev-so")

python populate_packages:prepend() {
    depmap = dict(pppd="ppp")
    multilib_prefix = (d.getVar("MLPREFIX") or "")

    hook = lambda file,pkg,x,y,z: \
        add_rdepends(bb, d, file, pkg, depmap, multilib_prefix, False)
    plugin_dir = d.expand('${libdir}/connman/plugins/')
    plugin_name = d.expand('${PN}-plugin-%s')
    do_split_packages(d, plugin_dir, r'^(.*).so$', plugin_name, \
        '${PN} plugin for %s', extra_depends='', hook=hook, prepend=True )

    hook = lambda file,pkg,x,y,z: \
        add_rdepends(bb, d, file, pkg, depmap, multilib_prefix, True)
    plugin_dir = d.expand('${libdir}/connman/plugins-vpn/')
    plugin_name = d.expand('${PN}-plugin-vpn-%s')
    do_split_packages(d, plugin_dir, r'^(.*).so$', plugin_name, \
        '${PN} VPN plugin for %s', extra_depends='', hook=hook, prepend=True )
}

PACKAGES =+ "${PN}-tools ${PN}-tests ${PN}-client"

FILES:${PN}-tools = "${bindir}/wispr"
RDEPENDS:${PN}-tools = "${PN}"

FILES:${PN}-tests = "${bindir}/*-test"
RDEPENDS:${PN}-tests = "${@bb.utils.contains('PACKAGECONFIG', 'iptables', 'iptables', '', d)}"

FILES:${PN}-client = "${bindir}/connmanctl"
RDEPENDS:${PN}-client = "${PN}"

FILES:${PN} = "${bindir}/* ${sbindir}/* ${libexecdir}/* ${libdir}/lib*.so.* \
            ${libdir}/connman/plugins \
            ${sysconfdir} ${sharedstatedir} ${localstatedir} ${datadir} \
            ${base_bindir}/* ${base_sbindir}/* ${base_libdir}/*.so* ${datadir}/${PN} \
            ${datadir}/dbus-1/system-services/* \
            ${sysconfdir}/tmpfiles.d/connman_resolvconf.conf"

FILES:${PN}-dev += "${libdir}/connman/*/*.la"

PACKAGES =+ "${PN}-vpn ${PN}-wait-online"

SUMMARY:${PN}-vpn = "A daemon for managing VPN connections within embedded devices"
DESCRIPTION:${PN}-vpn = "The ConnMan VPN provides a daemon for \
managing VPN connections within embedded devices running the Linux \
operating system.  The connman-vpnd handles all the VPN connections \
and starts/stops VPN client processes when necessary. The connman-vpnd \
provides a DBus API for managing VPN connections. All the different \
VPN technogies are implemented using plug-ins."
FILES:${PN}-vpn += "${sbindir}/connman-vpnd \
                    ${sysconfdir}/dbus-1/system.d/connman-vpn-dbus.conf \
                    ${datadir}/dbus-1/system-services/net.connman.vpn.service \
                    ${systemd_system_unitdir}/connman-vpn.service"

SUMMARY:${PN}-wait-online = "A program that will return once ConnMan has connected to a network"
DESCRIPTION:${PN}-wait-online = "A service that can be enabled so that \
the system waits until a network connection is established."
FILES:${PN}-wait-online += "${sbindir}/connmand-wait-online \
                            ${systemd_system_unitdir}/connman-wait-online.service"

SUMMARY:${PN}-plugin-vpn-openvpn = "An OpenVPN plugin for ConnMan VPN"
DESCRIPTION:${PN}-plugin-vpn-openvpn = "The ConnMan OpenVPN plugin uses openvpn client \
to create a VPN connection to OpenVPN server."
FILES:${PN}-plugin-vpn-openvpn += "${libdir}/connman/scripts/openvpn-script \
                                   ${libdir}/connman/plugins-vpn/openvpn.so"
RDEPENDS:${PN}-plugin-vpn-openvpn += "${PN}-vpn"
RRECOMMENDS:${PN} += "${@bb.utils.contains('PACKAGECONFIG','openvpn','${PN}-plugin-vpn-openvpn', '', d)}"

SUMMARY:${PN}-plugin-vpn-vpnc = "A vpnc plugin for ConnMan VPN"
DESCRIPTION:${PN}-plugin-vpn-vpnc = "The ConnMan vpnc plugin uses vpnc client \
to create a VPN connection to Cisco3000 VPN Concentrator."
FILES:${PN}-plugin-vpn-vpnc += "${libdir}/connman/scripts/openconnect-script \
                                ${libdir}/connman/plugins-vpn/vpnc.so \
                                ${libdir}/connman/scripts/vpn-script"
RDEPENDS:${PN}-plugin-vpn-vpnc += "${PN}-vpn"
RRECOMMENDS:${PN} += "${@bb.utils.contains('PACKAGECONFIG','vpnc','${PN}-plugin-vpn-vpnc', '', d)}"

SUMMARY:${PN}-plugin-vpn-l2tp = "A L2TP plugin for ConnMan VPN"
DESCRIPTION:${PN}-plugin-vpn-l2tp = "The ConnMan L2TP plugin uses xl2tpd daemon \
to create a VPN connection to L2TP server."
FILES:${PN}-plugin-vpn-l2tp += "${libdir}/connman/scripts/libppp-plugin.so* \
                                ${libdir}/connman/plugins-vpn/l2tp.so"
RDEPENDS:${PN}-plugin-vpn-l2tp += "${PN}-vpn"
RRECOMMENDS:${PN} += "${@bb.utils.contains('PACKAGECONFIG','l2tp','${PN}-plugin-vpn-l2tp', '', d)}"

SUMMARY:${PN}-plugin-vpn-pptp = "A PPTP plugin for ConnMan VPN"
DESCRIPTION:${PN}-plugin-vpn-pptp = "The ConnMan PPTP plugin uses pptp-linux client \
to create a VPN connection to PPTP server."
FILES:${PN}-plugin-vpn-pptp += "${libdir}/connman/scripts/libppp-plugin.so* \
                                ${libdir}/connman/plugins-vpn/pptp.so"
RDEPENDS:${PN}-plugin-vpn-pptp += "${PN}-vpn"
RRECOMMENDS:${PN} += "${@bb.utils.contains('PACKAGECONFIG','pptp','${PN}-plugin-vpn-pptp', '', d)}"
