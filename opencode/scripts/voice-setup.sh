#!/bin/bash

# PAI Voice Setup Script
# Configures voice providers for PAI OpenCode

set -e

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

log_info() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

log_success() {
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

log_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

# Check current voice configuration
check_current_config() {
    log_info "Checking current voice configuration..."

    if [ -f "opencode/voices/config.json" ]; then
        log_success "Voice configuration found"
        cat opencode/voices/config.json | jq . 2>/dev/null || cat opencode/voices/config.json
    else
        log_warning "No voice configuration found"
    fi
}

# Setup Piper (free option)
setup_piper() {
    log_info "Setting up Piper TTS (free option)..."

    # Check if Piper is installed
    if ! command -v piper &> /dev/null; then
        log_info "Installing Piper TTS..."
        pip3 install piper-tts[http]
    fi

    # Download voices if not present
    if [ ! -d "opencode/voices/models" ] || [ -z "$(ls -A opencode/voices/models 2>/dev/null)" ]; then
        log_info "Downloading voice models..."
        mkdir -p opencode/voices/models
        python3 -m piper.download_voices \
            en_US-lessac-medium \
            en_US-ryan-medium \
            en_US-amy-medium \
            en_GB-alan-medium
    fi

    # Update configuration
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
  "fallback_order": ["piper", "toast"],
  "default_provider": "piper"
}
EOF

    log_success "Piper TTS configured as primary voice provider"
}

# Setup ElevenLabs (premium option)
setup_elevenlabs() {
    log_info "Setting up ElevenLabs TTS (premium option)..."

    # Check for API key
    if [ -z "$ELEVENLABS_API_KEY" ]; then
        log_warning "ELEVENLABS_API_KEY not found in environment"
        echo "To use ElevenLabs:"
        echo "1. Get API key from https://elevenlabs.io"
        echo "2. Set: export ELEVENLABS_API_KEY=your_key"
        echo "3. Run: ./opencode/scripts/voice-setup.sh --elevenlabs"
        return 1
    fi

    # Update configuration to enable ElevenLabs
    if [ -f "opencode/voices/config.json" ]; then
        # Use jq if available, otherwise manual edit
        if command -v jq &> /dev/null; then
            jq '.providers.elevenlabs.enabled = true | .fallback_order = ["elevenlabs", "piper", "toast"] | .default_provider = "elevenlabs"' \
                opencode/voices/config.json > opencode/voices/config.json.tmp && \
                mv opencode/voices/config.json.tmp opencode/voices/config.json
        else
            # Manual configuration update
            sed -i.bak 's/"enabled": false/"enabled": true/g' opencode/voices/config.json
            sed -i.bak 's/"fallback_order": \["piper", "toast"\]/"fallback_order": ["elevenlabs", "piper", "toast"]/g' opencode/voices/config.json
            sed -i.bak 's/"default_provider": "piper"/"default_provider": "elevenlabs"/g' opencode/voices/config.json
        fi
    fi

    log_success "ElevenLabs TTS configured as primary voice provider"
}

# Setup hybrid (both providers)
setup_hybrid() {
    log_info "Setting up hybrid voice system (Piper + ElevenLabs)..."

    setup_piper

    if [ -n "$ELEVENLABS_API_KEY" ]; then
        setup_elevenlabs
    else
        log_info "ElevenLabs API key not found - configuring Piper-only with ElevenLabs ready"
        # Configuration already set for Piper primary with ElevenLabs ready
    fi

    log_success "Hybrid voice system configured"
}

# Test voice system
test_voice() {
    log_info "Testing voice system..."

    # Check if OpenCode is running (this would need to be implemented)
    log_info "Voice testing requires OpenCode to be running with PAI plugin loaded"
    log_info "Start OpenCode and run: pai_voice_test"
}

# Main function
main() {
    echo ""
    echo "🎤 PAI Voice Setup"
    echo "=================="
    echo ""

    case "${1:-status}" in
        "status")
            check_current_config
            ;;
        "piper")
            setup_piper
            ;;
        "elevenlabs")
            setup_elevenlabs
            ;;
        "hybrid")
            setup_hybrid
            ;;
        "test")
            test_voice
            ;;
        *)
            echo "Usage: $0 [status|piper|elevenlabs|hybrid|test]"
            echo ""
            echo "Commands:"
            echo "  status     - Show current voice configuration"
            echo "  piper      - Setup Piper TTS (free)"
            echo "  elevenlabs - Setup ElevenLabs TTS (premium)"
            echo "  hybrid     - Setup both providers"
            echo "  test       - Test voice system"
            exit 1
            ;;
    esac

    echo ""
    log_success "Voice setup complete!"
}

main "$@"