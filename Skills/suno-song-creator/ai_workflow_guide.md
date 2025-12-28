# Suno Song Creator - AI Assistant Workflow

## Overview
This workflow demonstrates how the AI assistant should orchestrate song creation using chrome-mcp tools. The AI assistant calls the tools directly, while Python scripts handle data processing.

## Prerequisites
- Chrome browser running
- chrome-mcp tools available
- Active Suno account with credits

## Step-by-Step Workflow

### Step 1: Initialize and Check Environment
**AI Action:** Check for existing Suno tab
```
Call: mcp-chrome_get_windows_and_tabs
Look for tabs with "suno.com" in URL
If found, use existing tab
If not found, navigate to create new tab
```

### Step 2: Navigate to Suno Create Page
**AI Action:** Ensure we're on the create page
```
Call: mcp-chrome_chrome_navigate
URL: https://suno.com/create
newWindow: false (reuse existing if available)
```

### Step 3: Verify Login and Credits
**AI Action:** Check login status and account credits
```
Call: mcp-chrome_chrome_get_web_content
Parameters: {"textContent": true}

Check response for:
- "/login" or "/signin" in URL (not logged in)
- "Credits" text and extract number
- Error messages
```

### Step 4: Configure Custom Mode
**AI Action:** Ensure Custom mode is selected
```
Call: mcp-chrome_chrome_get_interactive_elements
Parameters: {"textQuery": "simple custom", "includeCoordinates": true}

Analyze elements to find:
- Which mode is currently active
- Coordinates of Custom button if needed

If Simple mode active:
Call: mcp-chrome_chrome_click_element
Parameters: {"coordinates": {"x": X, "y": Y}}  # Custom button coordinates
```

### Step 5: Fill Song Parameters
**AI Action:** Input lyrics and style
```
Call: mcp-chrome_chrome_get_interactive_elements
Parameters: {"includeCoordinates": true}

Identify textareas by:
- Tag name "textarea"
- Placeholder text analysis
- Position in DOM

For lyrics textarea:
Call: mcp-chrome_chrome_fill_or_select
Parameters: {"selector": "textarea:nth-of-type(1)", "value": "lyrics content"}

For style textarea:
Call: mcp-chrome_chrome_fill_or_select
Parameters: {"selector": "textarea:nth-of-type(2)", "value": "style description"}
```

### Step 6: Initiate Generation
**AI Action:** Click Create button
```
Call: mcp-chrome_chrome_get_interactive_elements
Parameters: {"textQuery": "create", "includeCoordinates": true}

Find Create button and:
Call: mcp-chrome_chrome_click_element
Parameters: {"coordinates": {"x": X, "y": Y}}
```

### Step 7: Monitor Generation Progress
**AI Action:** Poll for completion (30-60 seconds)
```
Loop with 5-second intervals:
Call: mcp-chrome_chrome_get_web_content
Parameters: {"textContent": true}

Check for:
- Song URLs ("/song/" pattern)
- Error messages
- Timeout after 60 seconds
```

### Step 8: Extract Results
**AI Action:** Get share links and download options
```
Call: mcp-chrome_chrome_get_web_content
Parameters: {"htmlContent": true}

Parse HTML for:
- href="/song/..." links
- Download button availability
- Song titles and metadata
```

### Step 9: Handle Downloads (Optional)
**AI Action:** Download generated songs
```
For each song URL:
Call: mcp-chrome_chrome_navigate
Parameters: {"url": "full song URL"}

Call: mcp-chrome_chrome_get_interactive_elements
Parameters: {"textQuery": "download", "includeCoordinates": true}

If download button found:
Call: mcp-chrome_chrome_click_element
Parameters: {"coordinates": {"x": X, "y": Y}}
```

## Error Handling

### Login Issues
- Detect redirect to login page
- Notify user to log in manually
- Provide clear error message

### Credit Issues
- Parse credit count from page
- Warn when credits are low (< 10)
- Fail gracefully when credits exhausted

### Generation Failures
- Detect error messages in page content
- Handle timeouts gracefully
- Provide retry suggestions

### Network Issues
- Handle connection timeouts
- Retry failed operations
- Provide connectivity troubleshooting

## Integration with Python Scripts

The AI assistant workflow integrates with Python scripts for:

1. **CSV Processing**: `csv_processor.py` handles bulk operations
2. **Data Validation**: Python validates inputs and formats
3. **Result Processing**: Python processes extracted links and metadata
4. **File Management**: Python handles download organization

## Example Implementation

```python
# Pseudo-code showing AI assistant integration
class SunoSongCreatorAI:
    def create_song(self, lyrics: str, style: str):
        # Step 1: Check environment
        tabs = self.call_tool("mcp-chrome_get_windows_and_tabs", {})
        suno_tab = self.find_suno_tab(tabs)

        # Step 2: Navigate if needed
        if not suno_tab:
            self.call_tool("mcp-chrome_chrome_navigate",
                         {"url": "https://suno.com/create", "newWindow": True})

        # Step 3: Verify login
        content = self.call_tool("mcp-chrome_chrome_get_web_content",
                               {"textContent": True})
        if self.is_login_page(content):
            raise Exception("Please log in to Suno first")

        # Continue with remaining steps...
        # (Fill forms, click buttons, monitor progress, extract results)
```

This workflow shows how the AI assistant orchestrates the entire process using chrome-mcp tools, with Python scripts handling supporting data operations.