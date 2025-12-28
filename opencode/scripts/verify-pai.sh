#!/bin/bash
# PAI Verification Script

RED='\033[0;31m'
GREEN='\033[0;32m'
NC='\033[0m'

check() {
    if $1; then
        echo -e "${GREEN}PASS:${NC} $2"
    else
        echo -e "${RED}FAIL:${NC} $2"
        exit 1
    fi
}

echo "Starting PAI-OpenCode Verification..."

# 1. Check Structure
check "[ -f /home/wallase16/Workspaces/pai-opencode/settings.json ]" "settings.json exists"
check "grep -q PAI_DIR /home/wallase16/Workspaces/pai-opencode/settings.json" "settings.json contains PAI_DIR"

# 2. Check Plugin
check "[ -f /home/wallase16/.config/opencode/plugin/pai-adapter.ts ]" "pai-adapter.ts installed"

# 3. Check Native Skills
check "[ -L /home/wallase16/.opencode/skill/core ]" "CORE skill symlink exists"

# 4. Check OpenCode Runtime
log_out=$(opencode models 2>&1)
check "echo \"$log_out\" | grep -v -q \"Unexpected error\"" "OpenCode boots without errors"

echo -e "\n${GREEN}ALL CHECKS PASSED${NC}"

