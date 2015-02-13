# upstream_tracking.inc - This file contains data that tracks the
# upstream project associated with a given recipe. This list is needed
# for recipes that version information can not be automagically discovered.
# As we automate this checking, this file will slowed be reduced.
#
# This data is used by the package reporting system (packages.yoctoproject.org)
#
# The format is as a bitbake variable override for each recipe
#
#       RECIPE_UPSTREAM_VERSION_pn-<recipe name> = "<version>"
#       RECIPE_UPSTREAM_DATE_pn-<recipe name> = "Mmm dd, YYYY"
#	 - This is the latest upstream version and date
#       RECIPE_NO_UPDATE_REASON_pn-<recipe name> = "<free form text>"
#        - Used to note why a recipe should not be upgraded to a newer versoin
#       CHECK_DATE_pn-<recipe name> = "Mmm dd, YYYY"
#        - This is the date that upstream was last manually checked over time
#          this should be removed as we automate this checking
#
# These entries will slowly be removed as we can automatically determine
# the information in this file.  So for existing recipes that we can get 
# from the Recipe reporting system, the entries here can be removed.
#

# SVN support isn't implemented
RECIPE_UPSTREAM_VERSION_pn-tremor="20120314"
RECIPE_UPSTREAM_DATE_pn-tremor="Jan 22, 2012"
CHECK_DATE_pn-tremor = "Mar 11, 2013"
RECIPE_NO_UPDATE_REASON_pn-tremor = "Same revision on different SVN modules"

RECIPE_UPSTREAM_VERSION_pn-puzzles="r10286"
RECIPE_UPSTREAM_DATE_pn-puzzles="Oct 20, 2014"
CHECK_DATE_pn-puzzles = "Dec 18, 2014"

RECIPE_UPSTREAM_VERSION_pn-unfs3="0.9.22.r494"
RECIPE_UPSTREAM_DATE_pn-unfs3="Mar 14, 2014"
CHECK_DATE_pn-unfs3 = "Dec 18, 2014"

RECIPE_UPSTREAM_VERSION_pn-lz4 = "r123"
RECIPE_UPSTREAM_DATE_pn-lz4 = "Aug 28, 2014"
CHECK_DATE_pn-lz4 = "Aug 30, 2014"

# GIT don't have tag
RECIPE_UPSTREAM_VERSION_pn-x264 = "r2491"
RECIPE_UPSTREAM_DATE_pn-x264 = "Nov 13, 2014"
CHECK_DATE_pn-x264 = "Dec 17, 2014"

# Yocto project software
RECIPE_UPSTREAM_VERSION_pn-pseudo = "1.6.4"
RECIPE_UPSTREAM_DATE_pn-pseudo = "Jan 23, 2015"
CHECK_DATE_pseudo = "Feb 12, 2015"

# NO UPDATE REASONS
RECIPE_NO_UPDATE_REASON_pn-bluez4 = "BlueZ 5.x is not backward-compatible; components that interact with bluez not updated"
RECIPE_NO_UPDATE_REASON_pn-build-appliance = "Always reports behind"
RECIPE_NO_UPDATE_REASON_pn-cdrtools = "v3.x uses incompatible CDDL license"
RECIPE_NO_UPDATE_REASON_pn-createrepo = "Versions after 0.9.* use YUM, so we hold at 0.4.11"
RECIPE_NO_UPDATE_REASON_pn-db= "API compatibility issue"
RECIPE_NO_UPDATE_REASON_pn-dbus = "D-BUS 1.9.x is the development version, not stable."
RECIPE_NO_UPDATE_REASON_pn-gawk = "Version 4.1.0 requires Automake 1.13, but have 1.12.6"
RECIPE_NO_UPDATE_REASON_pn-glib-networking = "Pending Glib-2.0 Update"
RECIPE_NO_UPDATE_REASON_pn-gnome-desktop = "waiting for the sato gtk3 port"
RECIPE_NO_UPDATE_REASON_pn-gnome-icon-theme = "waiting for the sato gtk3 port"
RECIPE_NO_UPDATE_REASON_pn-gnome-keyring = "waiting for the sato gtk3 port"
RECIPE_NO_UPDATE_REASON_pn-gobject_introspection = "Does not cross-compile"
RECIPE_NO_UPDATE_REASON_pn-groff = "1.18.1.4 is latest GPLv2 Version no 1.21"
RECIPE_NO_UPDATE_REASON_pn-bash = "The latest version in yocto is 4.3.30"
RECIPE_NO_UPDATE_REASON_pn-gst-plugins-base = "not compatible with gst-fluendo 0.10.x"
RECIPE_NO_UPDATE_REASON_pn-gst-plugins-bad = "not compatible with gst-fluendo 0.10.x"
RECIPE_NO_UPDATE_REASON_pn-gst-plugins-good = "not compatible with gst-fluendo 0.10.x"
RECIPE_NO_UPDATE_REASON_pn-gstreamer=" not compatible with gst-fluendo 0.10.x "
RECIPE_NO_UPDATE_REASON_pn-gtk+ = "Do not upgrade to version: 2.99.2 because prefer stable tree"
RECIPE_NO_UPDATE_REASON_pn-gtk-engines = "2.91.1 is a 3.0 beta release"
RECIPE_NO_UPDATE_REASON_pn-jpeg = "webkit-gtk 1.8.3 doesn't work with jpeg 9"
RECIPE_NO_UPDATE_REASON_pn-kernelshark = "0.2 is the latest version."
RECIPE_NO_UPDATE_REASON_pn-liberation-fonts = "2.00.0 - fontforge package required "
RECIPE_NO_UPDATE_REASON_pn-libgnome-keyring = "waiting for the sato gtk3 port"
RECIPE_NO_UPDATE_REASON_pn-libnl = "libnl-3.2.2 is incompatible with libnl2, so no Upgrade"
RECIPE_NO_UPDATE_REASON_pn-libsoup = "2.41.90 is unstable"
RECIPE_NO_UPDATE_REASON_pn-libunique = "Do not upgrade to version: 2.91.4 because it requires gtk+ >= 2.90.0 and the stable version of gtk+ used by poky is 2.20.1"
RECIPE_NO_UPDATE_REASON-libxml2 = "only release candidates available "
RECIPE_NO_UPDATE_REASON_pn-mx-1.0 = "PRS 1.99 is dev version"
RECIPE_NO_UPDATE_REASON_pn-nettle = "3.0.0 breaks gnutls, api changes"
RECIPE_NO_UPDATE_REASON_pn-pkgconfig = "removes glib-conf, adds circular depends"
RECIPE_NO_UPDATE_REASON_pn-polkit = "requires spidermonkey 1.8.5, not available in poky"
RECIPE_NO_UPDATE_REASON_pn-python-distribute = "0.7.3 only upgrades 0.6.32, can't install on its own, also obsolete"
RECIPE_NO_UPDATE_REASON_pn-python-pygobject = "Newer versions of python-pygobject depend on gobject-introspection which doesn't cross-compile"
RECIPE_NO_UPDATE_REASON_pn-qemugl = "Do not upgrade to version: 33466cd8 because the upstream is broken in x86_64 build"
RECIPE_NO_UPDATE_REASON_pn-syslinux="Waiting for 4.06 for 3.3 kernel headers support"
RECIPE_NO_UPDATE_REASON_pn-texinfo = "Checking script parses directory wrong"
RECIPE_NO_UPDATE_REASON_pn-tinylogin = "TinyLogin was merged into BusyBox."
RECIPE_NO_UPDATE_REASON_pn-vte = "Pending Glib-2.0 Update"
RECIPE_NO_UPDATE_REASON_pn-webkit-gtk = ">= 1.10.2 needs ruby"
RECIPE_NO_UPDATE_REASON_pn-xdg-utils = "only release candidates available "
RECIPE_NO_UPDATE_REASON_pn-zaurusd = "SVN rev 426 is last Stable release"
RECIPE_NO_UPDATE_REASON_pn-tremor = "Same revision on different SVN modules"
