DEPENDS_atom-pc = "${STDDEPENDS} virtual/xserver-xf86 virtual/libgl"
EXTRA_OECONF_atom-pc = "${BASE_CONF} --with-flavour=glx"
PACKAGE_ARCH_atom-pc = "${MACHINE_ARCH}"

