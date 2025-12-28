---
name: generate-song
description: Create a single AI-generated song using Suno with custom lyrics and style via chrome-mcp browser automation
---

# Generate Single Song Workflow

## When to Activate
- User wants to create one specific song
- "generate a song", "create music", "make a track"
- Testing song generation functionality
- Quick music creation requests

## Prerequisites
- Chrome browser running
- chrome-mcp tools available
- Active Suno account with credits
- Internet connection

## Workflow Steps

### Step 1: Environment Check
**AI Action:** Verify chrome-mcp tools and browser access
```
Check: chrome-mcp tools responsive
Verify: Chrome browser running
Confirm: Network connectivity
```

### Step 2: Suno Tab Management
**AI Action:** Find or open Suno create page
```
Call: mcp-chrome_get_windows_and_tabs
If Suno tab exists: switch to it
If not: navigate to https://suno.com/create
```

### Step 3: Authentication Verification
**AI Action:** Check login status and credits
```
Call: mcp-chrome_chrome_get_web_content {"textContent": true}
Check: Current URL (not login page)
Parse: Credit count from page
Warn: If credits < 10
```

### Step 4: Mode Configuration
**AI Action:** Ensure Custom mode selected
```
Call: mcp-chrome_chrome_get_interactive_elements {"textQuery": "simple custom"}
Analyze: Current mode state
If Simple active: Click Custom button
```

### Step 5: Input Population
**AI Action:** Scroll to form, then fill lyrics, styles, and title fields
```
Call: mcp-chrome_chrome_keyboard {"keys": "PageDown"}  # Scroll to make form visible
Wait: 1 second for scroll completion
Call: mcp-chrome_chrome_fill_or_select {"selector": "lyrics_textarea_selector", "value": lyrics}
Call: mcp-chrome_chrome_fill_or_select {"selector": "styles_textarea_selector", "value": style}
Call: mcp-chrome_chrome_fill_or_select {"selector": "song_title_input_selector", "value": title} (optional)
```

### Step 6: Generation Initiation
**AI Action:** Click Create button using updated selector
```
Call: mcp-chrome_chrome_click_element {"selector": "button[aria-label=\"Create song\"]"}
```

### Step 7: Progress Monitoring
**AI Action:** Wait for generation completion
```
Poll every 5 seconds for 60 seconds:
Call: mcp-chrome_chrome_get_web_content {"textContent": true}
Check: Song URLs present
Check: Error messages
Timeout: After 60 seconds
```

### Step 8: Result Extraction
**AI Action:** Extract top 2 most recent share links
```
Call: mcp-chrome_chrome_get_web_content {"htmlContent": true}
Parse: Song URLs (/song/ pattern)
Extract: Top 2 most recent songs only (per Suno workflow)
Note: Suno puts most recently generated songs at the top
Return: 2 share links and status
```

### Step 9: Download Handling (Optional)
**AI Action:** Download generated songs
```
For each song URL:
Navigate to song page
Find download button
Trigger download
```

## Error Handling

### Authentication Errors
- **Detection:** Redirect to login page
- **Action:** Notify user to log in manually
- **Message:** "Please log in to Suno.com first"

### Credit Issues
- **Detection:** Low credit count or generation blocked
- **Action:** Show current credit balance
- **Message:** "Insufficient credits. Current balance: X"

### Generation Failures
- **Detection:** Error messages in page content
- **Action:** Extract and display error
- **Recovery:** Suggest retry or check account status

### Timeout Issues
- **Detection:** No completion after 60 seconds
- **Action:** Check network and account status
- **Recovery:** Suggest manual verification

## Success Criteria
- ✅ Top 2 most recent song URLs extracted
- ✅ No error messages
- ✅ Generation completed within timeout
- ✅ Share links functional
- ✅ Follows Suno workflow (top 2 songs only)

## Output Format
```
🎵 Song Generation Complete!
📀 Share Links (Top 2 Recent):
   • https://suno.com/song/abc123
   • https://suno.com/song/def456
🎯 Style: upbeat pop
📝 Lyrics: [preview]
⏱️ Duration: 45 seconds
📋 Note: Per Suno workflow, only the 2 most recently generated songs are extracted
```

## Integration Points
- **Scripts:** `scripts/suno_chrome_creator.py` (data processing)
- **Assets:** `assets/lyrics-templates.md` (input examples)
- **Related:** `workflows/batch-process.md` (bulk operations)