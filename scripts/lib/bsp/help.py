# ex:ts=4:sw=4:sts=4:et
# -*- tab-width: 4; c-basic-offset: 4; indent-tabs-mode: nil -*-
#
# Copyright (c) 2012, Intel Corporation.
# All rights reserved.
#
# This program is free software; you can redistribute it and/or modify
# it under the terms of the GNU General Public License version 2 as
# published by the Free Software Foundation.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License along
# with this program; if not, write to the Free Software Foundation, Inc.,
# 51 Franklin Street, Fifth Floor, Boston, MA 02110-1301 USA.
#
# DESCRIPTION
# This module implements some basic help invocation functions along
# with the bulk of the help topic text for the Yocto BSP Tools.
#
# AUTHORS
# Tom Zanussi <tom.zanussi (at] intel.com>
#

import subprocess
import logging


def subcommand_error(args):
    logging.info("invalid subcommand %s" % args[0])


def display_help(subcommand, subcommands):
    """
    Display help for subcommand.
    """
    if subcommand not in subcommands:
        return False

    help = subcommands.get(subcommand, subcommand_error)[2]
    pager = subprocess.Popen('less', stdin=subprocess.PIPE)
    pager.communicate(help)

    return True


def yocto_help(args, usage_str, subcommands):
    """
    Subcommand help dispatcher.
    """
    if len(args) == 1 or not display_help(args[1], subcommands):
        print(usage_str)


def invoke_subcommand(args, parser, main_command_usage, subcommands):
    """
    Dispatch to subcommand handler borrowed from combo-layer.
    Should use argparse, but has to work in 2.6.
    """
    if not args:
        logging.error("No subcommand specified, exiting")
        parser.print_help()
    elif args[0] == "help":
        yocto_help(args, main_command_usage, subcommands)
    elif args[0] not in subcommands:
        logging.error("Unsupported subcommand %s, exiting\n" % (args[0]))
        parser.print_help()
    else:
        usage = subcommands.get(args[0], subcommand_error)[1]
        subcommands.get(args[0], subcommand_error)[0](args[1:], usage)


##
# yocto-bsp help and usage strings
##

yocto_bsp_usage = """

 Create a customized Yocto BSP layer.

 usage: yocto-bsp [--version] [--help] COMMAND [ARGS]

 Current 'yocto-bsp' commands are:
    create            Create a new Yocto BSP
    list              List available values for options and BSP properties

 See 'yocto-bsp help COMMAND' for more information on a specific command.
"""

yocto_bsp_help_usage = """

 usage: yocto-bsp help <subcommand>

 This command displays detailed help for the specified subcommand.
"""

yocto_bsp_create_usage = """

 Create a new Yocto BSP

 usage: yocto-bsp create <bsp-name> <karch> [-o <DIRNAME> | --outdir <DIRNAME>]
            [-i <JSON PROPERTY FILE> | --infile <JSON PROPERTY_FILE>]

 This command creates a Yocto BSP based on the specified parameters.
 The new BSP will be a new Yocto BSP layer contained by default within
 the top-level directory specified as 'meta-bsp-name'.  The -o option
 can be used to place the BSP layer in a directory with a different
 name and location.

 The value of the 'karch' parameter determines the set of files that
 will be generated for the BSP, along with the specific set of
 'properties' that will be used to fill out the BSP-specific portions
 of the BSP.  The possible values for the 'karch' paramter can be
 listed via 'yocto-bsp list karch'.

 NOTE: Once created, you should add your new layer to your
 bblayers.conf file in order for it to be subsequently seen and
 modified by the yocto-kernel tool.

 See 'yocto bsp help create' for more detailed instructions.

 NOTE: For x86- and x86_64-based BSPs, the generated BSP assumes the
 presence of the meta-intel layer. Ensure the meta-intel layer is
 present and added to bblayers.conf.

 See 'yocto bsp help create' for more detailed instructions.
"""

yocto_bsp_create_help = """

NAME
    yocto-bsp create - Create a new Yocto BSP

SYNOPSIS
    yocto-bsp create <bsp-name> <karch> [-o <DIRNAME> | --outdir <DIRNAME>]
        [-i <JSON PROPERTY FILE> | --infile <JSON PROPERTY_FILE>]

DESCRIPTION
    This command creates a Yocto BSP based on the specified
    parameters.  The new BSP will be a new Yocto BSP layer contained
    by default within the top-level directory specified as
    'meta-bsp-name'.  The -o option can be used to place the BSP layer
    in a directory with a different name and location.

    The value of the 'karch' parameter determines the set of files
    that will be generated for the BSP, along with the specific set of
    'properties' that will be used to fill out the BSP-specific
    portions of the BSP.  The possible values for the 'karch' paramter
    can be listed via 'yocto-bsp list karch'.

    The BSP-specific properties that define the values that will be
    used to generate a particular BSP can be specified on the
    command-line using the -i option and supplying a JSON object
    consisting of the set of name:value pairs needed by the BSP.

    If the -i option is not used, the user will be interactively
    prompted for each of the required property values, which will then
    be used as values for BSP generation.

    The set of properties available for a given architecture can be
    listed using the 'yocto-bsp list' command.

    Specifying -c causes the Python code generated and executed to
    create the BSP to be dumped to the 'bspgen.out' file in the
    current directory, and is useful for debugging.

    NOTE: Once created, you should add your new layer to your
    bblayers.conf file in order for it to be subsequently seen and
    modified by the yocto-kernel tool.

    For example, assuming your poky repo is at /path/to/poky, your new
    BSP layer is at /path/to/poky/meta-mybsp, and your build directory
    is /path/to/build:

    $ gedit /path/to/build/conf/bblayers.conf

    BBLAYERS ?= " \\
      /path/to/poky/meta \\
      /path/to/poky/meta-yocto \\
      /path/to/poky/meta-mybsp \\
      "

    NOTE: For x86- and x86_64-based BSPs, the generated BSP assumes
    the presence of the meta-intel layer. Ensure the meta-intel layer
    is present and added to bblayers.conf.

    For example, assuming your poky repo is at /path/to/poky, your new
    BSP layer is at /path/to/poky/meta-mybsp, and your build directory
    is /path/to/build:

    $ cd /path/to/poky
    $ git clone git://git.yoctoproject.org/meta-intel.git

    $ gedit /path/to/build/conf/bblayers.conf

    BBLAYERS ?= " \\
      /path/to/poky/meta \\
      /path/to/poky/meta-yocto \\
      /path/to/poky/meta-intel \\
      /path/to/poky/meta-mybsp \\
      "
"""

yocto_bsp_list_usage = """

 usage: yocto-bsp list karch
        yocto-bsp list <karch> properties
                [-o <JSON PROPERTY FILE> | --outfile <JSON PROPERTY_FILE>]
        yocto-bsp list <karch> property <xxx>
                [-o <JSON PROPERTY FILE> | --outfile <JSON PROPERTY_FILE>]

 This command enumerates the complete set of possible values for a
 specified option or property needed by the BSP creation process.

 The first form enumerates all the possible values that exist and can
 be specified for the 'karch' parameter to the 'yocto bsp create'
 command.

 The second form enumerates all the possible properties that exist and
 must have values specified for them in the 'yocto bsp create' command
 for the given 'karch'.

 The third form enumerates all the possible values that exist and can
 be specified for any of the enumerable properties of the given
 'karch' in the 'yocto bsp create' command.

 See 'yocto-bsp help list' for more details.
"""

yocto_bsp_list_help = """

NAME
    yocto-bsp list - List available values for options and BSP properties

SYNOPSIS
    yocto-bsp list karch
    yocto-bsp list <karch> properties
            [--o <JSON PROPERTY FILE> | -outfile <JSON PROPERTY_FILE>]
    yocto-bsp list <karch> property <xxx>
            [--o <JSON PROPERTY FILE> | -outfile <JSON PROPERTY_FILE>]

DESCRIPTION
    This command enumerates the complete set of possible values for a
    specified option or property needed by the BSP creation process.

    The first form enumerates all the possible values that exist and
    can be specified for the 'karch' parameter to the 'yocto bsp
    create' command.  Example output for the 'list karch' command:

    $ yocto-bsp list karch
    Architectures available:
        arm
        powerpc
        i386
        mips
        x86_64
        qemu

    The second form enumerates all the possible properties that exist
    and must have values specified for them in the 'yocto bsp create'
    command for the given 'karch'.  This command is mainly meant to
    allow the development user interface alternatives to the default
    text-based prompting interface.  If the -o option is specified,
    the list of properties, in addition to being displayed, will be
    written to the specified file as a JSON object.  In this case, the
    object will consist of the set of name:value pairs corresponding
    to the (possibly nested) dictionary of properties defined by the
    input statements used by the BSP.  Some example output for the
    'list properties' command:

    $ yocto-bsp list arm properties
    "touchscreen" : {
        "msg" : Does your BSP have a touchscreen? (y/N)
        "default" : n
        "type" : boolean
    }
    "uboot_loadaddress" : {
        "msg" : Please specify a value for UBOOT_LOADADDRESS.
        "default" : 0x80008000
        "type" : edit
        "prio" : 40
    }
    "kernel_choice" : {
        "prio" : 10
        "default" : linux-yocto_3.2
        "depends-on" : use_default_kernel
        "depends-on-val" : n
        "msg" : Please choose the kernel to use in this BSP =>
        "type" : choicelist
        "gen" : bsp.kernel.kernels
    }
    "if kernel_choice == "linux-yocto_3.0":" : {
        "base_kbranch_linux_yocto_3_0" : {
            "prio" : 20
            "default" : yocto/standard
            "depends-on" : new_kbranch_linux_yocto_3_0
            "depends-on-val" : y
            "msg" : Please choose a machine branch to base this BSP on =>
            "type" : choicelist
            "gen" : bsp.kernel.all_branches
    }
    .
    .
    .

    Each entry in the output consists of the name of the input element
    e.g. "touchscreen", followed by the properties defined for that
    element enclosed in braces.  This information should provide
    sufficient information to create a complete user interface with.
    Two features of the scheme provide for conditional input.  First,
    if a Python "if" statement appears in place of an input element
    name, the set of enclosed input elements apply and should be
    presented to the user only if the 'if' statement evaluates to
    true.  The test in the if statement will always reference another
    input element in the list, which means that the element being
    tested should be presented to the user before the elements
    enclosed by the if block.  Secondly, in a similar way, some
    elements contain "depends-on" and depends-on-val" tags, which mean
    that the affected input element should only be presented to the
    user if the element it depends on has already been presented to
    the user and the user has selected the specified value for that
    element.

    The third form enumerates all the possible values that exist and
    can be specified for any of the enumerable properties of the given
    'karch' in the 'yocto bsp create' command.  If the -o option is
    specified, the list of values for the given property, in addition
    to being displayed, will be written to the specified file as a
    JSON object.  In this case, the object will consist of the set of
    name:value pairs corresponding to the array of property values
    associated with the property.

    $ yocto-bsp list i386 property xserver_choice
        ["xserver_vesa", "VESA xserver support"]
        ["xserver_emgd", "EMGD xserver support (proprietary)"]
        ["xserver_i915", "i915 xserver support"]

    $ yocto-bsp list arm property base_kbranch_linux_yocto_3_0
        Getting branches from remote repo git://git.yoctoproject.org/linux-yocto-3.0...
        ["yocto/base", "yocto/base"]
        ["yocto/eg20t", "yocto/eg20t"]
        ["yocto/emgd", "yocto/emgd"]
        ["yocto/emgd-1.10", "yocto/emgd-1.10"]
        ["yocto/gma500", "yocto/gma500"]
        ["yocto/pvr", "yocto/pvr"]
        ["yocto/standard/arm-versatile-926ejs", "yocto/standard/arm-versatile-926ejs"]
        ["yocto/standard/base", "yocto/standard/base"]
        ["yocto/standard/beagleboard", "yocto/standard/beagleboard"]
        ["yocto/standard/cedartrail", "yocto/standard/cedartrail"]
        .
        .
        .
        ["yocto/standard/qemu-ppc32", "yocto/standard/qemu-ppc32"]
        ["yocto/standard/routerstationpro", "yocto/standard/routerstationpro"]

    The third form as well is meant mainly for developers of
    alternative interfaces - it allows the developer to fetch the
    possible values for a given input element on-demand.  This
    on-demand capability is especially valuable for elements that
    require relatively expensive remote operations to fulfill, such as
    the example that returns the set of branches available in a remote
    git tree above.

"""

##
# yocto-kernel help and usage strings
##

yocto_kernel_usage = """

 Modify and list Yocto BSP kernel config items and patches.

 usage: yocto-kernel [--version] [--help] COMMAND [ARGS]

 Current 'yocto-kernel' commands are:
   config list       List the modifiable set of bare kernel config options for a BSP
   config add        Add or modify bare kernel config options for a BSP
   config rm         Remove bare kernel config options from a BSP
   patch list        List the patches associated with a BSP
   patch add         Patch the Yocto kernel for a BSP
   patch rm          Remove patches from a BSP

 See 'yocto-kernel help COMMAND' for more information on a specific command.

"""


yocto_kernel_help_usage = """

 usage: yocto-kernel help <subcommand>

 This command displays detailed help for the specified subcommand.
"""

yocto_kernel_config_list_usage = """

 List the modifiable set of bare kernel config options for a BSP

 usage: yocto-kernel config list <bsp-name>

 This command lists the 'modifiable' config items for a BSP i.e. the
 items which are eligible for modification or removal by other
 yocto-kernel commands.

 'modifiable' config items are the config items contained a BSP's
 user-config.cfg base config.
"""


yocto_kernel_config_list_help = """

NAME
    yocto-kernel config list - List the modifiable set of bare kernel
    config options for a BSP

SYNOPSIS
    yocto-kernel config list <bsp-name>

DESCRIPTION
    This command lists the 'modifiable' config items for a BSP
    i.e. the items which are eligible for modification or removal by
    other yocto-kernel commands.
"""


yocto_kernel_config_add_usage = """

 Add or modify bare kernel config options for a BSP

 usage: yocto-kernel config add <bsp-name> [<CONFIG_XXX=x> ...]

 This command adds one or more CONFIG_XXX=x items to a BSP's user-config.cfg
 base config.
"""


yocto_kernel_config_add_help = """

NAME
    yocto-kernel config add - Add or modify bare kernel config options
    for a BSP

SYNOPSIS
    yocto-kernel config add <bsp-name> [<CONFIG_XXX=x> ...]

DESCRIPTION
    This command adds one or more CONFIG_XXX=x items to a BSP's
    foo.cfg base config.

    NOTE: It's up to the user to determine whether or not the config
    options being added make sense or not - this command does no
    sanity checking or verification of any kind to ensure that a
    config option really makes sense and will actually be set in in
    the final config.  For example, if a config option depends on
    other config options, it will be turned off by kconfig if the
    other options aren't set correctly.
"""


yocto_kernel_config_rm_usage = """

 Remove bare kernel config options from a BSP

 usage: yocto-kernel config rm <bsp-name>

 This command removes (turns off) one or more CONFIG_XXX items from a
 BSP's user-config.cfg base config.

 The set of config items available to be removed by this command for a
 BSP is listed and the user prompted for the specific items to remove.
"""


yocto_kernel_config_rm_help = """

NAME
    yocto-kernel config rm - Remove bare kernel config options from a
    BSP

SYNOPSIS
    yocto-kernel config rm <bsp-name>

DESCRIPTION
    This command removes (turns off) one or more CONFIG_XXX items from a
    BSP's user-config.cfg base config.

    The set of config items available to be removed by this command
    for a BSP is listed and the user prompted for the specific items
    to remove.
"""


yocto_kernel_patch_list_usage = """

 List the patches associated with the kernel for a BSP

 usage: yocto-kernel patch list <bsp-name>

 This command lists the patches associated with a BSP.

 NOTE: this only applies to patches listed in the kernel recipe's
 user-patches.scc file (and currently repeated in its SRC_URI).
"""


yocto_kernel_patch_list_help = """

NAME
    yocto-kernel patch list - List the patches associated with the kernel
    for a BSP

SYNOPSIS
    yocto-kernel patch list <bsp-name>

DESCRIPTION
    This command lists the patches associated with a BSP.

    NOTE: this only applies to patches listed in the kernel recipe's
    user-patches.scc file (and currently repeated in its SRC_URI).
"""


yocto_kernel_patch_add_usage = """

 Patch the Yocto kernel for a specific BSP

 usage: yocto-kernel patch add <bsp-name> [<PATCH> ...]

 This command adds one or more patches to a BSP's machine branch.  The
 patch will be added to the BSP's linux-yocto kernel user-patches.scc
 file (and currently repeated in its SRC_URI) and will be guaranteed
 to be applied in the order specified.
"""


yocto_kernel_patch_add_help = """

NAME
    yocto-kernel patch add - Patch the Yocto kernel for a specific BSP

SYNOPSIS
    yocto-kernel patch add <bsp-name> [<PATCH> ...]

DESCRIPTION
    This command adds one or more patches to a BSP's machine branch.
    The patch will be added to the BSP's linux-yocto kernel
    user-patches.scc file (and currently repeated in its SRC_URI) and
    will be guaranteed to be applied in the order specified.

    NOTE: It's up to the user to determine whether or not the patches
    being added makes sense or not - this command does no sanity
    checking or verification of any kind to ensure that a patch can
    actually be applied to the BSP's kernel branch; it's assumed that
    the user has already done that.
"""


yocto_kernel_patch_rm_usage = """

 Remove a patch from the Yocto kernel for a specific BSP

 usage: yocto-kernel patch rm <bsp-name>

 This command removes one or more patches from a BSP's machine branch.
 The patch will be removed from the BSP's linux-yocto kernel
 user-patches.scc file (and currently repeated in its SRC_URI) and
 kernel SRC_URI dir.

 The set of patches available to be removed by this command for a BSP
 is listed and the user prompted for the specific patches to remove.
"""


yocto_kernel_patch_rm_help = """

NAME
    yocto-kernel patch rm - Remove a patch from the Yocto kernel for a specific BSP

SYNOPSIS
    yocto-kernel patch rm <bsp-name>

DESCRIPTION
    This command removes one or more patches from a BSP's machine
    branch.  The patch will be removed from the BSP's linux-yocto
    kernel user-patches.scc file (and currently repeated in its
    SRC_URI).

    The set of patches available to be removed by this command for a
    BSP is listed and the user prompted for the specific patches to
    remove.
"""

##
# test code
##

test_bsp_properties = {
    'smp': 'yes',
    'touchscreen': 'yes',
    'keyboard': 'no',
    'xserver': 'yes',
    'xserver_choice': 'xserver-i915',
    'features': ['goodfeature', 'greatfeature'],
    'tunefile': 'tune-quark',
}

