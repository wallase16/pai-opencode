# Bible Verse Song Automation Plan (v2)

## Goal
Automate the daily creation and release of Bible verse songs to YouTube and Podcast platforms.

## Core Strategy
1.  **Creation**: Script generates Song (Suno) + Visuals (AI Art) -> Combined into Video (FFmpeg).
2.  **Protection**: Register song with **DistroKid** (Content ID) to protect copyright and enable monetization.
3.  **Distribution**:
    *   **YouTube**: Upload video for visual audience.
    *   **RSS Feed**: Update XML feed for podcast platforms (Spotify/Apple Podcasts).

## Detailed Pipeline

### Step 1: Song Generation (Suno)
*   **Input**: CSV Row (Lyrics, Style).
*   **Action**: Batch generate via `suno_chrome_creator.py`.
*   **Output**: MP3 File.

### Step 2: Content Protection (DistroKid) - *New*
*   **Why**: Prevents others from stealing your song and flagging *you*. Enables YouTube Content ID so *you* get paid for views.
*   **Action**:
    *   *Manual Mode (Recommended)*: You manually upload the batch of MP3s to DistroKid once a week.
    *   *Automation*: DistroKid has no public API. Automation would require brittle browser scripts.
    *   **Decision**: Is manual weekly upload acceptable, or do you need full automation here?

### Step 3: Visuals & Assembly
*   **Visual**: Generate Thumbnail (DALL-E 3 / Midjourney).
*   **Video**: Combine MP3 + JPG -> MP4 (FFmpeg).

### Step 4: Distribution A - YouTube
*   **Action**: Browser automation uploads MP4 to YouTube Studio.
*   **Schedule**: Set release date from CSV.

### Step 5: Distribution B - Podcast RSS - *New*
*   **Action**:
    1.  Upload MP3 to a hosting location (e.g., S3 bucket, GitHub Pages, or a dedicated host).
    2.  Update `podcast.xml` (RSS Feed) with new episode details (Title, MP3 URL, Description).
    3.  Commit/Push updated XML to host.
*   **Result**: Spotify/Apple Podcasts automatically pick up the new "episode".

## Key Questions for You
1.  **DistroKid Automation**: Since they don't have an API, are you okay with a **"Manual Hand-off"** step? (e.g., Script generates 7 songs, you drag-and-drop them to DistroKid once a week).
    *   *Alternative*: We try to automate the browser click-path, but it's risky with financial accounts.
2.  **Hosting for RSS**: Where should the MP3 files live for the Podcast feed?
    *   A) **GitHub Pages**: Free, easy, but file size limits (100MB max, fine for MP3s).
    *   B) **AWS S3**: Cheap, reliable, standard industry practice.
    *   C) **Anchor/Spotify for Podcasters**: Free, handles hosting, but manual upload (unless we automate browser).

*My Recommendation*:
*   **DistroKid**: Manual weekly upload (Safe).
*   **RSS**: GitHub Pages (Free/Easy) or S3 (Professional).
