"""
   class for handling configuration data files

   Reads a .conf file and obtains its metadata

"""

# Copyright (C) 2003, 2004  Chris Larson
# Copyright (C) 2003, 2004  Phil Blundell
#
# SPDX-License-Identifier: GPL-2.0-only
#

import errno
import re
import os
import bb.utils
from bb.parse import ParseError, resolve_file, ast, logger, handle

__config_regexp__  = re.compile( r"""
    ^
    (?P<exp>export\s+)?
    (?P<var>[a-zA-Z0-9\-_+.${}/~:]*?)
    (\[(?P<flag>[a-zA-Z0-9\-_+.][a-zA-Z0-9\-_+.@/]*)\])?

    (?P<whitespace>\s*) (
        (?P<colon>:=) |
        (?P<lazyques>\?\?=) |
        (?P<ques>\?=) |
        (?P<append>\+=) |
        (?P<prepend>=\+) |
        (?P<predot>=\.) |
        (?P<postdot>\.=) |
        =
    ) (?P<whitespace2>\s*)

    (?!'[^']*'[^']*'$)
    (?!\"[^\"]*\"[^\"]*\"$)
    (?P<apo>['\"])
    (?P<value>.*)
    (?P=apo)
    $
    """, re.X)
__include_regexp__ = re.compile( r"include\s+(.+)" )
__require_regexp__ = re.compile( r"require\s+(.+)" )
__includeall_regexp__ = re.compile( r"include_all\s+(.+)" )
__export_regexp__ = re.compile( r"export\s+([a-zA-Z0-9\-_+.${}/~]+)$" )
__unset_regexp__ = re.compile( r"unset\s+([a-zA-Z0-9\-_+.${}/~]+)$" )
__unset_flag_regexp__ = re.compile( r"unset\s+([a-zA-Z0-9\-_+.${}/~]+)\[([a-zA-Z0-9\-_+.][a-zA-Z0-9\-_+.@]+)\]$" )
__addpylib_regexp__      = re.compile(r"addpylib\s+(.+)\s+(.+)" )
__addfragments_regexp__  = re.compile(r"addfragments\s+(.+)\s+(.+)\s+(.+)\s+(.+)" )

def init(data):
    return

def supports(fn, d):
    return fn[-5:] == ".conf"

def include(parentfn, fns, lineno, data, error_out, all=False):
    """
    error_out: A string indicating the verb (e.g. "include", "inherit") to be
    used in a ParseError that will be raised if the file to be included could
    not be included. Specify False to avoid raising an error in this case.
    """
    fns = data.expand(fns)
    parentfn = data.expand(parentfn)

    # "include" or "require" accept zero to n space-separated file names to include.
    for fn in fns.split():
        if all:
            for path in data.getVar("BBPATH").split(":"):
                include_single_file(parentfn, os.path.join(path, fn), lineno, data, error_out)
        else:
            include_single_file(parentfn, fn, lineno, data, error_out)

def include_single_file(parentfn, fn, lineno, data, error_out):
    """
    Helper function for include() which does not expand or split its parameters.
    """
    if parentfn == fn: # prevent infinite recursion
        return None

    if not os.path.isabs(fn):
        dname = os.path.dirname(parentfn)
        bbpath = "%s:%s" % (dname, data.getVar("BBPATH"))
        abs_fn, attempts = bb.utils.which(bbpath, fn, history=True)
        if abs_fn and bb.parse.check_dependency(data, abs_fn):
            logger.warning("Duplicate inclusion for %s in %s" % (abs_fn, data.getVar('FILE')))
        for af in attempts:
            bb.parse.mark_dependency(data, af)
        if abs_fn:
            fn = abs_fn
    elif bb.parse.check_dependency(data, fn):
        logger.warning("Duplicate inclusion for %s in %s" % (fn, data.getVar('FILE')))

    try:
        bb.parse.handle(fn, data, True)
    except (IOError, OSError) as exc:
        if exc.errno == errno.ENOENT:
            if error_out:
                raise ParseError("Could not %s file %s" % (error_out, fn), parentfn, lineno)
            logger.debug2("CONF file '%s' not found", fn)
        else:
            if error_out:
                raise ParseError("Could not %s file %s: %s" % (error_out, fn, exc.strerror), parentfn, lineno)
            else:
                raise ParseError("Error parsing %s: %s" % (fn, exc.strerror), parentfn, lineno)

# We have an issue where a UI might want to enforce particular settings such as
# an empty DISTRO variable. If configuration files do something like assigning
# a weak default, it turns out to be very difficult to filter out these changes,
# particularly when the weak default might appear half way though parsing a chain
# of configuration files. We therefore let the UIs hook into configuration file
# parsing. This turns out to be a hard problem to solve any other way.
confFilters = []

def handle(fn, data, include, baseconfig=False):
    init(data)

    if include == 0:
        oldfile = None
    else:
        oldfile = data.getVar('FILE', False)

    abs_fn = resolve_file(fn, data)
    with open(abs_fn, 'r') as f:

        statements = ast.StatementGroup()
        lineno = 0
        while True:
            lineno = lineno + 1
            s = f.readline()
            if not s:
                break
            origlineno = lineno
            origline = s
            w = s.strip()
            # skip empty lines
            if not w:
                continue
            s = s.rstrip()
            while s[-1] == '\\':
                line = f.readline()
                origline += line
                s2 = line.rstrip()
                lineno = lineno + 1
                if (not s2 or s2 and s2[0] != "#") and s[0] == "#" :
                    bb.fatal("There is a confusing multiline, partially commented expression starting on line %s of file %s:\n%s\nPlease clarify whether this is all a comment or should be parsed." % (origlineno, fn, origline))

                s = s[:-1] + s2
            # skip comments
            if s[0] == '#':
                continue
            feeder(lineno, s, abs_fn, statements, baseconfig=baseconfig)

    # DONE WITH PARSING... time to evaluate
    data.setVar('FILE', abs_fn)
    statements.eval(data)
    if oldfile:
        data.setVar('FILE', oldfile)

    for f in confFilters:
        f(fn, data)

    return data

# baseconfig is set for the bblayers/layer.conf cookerdata config parsing
# The function is also used by BBHandler, conffile would be False
def feeder(lineno, s, fn, statements, baseconfig=False, conffile=True):
    m = __config_regexp__.match(s)
    if m:
        groupd = m.groupdict()
        if groupd['var'] == "":
            raise ParseError("Empty variable name in assignment: '%s'" % s, fn, lineno);
        if not groupd['whitespace'] or not groupd['whitespace2']:
            logger.warning("%s:%s has a lack of whitespace around the assignment: '%s'" % (fn, lineno, s))
        ast.handleData(statements, fn, lineno, groupd)
        return

    m = __include_regexp__.match(s)
    if m:
        ast.handleInclude(statements, fn, lineno, m, False)
        return

    m = __require_regexp__.match(s)
    if m:
        ast.handleInclude(statements, fn, lineno, m, True)
        return

    m = __includeall_regexp__.match(s)
    if m:
        ast.handleIncludeAll(statements, fn, lineno, m)
        return

    m = __export_regexp__.match(s)
    if m:
        ast.handleExport(statements, fn, lineno, m)
        return

    m = __unset_regexp__.match(s)
    if m:
        ast.handleUnset(statements, fn, lineno, m)
        return

    m = __unset_flag_regexp__.match(s)
    if m:
        ast.handleUnsetFlag(statements, fn, lineno, m)
        return

    m = __addpylib_regexp__.match(s)
    if baseconfig and conffile and m:
        ast.handlePyLib(statements, fn, lineno, m)
        return

    m = __addfragments_regexp__.match(s)
    if m:
        ast.handleAddFragments(statements, fn, lineno, m)
        return

    raise ParseError("unparsed line: '%s'" % s, fn, lineno);

# Add us to the handlers list
from bb.parse import handlers
handlers.append({'supports': supports, 'handle': handle, 'init': init})
del handlers
