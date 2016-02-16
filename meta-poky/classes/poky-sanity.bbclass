# Provide some extensions to sanity.bbclass to handle poky-specific conf file upgrades

python poky_update_bblayersconf() {
    current_version = int(d.getVar('POKY_BBLAYERS_CONF_VERSION', True) or -1)
    latest_version = int(d.getVar('REQUIRED_POKY_BBLAYERS_CONF_VERSION', True) or -1)

    # No version transitions here yet
    raise NotImplementedError("You need to update bblayers.conf manually for this version transision")
}

# Prepend to ensure our function runs before the OE-Core one
BBLAYERS_CONF_UPDATE_FUNCS =+ "conf/bblayers.conf:POKY_BBLAYERS_CONF_VERSION:REQUIRED_POKY_BBLAYERS_CONF_VERSION:poky_update_bblayersconf"
