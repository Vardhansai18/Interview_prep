#!/bin/bash

#########################################################
# Script Name : ai-agent-mapper.sh
# Description : Scans a folder and its subfolders for
#               all *.agent.md files and creates soft
#               links in the .github/agents directory
#
# Note        : Ignores *.agent.md files found inside
#               any "subagents" directory
#
# Usage       : ./ai-agent-mapper.sh <scan_folder>
#               ./ai-agent-mapper.sh              (defaults to current directory)
#########################################################

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# --------------------
# Configuration
# --------------------
SOFTLINK_DIR=".github/agents"
EXCLUDE_DIRS=("subagents")    # Directories to exclude

# --------------------
# Function: log messages
# --------------------
log_success() {
    echo -e "${GREEN}[✔] $1${NC}"
}

log_error() {
    echo -e "${RED}[✘] $1${NC}"
}

log_info() {
    echo -e "${YELLOW}[i] $1${NC}"
}

log_link() {
    echo -e "${CYAN}[→] $1${NC}"
}

log_skip() {
    echo -e "${RED}[⊘] $1${NC}"
}

# --------------------
# Function: usage
# --------------------
usage() {
    echo -e "${YELLOW}Usage: $0 [scan_folder]${NC}"
    echo ""
    echo "  Scans the given folder (and subfolders) for *.agent.md files"
    echo "  and creates soft links in '${SOFTLINK_DIR}/' directory."
    echo ""
    echo "  ${RED}Excludes:${NC} Files inside 'subagents/' directories are ignored."
    echo ""
    echo "  If no folder is provided, the current directory is used."
    echo ""
    echo "  Options:"
    echo "    -h, --help    Show this help message"
    echo ""
    echo "  Examples:"
    echo "    $0                     # Scan current directory"
    echo "    $0 /home/user/project  # Scan specific folder"
    exit 0
}

# --------------------
# Function: check if path contains excluded directory
# --------------------
is_excluded() {
    local filepath="$1"

    for exclude_dir in "${EXCLUDE_DIRS[@]}"; do
        if [[ "$filepath" == *"/${exclude_dir}/"* ]] || [[ "$filepath" == "${exclude_dir}/"* ]]; then
            return 0  # true — should be excluded
        fi
    done

    return 1  # false — should NOT be excluded
}

# --------------------
# Function: cleanup broken softlinks
# --------------------
cleanup_broken_links() {
    local link_dir="$1"
    local broken_count=0

    if [ -d "$link_dir" ]; then
        while IFS= read -r -d '' broken_link; do
            log_info "Removing broken softlink: ${broken_link}"
            rm -f "$broken_link"
            ((broken_count++))
        done < <(find "$link_dir" -maxdepth 1 -type l ! -exec test -e {} \; -print0 2>/dev/null)

        if [ "$broken_count" -gt 0 ]; then
            log_info "Cleaned up ${broken_count} broken softlink(s)"
        fi
    fi
}

# --------------------
# Function: build find exclude arguments
# --------------------
build_find_excludes() {
    local exclude_args=""

    for exclude_dir in "${EXCLUDE_DIRS[@]}"; do
        if [ -n "$exclude_args" ]; then
            exclude_args="$exclude_args -o"
        fi
        exclude_args="$exclude_args -name $exclude_dir -type d"
    done

    echo "$exclude_args"
}

# --------------------
# Function: create softlinks
# --------------------
create_softlinks() {
    local scan_dir="$1"
    local link_dir="$2"
    local created_count=0
    local skipped_count=0
    local excluded_count=0
    local error_count=0
    local total_found=0

    # Find all *.agent.md files, excluding subagents directories
    while IFS= read -r -d '' agent_file; do
        ((total_found++))

        # Check if the file is inside an excluded directory
        if is_excluded "$agent_file"; then
            log_skip "Excluded (subagents): ${agent_file}"
            ((excluded_count++))
            continue
        fi

        # Get the absolute path of the found file
        abs_path=$(realpath "$agent_file")

        # Get the filename
        filename=$(basename "$agent_file")

        # Full path of the softlink to be created
        link_path="${link_dir}/${filename}"

        # Check if softlink already exists
        if [ -L "$link_path" ]; then
            # Check if existing link points to the same file
            existing_target=$(realpath "$link_path" 2>/dev/null)
            if [ "$existing_target" == "$abs_path" ]; then
                log_info "Softlink already exists (skipping): ${filename} → ${abs_path}"
                ((skipped_count++))
                continue
            else
                # Remove old link pointing to a different file
                log_info "Updating existing softlink: ${filename}"
                rm -f "$link_path"
            fi
        fi

        # Handle duplicate filenames from different directories
        if [ -e "$link_path" ]; then
            # Append parent directory name to avoid conflicts
            parent_dir=$(basename "$(dirname "$agent_file")")
            new_filename="${parent_dir}_${filename}"
            link_path="${link_dir}/${new_filename}"
            log_info "Duplicate filename detected. Using: ${new_filename}"
        fi

        # Create the softlink
        ln -s "$abs_path" "$link_path" 2>/dev/null
        if [ $? -eq 0 ]; then
            log_link "${link_path} → ${abs_path}"
            ((created_count++))
        else
            log_error "Failed to create softlink for: ${agent_file}"
            ((error_count++))
        fi

    done < <(find "$scan_dir" -type d -name "subagents" -prune -o -type f -name "*.agent.md" -print0 2>/dev/null)

    # --------------------
    # Summary
    # --------------------
    echo ""
    echo "========================================="
    echo "  Summary"
    echo "========================================="
    echo ""
    echo -e "  ${CYAN}Scan Directory  :${NC} $(realpath "$scan_dir")"
    echo -e "  ${CYAN}Softlink Dir    :${NC} $(realpath "$link_dir")"
    echo -e "  ${CYAN}Excluded Dirs   :${NC} ${EXCLUDE_DIRS[*]}"
    echo ""
    echo -e "  ${YELLOW}Total Found     :${NC} ${total_found}"
    echo -e "  ${GREEN}Links Created   :${NC} ${created_count}"
    echo -e "  ${YELLOW}Skipped (exist) :${NC} ${skipped_count}"
    echo -e "  ${RED}Excluded        :${NC} ${excluded_count}"
    echo -e "  ${RED}Errors          :${NC} ${error_count}"
    echo ""

    if [ "$total_found" -eq 0 ]; then
        log_info "No *.agent.md files found in '${scan_dir}' or its subdirectories."
    fi

    # List all softlinks in the directory
    if [ "$created_count" -gt 0 ] || [ "$skipped_count" -gt 0 ]; then
        echo "========================================="
        echo "  Softlinks in ${link_dir}/"
        echo "========================================="
        echo ""
        ls -la "${link_dir}/"*.agent.md 2>/dev/null | while read -r line; do
            echo "  $line"
        done
        echo ""
    fi
}

# --------------------
# Main script
# --------------------

# Handle help flag
if [ "$1" == "-h" ] || [ "$1" == "--help" ]; then
    usage
fi

# Set scan directory (default: current directory)
SCAN_DIR="${1:-.}"

# Validate scan directory
if [ ! -d "$SCAN_DIR" ]; then
    log_error "Directory '${SCAN_DIR}' does not exist!"
    exit 1
fi

# Display start info
echo ""
echo "========================================="
echo "  Agent MD Softlink Creator"
echo "========================================="
echo ""
log_info "Scan directory   : $(realpath "$SCAN_DIR")"
log_info "Softlink target  : ${SOFTLINK_DIR}/"
log_info "Excluding dirs   : ${EXCLUDE_DIRS[*]}"
echo ""

# Create softlink directory if it doesn't exist
if [ ! -d "$SOFTLINK_DIR" ]; then
    mkdir -p "$SOFTLINK_DIR"
    if [ $? -ne 0 ]; then
        log_error "Failed to create directory '${SOFTLINK_DIR}'"
        exit 1
    fi
    log_success "Created softlink directory: ${SOFTLINK_DIR}/"
else
    log_info "Softlink directory already exists: ${SOFTLINK_DIR}/"
fi

# Cleanup any broken softlinks first
cleanup_broken_links "$SOFTLINK_DIR"

echo ""
log_info "Scanning for *.agent.md files (excluding subagents/)..."
echo ""

# Create softlinks
create_softlinks "$SCAN_DIR" "$SOFTLINK_DIR"

log_success "Done!"
echo ""

exit 0
