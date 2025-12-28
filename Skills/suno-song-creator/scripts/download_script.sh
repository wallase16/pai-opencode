#!/bin/bash

# Suno Song Download Script
# Usage: ./download_script.sh <audio_url> <song_id>

AUDIO_URL=$1
SONG_ID=$2

if [ -z "$AUDIO_URL" ]; then
    echo "Error: Audio URL required"
    exit 1
fi

# Download MP3
FILENAME="suno_song_${SONG_ID}.mp3"
curl -L -o "$FILENAME" "$AUDIO_URL"

if [ $? -eq 0 ]; then
    echo "Downloaded: $FILENAME"
else
    echo "Download failed"
    exit 1
fi

# Copy share link to clipboard (if xclip available)
SHARE_LINK="https://suno.com/song/${SONG_ID}"
if command -v xclip &> /dev/null; then
    echo "$SHARE_LINK" | xclip -selection clipboard
    echo "Share link copied to clipboard: $SHARE_LINK"
else
    echo "Share link: $SHARE_LINK"
fi