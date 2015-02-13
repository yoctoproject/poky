# package_regex.inc - This file contains data that tracks
# upstream project associated with a given recipe. This list is needed
# for recipes that version information can not be automagically discovered.
# As we automate this checking, this file will slowly be reduced.
#"
# This data is used by the package reporting system (packages.yoctoproject.org)
#"
# The format is as a bitbake variable override for each recipe
#"
#       REGEX_URI_pn-<recipe name> = "recipe_url"
#	 - This is the url used by the package checking system to
#	   get the latest version of the package
#       REGEX_pn-<recipe name> = "package_regex"
#	 - This is the regex the package checking system uses to
#	   parse the page found at REGEX_URI_pn-<recipe name>
#

COMMON_REGEX = "(?P<pver>(\d+[\.-_]*)+)"

# Generic regex don't match
REGEX_URI_pn-wireless-tools = "http://www.hpl.hp.com/personal/Jean_Tourrilhes/Linux/Tools.html"
REGEX_pn-wireless-tools = "wireless_tools\.(?P<pver>(\d+)(\..*|))\.tar\.gz"

REGEX_URI_pn-midori="http://midori-browser.org/download/source/"
REGEX_pn-midori="midori_(?P<pver>((\d+[\.-_]*)+))_all_\.tar\.bz2"

REGEX_URI_pn-sqlite3="http://www.sqlite.org/"
REGEX_pn-sqlite3="${COMMON_REGEX}"

REGEX_URI_pn-dhcp = "ftp://ftp.isc.org/isc/dhcp/"
REGEX_pn-dhcp="(?P<pver>\d+\.\d+\.(\d+?))"

REGEX_pn-foomatic-filters = "foomatic-filters-(?P<pver>((\d|\d\d)\.*)+)\.tar\.gz"
REGEX_pn-xdg-utils = "xdg-utils-(?P<pver>((\d+[\.-_]*)+)((rc|alpha|beta)\d+)?)\.(tar\.gz|tgz)"
REGEX_pn-rpm="rpm-${COMMON_REGEX}-.*$"

# Isn't possible to download with the default URI web server returns
# (403, 404, 550)
REGEX_URI_pn-json-c = "https://github.com/json-c/json-c/releases"
REGEX_URI_pn-chrpath = "http://alioth.debian.org/frs/?group_id=31052"
REGEX_URI_pn-adt-installer = "http://code.google.com/p/opkg/downloads/list"

REGEX_URI_pn-distcc = "http://code.google.com/p/distcc/downloads/list"
REGEX_URI_pn-ossp-uuid = "http://www.ossp.org/pkg/lib/uuid/"
REGEX_URI_pn-powertop = "https://01.org/powertop/downloads"
REGEX_URI_pn-libsamplerate0 = "http://www.mega-nerd.com/SRC/download.html"
REGEX_URI_pn-libxkbcommon = "http://xkbcommon.org/"
REGEX_URI_pn-tslib = "https://github.com/kergoth/tslib/releases"
REGEX_URI_pn-waffle="http://www.waffle-gl.org/releases.html"
REGEX_URI_pn-qt4-embedded="http://www.qt.io/download-open-source/"
REGEX_URI_pn-qt4-x11-free="http://www.qt.io/download-open-source/"
REGEX_URI_pn-fotowall = "https://code.google.com/p/fotowall/downloads/list"
REGEX_URI_pn-lrzsz = "http://ohse.de/uwe/software/lrzsz.html"
REGEX_URI_pn-libacpi = "http://www.ngolde.de/libacpi.html"
REGEX_URI_pn-less  = "http://www.greenwoodsoftware.com/less/download.html"
REGEX_URI_pn-cups = "http://www.cups.org/software.php"
REGEX_URI_pn-bzip2 = "http://www.bzip.org/downloads.html"
REGEX_URI_pn-minicom = "https://alioth.debian.org/frs/?group_id=30018"
REGEX_URI_pn-sysstat = "http://sebastien.godard.pagesperso-orange.fr/download.html"
REGEX_URI_pn-libical = "https://github.com/libical/libical/releases/"
REGEX_URI_pn-libmpc = "http://www.multiprecision.org/index.php?prog=mpc&page=download"
REGEX_URI_pn-taglib = "http://github.com/taglib/taglib/releases/"
REGEX_URI_pn-libevent = "http://libevent.org/"
REGEX_URI_pn-libproxy = "http://code.google.com/p/libproxy/downloads/list"
REGEX_URI_pn-db = "http://www.oracle.com/technetwork/products/berkeleydb/downloads/index-082944.html"
REGEX_URI_pn-python-smartpm="https://launchpad.net/smart/trunk/"
REGEX_URI_pn-libatomics-ops="http://www.hpl.hp.com/research/linux/atomic_ops/download.php4"
REGEX_URI_pn-libmad = "ftp://ftp.mars.org/pub/mpeg/"
REGEX_URI_pn-gamin = "http://ftp.gnome.org/pub/gnome/sources/gamin/0.1/"
REGEX_URI_pn-lsof = "ftp://sunsite.ualberta.ca/pub/Mirror/lsof/"

# The engine tries to use directory versioning but is a false-positive
REGEX_URI_pn-intltool = "https://launchpad.net/intltool/trunk/"
REGEX_URI_pn-libnfsidmap = "http://www.citi.umich.edu/projects/nfsv4/linux/libnfsidmap/"

# PyPI sites
REGEX_URI_pn-python-nose = "https://pypi.python.org/pypi/nose/"
REGEX_pn-python-nose = "/nose/${COMMON_REGEX}"
REGEX_URI_pn-python-distribute = "https://pypi.python.org/pypi/distribute/"
REGEX_pn-python-distribute = "/distribute/${COMMON_REGEX}"
REGEX_URI_pn-python3-distribute = "https://pypi.python.org/pypi/distribute/"
REGEX_pn-python3-distribute = "/distribute/${COMMON_REGEX}"
REGEX_URI_pn-python-gitdb = "https://pypi.python.org/pypi/gitdb/"
REGEX_pn-python-gitdb = "/gitdb/${COMMON_REGEX}"
REGEX_URI_pn-python-async = "https://pypi.python.org/pypi/async/"
REGEX_pn-python-async = "/async/${COMMON_REGEX}"
REGEX_URI_pn-python-smmap = "https://pypi.python.org/pypi/smmap/"
REGEX_pn-python-smmap = "/smmap/${COMMON_REGEX}"
REGEX_URI_pn-python-git = "https://pypi.python.org/pypi/GitPython/"
REGEX_pn-python-git = "/GitPython/${COMMON_REGEX}"
REGEX_URI_pn-python-mako = "https://pypi.python.org/pypi/mako/"
REGEX_pn-python-mako = "/Mako/${COMMON_REGEX}"

# Sourceforge sites
REGEX_URI_pn-expect = "http://sourceforge.net/projects/expect/files/Expect/"
REGEX_pn-expect = "/Expect/${COMMON_REGEX}/"
REGEX_URI_pn-docbook-xsl-stylesheets = "http://sourceforge.net/projects/docbook/files/docbook-xsl/"
REGEX_pn-docbook-xsl-stylesheets = "/docbook-xsl/${COMMON_REGEX}/"
REGEX_URI_pn-glew = "http://sourceforge.net/projects/glew/files/glew"
REGEX_pn-glew = "/glew/${COMMON_REGEX}/"
REGEX_URI_pn-menu-cache = "http://sourceforge.net/projects/lxde/files/menu-cache/"
REGEX_pn-menu-cache = "/menu-cache/${COMMON_REGEX}/"
REGEX_URI_pn-x11vnc = "http://sourceforge.net/projects/libvncserver/files/x11vnc/"
REGEX_pn-x11vnc = "/x11vnc/${COMMON_REGEX}/"
REGEX_URI_pn-quota = "http://sourceforge.net/projects/linuxquota/files/quota-tools/"
REGEX_pn-quota = "/quota-tools/${COMMON_REGEX}/"
REGEX_URI_pn-lsb = "http://sourceforge.net/projects/lsb/files/lsb_release/"
REGEX_pn-lsb = "/lsb_release/${COMMON_REGEX}/"
REGEX_URI_pn-libpcre = "http://sourceforge.net/projects/pcre/files/pcre/"
REGEX_pn-libpcre = "/pcre/${COMMON_REGEX}/"
REGEX_URI_pn-libusb-compat = "http://sourceforge.net/projects/libusb/files/libusb-compat-0.1/"
REGEX_pn-libusb-compat = "/libusb-compat-${COMMON_REGEX}/$"
REGEX_URI_pn-sysfsutils = "http://sourceforge.net/projects/linux-diag/files/sysfsutils/"
REGEX_pn-sysfsutils = "/sysfsutils/${COMMON_REGEX}/"
REGEX_URI_pn-console-tools = "http://sourceforge.net/projects/lct/files/console-tools-devel/"
REGEX_pn-console-tools = "/console-tools-devel/${COMMON_REGEX}/"
REGEX_URI_pn-watchdog = "http://sourceforge.net/projects/watchdog/files/watchdog/"
REGEX_pn-watchdog = "/watchdog/${COMMON_REGEX}/"
REGEX_URI_pn-cracklib = "http://sourceforge.net/projects/cracklib/files/cracklib/"
REGEX_pn-cracklib = "/cracklib/${COMMON_REGEX}/"

REGEX_URI_pn-libpfm4 = "http://sourceforge.net/projects/perfmon2/files/libpfm4/"
REGEX_URI_pn-liba52 = "http://liba52.sourceforge.net/downloads.html"
REGEX_URI_pn-mpeg2dec = "http://libmpeg2.sourceforge.net/downloads.html"
REGEX_URI_pn-pcmanfm = "http://sourceforge.net/projects/pcmanfm/files/PCManFM%20%2B%20Libfm%20%28tarball%20release%29/PCManFM/"
REGEX_URI_pn-libcgroup = "http://sourceforge.net/projects/libcg/files/libcgroup/"

# GIT
GITTAGREGEX_COMMON = "(?P<pver>\d+\.\d+\.(\d\.?)*)"

GITTAGREGEX_pn-linux-yocto = "${GITTAGREGEX_COMMON}"
GITTAGREGEX_pn-linux-yocto-tiny = "${GITTAGREGEX_COMMON}"
GITTAGREGEX_pn-linux-yocto-dev = "${GITTAGREGEX_COMMON}"
GITTAGREGEX_pn-uclibc = "${GITTAGREGEX_COMMON}"
GITTAGREGEX_pn-glibc = "${GITTAGREGEX_COMMON}"
GITTAGREGEX_pn-xf86-video-omap = "${GITTAGREGEX_COMMON}"
