# Browser Automation Guide for Suno Song Creation

## Prerequisites
- Chrome browser with automation tools
- Suno account logged in
- Sufficient credits (free tier: ~10/month)

## Step-by-Step Automation

### 1. Navigate to Create Page
- URL: https://suno.com/create
- Ensure page loads completely
- Account must be logged in with sufficient credits

### 2. Switch to Custom Mode (Critical)
- Default mode is "Simple" which has combined prompt input
- Locate mode toggle buttons (Simple/Custom)
- Click "Custom" button to enable separate lyrics and style inputs
- Selector: Find buttons with text "Simple" and "Custom", click the Custom one

### 3. Fill Lyrics
- Locate lyrics textarea (usually has placeholder about writing lyrics)
- Fill with the actual song lyrics (verses, chorus, etc.)
- Dispatch 'input' and 'change' events after filling

### 4. Fill Style/Genre
- Locate style textarea/input (usually has placeholder like "indie, electronic, synths")
- Fill with genre and style description (e.g., "upbeat pop", "indie rock")
- Dispatch 'input' and 'change' events after filling

### 5. Verify Create Button State
- Create button remains disabled until all requirements are met
- Check button.disabled property before attempting to click
- In Custom mode, both lyrics and style fields are typically required

### 5. Initiate Generation
- Find "Create" button using text search: `btn.textContent.includes('Create')`
- Button may show loading state during generation
- Click to start generation process

### 5. Wait for Completion
- Wait 20 seconds for generation progress
- Monitor page for new song elements
- Generation takes 30-60 seconds total, but check after 20s for access
- Look for song duration indicators (e.g., "0:18v4.5+")

### 6. Download Song
- Locate download button on song card
- May require premium for full downloads
- Click to save MP3 file

### 7. Identify Recent Songs
- After generation, locate the two newest songs (by timestamp or position)
- Use library view or results panel to find them

### 8. Download Each Song
- For each recent song, click download button
- Save MP3 files with descriptive names

### 9. Get Share Links for Both (Using Direct Navigation)
- Identify the two latest generated songs (always the top two in the library/results page)
- Confirm they have duplicate song titles (variations of the same prompt)
- Parse the page HTML to extract the href attributes of the top two song links
- Navigate directly to each URL in new tabs
- Extract unique share URLs from the new tab addresses
- Close the song tabs
- Return to the create tab for continued use
- Do not process any other songs

## Error Scenarios
- **Not Logged In**: Redirect to login page
- **No Credits**: Show upgrade prompt with credit count
- **Create Button Disabled**: Check if in Custom mode, verify both lyrics and style are filled
- **Wrong Mode Selected**: Simple mode has combined input, switch to Custom mode for separate fields
- **Missing Lyrics**: Lyrics field is required in Custom mode
- **Missing Style**: Style/genre field is required in Custom mode
- **Generation Failed**: Timeout after 60 seconds, check for error messages
- **Download Blocked**: Premium feature, check account status
- **Multiple Songs Not Found**: Handle case where fewer than 2 songs generated
- **Element Not Found**: UI changes frequently, use text-based selectors instead of CSS paths

## Modal Parsing Details
- After clicking share, locate modal container (often with class like "modal" or "dialog")
- Find input field or link element containing the URL (e.g., selector: .modal input[type="text"] or .modal a)
- Extract the value or href attribute
- Example: Use get_web_content or get_interactive_elements on modal to find URL

## Selectors (Dynamic - Use Text/Content Matching)
- Mode buttons: Find buttons containing "Simple" or "Custom" text
- Lyrics textarea: Find textarea with placeholder containing "lyrics" or "write"
- Style textarea: Find textarea with placeholder containing "style", "genre", or "indie, electronic"
- Create button: Find button with `textContent.includes('Create')`
- Model selector: Find button with text "v5" or "v4.5"
- Share buttons: Find buttons with text "Share" or similar
- Download buttons: Find buttons with download icons or "Download" text

**Critical**: Avoid using complex CSS selectors as they change frequently. Use text content, element type, and position-based selection instead.</content>
<parameter name="filePath">suno-song-creator/browser_automation_guide.md