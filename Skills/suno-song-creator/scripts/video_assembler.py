#!/usr/bin/env python3
"""
Video Assembler
Combines Image + Audio into MP4 using FFmpeg
"""

import os
import subprocess


class VideoAssembler:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def assemble_video(
        self, audio_path: str, image_path: str, output_filename: str
    ) -> str:
        """Combines MP3 and Image into MP4"""
        try:
            print(f"Assembling video: {output_filename}")

            output_path = os.path.join(self.output_dir, output_filename)

            # FFmpeg Command
            # -loop 1: Loop image
            # -i image_path: Input image
            # -i audio_path: Input audio
            # -c:v libx264: Video codec
            # -tune stillimage: Optimize for still image
            # -c:a aac: Audio codec
            # -b:a 192k: Audio bitrate
            # -pix_fmt yuv420p: Ensure compatibility
            # -shortest: Stop when audio ends

            # Use local ffmpeg binary path
            ffmpeg_bin = os.path.expanduser("~/bin/ffmpeg")

            cmd = [
                ffmpeg_bin,
                "-y",
                "-loop",
                "1",
                "-i",
                image_path,
                "-i",
                audio_path,
                "-c:v",
                "libx264",
                "-tune",
                "stillimage",
                "-c:a",
                "aac",
                "-b:a",
                "192k",
                "-pix_fmt",
                "yuv420p",
                "-shortest",
                output_path,
            ]

            # Run command
            subprocess.run(
                cmd, check=True, stdout=subprocess.DEVNULL, stderr=subprocess.PIPE
            )

            print(f"Video saved to: {output_path}")
            return output_path

        except subprocess.CalledProcessError as e:
            print(f"FFmpeg Error: {e.stderr.decode()}")
            return ""
        except Exception as e:
            print(f"Assembly Error: {e}")
            return ""


if __name__ == "__main__":
    # Test requires files, skip for now or mock
    pass
