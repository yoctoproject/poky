python poky_update_bblayersconf() {
    current_version = int(d.getVar('LCONF_VERSION', True) or -1)
    latest_version = int(d.getVar('LAYER_CONF_VERSION', True) or -1)

    bblayers_fn = bblayers_conf_file(d)
    lines = sanity_conf_read(bblayers_fn)

    if current_version == 5 and latest_version == 6:
        if '/meta-yocto-bsp' not in d.getVar('BBLAYERS', True):
            index, meta_yocto_line = sanity_conf_find_line('meta-yocto\s*\\\\\\n', lines)
            if meta_yocto_line:
                lines.insert(index + 1, meta_yocto_line.replace('meta-yocto',
                                                                'meta-yocto-bsp'))
            else:
                sys.exit()

        current_version += 1
        sanity_conf_update(bblayers_fn, lines, 'LCONF_VERSION', current_version)
        return

    sys.exit()
}

BBLAYERS_CONF_UPDATE_FUNCS += "poky_update_bblayersconf"
