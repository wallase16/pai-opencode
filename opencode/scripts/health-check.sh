#!/bin/bash

# PAI OpenCode Health Check Script
# Verifies that all PAI components are properly installed and running

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m'

# Status counters
CHECKS_TOTAL=0
CHECKS_PASSED=0

check() {
    local name="$1"
    local command="$2"
    local expected_exit=${3:-0}

    ((CHECKS_TOTAL++))

    echo -n "Checking $name... "

    if eval "$command" > /dev/null 2>&1; then
        if [ $? -eq $expected_exit ]; then
            echo -e "${GREEN}✅ PASSED${NC}"
            ((CHECKS_PASSED++))
            return 0
        fi
    fi

    echo -e "${RED}❌ FAILED${NC}"
    return 1
}

echo ""
echo "🔍 PAI OpenCode Health Check"
echo "============================"
echo ""

# Core Components
echo "Core Components:"
echo "----------------"
check "OpenCode Installation" "command -v opencode"
check "PAI-Core Plugin" "[ -f \"$HOME/.config/opencode/plugin/pai-core.ts\" ]"
check "PAI Context" "[ -f \"$HOME/.config/opencode/rules.md\" ]"

# Voice System
echo ""
echo "Voice System:"
echo "-------------"
check "Python 3.8+" "python3 -c 'import sys; sys.exit(0 if sys.version_info >= (3, 8) else 1)'"
check "Piper TTS" "[ -f \"$HOME/.pai-venv/bin/piper\" ]"
check "Voice Models Directory" "[ -d \"opencode/voices/models\" ]"
check "Voice Models Downloaded" "[ \"\$(ls -A opencode/voices/models 2>/dev/null)\" ]"
check "Voice Configuration" "[ -f \"opencode/voices/config.json\" ]"
check "Piper Server Running" "curl -s --max-time 2 http://localhost:5000/voices"

# PAI Skills
echo ""
echo "PAI Skills:"
echo "-----------"
check "CORE Skill" "[ -f \".claude/skills/CORE/SKILL.md\" ]"
check "Skills Directory" "[ -d \".claude/skills\" ]"
check "Skills Available" "[ \"\$(find .claude/skills -name \"SKILL.md\" | wc -l)\" -gt 0 ]"

# History System
echo ""
echo "History System:"
echo "---------------"
check "History Directory" "[ -d \".claude/history\" ]"
check "Sessions Directory" "[ -d \".claude/history/sessions\" ]"
check "Learnings Directory" "[ -d \".claude/history/learnings\" ]"

# Summary
echo ""
echo "Summary:"
echo "--------"
echo "Checks passed: $CHECKS_PASSED / $CHECKS_TOTAL"

if [ $CHECKS_PASSED -eq $CHECKS_TOTAL ]; then
    echo -e "${GREEN}🎉 All checks passed! PAI OpenCode is fully operational.${NC}"
    echo ""
    echo "Next steps:"
    echo "• Run: opencode"
    echo "• Try: use_skill brainstorming"
    echo "• Test voice: pai_voice_test"
    exit 0
elif [ $CHECKS_PASSED -ge $(($CHECKS_TOTAL * 3 / 4)) ]; then
    echo -e "${YELLOW}⚠️  Most checks passed. PAI OpenCode should work but some features may be limited.${NC}"
    exit 1
else
    echo -e "${RED}❌ Critical issues detected. Please run the install script again.${NC}"
    echo ""
    echo "Troubleshooting:"
    echo "• Re-run: ./opencode/scripts/install.sh"
    echo "• Check logs in opencode/voices/piper-server.log"
    exit 1
fi