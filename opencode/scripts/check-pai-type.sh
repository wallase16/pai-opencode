#!/bin/bash

# PAI Installation Type Detector
# Helps identify which PAI version you're using

echo "🔍 PAI Installation Type Detector"
echo "=================================="
echo ""

# Check current directory
echo "📍 Current Directory: $(pwd)"
echo ""

# Check for PAI directories
echo "📂 PAI Directories Found:"
find /home/wallase16 -maxdepth 2 -name "*pai*" -type d 2>/dev/null | grep -v "/\." | sort
echo ""

# Determine installation type based on current directory
if [[ "$PWD" == *"pai-opencode-fork"* ]]; then
    echo "🎯 CURRENT DIRECTORY: PAI OpenCode Fork ✅"
    echo "   - Full OpenCode integration"
    echo "   - Piper TTS voice system"
    echo "   - One-click installation"
    echo "   - GitHub: https://github.com/wallase16/pai-opencode"
elif [[ "$PWD" == *"Personal_AI_Infrastructure"* ]]; then
    echo "🎯 CURRENT DIRECTORY: Original PAI (Claude Code) 📝"
    echo "   - Standard PAI installation"
    echo "   - ElevenLabs TTS (if configured)"
    echo "   - Claude Code integration"
elif [ -d ".claude" ]; then
    echo "🎯 CURRENT DIRECTORY: Some PAI Installation"
    echo "   - Contains PAI configuration"
    if [ -d "opencode" ]; then
        echo "   - Has OpenCode enhancements (likely fork)"
    else
        echo "   - Standard PAI setup"
    fi
else
    echo "🎯 CURRENT DIRECTORY: Not a PAI directory"
    echo "   - Navigate to a PAI directory to check type"
fi

echo ""
echo "🔧 Global PAI Status:"
if [ -f ~/.config/opencode/plugin/pai-core.ts ]; then
    echo "   ✅ PAI-Core plugin active in OpenCode"
else
    echo "   ❌ No PAI plugin found"
fi

if curl -s --max-time 2 http://localhost:5000/voices &>/dev/null; then
    echo "   ✅ Piper TTS voice server running"
else
    echo "   ❌ No voice server detected"
fi

echo ""
echo "🔧 System Components:"
echo "   OpenCode: $(command -v opencode &>/dev/null && echo '✅ Installed' || echo '❌ Not found')"
echo "   PAI Plugin: $([ -f ~/.config/opencode/plugin/pai-core.ts ] && echo '✅ Active' || echo '❌ Not found')"
echo "   Voice Server: $(curl -s --max-time 2 http://localhost:5000/voices &>/dev/null && echo '✅ Piper Running' || echo '❌ Not running')"
echo "   PAI Context: $([ -f ~/.config/opencode/rules.md ] && echo '✅ Loaded' || echo '❌ Not found')"

echo ""
echo "💡 Quick Commands:"
echo "   Check status: ./pai-status.sh (in fork directory)"
echo "   Test voice: curl -X POST -H 'Content-Type: application/json' -d '{\"text\":\"Hello\"}' http://localhost:5000"
echo "   Start PAI: opencode && pai_voice_test"