#
# Copyright OpenEmbedded Contributors
#
# SPDX-License-Identifier: GPL-2.0-only
#

import logging
import os
import sys
import os.path

import bb.utils

from bblayers.common import LayerPlugin

logger = logging.getLogger('bitbake-config-layers')

sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

def plugin_init(plugins):
    return ConfigFragmentsPlugin()

class ConfigFragmentsPlugin(LayerPlugin):
    def get_fragment_info(self, path, name):
        d = bb.data.init()
        d.setVar('BBPATH', self.tinfoil.config_data.getVar('BBPATH'))
        bb.parse.handle(path, d, True)
        summary = d.getVar('BB_CONF_FRAGMENT_SUMMARY')
        description = d.getVar('BB_CONF_FRAGMENT_DESCRIPTION')
        if not summary:
            raise Exception('Please add a one-line summary as BB_CONF_FRAGMENT_SUMMARY = \"...\" variable at the beginning of {}'.format(path))

        if not description:
            raise Exception('Please add a description as BB_CONF_FRAGMENT_DESCRIPTION = \"...\" variable at the beginning of {}'.format(path))

        return summary, description

    def discover_fragments(self):
        fragments_path_prefix = self.tinfoil.config_data.getVar('OE_FRAGMENTS_PREFIX')
        allfragments = {}
        for layername in self.bbfile_collections:
             layerdir = self.bbfile_collections[layername]
             fragments = []
             for topdir, dirs, files in os.walk(os.path.join(layerdir, fragments_path_prefix)):
                 fragmentdir = os.path.relpath(topdir, os.path.join(layerdir, fragments_path_prefix))
                 for fragmentfile in sorted(files):
                     if fragmentfile.startswith(".") or not fragmentfile.endswith(".conf"):
                         continue
                     fragmentname = os.path.normpath("/".join((layername, fragmentdir, fragmentfile.split('.')[0])))
                     fragmentpath = os.path.join(topdir, fragmentfile)
                     fragmentsummary, fragmentdesc = self.get_fragment_info(fragmentpath, fragmentname)
                     fragments.append({'path':fragmentpath, 'name':fragmentname, 'summary':fragmentsummary, 'description':fragmentdesc})
             if fragments:
                 allfragments[layername] = {'layerdir':layerdir,'fragments':fragments}
        return allfragments

    def do_list_fragments(self, args):
        """ List available configuration fragments """
        def print_fragment(f, verbose, is_enabled):
            if not verbose:
                print('{}\t{}'.format(f['name'], f['summary']))
            else:
                print('Name: {}\nPath: {}\nEnabled: {}\nSummary: {}\nDescription:\n{}\n'.format(f['name'], f['path'], 'yes' if is_enabled else 'no', f['summary'],''.join(f['description'])))

        def print_builtin_fragments(builtin, enabled):
            print('Available built-in fragments:')
            builtin_dict = {i[0]:i[1] for i in [f.split(':') for f in builtin]}
            for prefix,var in builtin_dict.items():
                print('{}/...\tSets {} = ...'.format(prefix, var))
            print('')
            enabled_builtin_fragments = [f for f in enabled if self.builtin_fragment_exists(f)]
            print('Enabled built-in fragments:')
            for f in enabled_builtin_fragments:
                 prefix, value = f.split('/', 1)
                 print('{}\tSets {} = "{}"'.format(f, builtin_dict[prefix], value))
            print('')

        all_enabled_fragments = (self.tinfoil.config_data.getVar('OE_FRAGMENTS') or "").split()
        all_builtin_fragments = (self.tinfoil.config_data.getVar('OE_FRAGMENTS_BUILTIN') or "").split()
        print_builtin_fragments(all_builtin_fragments, all_enabled_fragments)

        for layername, layerdata in self.discover_fragments().items():
            layerdir = layerdata['layerdir']
            fragments = layerdata['fragments']
            enabled_fragments = [f for f in fragments if f['name'] in all_enabled_fragments]
            disabled_fragments = [f for f in fragments if f['name'] not in all_enabled_fragments]

            print('Available fragments in {} layer located in {}:\n'.format(layername, layerdir))
            if enabled_fragments:
                print('Enabled fragments:')
                for f in enabled_fragments:
                    print_fragment(f, args.verbose, is_enabled=True)
                print('')
            if disabled_fragments:
                print('Unused fragments:')
                for f in disabled_fragments:
                    print_fragment(f, args.verbose, is_enabled=False)
            print('')

    def fragment_exists(self, fragmentname):
        for layername, layerdata in self.discover_fragments().items():
            for f in layerdata['fragments']:
              if f['name'] == fragmentname:
                  return True
        return False

    def builtin_fragment_exists(self, fragmentname):
        fragment_prefix = fragmentname.split("/",1)[0]
        fragment_prefix_defs = set([f.split(':')[0] for f in self.tinfoil.config_data.getVar('OE_FRAGMENTS_BUILTIN').split()])
        return fragment_prefix in fragment_prefix_defs

    def create_conf(self, confpath):
        if not os.path.exists(confpath):
            with open(confpath, 'w') as f:
                f.write('')
        with open(confpath, 'r') as f:
            lines = f.read()
        if "OE_FRAGMENTS += " not in lines:
            lines += "\nOE_FRAGMENTS += \"\"\n"
        with open(confpath, 'w') as f:
            f.write(lines)

    def do_enable_fragment(self, args):
        """ Enable a fragment in the local build configuration """
        def enable_helper(varname, origvalue, op, newlines):
            enabled_fragments = origvalue.split()
            for f in args.fragmentname:
                if f in enabled_fragments:
                    print("Fragment {} already included in {}".format(f, args.confpath))
                else:
                    enabled_fragments.append(f)
            return " ".join(enabled_fragments), None, 0, True

        for f in args.fragmentname:
            if not self.fragment_exists(f) and not self.builtin_fragment_exists(f):
                raise Exception("Fragment {} does not exist; use 'list-fragments' to see the full list.".format(f))

        self.create_conf(args.confpath)
        modified = bb.utils.edit_metadata_file(args.confpath, ["OE_FRAGMENTS"], enable_helper)
        if modified:
            print("Fragment {} added to {}.".format(", ".join(args.fragmentname), args.confpath))

    def do_disable_fragment(self, args):
        """ Disable a fragment in the local build configuration """
        def disable_helper(varname, origvalue, op, newlines):
            enabled_fragments = origvalue.split()
            for f in args.fragmentname:
                if f in enabled_fragments:
                    enabled_fragments.remove(f)
                else:
                    print("Fragment {} not currently enabled in {}".format(f, args.confpath))
            return " ".join(enabled_fragments), None, 0, True

        self.create_conf(args.confpath)
        modified = bb.utils.edit_metadata_file(args.confpath, ["OE_FRAGMENTS"], disable_helper)
        if modified:
            print("Fragment {} removed from {}.".format(", ".join(args.fragmentname), args.confpath))

    def do_show_fragment(self, args):
        """ Show the content of a fragment """
        for layername, layerdata in self.discover_fragments().items():
            fragments = layerdata['fragments']
            for fragment in fragments:
                if fragment['name'] == args.fragmentname:
                    print(f"{fragment['path']}:")
                    print()
                    with open(fragment['path']) as fd:
                        print(fd.read())
                    return

    def do_disable_all_fragments(self, args):
        """ Disable all fragments in the local build configuration """
        def disable_all_helper(varname, origvalue, op, newlines):
            return "", None, 0, True

        self.create_conf(args.confpath)
        modified = bb.utils.edit_metadata_file(args.confpath, ["OE_FRAGMENTS"], disable_all_helper)
        if modified:
            print("All fragments removed from {}.".format(args.confpath))

    def register_commands(self, sp):
        default_confpath = os.path.join(os.environ["BBPATH"], "conf/auto.conf")

        parser_list_fragments = self.add_command(sp, 'list-fragments', self.do_list_fragments, parserecipes=False)
        parser_list_fragments.add_argument("--confpath", default=default_confpath, help='Configuration file which contains a list of enabled fragments (default is {}).'.format(default_confpath))
        parser_list_fragments.add_argument('--verbose', '-v', action='store_true', help='Print extended descriptions of the fragments')

        parser_enable_fragment = self.add_command(sp, 'enable-fragment', self.do_enable_fragment, parserecipes=False)
        parser_enable_fragment.add_argument("--confpath", default=default_confpath, help='Configuration file which contains a list of enabled fragments (default is {}).'.format(default_confpath))
        parser_enable_fragment.add_argument('fragmentname', help='The name of the fragment (use list-fragments to see them)', nargs='+')

        parser_disable_fragment = self.add_command(sp, 'disable-fragment', self.do_disable_fragment, parserecipes=False)
        parser_disable_fragment.add_argument("--confpath", default=default_confpath, help='Configuration file which contains a list of enabled fragments (default is {}).'.format(default_confpath))
        parser_disable_fragment.add_argument('fragmentname', help='The name of the fragment', nargs='+')

        parser_show_fragment = self.add_command(sp, 'show-fragment', self.do_show_fragment, parserecipes=False)
        parser_show_fragment.add_argument('fragmentname', help='The name of the fragment')

        parser_disable_all = self.add_command(sp, 'disable-all-fragments', self.do_disable_all_fragments, parserecipes=False)
        parser_disable_all.add_argument("--confpath", default=default_confpath, help='Configuration file which contains a list of enabled fragments (default is {}).'.format(default_confpath))
