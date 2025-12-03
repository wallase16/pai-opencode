#!/bin/bash

# PAI OpenCode One-Click Install Script
# This script sets up PAI (Personal AI Infrastructure) for SST OpenCode

set -e  # Exit on any error

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Logging functions
log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

log_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

# Check if running on macOS or Linux
check_os() {
    if [[ "$OSTYPE" == "darwin"* ]]; then
        OS="macos"
        log_info "Detected macOS"
    elif [[ "$OSTYPE" == "linux-gnu"* ]]; then
        OS="linux"
        log_info "Detected Linux"
    else
        log_error "Unsupported OS: $OSTYPE"
        exit 1
    fi
}

# Check if OpenCode is installed
check_opencode() {
    if ! command -v opencode &> /dev/null; then
        log_error "OpenCode is not installed. Please install OpenCode first:"
        echo "  curl -fsSL https://opencode.ai/install | bash"
        exit 1
    fi
    log_success "OpenCode is installed"
}

# Check if Python 3.8+ is available (for Piper TTS)
check_python() {
    if ! command -v python3 &> /dev/null; then
        log_error "Python 3 is not installed. Please install Python 3.8 or later."
        exit 1
    fi

    PYTHON_VERSION=$(python3 -c 'import sys; print(".".join(map(str, sys.version_info[:2])))')
    if [[ "$(printf '%s\n' "$PYTHON_VERSION" "3.8" | sort -V | head -n1)" != "3.8" ]]; then
        log_error "Python $PYTHON_VERSION is too old. Please install Python 3.8 or later."
        exit 1
    fi

    log_success "Python $PYTHON_VERSION is available"
}

# Install Piper TTS
install_piper() {
    log_info "Installing Piper TTS..."

    if command -v pip3 &> /dev/null; then
        PIP_CMD="pip3"
    elif command -v pip &> /dev/null; then
        PIP_CMD="pip"
    else
        log_error "pip is not available. Please install pip."
        exit 1
    fi

    # Install Piper with HTTP server support
    $PIP_CMD install piper-tts[http]

    if [ $? -eq 0 ]; then
        log_success "Piper TTS installed successfully"
    else
        log_error "Failed to install Piper TTS"
        exit 1
    fi
}

# Download voice models
download_voices() {
    log_info "Downloading Piper voice models..."

    # Create voices directory
    mkdir -p opencode/voices/models

    # Download essential voices
    python3 -m piper.download_voices \
        en_US-lessac-medium \
        en_US-ryan-medium \
        en_US-amy-medium \
        en_GB-alan-medium

    if [ $? -eq 0 ]; then
        log_success "Voice models downloaded"
    else
        log_warning "Some voice downloads failed - continuing with available voices"
    fi
}

# Create voice configuration
create_voice_config() {
    log_info "Creating voice configuration..."

    cat > opencode/voices/config.json << 'EOF'
{
  "providers": {
    "piper": {
      "enabled": true,
      "server_port": 5000,
      "voices": {
        "kai": "en_US-lessac-medium",
        "engineer": "en_US-ryan-medium",
        "researcher": "en_US-amy-medium",
        "designer": "en_GB-alan-medium",
        "architect": "en_US-lessac-medium",
        "pentester": "en_US-ryan-medium"
      }
    },
    "elevenlabs": {
      "enabled": false,
      "api_key": null,
      "voices": {
        "kai": "s3TPKV1kjDlVtZbl4Ksh",
        "engineer": "fATgBRI8wg5KkDFg8vBd",
        "researcher": "AXdMgz6evoL7OPd7eU12",
        "designer": "ZF6FPAbjXT4488VcRRnw",
        "architect": "muZKMsIDGYtIkjjiUS82",
        "pentester": "xvHLFjaUEpx4BOf7EiDd"
      }
    }
  },
  "fallback_order": ["piper", "elevenlabs", "toast"],
  "default_provider": "piper"
}
EOF

    log_success "Voice configuration created"
}

# Configure OpenCode
configure_opencode() {
    log_info "Configuring OpenCode..."

    # Create OpenCode plugin directory if it doesn't exist
    OPENCODE_PLUGIN_DIR="$HOME/.config/opencode/plugin"
    mkdir -p "$OPENCODE_PLUGIN_DIR"

    # Copy PAI-Core plugin
    cp opencode/plugin/pai-core.ts "$OPENCODE_PLUGIN_DIR/"

    # Create or update opencode.json to include PAI instructions
    OPENCODE_CONFIG="$HOME/.config/opencode/opencode.json"
    if [ ! -f "$OPENCODE_CONFIG" ]; then
        cat > "$OPENCODE_CONFIG" << 'EOF'
{
  "$schema": "https://opencode.ai/config.json",
  "instructions": [
    "~/.config/opencode/rules.md"
  ]
}
EOF
    fi

    # Update rules.md with PAI context
    RULES_FILE="$HOME/.config/opencode/rules.md"
    PAI_CONTEXT_FILE=".claude/skills/CORE/SKILL.md"

    if [ -f "$PAI_CONTEXT_FILE" ]; then
        log_info "Setting up PAI context..."

        # Create header for PAI context
        cat > "$RULES_FILE" << 'EOF'
# PAI IDENTITY
# Identity Synced from: pai-opencode/.claude/skills/CORE/SKILL.md
# PAI_DIR Baked as: <current-directory>

EOF

        # Append PAI context
        cat "$PAI_CONTEXT_FILE" >> "$RULES_FILE"

        log_success "PAI context configured"
    else
        log_warning "PAI context file not found - skipping context setup"
    fi
}

# Start Piper voice server
start_voice_server() {
    log_info "Starting Piper voice server..."

    # Check if server is already running
    if curl -s http://localhost:5000/voices > /dev/null 2>&1; then
        log_info "Piper server already running"
        return
    fi

    # Start server in background
    nohup python3 -m piper.http_server \
        --model en_US-lessac-medium \
        --data-dir opencode/voices/models \
        --port 5000 > opencode/voices/piper-server.log 2>&1 &

    # Wait a moment for server to start
    sleep 3

    # Verify server is running
    if curl -s http://localhost:5000/voices > /dev/null 2>&1; then
        log_success "Piper voice server started on port 5000"
    else
        log_warning "Piper server may not have started correctly - check opencode/voices/piper-server.log"
    fi
}

# Run health check
run_health_check() {
    log_info "Running PAI OpenCode health check..."

    # Create health check script
    cat > opencode/scripts/health-check.sh << 'EOF'
#!/bin/bash

echo "PAI OpenCode Health Check"
echo "========================="

# Check OpenCode
if command -v opencode &> /dev/null; then
    echo "✅ OpenCode: Installed"
else
    echo "❌ OpenCode: Not found"
fi

# Check PAI-Core plugin
if [ -f "$HOME/.config/opencode/plugin/pai-core.ts" ]; then
    echo "✅ PAI-Core Plugin: Installed"
else
    echo "❌ PAI-Core Plugin: Not found"
fi

# Check Piper
if command -v piper &> /dev/null; then
    echo "✅ Piper TTS: Installed"
else
    echo "❌ Piper TTS: Not found"
fi

# Check voice server
if curl -s http://localhost:5000/voices > /dev/null 2>&1; then
    echo "✅ Voice Server: Running"
else
    echo "❌ Voice Server: Not running"
fi

# Check voice models
if [ -d "opencode/voices/models" ] && [ "$(ls -A opencode/voices/models)" ]; then
    echo "✅ Voice Models: Downloaded"
else
    echo "❌ Voice Models: Not found"
fi

echo ""
echo "Health check complete!"
EOF

    chmod +x opencode/scripts/health-check.sh

    # Run the health check
    ./opencode/scripts/health-check.sh
}

# Main installation function
main() {
    echo ""
    echo "🚀 PAI OpenCode Installation"
    echo "============================"
    echo ""

    log_info "Starting PAI OpenCode setup..."

    # Pre-flight checks
    check_os
    check_opencode
    check_python

    # Install components
    install_piper
    download_voices
    create_voice_config
    configure_opencode
    start_voice_server

    # Health check
    run_health_check

    echo ""
    log_success "PAI OpenCode installation complete!"
    echo ""
    echo "Next steps:"
    echo "1. Start OpenCode: opencode"
    echo "2. Test PAI: Try 'use_skill brainstorming' or 'pai_status'"
    echo "3. Test voice: Try 'pai_voice_test'"
    echo ""
    echo "For help, run: ./opencode/scripts/health-check.sh"
    echo ""
}

# Run main function
main "$@"