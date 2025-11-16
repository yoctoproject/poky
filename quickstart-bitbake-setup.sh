#!/bin/bash

# Yocto BitBake-Setup Quick Start Script
# This script automates the setup process for using bitbake-setup

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Functions
print_info() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warn() {
    echo -e "${YELLOW}[WARN]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_header() {
    echo ""
    echo "========================================"
    echo "$1"
    echo "========================================"
    echo ""
}

# Check prerequisites
check_prerequisites() {
    print_header "Checking Prerequisites"

    if ! command -v git &> /dev/null; then
        print_error "git is not installed. Please install git first."
        exit 1
    fi

    print_info "Git found: $(git --version)"

    if ! command -v python3 &> /dev/null; then
        print_warn "python3 not found. BitBake requires Python 3."
        print_warn "Please ensure Python 3 is installed."
    else
        print_info "Python found: $(python3 --version)"
    fi
}

# Main setup
main() {
    print_header "Yocto BitBake-Setup Quick Start"

    echo "This script will help you set up a new Yocto build environment using bitbake-setup."
    echo ""

    # Get workspace directory
    read -p "Enter the directory where you want to create your Yocto workspace [~/yocto-workspace]: " WORKSPACE_DIR
    WORKSPACE_DIR=${WORKSPACE_DIR:-~/yocto-workspace}
    WORKSPACE_DIR=$(eval echo "$WORKSPACE_DIR")  # Expand ~ if present

    # Check if directory exists
    if [ -d "$WORKSPACE_DIR" ]; then
        print_warn "Directory $WORKSPACE_DIR already exists."
        read -p "Do you want to continue and use this directory? (y/n): " CONTINUE
        if [[ ! $CONTINUE =~ ^[Yy]$ ]]; then
            print_info "Exiting..."
            exit 0
        fi
    else
        print_info "Creating directory: $WORKSPACE_DIR"
        mkdir -p "$WORKSPACE_DIR"
    fi

    cd "$WORKSPACE_DIR"
    print_info "Working in: $(pwd)"

    # Check prerequisites
    check_prerequisites

    # Clone BitBake if not already present
    print_header "Step 1: Cloning BitBake"

    if [ -d "bitbake" ]; then
        print_warn "bitbake directory already exists."
        read -p "Do you want to update it? (y/n): " UPDATE
        if [[ $UPDATE =~ ^[Yy]$ ]]; then
            print_info "Updating BitBake..."
            cd bitbake
            git fetch origin
            git pull origin master
            cd ..
        fi
    else
        print_info "Cloning BitBake repository..."
        git clone https://git.openembedded.org/bitbake
        print_info "BitBake cloned successfully!"
    fi

    # Check if bitbake-setup exists
    if [ ! -f "bitbake/bin/bitbake-setup" ]; then
        print_error "bitbake-setup not found in bitbake/bin/"
        print_error "Please ensure you have the latest version of BitBake."
        exit 1
    fi

    # Run bitbake-setup list to show available configs
    print_header "Step 2: Available Configurations"

    print_info "Listing available configurations..."
    ./bitbake/bin/bitbake-setup list || {
        print_warn "Could not list configurations. This might be expected if running for the first time."
    }

    # Initialize setup
    print_header "Step 3: Initialize Setup"

    echo "You can now initialize your build environment."
    echo "The initialization process will:"
    echo "  1. Let you select a configuration"
    echo "  2. Clone required repositories (openembedded-core, meta-yocto, etc.)"
    echo "  3. Set up your build directory"
    echo ""

    read -p "Do you want to run 'bitbake-setup init' now? (y/n): " RUN_INIT

    if [[ $RUN_INIT =~ ^[Yy]$ ]]; then
        print_info "Running bitbake-setup init..."
        echo ""
        ./bitbake/bin/bitbake-setup init

        print_header "Setup Complete!"

        # Find the setup directory
        SETUP_DIR=$(find . -maxdepth 1 -type d -name "*-setup" | head -n 1)

        if [ -n "$SETUP_DIR" ]; then
            print_info "Setup directory created: $SETUP_DIR"
            echo ""
            echo "To start using your build environment, run:"
            echo ""
            echo "  cd $WORKSPACE_DIR"
            echo "  source ./$SETUP_DIR/build/init-build-env"
            echo ""
            echo "Then you can use BitBake commands, for example:"
            echo "  bitbake core-image-minimal"
        else
            print_info "To start using your build environment, find your setup directory and run:"
            echo ""
            echo "  source ./YOUR-SETUP-DIR/build/init-build-env"
        fi

    else
        print_info "Skipping initialization."
        echo ""
        echo "To initialize later, run:"
        echo "  cd $WORKSPACE_DIR"
        echo "  ./bitbake/bin/bitbake-setup init"
    fi

    print_header "Useful Commands"

    echo "Here are some useful bitbake-setup commands:"
    echo ""
    echo "  ./bitbake/bin/bitbake-setup list      - List available configurations"
    echo "  ./bitbake/bin/bitbake-setup status    - Check setup status"
    echo "  ./bitbake/bin/bitbake-setup update    - Update to latest upstream changes"
    echo "  ./bitbake/bin/bitbake-setup settings  - Manage settings"
    echo ""

    print_info "For more information, see the MIGRATION_GUIDE.md"
    print_info "Documentation: https://docs.yoctoproject.org/"

    print_header "Done!"
}

# Run main function
main
