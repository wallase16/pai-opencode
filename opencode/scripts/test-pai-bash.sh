#!/bin/bash

# PAI OpenCode Bash Testing Script
# Test PAI functions directly from bash terminal

set -e

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🎵 PAI OpenCode Bash Testing Script${NC}"
echo "=================================="

# Function to test voice
test_voice() {
    echo -e "\n${YELLOW}🗣️  Testing Voice System...${NC}"

    local test_text="PAI voice test from bash terminal"
    local output_file="/tmp/pai_voice_test_$(date +%s).wav"

    echo "Generating audio: '$test_text'"

    if curl -s -X POST \
         -H 'Content-Type: application/json' \
         -d "{\"text\": \"$test_text\"}" \
         http://localhost:5000 > "$output_file"; then

        local file_size=$(stat -f%z "$output_file" 2>/dev/null || stat -c%s "$output_file" 2>/dev/null)
        echo -e "${GREEN}✅ Voice test successful!${NC}"
        echo "   Audio file: $output_file (${file_size} bytes)"

        # Try to play it
        if command -v aplay &> /dev/null; then
            echo "   Playing audio..."
            timeout 10 aplay "$output_file" 2>/dev/null || echo "   Audio playback completed"
        elif command -v paplay &> /dev/null; then
            echo "   Playing audio..."
            timeout 10 paplay "$output_file" 2>/dev/null || echo "   Audio playback completed"
        else
            echo "   Audio saved - play manually: aplay $output_file"
        fi
    else
        echo -e "${RED}❌ Voice test failed${NC}"
        return 1
    fi
}

# Function to check PAI status
check_status() {
    echo -e "\n${YELLOW}📊 Checking PAI Status...${NC}"

    local checks_passed=0
    local total_checks=0

    # Check OpenCode
    ((total_checks++))
    if command -v opencode &> /dev/null; then
        echo -e "${GREEN}✅ OpenCode installed${NC} ($(opencode --version 2>/dev/null || echo 'unknown version'))"
        ((checks_passed++))
    else
        echo -e "${RED}❌ OpenCode not found${NC}"
    fi

    # Check PAI plugin
    ((total_checks++))
    if [ -f ~/.config/opencode/plugin/pai-core.ts ]; then
        echo -e "${GREEN}✅ PAI-Core plugin installed${NC}"
        ((checks_passed++))
    else
        echo -e "${RED}❌ PAI-Core plugin missing${NC}"
    fi

    # Check voice server
    ((total_checks++))
    if curl -s --max-time 5 http://localhost:5000/voices &> /dev/null; then
        echo -e "${GREEN}✅ Voice server running${NC} (Piper TTS active)"
        ((checks_passed++))
    else
        echo -e "${RED}❌ Voice server not responding${NC}"
    fi

    # Check PAI context
    ((total_checks++))
    if [ -f ~/.config/opencode/rules.md ]; then
        echo -e "${GREEN}✅ PAI context loaded${NC}"
        ((checks_passed++))
    else
        echo -e "${RED}❌ PAI context missing${NC}"
    fi

    echo -e "\n${BLUE}Status: $checks_passed/$total_checks checks passed${NC}"

    if [ $checks_passed -eq $total_checks ]; then
        echo -e "${GREEN}🎉 PAI OpenCode is fully operational!${NC}"
        return 0
    else
        echo -e "${YELLOW}⚠️  Some components may need attention${NC}"
        return 1
    fi
}

# Function to test different voices
test_voices() {
    echo -e "\n${YELLOW}🎭 Testing Different Voices...${NC}"

    local voices=("en_US-lessac-medium" "en_US-ryan-medium" "en_US-amy-medium" "en_GB-alan-medium")

    for voice in "${voices[@]}"; do
        echo "Testing voice: $voice"
        local output_file="/tmp/pai_voice_${voice}_test.wav"

        if curl -s -X POST \
             -H 'Content-Type: application/json' \
             -d "{\"text\": \"Hello from $voice\", \"voice\": \"$voice\"}" \
             http://localhost:5000 > "$output_file"; then
            echo -e "${GREEN}  ✅ $voice: Success${NC}"
        else
            echo -e "${RED}  ❌ $voice: Failed${NC}"
        fi
    done
}

# Main script
case "${1:-all}" in
    "voice")
        test_voice
        ;;
    "status")
        check_status
        ;;
    "voices")
        test_voices
        ;;
    "all")
        check_status
        test_voice
        test_voices
        ;;
    *)
        echo "Usage: $0 [voice|status|voices|all]"
        echo ""
        echo "Commands:"
        echo "  voice   - Test voice generation"
        echo "  status  - Check PAI system status"
        echo "  voices  - Test different voice models"
        echo "  all     - Run all tests (default)"
        exit 1
        ;;
esac

echo -e "\n${BLUE}🎯 Testing complete!${NC}"
echo ""
echo "To use PAI in OpenCode:"
echo "  opencode"
echo "  pai_voice_test"
echo "  use_skill brainstorming"