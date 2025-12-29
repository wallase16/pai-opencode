#!/usr/bin/env python3
"""
Mock Visual Generator
Creates a simple placeholder image with text overlay using PIL
"""

import os
from PIL import Image, ImageDraw, ImageFont


class VisualGeneratorMock:
    def __init__(self, output_dir: str):
        self.output_dir = output_dir
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_image(
        self, prompt: str, title: str, filename: str = "thumb_mock.png"
    ) -> str:
        """Generates a 1920x1080 placeholder image"""
        try:
            print(f"Generating mock image for: {title}")

            # Create a 1920x1080 image (Deep Blue background)
            img = Image.new("RGB", (1920, 1080), color=(10, 20, 50))
            d = ImageDraw.Draw(img)

            # Draw Title (Centered)
            # Default to default font if custom font not found
            try:
                # Try to find a system font or use default
                font = ImageFont.truetype("DejaVuSans-Bold.ttf", 60)
            except IOError:
                font = ImageFont.load_default()

            # Calculate text position (approximate center)
            # PIL default font doesn't support getsize nicely, so we just place it
            d.text((960, 540), title, fill=(255, 255, 255), anchor="mm", font=font)

            # Draw "Mock Mode" stamp
            d.text((50, 50), "MOCK VISUAL - PLACEHOLDER", fill=(200, 50, 50))

            # Save
            output_path = os.path.join(self.output_dir, filename)
            img.save(output_path)

            print(f"Image saved to: {output_path}")
            return output_path

        except Exception as e:
            print(f"Error generating mock image: {e}")
            return ""


if __name__ == "__main__":
    gen = VisualGeneratorMock(".")
    gen.generate_image("A cool vibe", "Test Song Title")
