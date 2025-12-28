#!/bin/bash
set -e

# PAI Adapter Setup Script
# Implements logic to set up and verify the PAI Adapter environment.

# 1. Generate settings.json from template if missing
if [ ! -f "settings.json" ]; then
  if [ -f "opencode/config/settings.template.json" ]; then
    echo "Creating settings.json from template..."
    cp opencode/config/settings.template.json settings.json
  else
    echo "Error: opencode/config/settings.template.json not found!"
    exit 1
  fi
else
  echo "settings.json already exists."
fi

# 2. Verify Skills/ directory exists
if [ -d "Skills" ]; then
  echo "Skills/ directory verified."
else
  echo "Error: Skills/ directory not found!"
  exit 1
fi

# 3. Verify opencode/plugin/pai-adapter.ts exists
if [ -f "opencode/plugin/pai-adapter.ts" ]; then
  echo "opencode/plugin/pai-adapter.ts verified."
else
  echo "Error: opencode/plugin/pai-adapter.ts not found!"
  exit 1
fi

echo "PAI Adapter setup verification complete."
