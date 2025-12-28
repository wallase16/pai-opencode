#!/bin/bash

# Suno Song Creator Test Script
# This script demonstrates how to use the Chrome MCP automation

echo "Suno Song Creator - Chrome MCP Test Script"
echo "==========================================="

# Check if Python3 is available
if ! command -v python3 &> /dev/null; then
    echo "Error: Python3 is required to run the automation script"
    echo "Please install Python3"
    exit 1
fi

echo ""
echo "Usage Examples:"
echo "==============="
echo ""
echo "1. Generate a song with default lyrics and style:"
echo "   python3 suno_chrome_creator.py"
echo ""
echo "2. Generate a song with custom lyrics and style:"
echo "   python3 suno_chrome_creator.py \"Verse 1: Walking down the sunny street\nChorus: Summer days are here to stay\" \"upbeat pop\""
echo ""
echo "3. Show help and options:"
echo "   python3 suno_chrome_creator.py --help"
echo ""
echo "Requirements:"
echo "- Chrome browser running"
echo "- chrome-mcp tools available"
echo "- Active Suno account with credits"
echo "- Internet connection"
echo ""
echo "The automation will:"
echo "- Find or open suno.com/create in Chrome"
echo "- Check login status"
echo "- Ensure Custom mode is selected"
echo "- Fill the lyrics textarea with song lyrics"
echo "- Fill the style field with genre description"
echo "- Generate the song (30-60 seconds)"
echo "- Extract share links"
echo ""
echo "Note: This uses chrome-mcp tools instead of puppeteer for browser automation."