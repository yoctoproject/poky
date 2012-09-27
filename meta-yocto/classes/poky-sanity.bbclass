python check_bblayers_conf_append() {
    if current_lconf != lconf_version:
        if current_lconf == 5:
            index, meta_yocto_line = find_line('meta-yocto\s*\\\\\\n', lines)
            if meta_yocto_line:
                lines.insert(index + 1, meta_yocto_line.replace('meta-yocto',
                                                                'meta-yocto-bsp'))
            else:
                sys.exit()

            index, line = find_line('LCONF_VERSION', lines)
            current_lconf += 1
            lines[index] = 'LCONF_VERSION = "%d"\n' % current_lconf
            with open(bblayers_fn, "w") as f:
                f.write(''.join(lines))
}
