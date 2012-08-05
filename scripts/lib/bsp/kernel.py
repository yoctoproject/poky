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
# This module implements the kernel-related functions used by
# 'yocto-kernel' to manage kernel config items and patches for Yocto
# BSPs.
#
# AUTHORS
# Tom Zanussi <tom.zanussi (at] intel.com>
#

import sys
import os
import shutil
from tags import *
import glob


def find_bblayers(scripts_path):
    """
    Find and return a sanitized list of the layers found in BBLAYERS.
    """
    try:
        builddir = os.environ["BUILDDIR"]
    except KeyError:
        print "BUILDDIR not found, exiting. (Did you forget to source oe-init-build-env?)"
        sys.exit(1)
    bblayers_conf = os.path.join(builddir, "conf/bblayers.conf")

    layers = []

    f = open(bblayers_conf, "r")
    lines = f.readlines()
    bblayers_lines = []
    in_bblayers = False
    for line in lines:
        line = line.strip()
        if line.strip().startswith("BBLAYERS"):
            bblayers_lines.append(line)
            in_bblayers = True
            quotes = line.strip().count('"')
            if quotes > 1:
                break
            continue
        if in_bblayers:
            bblayers_lines.append(line)
            if line.strip().endswith("\""):
                break
            else:
                continue

    for i, line in enumerate(bblayers_lines):
        if line.strip().endswith("\\"):
            bblayers_lines[i] = line.strip().replace('\\', '')

    bblayers_line = " ".join(bblayers_lines)

    start_quote = bblayers_line.find("\"")
    if start_quote == -1:
        print "Invalid BBLAYERS found in %s, exiting" % bblayers_conf
        sys.exit(1)

    start_quote += 1
    end_quote = bblayers_line.find("\"", start_quote)
    if end_quote == -1:
        print "Invalid BBLAYERS found in %s, exiting" % bblayers_conf
        sys.exit(1)

    bblayers_line = bblayers_line[start_quote:end_quote]
    layers = bblayers_line.split()

    f.close()

    return layers


def find_meta_layer(scripts_path):
    """
    Find and return the meta layer in BBLAYERS.
    """
    layers = find_bblayers(scripts_path)

    for layer in layers:
        if layer.endswith("meta"):
            return layer

    return None


def find_bsp_layer(scripts_path, machine):
    """
    Find and return a machine's BSP layer in BBLAYERS.
    """
    layers = find_bblayers(scripts_path)

    for layer in layers:
        if machine in layer:
            return layer

    print "Unable to find the BSP layer for machine %s." % machine
    print "Please make sure it is listed in bblayers.conf"
    sys.exit(1)


def gen_choices_str(choices):
    """
    Generate a numbered list of choices from a list of choices for
    display to the user.
    """
    choices_str = ""

    for i, choice in enumerate(choices):
        choices_str += "\t" + str(i + 1) + ") " + choice + "\n"

    return choices_str


def read_config_items(scripts_path, machine):
    """
    Find and return a list of config items (CONFIG_XXX) in a machine's
    user-defined config fragment [user-config.cfg].
    """
    config_items = []

    layer = find_bsp_layer(scripts_path, machine)
    cfg = os.path.join(layer, "recipes-kernel/linux/files/user-config.cfg")

    f = open(cfg, "r")
    lines = f.readlines()
    for line in lines:
        s = line.strip()
        if s:
            config_items.append(s)
    f.close()

    return config_items


def write_config_items(scripts_path, machine, config_items):
    """
    Write (replace) the list of config items (CONFIG_XXX) in a
    machine's user-defined config fragment [user-config.cfg].
    """
    layer = find_bsp_layer(scripts_path, machine)
    cfg = os.path.join(layer, "recipes-kernel/linux/files/user-config.cfg")

    f = open(cfg, "w")
    for item in config_items:
        f.write(item + "\n")
    f.close()

    kernel_contents_changed(scripts_path, machine)


def yocto_kernel_config_list(scripts_path, machine):
    """
    Display the list of config items (CONFIG_XXX) in a machine's
    user-defined config fragment [user-config.cfg].
    """
    config_items = read_config_items(scripts_path, machine)

    print "The current set of machine-specific kernel config items for %s is:" % machine
    print gen_choices_str(config_items)


def map_choice(choice_str, array):
    """
    Match the text of a choice with a list of choices, returning the
    index of the match, or -1 if not found.
    """
    for i, item in enumerate(array):
        if choice_str == array[i]:
            return i

    return -1


def yocto_kernel_config_rm(scripts_path, machine):
    """
    Display the list of config items (CONFIG_XXX) in a machine's
    user-defined config fragment [user-config.cfg], prompt the user
    for one or more to remove, and remove them.
    """
    config_items = read_config_items(scripts_path, machine)

    print "Specify the kernel config items to remove:"
    input = raw_input(gen_choices_str(config_items))
    rm_choices = input.split()
    rm_choices.sort()

    removed = []

    for choice in reversed(rm_choices):
        try:
            idx = int(choice) - 1
        except ValueError:
            print "Invalid choice (%s), exiting" % choice
            sys.exit(1)
        if idx < 0 or idx >= len(config_items):
            print "Invalid choice (%d), exiting" % (idx + 1)
            sys.exit(1)
        removed.append(config_items.pop(idx))

    write_config_items(scripts_path, machine, config_items)

    print "Removed items:"
    for r in removed:
        print "\t%s" % r


def yocto_kernel_config_add(scripts_path, machine, config_items):
    """
    Add one or more config items (CONFIG_XXX) to a machine's
    user-defined config fragment [user-config.cfg].
    """
    new_items = []

    for item in config_items:
        if not item.startswith("CONFIG") or (not "=y" in item and not "=m" in item):
            print "Invalid config item (%s), exiting" % item
            sys.exit(1)
        new_items.append(item)

    cur_items = read_config_items(scripts_path, machine)
    cur_items.extend(new_items)

    write_config_items(scripts_path, machine, cur_items)

    print "Added items:"
    for n in new_items:
        print "\t%s" % n


def find_current_kernel(bsp_layer, machine):
    """
    Determine the kernel and version currently being used in the BSP.
    """
    machine_conf = os.path.join(bsp_layer, "conf/machine/" + machine + ".conf")

    preferred_kernel = preferred_kernel_version = preferred_version_varname = None

    f = open(machine_conf, "r")
    lines = f.readlines()
    for line in lines:
        if line.strip().startswith("PREFERRED_PROVIDER_virtual/kernel"):
            preferred_kernel = line.split()[-1]
            preferred_kernel = preferred_kernel.replace('\"','')
            preferred_version_varname = "PREFERRED_VERSION_" + preferred_kernel
        if preferred_version_varname and line.strip().startswith(preferred_version_varname):
            preferred_kernel_version = line.split()[-1]
            preferred_kernel_version = preferred_kernel_version.replace('\"','')
            preferred_kernel_version = preferred_kernel_version.replace('%','')

    if preferred_kernel and preferred_kernel_version:
        return preferred_kernel + "_" + preferred_kernel_version


def find_bsp_kernel_src_uri(scripts_path, machine, start_end_only = False):
    """
    Parse the SRC_URI append in the kernel .bbappend, returing a list
    of individual components, and the start/end positions of the
    SRC_URI statement, so it can be regenerated in the same position.
    If start_end_only is True, don't return the list of elements, only
    the start and end positions.

    Returns (SRC_URI start line, SRC_URI end_line, list of split
    SRC_URI items).

    If no SRC_URI, start line = -1.

    NOTE: this and all the src_uri functions are temporary and
    deprecated and will be removed, but are needed until the
    equivalent .scc mechanism works.  i.e. for now we unfortunately
    can't get around putting patches in the SRC_URI.
    """
    layer = find_bsp_layer(scripts_path, machine)

    kernel = find_current_kernel(layer, machine)
    if not kernel:
        print "Couldn't determine the kernel for this BSP, exiting."
        sys.exit(1)

    kernel_bbappend = os.path.join(layer, "recipes-kernel/linux/" + kernel + ".bbappend")

    f = open(kernel_bbappend, "r")
    src_uri_line = ""
    in_src_uri = False
    lines = f.readlines()
    first_line = last_line = -1
    quote_start = quote_end = -1
    for n, line in enumerate(lines):
        line = line.strip()
        if line.startswith("SRC_URI"):
            first_line = n
            in_src_uri = True
        if in_src_uri:
            src_uri_line += line
            if quote_start == -1:
                idx = line.find("\"")
                if idx != -1:
                    quote_start = idx + 1
            idx = line.find("\"", quote_start)
            quote_start = 0 # set to 0 for all but first line
            if idx != -1:
                quote_end = idx
                last_line = n
                break

    if first_line == -1: # no SRC_URI, which is fine too
        return (-1, -1, None)
    if quote_start == -1:
        print "Bad kernel SRC_URI (missing opening quote), exiting."
        sys.exit(1)
    if quote_end == -1:
        print "Bad SRC_URI (missing closing quote), exiting."
        sys.exit(1)
    if start_end_only:
        return (first_line, last_line, None)

    idx = src_uri_line.find("\"")
    src_uri_line = src_uri_line[idx + 1:]
    idx = src_uri_line.find("\"")
    src_uri_line = src_uri_line[:idx]

    src_uri = src_uri_line.split()
    for i, item in enumerate(src_uri):
        idx = item.find("\\")
        if idx != -1:
            src_uri[i] = item[idx + 1:]

    if not src_uri[len(src_uri) - 1]:
        src_uri.pop()

    for i, item in enumerate(src_uri):
        idx = item.find(SRC_URI_FILE)
        if idx == -1:
            print "Bad SRC_URI (invalid item, %s), exiting." % item
            sys.exit(1)
        src_uri[i] = item[idx + len(SRC_URI_FILE):]

    return (first_line, last_line, src_uri)     


def find_patches(src_uri):
    """
    Filter out the top-level patches from the SRC_URI.
    """
    patches = []
    for item in src_uri:
        if item.endswith(".patch") and "/" not in item:
            patches.append(item)
    return patches


def read_patch_items(scripts_path, machine):
    """
    Find and return a list of patch items in a machine's user-defined
    patch list [user-patches.scc].
    """
    patch_items = []

    layer = find_bsp_layer(scripts_path, machine)
    patches = os.path.join(layer, "recipes-kernel/linux/files/user-patches.scc")

    f = open(patches, "r")
    lines = f.readlines()
    for line in lines:
        s = line.strip()
        if s:
            fields = s.split()
            if not fields[0] == "patch":
                continue
            patch_items.append(fields[1])
    f.close()

    return patch_items


def write_patch_items(scripts_path, machine, patch_items):
    """
    Write (replace) the list of patches in a machine's user-defined
    patch list [user-patches.scc].
    """
    layer = find_bsp_layer(scripts_path, machine)

    patches = os.path.join(layer, "recipes-kernel/linux/files/user-patches.scc")

    f = open(patches, "w")
    for item in patch_items:
        pass
        # this currently breaks do_patch, but is really what we want
        # once this works, we can remove all the src_uri stuff
        # f.write("patch " + item + "\n")
    f.close()

    kernel_contents_changed(scripts_path, machine)


def yocto_kernel_patch_list(scripts_path, machine):
    """
    Display the list of patches in a machine's user-defined patch list
    [user-patches.scc].
    """
    (start_line, end_line, src_uri) = find_bsp_kernel_src_uri(scripts_path, machine)
    patches = find_patches(src_uri)

    print "The current set of machine-specific patches for %s is:" % machine
    print gen_choices_str(patches)


def yocto_kernel_patch_rm(scripts_path, machine):
    """
    Remove one or more patches from a machine's user-defined patch
    list [user-patches.scc].
    """
    (start_line, end_line, src_uri) = find_bsp_kernel_src_uri(scripts_path, machine)
    patches = find_patches(src_uri)

    print "Specify the patches to remove:"
    input = raw_input(gen_choices_str(patches))
    rm_choices = input.split()
    rm_choices.sort()

    removed = []

    layer = find_bsp_layer(scripts_path, machine)
    src_uri_dir = os.path.join(layer, "recipes-kernel/linux/files")

    for choice in reversed(rm_choices):
        try:
            idx = int(choice) - 1
        except ValueError:
            print "Invalid choice (%s), exiting" % choice
            sys.exit(1)
        if idx < 0 or idx >= len(patches):
            print "Invalid choice (%d), exiting" % (idx + 1)
            sys.exit(1)
        src_uri_patch = os.path.join(src_uri_dir, patches[idx])
        if os.path.isfile(src_uri_patch):
            os.remove(src_uri_patch)
        idx = map_choice(patches[idx], src_uri)
        removed.append(src_uri.pop(idx))

    write_patch_items(scripts_path, machine, patches)
    write_kernel_src_uri(scripts_path, machine, src_uri)

    print "Removed patches:"
    for r in removed:
        print "\t%s" % r


def yocto_kernel_patch_add(scripts_path, machine, patches):
    """
    Add one or more patches to a machine's user-defined patch list
    [user-patches.scc].
    """
    (start_line, end_line, src_uri) = find_bsp_kernel_src_uri(scripts_path, machine)
    src_uri_patches = find_patches(src_uri)

    for patch in patches:
        if os.path.basename(patch) in src_uri_patches:
            print "Couldn't add patch (%s) since it's already been added" % os.path.basename(patch)
            sys.exit(1)

    layer = find_bsp_layer(scripts_path, machine)
    src_uri_dir = os.path.join(layer, "recipes-kernel/linux/files")

    new_patches = []

    for patch in patches:
        if not os.path.isfile(patch):
            print "Couldn't find patch (%s), exiting" % patch
            sys.exit(1)
        basename = os.path.basename(patch)
        src_uri_patch = os.path.join(src_uri_dir, basename)
        shutil.copyfile(patch, src_uri_patch)
        new_patches.append(basename)

    cur_items = read_patch_items(scripts_path, machine)
    cur_items.extend(new_patches)
    write_patch_items(scripts_path, machine, cur_items)

    (unused, unused, src_uri) = find_bsp_kernel_src_uri(scripts_path, machine)
    src_uri.extend(new_patches)
    write_kernel_src_uri(scripts_path, machine, src_uri)

    print "Added patches:"
    for n in new_patches:
        print "\t%s" % n


def write_uri_lines(ofile, src_uri):
    """
    Write URI elements to output file ofile.
    """
    ofile.write("SRC_URI += \" \\\n")
    for item in src_uri:
        ofile.write("\t%s%s \\\n" % (SRC_URI_FILE, item))
    ofile.write("\t\"\n")


def inc_pr(line):
    """
    Add 1 to the PR value in the given bbappend PR line.  For the PR
    lines in kernel .bbappends after modifications.
    """
    idx = line.find("\"")

    pr_str = line[idx:]
    pr_str = pr_str.replace('\"','')
    fields = pr_str.split('.')
    fields[1] = str(int(fields[1]) + 1)
    pr_str = "\"" + '.'.join(fields) + "\"\n"

    idx2 = line.find("\"", idx + 1)
    line = line[:idx] + pr_str
    
    return line


def kernel_contents_changed(scripts_path, machine):
    """
    Do what we need to do to notify the system that the kernel
    recipe's contents have changed.
    """
    layer = find_bsp_layer(scripts_path, machine)

    kernel = find_current_kernel(layer, machine)
    if not kernel:
        print "Couldn't determine the kernel for this BSP, exiting."
        sys.exit(1)

    kernel_bbappend = os.path.join(layer, "recipes-kernel/linux/" + kernel + ".bbappend")
    kernel_bbappend_prev = kernel_bbappend + ".prev"
    shutil.copyfile(kernel_bbappend, kernel_bbappend_prev)

    ifile = open(kernel_bbappend_prev, "r")
    ofile = open(kernel_bbappend, "w")
    ifile_lines = ifile.readlines()
    for ifile_line in ifile_lines:
        if ifile_line.strip().startswith("PR"):
            ifile_line = inc_pr(ifile_line)
        ofile.write(ifile_line)
    ofile.close()
    ifile.close()


def write_kernel_src_uri(scripts_path, machine, src_uri):
    """
    Write (replace) the SRC_URI append for a machine from a list
    SRC_URI elements.
    """
    layer = find_bsp_layer(scripts_path, machine)

    kernel = find_current_kernel(layer, machine)
    if not kernel:
        print "Couldn't determine the kernel for this BSP, exiting."
        sys.exit(1)

    kernel_bbappend = os.path.join(layer, "recipes-kernel/linux/" + kernel + ".bbappend")

    (uri_start_line, uri_end_line, unused) = find_bsp_kernel_src_uri(scripts_path, machine, True)

    kernel_bbappend_prev = kernel_bbappend + ".prev"
    shutil.copyfile(kernel_bbappend, kernel_bbappend_prev)
    ifile = open(kernel_bbappend_prev, "r")
    ofile = open(kernel_bbappend, "w")

    ifile_lines = ifile.readlines()
    if uri_start_line == -1:
        uri_end_line = len(ifile_lines) # make sure we add at end
    wrote_src_uri = False
    for i, ifile_line in enumerate(ifile_lines):
        if ifile_line.strip().startswith("PR"):
            ifile_line = inc_pr(ifile_line)
        if i < uri_start_line:
            ofile.write(ifile_line)
        elif i > uri_end_line:
            ofile.write(ifile_line)
        else:
            if not wrote_src_uri:
                write_uri_lines(ofile, src_uri)
                wrote_src_uri = True
    if uri_start_line == -1:
        write_uri_lines(ofile, src_uri)


def kernels(context):
    """
    Return the list of available kernels in the BSP i.e. corresponding
    to the kernel .bbappends found in the layer.
    """
    archdir = os.path.join(context["scripts_path"], "lib/bsp/substrate/target/arch/" + context["arch"])
    kerndir = os.path.join(archdir, "recipes-kernel/linux")
    bbglob = os.path.join(kerndir, "*.bbappend")

    bbappends = glob.glob(bbglob)

    kernels = []

    for kernel in bbappends:
        filename = os.path.splitext(os.path.basename(kernel))[0]
        idx = filename.find(CLOSE_TAG)
        if idx != -1:
            filename = filename[idx + len(CLOSE_TAG):].strip()
        kernels.append(filename)

    return kernels


def extract_giturl(file):
    """
    Extract the git url of the kernel repo from the kernel recipe's
    SRC_URI.
    """
    f = open(file, "r")
    lines = f.readlines()
    for line in lines:
        line = line.strip()
        if line.startswith("SRC_URI"):
            line = line[len("SRC_URI"):].strip()
            if line.startswith("="):
                line = line[1:].strip()
                if line.startswith("\""):
                    line = line[1:].strip()
                    fields = line.split(";")
                    if fields:
                        return fields[0]
    return None


def find_giturl(context):
    """
    Find the git url of the kernel repo from the kernel recipe's
    SRC_URI.
    """
    name = context["name"]
    filebase = context["filename"]
    scripts_path = context["scripts_path"]

    meta_layer = find_meta_layer(scripts_path)

    kerndir = os.path.join(meta_layer, "recipes-kernel/linux")
    bbglob = os.path.join(kerndir, "*.bb")
    bbs = glob.glob(bbglob)
    for kernel in bbs:
        filename = os.path.splitext(os.path.basename(kernel))[0]
        if filename in filebase:
            giturl = extract_giturl(kernel)
            return giturl
    
    return None

    
def base_branches(context):
    """
    Return a list of the base branches found in the kernel git repo.
    """
    giturl = find_giturl(context)

    print "Getting branches from remote repo %s..." % giturl

    gitcmd = "git ls-remote %s *heads* 2>&1" % (giturl)
    tmp = os.popen(gitcmd).read()

    branches = []

    if tmp:
        tmpline = tmp.split("\n")
        for line in tmpline:
            if len(line)==0:
                break;
            if not line.endswith("base"):
                continue;
            idx = line.find("refs/heads/")
            kbranch = line[idx + len("refs/heads/"):]
            if kbranch.find("/") == -1 and kbranch.find("base") == -1:
                continue
            idx = kbranch.find("base")
            branches.append(kbranch[:idx - 1])

    return branches


def all_branches(context):
    """
    Return a list of all the branches found in the kernel git repo.
    """
    giturl = find_giturl(context)

    print "Getting branches from remote repo %s..." % giturl

    gitcmd = "git ls-remote %s *heads* 2>&1" % (giturl)
    tmp = os.popen(gitcmd).read()

    branches = []
    base_prefixes = None

    try:
        branches_base = context["branches_base"]
        if branches_base:
            base_prefixes = branches_base.split(":")
    except KeyError:
        pass

    arch = context["arch"]

    if tmp:
        tmpline = tmp.split("\n")
        for line in tmpline:
            if len(line)==0:
                break;
            idx = line.find("refs/heads/")
            kbranch = line[idx + len("refs/heads/"):]
            kbranch_prefix = kbranch.rsplit("/", 1)[0]

            if base_prefixes:
                for base_prefix in base_prefixes:
                    if kbranch_prefix == base_prefix:
                        branches.append(kbranch)
                continue

            if (kbranch.find("/") != -1 and
                (kbranch.find("standard") != -1 or kbranch.find("base") != -1) or
                kbranch == "base"):
                branches.append(kbranch)
                continue

    return branches
