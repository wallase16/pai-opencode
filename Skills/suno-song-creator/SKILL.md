---
name: Suno Song Creator
description: Create AI-generated songs on Suno.com, download MP3s, and copy share links
---

# Suno Song Creator Skill

This skill equips Claude with the ability to generate original music using Suno's AI platform, download the audio files, and provide shareable links using Chrome MCP browser automation.

## Available Workflows

### generate-song.md
**Purpose:** Create individual AI-generated songs
**Trigger:** "generate a song", "create music", "make a track"
**Process:** Single song creation with custom lyrics and style
**Location:** `workflows/generate-song.md`

### batch-process.md
**Purpose:** Process CSV files for bulk song generation
**Trigger:** "process CSV", "batch generate songs", "bulk music creation"
**Process:** Automated processing of multiple song prompts
**Location:** `workflows/batch-process.md`

### manage-downloads.md
**Purpose:** Organize and manage downloaded song files
**Trigger:** "manage downloads", "organize songs", "cleanup files"
**Process:** File organization, downloads, and cleanup
**Location:** `workflows/manage-downloads.md`

## Core Functionality

- **Song Generation**: Create songs from natural language prompts specifying style, mood, genre, and lyrics
- **File Download**: Automatically download generated MP3 files
- **Link Sharing**: Extract and copy public share URLs for songs

## Workflow

1. **Access Suno**: Navigate to https://suno.com/create (login required for full access)
2. **Switch to Custom Mode**: Use Custom mode for separate lyrics and style inputs
3. **Input Parameters**:
    - Lyrics: Actual song lyrics (verses, chorus, etc.)
    - Style: Genre and style description (e.g., "upbeat pop", "indie rock", "electronic")
    - Model: Song generation model ("v5" or "v4.5", default: "v5")
    - Additional options: Mood, instrumental settings, etc.
4. **Generate**: Submit and wait 30-60 seconds for 2 song variations
5. **Select & Download**: Choose preferred song, download MP3 file
6. **Share**: Copy the public URL (format: https://suno.com/song/{id})

## Chrome MCP Browser Automation

Uses chrome-mcp tools for browser automation (no Node.js/puppeteer dependencies):

1. **Navigate**: Use `chrome_navigate` to go to https://suno.com/create
2. **Login Check**: Use `chrome_get_web_content` to verify login status
3. **Switch Mode**: Use `chrome_click_element` on styles button for mode switching
4. **Fill Forms**:
   - Lyrics: `chrome_fill_or_select` on textarea selector
   - Styles: `chrome_fill_or_select` on styles textarea selector
   - Title: `chrome_fill_or_select` on title input (optional)
5. **Generate**: Use `chrome_click_element` on create button (aria-label="Create song")
6. **Monitor**: Use polling with `chrome_get_web_content` to wait for completion
7. **Extract Links**: Parse HTML content to find song URLs
8. **Download**: Navigate to song pages and trigger downloads

## Current Selectors (Updated 2025)

- **Lyrics Textarea**: `body > div:nth-of-type(1) > ... > textarea`
- **Styles Textarea**: `textarea[placeholder*="indie, electronic, synths"]`
- **Song Title Input**: `body > div:nth-of-type(1) > ... > input`
- **Create Button**: `button[aria-label="Create song"]`

## Error Handling

- Check for login prompts or rate limits
- Handle generation timeouts
- Verify song creation success
- Ensure downloads and shares work for both songs

## Limitations

- Requires Chrome browser access and Suno login
- Free tier: ~10 songs/month (based on account showing 2,355 credits)
- Generation time: 30-60 seconds
- Dependent on site UI changes (element detection may need updates)
- Simple vs Custom mode affects available features
- Create button validation logic may change
- Uses polling for completion detection (less efficient than events)
- Requires chrome-mcp tools to be available

## Resources

For detailed workflows: `ls workflows/`
For implementation scripts: `ls scripts/`
For templates and examples: `ls assets/`
For comprehensive guide: `read CLAUDE.md`

## Implementation

- **Primary Script**: `suno_chrome_creator.py` - Python script using chrome-mcp tools
- **Legacy Script**: `suno_automation.js` - Original Node.js/puppeteer implementation (deprecated)
- **Testing**: Run `python3 suno_chrome_creator.py "lyrics" "style"` for basic testing

## Testing

Run `python3 suno_chrome_creator.py` to test the Chrome MCP implementation. The automation uses chrome-mcp tools for reliable browser interaction without external dependencies.</content>
<parameter name="filePath">suno-song-creator/SKILL.md