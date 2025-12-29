# Bible Verse Song Automation Plan

## Input Source
- **File**: `youtube-bible-verse-plan11092025.csv`
- **Structure**:
    - `Date`: Scheduled release date (e.g., `2025-11-08`)
    - `Suno Genre And Style Prompt`: e.g., "Uplifting Christian R&B..."
    - `Full Bible Verse Text`: Lyrics content.
    - `You Tube Thumbnail Concept`: Detailed prompt for image generation.
    - `You Tube Title` / `Video Description`: Metadata for upload.
    - `Status`: Track progress (e.g., "Planned", "Generated", "Uploaded").

## Pipeline Architecture

### Step 1: Song Generation (Suno)
- **Input**: `Full Bible Verse Text` (Lyrics), `Suno Genre And Style Prompt` (Style).
- **Action**: Use `suno_chrome_creator.py` (Batch Mode) to generate the song.
- **Output**: MP3 file + `Suno Share Link` updated in CSV.

### Step 2: Thumbnail Generation (AI Art)
- **Input**: `You Tube Thumbnail Concept`.
- **Action**: Use an AI Image Generator (e.g., DALL-E 3 via API or Midjourney via Discord automation if feasible, or potentially Flux/Stable Diffusion locally if hardware allows).
- **Output**: JPG/PNG file (1920x1080).

### Step 3: Video Assembly (FFmpeg)
- **Input**: MP3 (Audio) + JPG (Image).
- **Action**: `ffmpeg -loop 1 -i thumb.jpg -i song.mp3 -c:v libx264 -c:a aac -b:a 192k -shortest output.mp4`
- **Output**: MP4 video file.

### Step 4: YouTube Upload
- **Input**: MP4, Title, Description, Tags.
- **Action**:
    - **Option A (Browser Automation)**: Use Selenium/Playwright to log into YouTube Studio and upload. (No quota limits, but fragile).
    - **Option B (API)**: Use official YouTube Data API. (Reliable, but requires quota management).
- **Scheduling**: Set visibility to `Scheduled` based on the `Date` column.

## Decision Points for User
1.  **Image Generator**: Which tool do you prefer? (DALL-E 3 is easiest via API; Midjourney is best quality but hardest to automate; Flux is free if local).
2.  **Upload Method**: Browser Automation (Free/Unlimited) or API (Stable/Limited)?

## Recommendation
Build a `master_controller.py` that iterates the CSV rows:
1.  Checks `Status`.
2.  If `Planned` -> Calls Suno -> Updates Status to `Song Generated`.
3.  If `Song Generated` -> Calls Image Gen -> Updates Status to `Image Generated`.
4.  If `Image Generated` -> Calls FFmpeg -> Updates Status to `Video Ready`.
5.  If `Video Ready` -> Calls Uploader -> Updates Status to `Scheduled`.
