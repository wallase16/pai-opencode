#!/usr/bin/env python3
"""
Visual Generator - Gemini API Version
Generates images using Google's Generative AI
"""

import os
import sys
import base64
import json
import requests


class VisualGeneratorGemini:
    def __init__(self, output_dir: str, api_key: str):
        self.output_dir = output_dir
        self.api_key = api_key
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)

    def generate_image(
        self, prompt: str, title: str, filename: str = "thumb.png"
    ) -> str:
        """Generates an image via Gemini/Imagen API"""
        try:
            print(f"Generating Gemini image for: {title}")
            print(f"Prompt: {prompt}")

            # API Endpoint for Imagen 4
            # Updated based on ListModels response: models/imagen-4.0-generate-001

            url = f"https://generativelanguage.googleapis.com/v1beta/models/imagen-4.0-generate-001:predict?key={self.api_key}"

            # Request Body
            # Imagen 4 might require different parameters, but standard predict often accepts 'instances'
            data = {
                "instances": [{"prompt": prompt}],
                "parameters": {"sampleCount": 1, "aspectRatio": "16:9"},
            }

            # Execute
            response = requests.post(url, json=data)

            if response.status_code != 200:
                print(f"Gemini API Error {response.status_code}: {response.text}")
                return ""

            # Parse Response
            # Expected: {"predictions": [{"bytesBase64Encoded": "..."}]}
            result = response.json()
            predictions = result.get("predictions", [])

            if not predictions:
                print("No predictions returned")
                return ""

            b64_data = predictions[0].get("bytesBase64Encoded", "")
            if not b64_data:
                # Try alternate format just in case
                b64_data = predictions[0].get("image", {}).get("bytesBase64Encoded", "")

            if not b64_data:
                print("No image data found in response")
                return ""

            # Decode and Save
            img_data = base64.b64decode(b64_data)
            output_path = os.path.join(self.output_dir, filename)

            with open(output_path, "wb") as f:
                f.write(img_data)

            print(f"Image saved to: {output_path}")
            return output_path

        except Exception as e:
            print(f"Error generating Gemini image: {e}")
            return ""


if __name__ == "__main__":
    # Test
    key = os.environ.get("GEMINI_API_KEY", "")
    if key:
        gen = VisualGeneratorGemini(".", key)
        gen.generate_image("A futuristic city", "Test City")
    else:
        print("Set GEMINI_API_KEY to test")
