#!/bin/bash
# PAI-OpenCode Adapter Setup Script (v0.9.1 Compliant)
# This script sets up the "Bridge" between OpenCode and PAI.

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m'

log() { echo -e "${BLUE}[PAI]${NC} $1"; }
success() { echo -e "${GREEN}[SUCCESS]${NC} $1"; }

# 1. Environment Check
if ! command -v opencode &> /dev/null; then
    echo "Error: OpenCode is not installed."
    exit 1
fi

# Determine PAI Directory (Assume this script is in PAI_ROOT/opencode/scripts/)
PAI_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/../../" && pwd)"
log "Setting up PAI Adapter at: $PAI_DIR"

# 2. Standard Structure (v0.9.1)
mkdir -p "$PAI_DIR"/{Skills,Tools,Memories,Docs}
success "PAI directory structure verified."

# 3. Configure settings.json
cat > "$PAI_DIR/settings.json" << EOF
{
  "PAI_DIR": "$PAI_DIR",
  "_setupNote": "PAI_DIR auto-configured for OpenCode compatibility v0.9.1"
}
EOF
success "settings.json generated."

# 4. Install Adapter Plugin
OPENCODE_PLUGIN_DIR="$HOME/.config/opencode/plugin"
mkdir -p "$OPENCODE_PLUGIN_DIR"
cp "$PAI_DIR/opencode/plugin/pai-adapter.ts" "$OPENCODE_PLUGIN_DIR/pai-adapter.ts" 2>/dev/null || \
ln -sf "$PAI_DIR/opencode/plugin/pai-adapter.ts" "$OPENCODE_PLUGIN_DIR/pai-adapter.ts"
success "PAI-Adapter plugin installed to OpenCode."

# 5. Configure Native Skills
mkdir -p "$HOME/.opencode/skill"
# Symlink each skill to global skill directory
for skill_path in "$PAI_DIR/Skills"/*; do
    if [ -d "$skill_path" ]; then
        skill_name=$(basename "$skill_path" | tr '[:upper:]' '[:lower:]')
        ln -sf "$skill_path" "$HOME/.opencode/skill/$skill_name"
        log "Linked skill: $skill_name"
    fi
done
success "Native skills synchronized."

# 6. Final Health Check
log "Running PAI Status check..."
opencode run "pai_status" --print-logs 2>/dev/null || log "Note: opencode run failed (might be normal if not authenticated), but configuration is complete."

echo -e "\n${GREEN}PAI OpenCode Adapter is now ready!${NC}"