#!/usr/bin/env python3
#
# Add version information to poky.yaml based upon current git branch/tags
#
# Copyright Linux Foundation
# Author: Richard Purdie <richard.purdie@linuxfoundation.org>
#
# SPDX-License-Identifier: MIT
#


import subprocess
import collections
import sys

ourversion = None
if len(sys.argv) == 2:
    ourversion = sys.argv[1]

activereleases = ["honister", "hardknott", "gatesgarth", "dunfell", "zeus", "warrior"]
#devbranch = "langdale"
devbranch = "kirkstone"
ltsseries = ["kirkstone", "dunfell"]

release_series = collections.OrderedDict()
#release_series["langdale"] = "4.1"
release_series["kirkstone"] = "4.0"
release_series["honister"] = "3.4"
release_series["hardknott"] = "3.3"
release_series["gatesgarth"] = "3.2"
release_series["dunfell"] = "3.1"

#    "langdale" : "2.2",
bitbake_mapping = {
    "kirkstone" : "2.0",
    "honister" : "1.52",
    "hardknott" : "1.50",
    "gatesgarth" : "1.48",
    "dunfell" : "1.46",
}

ourversion = None
ourseries = None
ourbranch = None
bitbakeversion = None
docconfver = None

# Test tags exist and inform the user to fetch if not
try:
    subprocess.run(["git", "show", "yocto-3.4.2"], capture_output=True, check=True)
except subprocess.CalledProcessError:
    sys.exit("Please run 'git fetch --tags' before building the documentation")

# Try and figure out what we are
tags = subprocess.run(["git", "tag", "--points-at", "HEAD"], capture_output=True, text=True).stdout
for t in tags.split():
    if t.startswith("yocto-"):
        ourversion = t[6:]

if ourversion:
    # We're a tagged release
    components = ourversion.split(".")
    baseversion = components[0] + "." + components[1]
    docconfver = ourversion
    for i in release_series:
        if release_series[i] == baseversion:
            ourseries = i
            ourbranch = i
            bitbakeversion = bitbake_mapping[i]
else:
    # We're floating on a branch
    branch = subprocess.run(["git", "branch", "--show-current"], capture_output=True, text=True).stdout.strip()
    ourbranch = branch
    if branch != "master" and branch not in release_series:
        possible_branches = []
        for b in release_series.keys():
            result = subprocess.run(["git", "show-ref", "heads/" + b], capture_output=True, text=True)
            if result.returncode == 0:
                possible_branches.append(b)
                continue
            result = subprocess.run(["git", "show-ref", "origin/" + b], capture_output=True, text=True)
            if result.returncode == 0:
                possible_branches.append("origin/" + b)
        nearestbranch = subprocess.run('git show-branch master ' + ' '.join(possible_branches) + ' | grep "*" | grep -v "$(git rev-parse --abbrev-ref HEAD)" | head -n1', shell=True, capture_output=True, text=True).stdout
        branch = nearestbranch.split('[')[1].split('~')[0]
        print("Nearest release branch esimtated to be %s" % branch)
    if branch == "master":
        ourseries = devbranch
        docconfver = "dev"
        bitbakeversion = ""
    elif branch in release_series:
        ourseries = branch
        bitbakeversion = bitbake_mapping[branch]
    else:
        sys.exit("Unknown series for branch %s" % branch)

    previoustags = subprocess.run(["git", "tag", "--merged", "HEAD"], capture_output=True, text=True).stdout
    previoustags = [t[6:] for t in previoustags.split() if t.startswith("yocto-" + release_series[ourseries])]
    futuretags = subprocess.run(["git", "tag", "--merged", ourbranch], capture_output=True, text=True).stdout
    futuretags = [t[6:] for t in futuretags.split() if t.startswith("yocto-" + release_series[ourseries])]

    # Append .999 against the last known version
    if len(previoustags) != len(futuretags):
        ourversion = previoustags[-1] + ".999"
    else:
        ourversion = release_series[ourseries] + ".999"
    if not docconfver:
        docconfver = ourversion

series = [k for k in release_series]
previousseries = series[series.index(ourseries)+1:]
lastlts = [k for k in previousseries if k in ltsseries]

print("Version calculated to be %s" % ourversion)
print("Release series calculated to be %s" % ourseries)

replacements = {
    "DISTRO" : ourversion,
    "DISTRO_NAME_NO_CAP" : ourseries,
    "DISTRO_NAME" : ourseries.capitalize(),
    "DISTRO_NAME_NO_CAP_MINUS_ONE" : previousseries[0],
    "DISTRO_NAME_NO_CAP_LTS" : lastlts[0],
    "YOCTO_DOC_VERSION" : ourversion,
    "DISTRO_REL_TAG" : "yocto-" + ourversion,
    "DOCCONF_VERSION" : docconfver,
    "BITBAKE_SERIES" : bitbakeversion,
}

with open("poky.yaml.in", "r") as r, open("poky.yaml", "w") as w:
    lines = r.readlines()
    for line in lines:
        data = line.split(":")
        k = data[0].strip()
        if k in replacements:
            w.write("%s : \"%s\"\n" % (k, replacements[k]))
        else:
            w.write(line)

print("poky.yaml generated from poky.yaml.in")

