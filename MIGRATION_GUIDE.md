# Poky Migration Guide

The poky repository master branch is no longer being updated. This guide will help you migrate to one of the two recommended approaches.

## Quick Overview

You have two options:

1. **bitbake-setup** (Recommended) - Automated tool for managing Yocto/BitBake environments
2. **Manual Setup** - Individual clones of required repositories

## Option 1: Using bitbake-setup (Recommended)

The `bitbake-setup` tool is the new official way to set up Yocto build environments. It automates repository cloning, version management, and configuration.

### Prerequisites

- Git installed on your system
- Internet connection for cloning repositories

### Step 1: Clone BitBake

```bash
# Create a new directory for your Yocto environment
mkdir ~/yocto-workspace
cd ~/yocto-workspace

# Clone the BitBake repository
git clone https://git.openembedded.org/bitbake
```

### Step 2: Initialize Your Setup

```bash
# Run bitbake-setup init to create a new setup
./bitbake/bin/bitbake-setup init
```

This will:
- Prompt you to select from available configurations
- Clone required repositories (openembedded-core, meta-yocto, etc.)
- Set up your build directory with proper configuration

### Step 3: Configure Your Build

After initialization, you'll have a setup directory (e.g., `poky-setup`). Source the build environment:

```bash
# Source the build environment (path may vary based on your setup name)
source ./poky-setup/build/init-build-env
```

### Step 4: Start Building

Now you can use BitBake commands as usual:

```bash
# Build an image
bitbake core-image-minimal

# Or build for QEMU
bitbake core-image-sato
```

### Useful bitbake-setup Commands

```bash
# List available configurations
./bitbake/bin/bitbake-setup list

# Check status of your setup
./bitbake/bin/bitbake-setup status

# Update your setup to latest upstream changes
./bitbake/bin/bitbake-setup update

# Manage settings
./bitbake/bin/bitbake-setup settings
```

## Option 2: Manual Setup

If you prefer more control or want to use specific versions, you can manually clone the required repositories.

### Step 1: Create Layers Directory

```bash
# Create a new workspace
mkdir ~/yocto-workspace
cd ~/yocto-workspace
mkdir layers
```

### Step 2: Clone Required Repositories

For the latest development version (master):

```bash
# Clone BitBake
git clone https://git.openembedded.org/bitbake ./layers/bitbake

# Clone OpenEmbedded-Core
git clone https://git.openembedded.org/openembedded-core ./layers/openembedded-core

# Clone meta-yocto
git clone https://git.yoctoproject.org/meta-yocto ./layers/meta-yocto
```

For a specific release (e.g., yocto-5.2):

```bash
# Clone with specific branch
git clone -b yocto-5.2 https://git.openembedded.org/bitbake ./layers/bitbake
git clone -b yocto-5.2 https://git.openembedded.org/openembedded-core ./layers/openembedded-core
git clone -b yocto-5.2 https://git.yoctoproject.org/meta-yocto ./layers/meta-yocto
```

### Step 3: Initialize Build Environment

```bash
# Initialize with Poky template
TEMPLATECONF=$PWD/layers/meta-yocto/meta-poky/conf/templates/default \
    source ./layers/openembedded-core/oe-init-build-env
```

This creates a `build` directory with your configuration.

### Step 4: Configure and Build

Edit `build/conf/local.conf` as needed, then:

```bash
# Build your image
bitbake core-image-minimal
```

## Migrating Existing Builds

If you have an existing build that used the old poky repository:

### For bitbake-setup users:

1. Save your `build/conf/local.conf` and `build/conf/bblayers.conf` customizations
2. Set up a new environment using `bitbake-setup init`
3. Apply your customizations to the new setup's configuration files

### For manual setup users:

1. Save your configuration files from `build/conf/`
2. Clone the individual repositories as shown above
3. Initialize the build environment
4. Restore your customizations
5. Note: You may need to update layer paths in `bblayers.conf`

## Important Notes

### The "Poky" Distro Still Exists

The Poky distribution configuration (`DISTRO = "poky"`) is still available in meta-yocto and continues to be maintained. What changed is only the repository structure, not the distro itself.

### LTS Branches

If you're using an LTS (Long Term Support) branch of poky, those continue to be maintained according to their lifecycle. This change only affects the master branch.

### CI/CD Systems

For CI/CD systems, you can:
- Use `bitbake-setup` with automation-friendly commands
- Use manual setup with just bitbake and openembedded-core clones
- Use tools like kas if preferred (bitbake-setup is not mandatory)

## Getting Help

- Yocto Project Documentation: https://docs.yoctoproject.org/
- BitBake Setup Manual: https://docs.yoctoproject.org/bitbake/dev/bitbake-user-manual/bitbake-user-manual-environment-setup.html
- Manual Setup Guide: https://docs.yoctoproject.org/dev/dev-manual/poky-manual-setup.html
- Mailing Lists: https://lists.yoctoproject.org/

## Troubleshooting

### Issue: "bitbake command not found"

Make sure you've sourced the build environment:
```bash
source ./poky-setup/build/init-build-env  # for bitbake-setup
# or
source ./layers/openembedded-core/oe-init-build-env  # for manual setup
```

### Issue: Layer configuration errors

If you migrated from old poky and have layer path issues:
1. Check `build/conf/bblayers.conf`
2. Update layer paths to point to the new locations
3. Ensure all required layers are cloned

### Issue: Missing dependencies

BitBake will tell you if layers are missing. Clone any additional required layers:
```bash
# Example for meta-openembedded
git clone https://git.openembedded.org/meta-openembedded ./layers/meta-openembedded
```

Then add them to `bblayers.conf`.

## Quick Start Scripts

For your convenience, you can use the included quick-start scripts in this repository to automate the setup process.

See `quickstart-bitbake-setup.sh` for an automated bitbake-setup installation.

---

**Long live Poky!** 🎉
