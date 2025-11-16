#!/bin/bash

# Yocto Manual Setup Quick Start Script
# This script automates the manual setup process with individual repository clones

set -e  # Exit on error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
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
    print_header "Yocto Manual Setup Quick Start"

    echo "This script will help you set up a Yocto build environment with individual repository clones."
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

    # Ask for branch/version
    print_header "Select Version"

    echo "Which version do you want to use?"
    echo "  1) Latest development (master branch)"
    echo "  2) Yocto 5.2 (LTS)"
    echo "  3) Yocto 5.1"
    echo "  4) Custom branch"
    echo ""
    read -p "Enter your choice [1]: " VERSION_CHOICE
    VERSION_CHOICE=${VERSION_CHOICE:-1}

    case $VERSION_CHOICE in
        1)
            BRANCH="master"
            print_info "Using master branch (latest development)"
            ;;
        2)
            BRANCH="yocto-5.2"
            print_info "Using yocto-5.2 (LTS)"
            ;;
        3)
            BRANCH="yocto-5.1"
            print_info "Using yocto-5.1"
            ;;
        4)
            read -p "Enter custom branch name: " BRANCH
            print_info "Using custom branch: $BRANCH"
            ;;
        *)
            print_error "Invalid choice. Exiting."
            exit 1
            ;;
    esac

    # Create layers directory
    print_header "Step 1: Creating Layers Directory"

    if [ ! -d "layers" ]; then
        mkdir layers
        print_info "Created layers directory"
    else
        print_info "Layers directory already exists"
    fi

    # Clone repositories
    print_header "Step 2: Cloning Repositories"

    # Clone BitBake
    if [ -d "layers/bitbake" ]; then
        print_warn "layers/bitbake already exists. Skipping clone."
    else
        print_info "Cloning BitBake ($BRANCH)..."
        if [ "$BRANCH" = "master" ]; then
            git clone https://git.openembedded.org/bitbake ./layers/bitbake
        else
            git clone -b "$BRANCH" https://git.openembedded.org/bitbake ./layers/bitbake
        fi
        print_info "✓ BitBake cloned"
    fi

    # Clone OpenEmbedded-Core
    if [ -d "layers/openembedded-core" ]; then
        print_warn "layers/openembedded-core already exists. Skipping clone."
    else
        print_info "Cloning OpenEmbedded-Core ($BRANCH)..."
        if [ "$BRANCH" = "master" ]; then
            git clone https://git.openembedded.org/openembedded-core ./layers/openembedded-core
        else
            git clone -b "$BRANCH" https://git.openembedded.org/openembedded-core ./layers/openembedded-core
        fi
        print_info "✓ OpenEmbedded-Core cloned"
    fi

    # Clone meta-yocto
    if [ -d "layers/meta-yocto" ]; then
        print_warn "layers/meta-yocto already exists. Skipping clone."
    else
        print_info "Cloning meta-yocto ($BRANCH)..."
        if [ "$BRANCH" = "master" ]; then
            git clone https://git.yoctoproject.org/meta-yocto ./layers/meta-yocto
        else
            git clone -b "$BRANCH" https://git.yoctoproject.org/meta-yocto ./layers/meta-yocto
        fi
        print_info "✓ meta-yocto cloned"
    fi

    # Initialize build environment
    print_header "Step 3: Initialize Build Environment"

    echo "The build environment will be initialized with the Poky default template."
    echo ""
    read -p "Do you want to initialize the build environment now? (y/n): " INIT_BUILD

    if [[ $INIT_BUILD =~ ^[Yy]$ ]]; then
        print_info "Initializing build environment..."

        # Create a helper script for sourcing
        cat > init-env.sh << 'EOF'
#!/bin/bash
TEMPLATECONF=$PWD/layers/meta-yocto/meta-poky/conf/templates/default \
    source ./layers/openembedded-core/oe-init-build-env
EOF
        chmod +x init-env.sh

        print_info "Created init-env.sh helper script"
        echo ""
        print_info "To initialize your build environment, run:"
        echo ""
        echo "  cd $WORKSPACE_DIR"
        echo "  source init-env.sh"
        echo ""
        print_info "This will create a 'build' directory and set up your environment."
        echo ""
        echo "Then you can configure build/conf/local.conf and run:"
        echo "  bitbake core-image-minimal"

    else
        print_info "Skipping build environment initialization."
        echo ""
        print_info "To initialize later, run:"
        echo ""
        echo "  cd $WORKSPACE_DIR"
        echo "  TEMPLATECONF=\$PWD/layers/meta-yocto/meta-poky/conf/templates/default \\"
        echo "      source ./layers/openembedded-core/oe-init-build-env"
    fi

    print_header "Next Steps"

    echo "Your Yocto environment has been set up with the following structure:"
    echo ""
    echo "  $WORKSPACE_DIR/"
    echo "  ├── layers/"
    echo "  │   ├── bitbake/           (BitBake build tool)"
    echo "  │   ├── openembedded-core/ (Core metadata)"
    echo "  │   └── meta-yocto/        (Yocto reference distribution)"
    echo "  └── build/                 (Created after sourcing init-build-env)"
    echo ""

    echo -e "${BLUE}To start building:${NC}"
    echo ""
    echo "  1. Source the build environment:"
    echo "     cd $WORKSPACE_DIR"
    echo "     source init-env.sh  (or use the TEMPLATECONF command above)"
    echo ""
    echo "  2. Configure your build (optional):"
    echo "     Edit build/conf/local.conf"
    echo "     - Set MACHINE (e.g., qemux86-64)"
    echo "     - Set DL_DIR and SSTATE_DIR for shared downloads/cache"
    echo ""
    echo "  3. Build an image:"
    echo "     bitbake core-image-minimal"
    echo ""

    echo -e "${BLUE}For additional layers:${NC}"
    echo ""
    echo "  Clone additional layers into the layers/ directory:"
    echo "    git clone <layer-url> ./layers/<layer-name>"
    echo ""
    echo "  Then add them to build/conf/bblayers.conf"
    echo ""

    print_info "For more information, see the MIGRATION_GUIDE.md"
    print_info "Documentation: https://docs.yoctoproject.org/"

    print_header "Setup Complete!"
}

# Run main function
main
