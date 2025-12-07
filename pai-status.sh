#!/bin/bash

# Simple PAI Status Check for Bash
echo "🎵 PAI OpenCode Status Check"
echo "============================"

echo ""
echo "1. OpenCode Installation:"
if command -v opencode &> /dev/null; then
    echo "   ✅ Found: $(which opencode)"
    echo "   ✅ Version: $(opencode --version 2>/dev/null || echo 'unknown')"
else
    echo "   ❌ Not found"
fi

echo ""
echo "2. PAI Plugin:"
if [ -f ~/.config/opencode/plugin/pai-core.ts ]; then
    echo "   ✅ Installed: ~/.config/opencode/plugin/pai-core.ts"
    echo "   ✅ Size: $(stat -f%z ~/.config/opencode/plugin/pai-core.ts 2>/dev/null || stat -c%s ~/.config/opencode/plugin/pai-core.ts 2>/dev/null) bytes"
else
    echo "   ❌ Not found"
fi

echo ""
echo "3. Voice Server:"
if curl -s --max-time 3 http://localhost:5000/voices &> /dev/null; then
    echo "   ✅ Running on localhost:5000"
    echo "   ✅ Piper TTS active"
else
    echo "   ❌ Not responding"
fi

echo ""
echo "4. PAI Context:"
if [ -f ~/.config/opencode/rules.md ]; then
    echo "   ✅ Loaded: ~/.config/opencode/rules.md"
else
    echo "   ❌ Not found"
fi

echo ""
echo "🎯 Quick Voice Test:"
echo "   Run: curl -X POST -H 'Content-Type: application/json' -d '{\"text\": \"Hello from PAI\"}' http://localhost:5000 > test.wav"
echo "   Play: aplay test.wav (if aplay available)"

echo ""
echo "🚀 To use PAI in OpenCode:"
echo "   opencode"
echo "   pai_voice_test"
echo "   use_skill brainstorming"