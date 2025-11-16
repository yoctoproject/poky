# Configuration Examples

This directory contains example configuration files for Yocto/BitBake builds.

## Files

### local.conf.sample

Sample build configuration file with common settings and options.

**Usage:**
```bash
# After initializing your build environment
cp local.conf.sample build/conf/local.conf

# Then edit build/conf/local.conf to customize for your needs
```

**Key configurations included:**
- Machine selection (target hardware)
- Distribution settings
- Package management options
- Download and shared state cache directories
- Build optimization settings
- Development and debugging features
- QEMU configuration
- Security features

### bblayers.conf.sample

Sample layer configuration file showing how to add layers to your build.

**Usage:**
```bash
# This file is usually auto-generated when you initialize your build
# Use it as a reference for adding additional layers

# To add a new layer:
bitbake-layers add-layer /path/to/layer

# Or manually edit build/conf/bblayers.conf
```

**Common layers:**
- meta-openembedded (additional recipes)
- meta-qt5 (Qt framework)
- meta-security (security tools)
- meta-virtualization (containers, virtualization)

## Quick Tips

### Setting Up Shared Cache Directories

To speed up builds and save disk space across multiple build directories:

1. Edit `local.conf`:
```bash
DL_DIR ?= "/opt/yocto/downloads"
SSTATE_DIR ?= "/opt/yocto/sstate-cache"
```

2. Create the directories:
```bash
sudo mkdir -p /opt/yocto/downloads /opt/yocto/sstate-cache
sudo chown $USER:$USER /opt/yocto/downloads /opt/yocto/sstate-cache
```

### Build Performance Tuning

Adjust based on your system:

```bash
# For a system with 8 cores and 16GB RAM:
BB_NUMBER_THREADS = "8"
PARALLEL_MAKE = "-j 8"

# For a system with 16 cores and 32GB RAM:
BB_NUMBER_THREADS = "16"
PARALLEL_MAKE = "-j 16"
```

### Common Machine Targets

```bash
# For QEMU emulation:
MACHINE = "qemux86-64"     # x86_64 QEMU
MACHINE = "qemuarm64"      # ARM64 QEMU
MACHINE = "qemuarm"        # ARM QEMU

# For real hardware:
MACHINE = "beaglebone-yocto"
MACHINE = "genericx86-64"
MACHINE = "raspberrypi4-64"  # Requires meta-raspberrypi layer
```

### Useful Build Commands

```bash
# Build a minimal image
bitbake core-image-minimal

# Build with graphical interface
bitbake core-image-sato

# Build SDK for application development
bitbake -c populate_sdk core-image-minimal

# Clean a recipe
bitbake -c clean <recipe-name>

# Show available images
ls layers/meta-*/recipes-*/images/*.bb
```

### Layer Management

```bash
# List available layers in your setup
bitbake-layers show-layers

# Add a layer
bitbake-layers add-layer /path/to/layer

# Remove a layer
bitbake-layers remove-layer meta-layername

# Show recipes provided by a layer
bitbake-layers show-recipes -i meta-layername
```

## Troubleshooting

### Build fails with "Nothing PROVIDES ..."

Add the required layer to `bblayers.conf`. Check which layer provides the missing recipe:
```bash
# Search for a recipe
bitbake-layers show-recipes | grep <recipe-name>
```

### Disk space issues

Enable `rm_work` to delete temporary files after each package:
```bash
# In local.conf:
INHERIT += "rm_work"

# Exclude specific packages from cleanup:
RM_WORK_EXCLUDE += "package-name"
```

### Build is slow

1. Check BB_NUMBER_THREADS and PARALLEL_MAKE settings
2. Set up shared DL_DIR and SSTATE_DIR
3. Use a local mirror if available
4. Consider using hash equivalence (BB_HASHSERVE)

## Documentation

For more information:
- Yocto Project Documentation: https://docs.yoctoproject.org/
- BitBake User Manual: https://docs.yoctoproject.org/bitbake/
- Yocto Dev Manual: https://docs.yoctoproject.org/dev-manual/
- Migration Guide: See MIGRATION_GUIDE.md in the repository root
