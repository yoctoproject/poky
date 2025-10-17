"""
 AbstractSyntaxTree classes for the Bitbake language
"""

# Copyright (C) 2003, 2004 Chris Larson
# Copyright (C) 2003, 2004 Phil Blundell
# Copyright (C) 2009 Holger Hans Peter Freyther
#
# SPDX-License-Identifier: GPL-2.0-only
#

import sys
import bb
from bb import methodpool
from bb.parse import logger

class StatementGroup(list):
    def eval(self, data):
        for statement in self:
            statement.eval(data)

class AstNode(object):
    def __init__(self, filename, lineno):
        self.filename = filename
        self.lineno = lineno

class IncludeNode(AstNode):
    def __init__(self, filename, lineno, what_file, force):
        AstNode.__init__(self, filename, lineno)
        self.what_file = what_file
        self.force = force

    def eval(self, data):
        """
        Include the file and evaluate the statements
        """
        s = data.expand(self.what_file)
        logger.debug2("CONF %s:%s: including %s", self.filename, self.lineno, s)

        # TODO: Cache those includes... maybe not here though
        if self.force:
            bb.parse.ConfHandler.include(self.filename, s, self.lineno, data, "include required")
        else:
            bb.parse.ConfHandler.include(self.filename, s, self.lineno, data, False)

class IncludeAllNode(AstNode):
    def __init__(self, filename, lineno, what_file):
        AstNode.__init__(self, filename, lineno)
        self.what_file = what_file

    def eval(self, data):
        """
        Include the file and evaluate the statements
        """
        s = data.expand(self.what_file)
        logger.debug2("CONF %s:%s: including all %s", self.filename, self.lineno, s)

        bb.parse.ConfHandler.include(self.filename, s, self.lineno, data, False, all=True)

class ExportNode(AstNode):
    def __init__(self, filename, lineno, var):
        AstNode.__init__(self, filename, lineno)
        self.var = var

    def eval(self, data):
        data.setVarFlag(self.var, "export", 1, op = 'exported')

class UnsetNode(AstNode):
    def __init__(self, filename, lineno, var):
        AstNode.__init__(self, filename, lineno)
        self.var = var

    def eval(self, data):
        loginfo = {
            'variable': self.var,
            'file': self.filename,
            'line': self.lineno,
        }
        data.delVar(self.var,**loginfo)

class UnsetFlagNode(AstNode):
    def __init__(self, filename, lineno, var, flag):
        AstNode.__init__(self, filename, lineno)
        self.var = var
        self.flag = flag

    def eval(self, data):
        loginfo = {
            'variable': self.var,
            'file': self.filename,
            'line': self.lineno,
        }
        data.delVarFlag(self.var, self.flag, **loginfo)

class DataNode(AstNode):
    """
    Various data related updates. For the sake of sanity
    we have one class doing all this. This means that all
    this need to be re-evaluated... we might be able to do
    that faster with multiple classes.
    """
    def __init__(self, filename, lineno, groupd):
        AstNode.__init__(self, filename, lineno)
        self.groupd = groupd

    def getFunc(self, key, data):
        if 'flag' in self.groupd and self.groupd['flag'] is not None:
            return data.getVarFlag(key, self.groupd['flag'], expand=False, noweakdefault=True)
        else:
            return data.getVar(key, False, noweakdefault=True, parsing=True)

    def eval(self, data):
        groupd = self.groupd
        key = groupd["var"]
        loginfo = {
            'variable': key,
            'file': self.filename,
            'line': self.lineno,
        }
        if "exp" in groupd and groupd["exp"] is not None:
            data.setVarFlag(key, "export", 1, op = 'exported', **loginfo)

        op = "set"
        if "ques" in groupd and groupd["ques"] is not None:
            val = self.getFunc(key, data)
            op = "set?"
            if val is None:
                val = groupd["value"]
        elif "colon" in groupd and groupd["colon"] is not None:
            e = data.createCopy()
            op = "immediate"
            val = e.expand(groupd["value"], key + "[:=]")
        elif "append" in groupd and groupd["append"] is not None:
            op = "append"
            val = "%s %s" % ((self.getFunc(key, data) or ""), groupd["value"])
        elif "prepend" in groupd and groupd["prepend"] is not None:
            op = "prepend"
            val = "%s %s" % (groupd["value"], (self.getFunc(key, data) or ""))
        elif "postdot" in groupd and groupd["postdot"] is not None:
            op = "postdot"
            val = "%s%s" % ((self.getFunc(key, data) or ""), groupd["value"])
        elif "predot" in groupd and groupd["predot"] is not None:
            op = "predot"
            val = "%s%s" % (groupd["value"], (self.getFunc(key, data) or ""))
        else:
            val = groupd["value"]

        if ":append" in key or ":remove" in key or ":prepend" in key:
            if op in ["append", "prepend", "postdot", "predot", "ques"]:
                bb.warn(key + " " + groupd[op] + " is not a recommended operator combination, please replace it.")

        flag = None
        if 'flag' in groupd and groupd['flag'] is not None:
            if groupd["lazyques"]:
                flag = "_defaultval_flag_"+groupd['flag']
            else:
                flag = groupd['flag']
        elif groupd["lazyques"]:
            flag = "_defaultval"

        loginfo['op'] = op
        loginfo['detail'] = groupd["value"]

        if flag:
            data.setVarFlag(key, flag, val, **loginfo)
        else:
            data.setVar(key, val, parsing=True, **loginfo)

class MethodNode(AstNode):
    tr_tbl = str.maketrans('/.+-@%&~', '________')

    def __init__(self, filename, lineno, func_name, body, python, fakeroot):
        AstNode.__init__(self, filename, lineno)
        self.func_name = func_name
        self.body = body
        self.python = python
        self.fakeroot = fakeroot

    def eval(self, data):
        text = '\n'.join(self.body)
        funcname = self.func_name
        if self.func_name == "__anonymous":
            funcname = ("__anon_%s_%s" % (self.lineno, self.filename.translate(MethodNode.tr_tbl)))
            self.python = True
            text = "def %s(d):\n" % (funcname) + text
            bb.methodpool.insert_method(funcname, text, self.filename, self.lineno - len(self.body) - 1)
            anonfuncs = data.getVar('__BBANONFUNCS', False) or []
            anonfuncs.append(funcname)
            data.setVar('__BBANONFUNCS', anonfuncs)
        if data.getVar(funcname, False):
            # clean up old version of this piece of metadata, as its
            # flags could cause problems
            data.delVarFlag(funcname, 'python')
            data.delVarFlag(funcname, 'fakeroot')
        if self.python:
            data.setVarFlag(funcname, "python", "1")
        if self.fakeroot:
            data.setVarFlag(funcname, "fakeroot", "1")
        data.setVarFlag(funcname, "func", 1)
        data.setVar(funcname, text, parsing=True)
        data.setVarFlag(funcname, 'filename', self.filename)
        data.setVarFlag(funcname, 'lineno', str(self.lineno - len(self.body)))

class PythonMethodNode(AstNode):
    def __init__(self, filename, lineno, function, modulename, body):
        AstNode.__init__(self, filename, lineno)
        self.function = function
        self.modulename = modulename
        self.body = body

    def eval(self, data):
        # Note we will add root to parsedmethods after having parse
        # 'this' file. This means we will not parse methods from
        # bb classes twice
        text = '\n'.join(self.body)
        bb.methodpool.insert_method(self.modulename, text, self.filename, self.lineno - len(self.body) - 1)
        data.setVarFlag(self.function, "func", 1)
        data.setVarFlag(self.function, "python", 1)
        data.setVar(self.function, text, parsing=True)
        data.setVarFlag(self.function, 'filename', self.filename)
        data.setVarFlag(self.function, 'lineno', str(self.lineno - len(self.body) - 1))

class ExportFuncsNode(AstNode):
    def __init__(self, filename, lineno, fns, classname):
        AstNode.__init__(self, filename, lineno)
        self.n = fns.split()
        self.classname = classname

    def eval(self, data):

        sentinel = "    # Export function set\n"
        for func in self.n:
            calledfunc = self.classname + "_" + func

            basevar = data.getVar(func, False)
            if basevar and sentinel not in basevar:
                continue

            if data.getVar(func, False):
                data.setVarFlag(func, 'python', None)
                data.setVarFlag(func, 'func', None)

            for flag in [ "func", "python" ]:
                if data.getVarFlag(calledfunc, flag, False):
                    data.setVarFlag(func, flag, data.getVarFlag(calledfunc, flag, False))
            for flag in ["dirs", "cleandirs", "fakeroot"]:
                if data.getVarFlag(func, flag, False):
                    data.setVarFlag(calledfunc, flag, data.getVarFlag(func, flag, False))
            data.setVarFlag(func, "filename", "autogenerated")
            data.setVarFlag(func, "lineno", 1)

            if data.getVarFlag(calledfunc, "python", False):
                data.setVar(func, sentinel + "    bb.build.exec_func('" + calledfunc + "', d)\n", parsing=True)
            else:
                if "-" in self.classname:
                   bb.fatal("The classname %s contains a dash character and is calling an sh function %s using EXPORT_FUNCTIONS. Since a dash is illegal in sh function names, this cannot work, please rename the class or don't use EXPORT_FUNCTIONS." % (self.classname, calledfunc))
                data.setVar(func, sentinel + "    " + calledfunc + "\n", parsing=True)

class AddTaskNode(AstNode):
    def __init__(self, filename, lineno, tasks, before, after):
        AstNode.__init__(self, filename, lineno)
        self.tasks = tasks
        self.before = before
        self.after = after

    def eval(self, data):
        tasks = self.tasks.split()
        for task in tasks:
            bb.build.addtask(task, self.before, self.after, data)

class DelTaskNode(AstNode):
    def __init__(self, filename, lineno, tasks):
        AstNode.__init__(self, filename, lineno)
        self.tasks = tasks

    def eval(self, data):
        tasks = data.expand(self.tasks).split()
        for task in tasks:
            bb.build.deltask(task, data)

class BBHandlerNode(AstNode):
    def __init__(self, filename, lineno, fns):
        AstNode.__init__(self, filename, lineno)
        self.hs = fns.split()

    def eval(self, data):
        bbhands = data.getVar('__BBHANDLERS', False) or []
        for h in self.hs:
            bbhands.append(h)
            data.setVarFlag(h, "handler", 1)
        data.setVar('__BBHANDLERS', bbhands)

class PyLibNode(AstNode):
    def __init__(self, filename, lineno, libdir, namespace):
        AstNode.__init__(self, filename, lineno)
        self.libdir = libdir
        self.namespace = namespace

    def eval(self, data):
        global_mods = (data.getVar("BB_GLOBAL_PYMODULES") or "").split()
        for m in global_mods:
            if m not in bb.utils._context:
                bb.utils._context[m] = __import__(m)

        libdir = data.expand(self.libdir)
        if libdir not in sys.path:
            sys.path.append(libdir)
        try:
            bb.utils._context[self.namespace] = __import__(self.namespace)
            toimport = getattr(bb.utils._context[self.namespace], "BBIMPORTS", [])
            for i in toimport:
                bb.utils._context[self.namespace] = __import__(self.namespace + "." + i)
                mod = getattr(bb.utils._context[self.namespace], i)
                fn = getattr(mod, "__file__")
                funcs = {}
                for f in dir(mod):
                    if f.startswith("_"):
                        continue
                    fcall = getattr(mod, f)
                    if not callable(fcall):
                        continue
                    funcs[f] = fcall
                bb.codeparser.add_module_functions(fn, funcs, "%s.%s" % (self.namespace, i))

        except AttributeError as e:
            bb.error("Error importing OE modules: %s" % str(e))

class InheritNode(AstNode):
    def __init__(self, filename, lineno, classes):
        AstNode.__init__(self, filename, lineno)
        self.classes = classes

    def eval(self, data):
        bb.parse.BBHandler.inherit(self.classes, self.filename, self.lineno, data)

class InheritDeferredNode(AstNode):
    def __init__(self, filename, lineno, classes):
        AstNode.__init__(self, filename, lineno)
        self.inherit = (classes, filename, lineno)

    def eval(self, data):
        bb.parse.BBHandler.inherit_defer(*self.inherit, data)

class AddFragmentsNode(AstNode):
    def __init__(self, filename, lineno, fragments_path_prefix, fragments_variable, flagged_variables_list_variable, builtin_fragments_variable):
        AstNode.__init__(self, filename, lineno)
        self.fragments_path_prefix = fragments_path_prefix
        self.fragments_variable = fragments_variable
        self.flagged_variables_list_variable = flagged_variables_list_variable
        self.builtin_fragments_variable = builtin_fragments_variable

    def eval(self, data):
        # No need to use mark_dependency since we would only match a fragment
        # from a specific layer and there can only be a single layer with a
        # given namespace.
        def find_fragment(layers, layerid, full_fragment_name):
           for layerpath in layers.split():
               candidate_fragment_path = os.path.join(layerpath, full_fragment_name)
               if os.path.exists(candidate_fragment_path) and bb.utils.get_file_layer(candidate_fragment_path, data) == layerid:
                   return candidate_fragment_path
           return None

        def check_and_set_builtin_fragment(fragment, data, builtin_fragments):
            prefix, value = fragment.split('/', 1)
            if prefix in builtin_fragments.keys():
                # parsing=True since we want to emulate X=Y and allow X:override=Z to continue to exist
                data.setVar(builtin_fragments[prefix], value, parsing=True)
                return True
            return False

        fragments = data.getVar(self.fragments_variable)
        layers = data.getVar('BBLAYERS')
        flagged_variables = data.getVar(self.flagged_variables_list_variable).split()
        builtin_fragments = {f[0]:f[1] for f in [f.split(':') for f in data.getVar(self.builtin_fragments_variable).split()] }

        if not fragments:
            return

        # Check for multiple builtin fragments setting the same variable
        for builtin_fragment_key in builtin_fragments.keys():
            builtin_fragments_list = list(
                filter(
                    lambda f: f.startswith(builtin_fragment_key + "/"),
                    fragments.split(),
                )
            )
            if len(builtin_fragments_list) > 1:
                bb.warn(
                    ("Multiple builtin fragments are enabled for %s via variable %s: %s. "
                     "This likely points to a mis-configuration in the metadata, as only "
                     "one of them should be set. The build will use the last value.")
                    % (
                        builtin_fragment_key,
                        self.fragments_variable,
                        " ".join(builtin_fragments_list),
                    )
                )

        for f in fragments.split():
            if check_and_set_builtin_fragment(f, data, builtin_fragments):
                continue
            layerid, fragment_name = f.split('/', 1)
            full_fragment_name = data.expand("{}/{}.conf".format(self.fragments_path_prefix, fragment_name))
            fragment_path = find_fragment(layers, layerid, full_fragment_name)
            if fragment_path:
                bb.parse.ConfHandler.include(self.filename, fragment_path, self.lineno, data, "include fragment")
                for flagged_var in flagged_variables:
                    val = data.getVar(flagged_var)
                    data.setVarFlag(flagged_var, f, val)
                    data.setVar(flagged_var, None)
            else:
                bb.error("Could not find fragment {} in enabled layers: {}".format(f, layers))

def handleInclude(statements, filename, lineno, m, force):
    statements.append(IncludeNode(filename, lineno, m.group(1), force))

def handleIncludeAll(statements, filename, lineno, m):
    statements.append(IncludeAllNode(filename, lineno, m.group(1)))

def handleExport(statements, filename, lineno, m):
    statements.append(ExportNode(filename, lineno, m.group(1)))

def handleUnset(statements, filename, lineno, m):
    statements.append(UnsetNode(filename, lineno, m.group(1)))

def handleUnsetFlag(statements, filename, lineno, m):
    statements.append(UnsetFlagNode(filename, lineno, m.group(1), m.group(2)))

def handleData(statements, filename, lineno, groupd):
    statements.append(DataNode(filename, lineno, groupd))

def handleMethod(statements, filename, lineno, func_name, body, python, fakeroot):
    statements.append(MethodNode(filename, lineno, func_name, body, python, fakeroot))

def handlePythonMethod(statements, filename, lineno, funcname, modulename, body):
    statements.append(PythonMethodNode(filename, lineno, funcname, modulename, body))

def handleExportFuncs(statements, filename, lineno, m, classname):
    statements.append(ExportFuncsNode(filename, lineno, m.group(1), classname))

def handleAddTask(statements, filename, lineno, tasks, before, after):
    statements.append(AddTaskNode(filename, lineno, tasks, before, after))

def handleDelTask(statements, filename, lineno, tasks):
    statements.append(DelTaskNode(filename, lineno, tasks))

def handleBBHandlers(statements, filename, lineno, m):
    statements.append(BBHandlerNode(filename, lineno, m.group(1)))

def handlePyLib(statements, filename, lineno, m):
    statements.append(PyLibNode(filename, lineno, m.group(1), m.group(2)))

def handleInherit(statements, filename, lineno, m):
    classes = m.group(1)
    statements.append(InheritNode(filename, lineno, classes))

def handleInheritDeferred(statements, filename, lineno, m):
    classes = m.group(1)
    statements.append(InheritDeferredNode(filename, lineno, classes))

def handleAddFragments(statements, filename, lineno, m):
    fragments_path_prefix = m.group(1)
    fragments_variable = m.group(2)
    flagged_variables_list_variable = m.group(3)
    builtin_fragments_variable = m.group(4)
    statements.append(AddFragmentsNode(filename, lineno, fragments_path_prefix, fragments_variable, flagged_variables_list_variable, builtin_fragments_variable))

def runAnonFuncs(d):
    code = []
    for funcname in d.getVar("__BBANONFUNCS", False) or []:
        code.append("%s(d)" % funcname)
    bb.utils.better_exec("\n".join(code), {"d": d})

# Handle recipe level PREFERRED_PROVIDERs
def handleVirtRecipeProviders(tasklist, d):
    depends = (d.getVar("DEPENDS") or "").split()
    virtprovs = (d.getVar("BB_RECIPE_VIRTUAL_PROVIDERS") or "").split()
    newdeps = []
    for dep in depends:
        if dep in virtprovs:
            newdep = d.getVar("PREFERRED_PROVIDER_" + dep)
            if not newdep:
                 bb.fatal("Error, recipe virtual provider PREFERRED_PROVIDER_%s not set" % dep)
            newdeps.append(newdep)
        else:
            newdeps.append(dep)
    d.setVar("DEPENDS", " ".join(newdeps))
    for task in tasklist:
        taskdeps = (d.getVarFlag(task, "depends") or "").split()
        remapped = []
        for entry in taskdeps:
            r, t = entry.split(":")
            if r in virtprovs:
                r = d.getVar("PREFERRED_PROVIDER_" + r)
            remapped.append("%s:%s" % (r, t))
        d.setVarFlag(task, "depends", " ".join(remapped))

def finalize(fn, d, variant = None):
    saved_handlers = bb.event.get_handlers().copy()
    try:
        # Found renamed variables. Exit immediately
        if d.getVar("_FAILPARSINGERRORHANDLED", False) == True:
            raise bb.BBHandledException()

        inherits = [x[0] for x in (d.getVar('__BBDEFINHERITS', False) or [('',)])]
        bb.event.fire(bb.event.RecipePreDeferredInherits(fn, inherits), d)

        while True:
            inherits = d.getVar('__BBDEFINHERITS', False) or []
            if not inherits:
                break
            inherit, filename, lineno = inherits.pop(0)
            d.setVar('__BBDEFINHERITS', inherits)
            bb.parse.BBHandler.inherit(inherit, filename, lineno, d, deferred=True)

        for var in d.getVar('__BBHANDLERS', False) or []:
            # try to add the handler
            handlerfn = d.getVarFlag(var, "filename", False)
            if not handlerfn:
                bb.fatal("Undefined event handler function '%s'" % var)
            handlerln = int(d.getVarFlag(var, "lineno", False))
            bb.event.register(var, d.getVar(var, False), (d.getVarFlag(var, "eventmask") or "").split(), handlerfn, handlerln, data=d)

        bb.event.fire(bb.event.RecipePreFinalise(fn), d)

        bb.data.expandKeys(d)

        bb.event.fire(bb.event.RecipePostKeyExpansion(fn), d)

        runAnonFuncs(d)

        tasklist = d.getVar('__BBTASKS', False) or []
        bb.event.fire(bb.event.RecipeTaskPreProcess(fn, list(tasklist)), d)
        handleVirtRecipeProviders(tasklist, d)
        bb.build.add_tasks(tasklist, d)

        bb.parse.siggen.finalise(fn, d, variant)

        d.setVar('BBINCLUDED', bb.parse.get_file_depends(d))

        if d.getVar('__BBAUTOREV_SEEN') and d.getVar('__BBSRCREV_SEEN') and not d.getVar("__BBAUTOREV_ACTED_UPON"):
            bb.fatal("AUTOREV/SRCPV set too late for the fetcher to work properly, please set the variables earlier in parsing. Erroring instead of later obtuse build failures.")

        bb.event.fire(bb.event.RecipeParsed(fn), d)
    finally:
        bb.event.set_handlers(saved_handlers)

def _create_variants(datastores, names, function, onlyfinalise):
    def create_variant(name, orig_d, arg = None):
        if onlyfinalise and name not in onlyfinalise:
            return
        new_d = bb.data.createCopy(orig_d)
        function(arg or name, new_d)
        datastores[name] = new_d

    for variant in list(datastores.keys()):
        for name in names:
            if not variant:
                # Based on main recipe
                create_variant(name, datastores[""])
            else:
                create_variant("%s-%s" % (variant, name), datastores[variant], name)

def multi_finalize(fn, d):
    appends = (d.getVar("__BBAPPEND") or "").split()
    for append in appends:
        logger.debug("Appending .bbappend file %s to %s", append, fn)
        bb.parse.BBHandler.handle(append, d, True)

    onlyfinalise = d.getVar("__ONLYFINALISE", False)

    safe_d = d
    d = bb.data.createCopy(safe_d)
    try:
        finalize(fn, d)
    except bb.parse.SkipRecipe as e:
        d.setVar("__SKIPPED", e.args[0])
    datastores = {"": safe_d}

    extended = d.getVar("BBCLASSEXTEND") or ""
    if extended:
        # the following is to support bbextends with arguments, for e.g. multilib
        # an example is as follows:
        #   BBCLASSEXTEND = "multilib:lib32"
        # it will create foo-lib32, inheriting multilib.bbclass and set
        # BBEXTENDCURR to "multilib" and BBEXTENDVARIANT to "lib32"
        extendedmap = {}
        variantmap = {}

        for ext in extended.split():
            eext = ext.split(':', 2)
            if len(eext) > 1:
                extendedmap[ext] = eext[0]
                variantmap[ext] = eext[1]
            else:
                extendedmap[ext] = ext

        pn = d.getVar("PN")
        def extendfunc(name, d):
            if name != extendedmap[name]:
                d.setVar("BBEXTENDCURR", extendedmap[name])
                d.setVar("BBEXTENDVARIANT", variantmap[name])
            else:
                d.setVar("PN", "%s-%s" % (pn, name))
            bb.parse.BBHandler.inherit_defer(extendedmap[name], fn, 0, d)

        safe_d.setVar("BBCLASSEXTEND", extended)
        _create_variants(datastores, extendedmap.keys(), extendfunc, onlyfinalise)

    for variant in datastores.keys():
        if variant:
            try:
                if not onlyfinalise or variant in onlyfinalise:
                    finalize(fn, datastores[variant], variant)
            except bb.parse.SkipRecipe as e:
                datastores[variant].setVar("__SKIPPED", e.args[0])

    datastores[""] = d
    return datastores
