#
# Copyright (c) 2013-2016 Intel Corporation.
#
# SPDX-License-Identifier: GPL-2.0-only
#
# DESCRIPTION
# This module provides the OpenEmbedded partition object definitions.
#
# AUTHORS
# Tom Zanussi <tom.zanussi (at] linux.intel.com>
# Ed Bartosh <ed.bartosh> (at] linux.intel.com>

import logging
import os
import uuid

from wic import WicError
from wic.misc import exec_cmd, exec_native_cmd, get_bitbake_var
from wic.pluginbase import PluginMgr

logger = logging.getLogger('wic')

class Partition():

    def __init__(self, args, lineno):
        self.args = args
        self.active = args.active
        self.align = args.align
        self.disk = args.disk
        self.device = None
        self.extra_filesystem_space = args.extra_filesystem_space
        self.extra_partition_space = args.extra_partition_space
        self.exclude_path = args.exclude_path
        self.include_path = args.include_path
        self.change_directory = args.change_directory
        self.fsopts = args.fsopts
        self.fspassno = args.fspassno
        self.fstype = args.fstype
        self.label = args.label
        self.use_label = args.use_label
        self.mkfs_extraopts = args.mkfs_extraopts
        self.mountpoint = args.mountpoint
        self.no_table = args.no_table
        self.num = None
        self.offset = args.offset
        self.overhead_factor = args.overhead_factor
        self.part_name = args.part_name
        self.part_type = args.part_type
        self.rootfs_dir = args.rootfs_dir
        self.size = args.size
        self.fixed_size = args.fixed_size
        self.source = args.source
        self.sourceparams = args.sourceparams
        self.system_id = args.system_id
        self.use_uuid = args.use_uuid
        self.uuid = args.uuid
        self.fsuuid = args.fsuuid
        self.type = args.type
        self.no_fstab_update = args.no_fstab_update
        self.updated_fstab_path = None
        self.has_fstab = False
        self.update_fstab_in_rootfs = False
        self.hidden = args.hidden
        self.mbr = args.mbr

        self.lineno = lineno
        self.source_file = ""

    def get_extra_block_count(self, current_blocks):
        """
        The --size param is reflected in self.size (in kB), and we already
        have current_blocks (1k) blocks, calculate and return the
        number of (1k) blocks we need to add to get to --size, 0 if
        we're already there or beyond.
        """
        logger.debug("Requested partition size for %s: %d",
                     self.mountpoint, self.size)

        if not self.size:
            return 0

        requested_blocks = self.size

        logger.debug("Requested blocks %d, current_blocks %d",
                     requested_blocks, current_blocks)

        if requested_blocks > current_blocks:
            return requested_blocks - current_blocks
        else:
            return 0

    def get_rootfs_size(self, actual_rootfs_size=0):
        """
        Calculate the required size of rootfs taking into consideration
        --size/--fixed-size and --extra-partition-space flags as well as overhead
        and extra space, as specified in kickstart file. Raises an error
        if the `actual_rootfs_size` is larger than fixed-size rootfs.
        """
        if self.fixed_size:
            rootfs_size = self.fixed_size - self.extra_partition_space
            if actual_rootfs_size > rootfs_size:
                raise WicError("Actual rootfs size (%d kB) is larger than "
                               "allowed size %d kB" %
                               (actual_rootfs_size, rootfs_size))
        else:
            extra_blocks = self.get_extra_block_count(actual_rootfs_size)
            if extra_blocks < self.extra_filesystem_space:
                extra_blocks = self.extra_filesystem_space

            rootfs_size = actual_rootfs_size + extra_blocks
            rootfs_size = int(rootfs_size * self.overhead_factor)

            logger.debug("Added %d extra blocks to %s to get to %d total blocks",
                         extra_blocks, self.mountpoint, rootfs_size)

        return rootfs_size

    @property
    def disk_size(self):
        """
        Obtain on-disk size of partition taking into consideration
        --size/--fixed-size and --extra-partition-space options.

        """
        return self.fixed_size if self.fixed_size else self.size + self.extra_partition_space

    @property
    def fs_size(self):
        """
        Obtain on-disk size of filesystem inside the partition taking into
        consideration --size/--fixed-size and --extra-partition-space options.
        """
        return self.fixed_size - self.extra_partition_space if self.fixed_size else self.size

    def prepare(self, creator, cr_workdir, oe_builddir, rootfs_dir,
                bootimg_dir, kernel_dir, native_sysroot, updated_fstab_path):
        """
        Prepare content for individual partitions, depending on
        partition command parameters.
        """
        self.updated_fstab_path = updated_fstab_path
        if self.updated_fstab_path and not (self.fstype.startswith("ext") or self.fstype == "msdos"):
            self.update_fstab_in_rootfs = True

        if not self.source:
            if self.fstype == "none" or self.no_table:
                return
            if not self.size and not self.fixed_size:
                raise WicError("The %s partition has a size of zero. Please "
                               "specify a non-zero --size/--fixed-size for that "
                               "partition." % self.mountpoint)

            if self.fstype == "swap":
                self.prepare_swap_partition(cr_workdir, oe_builddir,
                                            native_sysroot)
                self.source_file = "%s/fs.%s" % (cr_workdir, self.fstype)
            else:
                if self.fstype in ('squashfs', 'erofs'):
                    raise WicError("It's not possible to create empty %s "
                                   "partition '%s'" % (self.fstype, self.mountpoint))

                rootfs = "%s/fs_%s.%s.%s" % (cr_workdir, self.label,
                                             self.lineno, self.fstype)
                if os.path.isfile(rootfs):
                    os.remove(rootfs)

                prefix = "ext" if self.fstype.startswith("ext") else self.fstype
                method = getattr(self, "prepare_empty_partition_" + prefix)
                method(rootfs, oe_builddir, native_sysroot)
                self.source_file = rootfs
            return

        plugins = PluginMgr.get_plugins('source')

        # Don't support '-' in plugin names
        self.source = self.source.replace("-", "_")

        if self.source not in plugins:
            raise WicError("The '%s' --source specified for %s doesn't exist.\n\t"
                           "See 'wic list source-plugins' for a list of available"
                           " --sources.\n\tSee 'wic help source-plugins' for "
                           "details on adding a new source plugin." %
                           (self.source, self.mountpoint))

        srcparams_dict = {}
        if self.sourceparams:
            # Split sourceparams string of the form key1=val1[,key2=val2,...]
            # into a dict.  Also accepts valueless keys i.e. without =
            splitted = self.sourceparams.split(',')
            srcparams_dict = dict((par.split('=', 1) + [None])[:2] for par in splitted if par)

        plugin = plugins[self.source]
        plugin.do_configure_partition(self, srcparams_dict, creator,
                                      cr_workdir, oe_builddir, bootimg_dir,
                                      kernel_dir, native_sysroot)
        plugin.do_stage_partition(self, srcparams_dict, creator,
                                  cr_workdir, oe_builddir, bootimg_dir,
                                  kernel_dir, native_sysroot)
        plugin.do_prepare_partition(self, srcparams_dict, creator,
                                    cr_workdir, oe_builddir, bootimg_dir,
                                    kernel_dir, rootfs_dir, native_sysroot)
        plugin.do_post_partition(self, srcparams_dict, creator,
                                    cr_workdir, oe_builddir, bootimg_dir,
                                    kernel_dir, rootfs_dir, native_sysroot)

        # further processing required Partition.size to be an integer, make
        # sure that it is one
        if not isinstance(self.size, int):
            raise WicError("Partition %s internal size is not an integer. "
                           "This a bug in source plugin %s and needs to be fixed." %
                           (self.mountpoint, self.source))

        if self.fixed_size and self.size + self.extra_partition_space > self.fixed_size:
            raise WicError("File system image of partition %s is "
                           "larger (%d kB + %d kB extra part space) than its allowed size %d kB" %
                           (self.mountpoint, self.size, self.extra_partition_space, self.fixed_size))

    def prepare_rootfs(self, cr_workdir, oe_builddir, rootfs_dir,
                       native_sysroot, real_rootfs = True, pseudo_dir = None):
        """
        Prepare content for a rootfs partition i.e. create a partition
        and fill it from a /rootfs dir.

        Currently handles ext2/3/4, btrfs, vfat and squashfs.
        """

        rootfs = "%s/rootfs_%s.%s.%s" % (cr_workdir, self.label,
                                         self.lineno, self.fstype)
        if os.path.isfile(rootfs):
            os.remove(rootfs)

        p_prefix = os.environ.get("PSEUDO_PREFIX", "%s/usr" % native_sysroot)
        if (pseudo_dir):
            # Canonicalize the ignore paths. This corresponds to
            # calling oe.path.canonicalize(), which is used in bitbake.conf.
            include_paths = [rootfs_dir] + (get_bitbake_var("PSEUDO_INCLUDE_PATHS") or "").split(",")
            canonical_paths = []
            for path in include_paths:
                if "$" not in path:
                    trailing_slash = path.endswith("/") and "/" or ""
                    canonical_paths.append(os.path.realpath(path) + trailing_slash)
            include_paths = ",".join(canonical_paths)

            pseudo = "export PSEUDO_PREFIX=%s;" % p_prefix
            pseudo += "export PSEUDO_LOCALSTATEDIR=%s;" % pseudo_dir
            pseudo += "export PSEUDO_PASSWD=%s;" % rootfs_dir
            pseudo += "export PSEUDO_NOSYMLINKEXP=1;"
            pseudo += "export PSEUDO_INCLUDE_PATHS=%s;" % include_paths
            pseudo += "%s " % get_bitbake_var("FAKEROOTCMD")
        else:
            pseudo = None

        if not self.size and real_rootfs:
            # The rootfs size is not set in .ks file so try to get it
            # from bitbake variable
            rsize_bb = get_bitbake_var('ROOTFS_SIZE')
            rdir = get_bitbake_var('IMAGE_ROOTFS')
            if rsize_bb and (rdir == rootfs_dir or (rootfs_dir.split('/')[-2] == "tmp-wic" and rootfs_dir.split('/')[-1][:6] == "rootfs")):
                # Bitbake variable ROOTFS_SIZE is calculated in
                # Image._get_rootfs_size method from meta/lib/oe/image.py
                # using IMAGE_ROOTFS_SIZE, IMAGE_ROOTFS_ALIGNMENT,
                # IMAGE_OVERHEAD_FACTOR and IMAGE_ROOTFS_EXTRA_SPACE
                self.size = int(round(float(rsize_bb)))
            else:
                # Bitbake variable ROOTFS_SIZE is not defined so compute it
                # from the rootfs_dir size using the same logic found in
                # get_rootfs_size() from meta/classes/image.bbclass
                du_cmd = "du -ks %s" % rootfs_dir
                out = exec_cmd(du_cmd)
                self.size = int(out.split()[0])

        prefix = "ext" if self.fstype.startswith("ext") else self.fstype
        method = getattr(self, "prepare_rootfs_" + prefix)
        method(rootfs, cr_workdir, oe_builddir, rootfs_dir, native_sysroot, pseudo)
        self.source_file = rootfs

        # get the rootfs size in the right units for kickstart (kB)
        du_cmd = "du -Lbks %s" % rootfs
        out = exec_cmd(du_cmd)
        self.size = int(out.split()[0])

    def prepare_rootfs_ext(self, rootfs, cr_workdir, oe_builddir, rootfs_dir,
                           native_sysroot, pseudo):
        """
        Prepare content for an ext2/3/4 rootfs partition.
        """
        du_cmd = "du -ks %s" % rootfs_dir
        out = exec_cmd(du_cmd)
        actual_rootfs_size = int(out.split()[0])

        rootfs_size = self.get_rootfs_size(actual_rootfs_size)

        with open(rootfs, 'w') as sparse:
            os.ftruncate(sparse.fileno(), rootfs_size * 1024)

        extraopts = self.mkfs_extraopts or "-F -i 8192"

        # use hash_seed to generate reproducible ext4 images
        (extraopts, pseudo) = self.get_hash_seed_ext4(extraopts, pseudo)

        label_str = ""
        if self.label:
            label_str = "-L %s" % self.label

        mkfs_cmd = "mkfs.%s %s %s %s -U %s -d %s" % \
            (self.fstype, extraopts, rootfs, label_str, self.fsuuid, rootfs_dir)
        exec_native_cmd(mkfs_cmd, native_sysroot, pseudo=pseudo)

        if self.updated_fstab_path and self.has_fstab and not self.no_fstab_update:
            debugfs_script_path = os.path.join(cr_workdir, "debugfs_script")
            with open(debugfs_script_path, "w") as f:
                f.write("cd etc\n")
                f.write("rm fstab\n")
                f.write("write %s fstab\n" % (self.updated_fstab_path))
            debugfs_cmd = "debugfs -w -f %s %s" % (debugfs_script_path, rootfs)
            exec_native_cmd(debugfs_cmd, native_sysroot)

        mkfs_cmd = "fsck.%s -pvfD %s" % (self.fstype, rootfs)
        exec_native_cmd(mkfs_cmd, native_sysroot, pseudo=pseudo)

        if os.getenv('SOURCE_DATE_EPOCH'):
            sde_time = hex(int(os.getenv('SOURCE_DATE_EPOCH')))
            debugfs_script_path = os.path.join(cr_workdir, "debugfs_script")
            files = []
            for root, dirs, others in os.walk(rootfs_dir):
                base = root.replace(rootfs_dir, "").rstrip(os.sep)
                files += [ "/" if base == "" else base ]
                files += [ base + "/" + n for n in dirs + others ]
            with open(debugfs_script_path, "w") as f:
                f.write("set_current_time %s\n" % (sde_time))
                if self.updated_fstab_path and self.has_fstab and not self.no_fstab_update:
                    f.write("set_inode_field /etc/fstab mtime %s\n" % (sde_time))
                    f.write("set_inode_field /etc/fstab mtime_extra 0\n")
                for file in set(files):
                    for time in ["atime", "ctime", "crtime"]:
                        f.write("set_inode_field \"%s\" %s %s\n" % (file, time, sde_time))
                        f.write("set_inode_field \"%s\" %s_extra 0\n" % (file, time))
                for time in ["wtime", "mkfs_time", "lastcheck"]:
                    f.write("set_super_value %s %s\n" % (time, sde_time))
                for time in ["mtime", "first_error_time", "last_error_time"]:
                    f.write("set_super_value %s 0\n" % (time))
            debugfs_cmd = "debugfs -w -f %s %s" % (debugfs_script_path, rootfs)
            exec_native_cmd(debugfs_cmd, native_sysroot)

        self.check_for_Y2038_problem(rootfs, native_sysroot)

    def get_hash_seed_ext4(self, extraopts, pseudo):
        if os.getenv('SOURCE_DATE_EPOCH'):
            sde_time = int(os.getenv('SOURCE_DATE_EPOCH'))
            if pseudo:
                pseudo = "export E2FSPROGS_FAKE_TIME=%s;%s " % (sde_time, pseudo)
            else:
                pseudo = "export E2FSPROGS_FAKE_TIME=%s; " % sde_time

            # Set hash_seed to generate deterministic directory indexes
            namespace = uuid.UUID("e7429877-e7b3-4a68-a5c9-2f2fdf33d460")
            if self.fsuuid:
                namespace = uuid.UUID(self.fsuuid)
            hash_seed = str(uuid.uuid5(namespace, str(sde_time)))
            extraopts += " -E hash_seed=%s" % hash_seed

        return (extraopts, pseudo)

    def prepare_rootfs_btrfs(self, rootfs, cr_workdir, oe_builddir, rootfs_dir,
                             native_sysroot, pseudo):
        """
        Prepare content for a btrfs rootfs partition.
        """
        du_cmd = "du -ks %s" % rootfs_dir
        out = exec_cmd(du_cmd)
        actual_rootfs_size = int(out.split()[0])

        rootfs_size = self.get_rootfs_size(actual_rootfs_size)

        with open(rootfs, 'w') as sparse:
            os.ftruncate(sparse.fileno(), rootfs_size * 1024)

        label_str = ""
        if self.label:
            label_str = "-L %s" % self.label

        mkfs_cmd = "mkfs.%s -b %d -r %s %s %s -U %s %s" % \
            (self.fstype, rootfs_size * 1024, rootfs_dir, label_str,
             self.mkfs_extraopts, self.fsuuid, rootfs)
        exec_native_cmd(mkfs_cmd, native_sysroot, pseudo=pseudo)

    def prepare_rootfs_msdos(self, rootfs, cr_workdir, oe_builddir, rootfs_dir,
                             native_sysroot, pseudo):
        """
        Prepare content for a msdos/vfat rootfs partition.
        """
        du_cmd = "du -bks %s" % rootfs_dir
        out = exec_cmd(du_cmd)
        blocks = int(out.split()[0])

        rootfs_size = self.get_rootfs_size(blocks)

        label_str = "-n boot"
        if self.label:
            label_str = "-n %s" % self.label

        size_str = ""

        extraopts = self.mkfs_extraopts or '-S 512'

        dosfs_cmd = "mkdosfs %s -i %s %s %s -C %s %d" % \
                    (label_str, self.fsuuid, size_str, extraopts, rootfs,
                     rootfs_size)
        exec_native_cmd(dosfs_cmd, native_sysroot)

        mcopy_cmd = "mcopy -i %s -s %s/* ::/" % (rootfs, rootfs_dir)
        exec_native_cmd(mcopy_cmd, native_sysroot)

        if self.updated_fstab_path and self.has_fstab and not self.no_fstab_update:
            mcopy_cmd = "mcopy -m -i %s %s ::/etc/fstab" % (rootfs, self.updated_fstab_path)
            exec_native_cmd(mcopy_cmd, native_sysroot)

        chmod_cmd = "chmod 644 %s" % rootfs
        exec_cmd(chmod_cmd)

    prepare_rootfs_vfat = prepare_rootfs_msdos

    def prepare_rootfs_squashfs(self, rootfs, cr_workdir, oe_builddir, rootfs_dir,
                                native_sysroot, pseudo):
        """
        Prepare content for a squashfs rootfs partition.
        """
        extraopts = self.mkfs_extraopts or '-noappend'
        squashfs_cmd = "mksquashfs %s %s %s" % \
                       (rootfs_dir, rootfs, extraopts)
        exec_native_cmd(squashfs_cmd, native_sysroot, pseudo=pseudo)

    def prepare_rootfs_erofs(self, rootfs, cr_workdir, oe_builddir, rootfs_dir,
                             native_sysroot, pseudo):
        """
        Prepare content for a erofs rootfs partition.
        """
        extraopts = self.mkfs_extraopts or ''
        erofs_cmd = "mkfs.erofs %s -U %s %s %s" % \
                       (extraopts, self.fsuuid, rootfs, rootfs_dir)
        exec_native_cmd(erofs_cmd, native_sysroot, pseudo=pseudo)

    def prepare_empty_partition_none(self, rootfs, oe_builddir, native_sysroot):
        pass

    def prepare_empty_partition_ext(self, rootfs, oe_builddir,
                                    native_sysroot):
        """
        Prepare an empty ext2/3/4 partition.
        """
        size = self.fs_size
        with open(rootfs, 'w') as sparse:
            os.ftruncate(sparse.fileno(), size * 1024)

        extraopts = self.mkfs_extraopts or "-i 8192"

        # use hash_seed to generate reproducible ext4 images
        (extraopts, pseudo) = self.get_hash_seed_ext4(extraopts, None)

        label_str = ""
        if self.label:
            label_str = "-L %s" % self.label

        mkfs_cmd = "mkfs.%s -F %s %s -U %s %s" % \
            (self.fstype, extraopts, label_str, self.fsuuid, rootfs)
        exec_native_cmd(mkfs_cmd, native_sysroot, pseudo=pseudo)

        self.check_for_Y2038_problem(rootfs, native_sysroot)

    def prepare_empty_partition_btrfs(self, rootfs, oe_builddir,
                                      native_sysroot):
        """
        Prepare an empty btrfs partition.
        """
        size = self.fs_size
        with open(rootfs, 'w') as sparse:
            os.ftruncate(sparse.fileno(), size * 1024)

        label_str = ""
        if self.label:
            label_str = "-L %s" % self.label

        mkfs_cmd = "mkfs.%s -b %d %s -U %s %s %s" % \
                   (self.fstype, self.size * 1024, label_str, self.fsuuid,
                    self.mkfs_extraopts, rootfs)
        exec_native_cmd(mkfs_cmd, native_sysroot)

    def prepare_empty_partition_msdos(self, rootfs, oe_builddir,
                                      native_sysroot):
        """
        Prepare an empty vfat partition.
        """
        blocks = self.fs_size

        label_str = "-n boot"
        if self.label:
            label_str = "-n %s" % self.label

        size_str = ""

        extraopts = self.mkfs_extraopts or '-S 512'

        dosfs_cmd = "mkdosfs %s -i %s %s %s -C %s %d" % \
                    (label_str, self.fsuuid, extraopts, size_str, rootfs,
                     blocks)

        exec_native_cmd(dosfs_cmd, native_sysroot)

        chmod_cmd = "chmod 644 %s" % rootfs
        exec_cmd(chmod_cmd)

    prepare_empty_partition_vfat = prepare_empty_partition_msdos

    def prepare_swap_partition(self, cr_workdir, oe_builddir, native_sysroot):
        """
        Prepare a swap partition.
        """
        path = "%s/fs.%s" % (cr_workdir, self.fstype)

        with open(path, 'w') as sparse:
            os.ftruncate(sparse.fileno(), self.size * 1024)

        label_str = ""
        if self.label:
            label_str = "-L %s" % self.label

        mkswap_cmd = "mkswap %s -U %s %s" % (label_str, self.fsuuid, path)
        exec_native_cmd(mkswap_cmd, native_sysroot)

    def check_for_Y2038_problem(self, rootfs, native_sysroot):
        """
        Check if the filesystem is affected by the Y2038 problem
        (Y2038 problem = 32 bit time_t overflow in January 2038)
        """
        def get_err_str(part):
            err = "The {} filesystem {} has no Y2038 support."
            if part.mountpoint:
                args = [part.fstype, "mounted at %s" % part.mountpoint]
            elif part.label:
                args = [part.fstype, "labeled '%s'" % part.label]
            elif part.part_name:
                args = [part.fstype, "in partition '%s'" % part.part_name]
            else:
                args = [part.fstype, "in partition %s" % part.num]
            return err.format(*args)

        # ext2 and ext3 are always affected by the Y2038 problem
        if self.fstype in ["ext2", "ext3"]:
            logger.warn(get_err_str(self))
            return

        ret, out = exec_native_cmd("dumpe2fs %s" % rootfs, native_sysroot)

        # if ext4 is affected by the Y2038 problem depends on the inode size
        for line in out.splitlines():
            if line.startswith("Inode size:"):
                size = int(line.split(":")[1].strip())
                if size < 256:
                    logger.warn("%s Inodes (of size %d) are too small." %
                                (get_err_str(self), size))
                break

