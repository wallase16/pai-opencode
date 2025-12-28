---
name: batch-process
description: Process CSV files containing multiple song prompts for bulk AI music generation using chrome-mcp automation
---

# Batch Song Processing Workflow

## When to Activate
- User has CSV file with multiple song prompts
- "process CSV", "batch generate songs", "bulk music creation"
- Multiple songs needed from structured data
- Automated playlist creation

## Prerequisites
- CSV file with required columns:
  - "Suno Genre And Style Prompt"
  - "Suno Share Link" (initially empty)
- Chrome browser running
- chrome-mcp tools available
- Sufficient Suno credits for batch size
- Python 3.x for CSV processing

## Workflow Steps

### Step 1: CSV Validation
**AI Action:** Analyze CSV structure and content
```
Run: python3 scripts/csv_processor.py read-prompts input.csv
Validate: Required columns present
Count: Songs needing generation
Estimate: Total credits required
Check: File permissions and access
```

### Step 2: Batch Planning
**AI Action:** Plan generation sequence
```
Analyze: Song complexity and estimated times
Calculate: Total duration (30-60s per song)
Check: Account credit sufficiency
Plan: Error recovery strategy
```

### Step 3: Sequential Processing
**AI Action:** Process each song in the CSV
```
For each row with empty share link:
   1. Extract prompt from CSV
   2. Call generate-song workflow
   3. Capture resulting share link
   4. Update CSV with link
   5. Log progress and any errors
```

### Step 4: Progress Tracking
**AI Action:** Monitor and report batch progress
```
Track: Songs completed vs total
Report: Success rate and errors
Update: Real-time progress indicators
Handle: Interruptions gracefully
```

### Step 5: Result Compilation
**AI Action:** Generate batch summary
```
Compile: All generated share links
Create: Success/failure report
Update: CSV with all results
Archive: Processing logs
```

## CSV Format Requirements

### Required Columns
```csv
Title,Suno Genre And Style Prompt,Suno Share Link,Notes
My First Song,upbeat pop,,
Love Song,romantic ballad,,
Rock Anthem,alternative rock,,
```

### Processing Logic
- **Read:** "Suno Genre And Style Prompt" column for input
- **Write:** "Suno Share Link" column with results
- **Skip:** Rows where share link already exists
- **Log:** Processing status in Notes column

## Error Handling

### CSV Format Errors
- **Detection:** Missing required columns
- **Action:** Show available columns, suggest fixes
- **Recovery:** Guide user to correct CSV format

### Credit Exhaustion
- **Detection:** Generation blocked mid-batch
- **Action:** Pause processing, show remaining credits
- **Recovery:** Resume after credit renewal or reduce batch size

### Network Interruptions
- **Detection:** Connection failures during processing
- **Action:** Retry failed songs, track retry attempts
- **Recovery:** Resume from last successful song

### Account Limits
- **Detection:** Rate limiting or daily limits hit
- **Action:** Calculate cooldown period
- **Recovery:** Schedule resumption after limits reset

## Performance Optimization

### Batch Sizing
- **Recommended:** 5-10 songs per batch initially
- **Monitoring:** Adjust based on success rate
- **Scaling:** Increase size for stable connections

### Timing Controls
- **Inter-song delay:** 5-10 seconds between generations
- **Timeout handling:** 60-second limit per song
- **Retry logic:** Up to 3 attempts per song

## Output Format

### Progress Updates
```
📊 Batch Processing: Song 3 of 10
✅ Song "Love Ballad" completed
🔗 Link: https://suno.com/song/abc123
⏱️ Elapsed: 2m 30s | Remaining: ~4m
```

### Final Summary
```
🎵 Batch Processing Complete!
📊 Results: 8/10 songs generated successfully
✅ Successful: 8 songs
❌ Failed: 2 songs (credit limit reached)
📁 Updated CSV: songs_with_links.csv
💾 Downloads: 6/8 songs downloaded
```

## Integration Points
- **Scripts:** `scripts/csv_processor.py` (CSV handling)
- **Assets:** `assets/csv-template.csv` (format example)
- **Related:** `workflows/generate-song.md` (individual song creation)
- **Related:** `workflows/manage-downloads.md` (file organization)