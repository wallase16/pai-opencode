# Brainstorming: Gemini Image Generation

## Context
- **Goal**: Replace `VisualGeneratorMock` with a real generator using Google's Gemini API.
- **Key**: `AIzaSyCJEP...` (Google API Key).
- **Endpoint**: Google AI Studio / Vertex AI (Generative Language API).
- **Model**: `imagen-3.0-generate-001` (or equivalent accessible via Gemini API).

## Strategy
1.  **Config**: Create `config.json` (or use env vars) to store the API Key securely.
2.  **Tool**: Create `scripts/visual_generator_gemini.py`.
3.  **Logic**:
    - Use `google.generativeai` library (or `requests` if library missing).
    - Call `models/imagen-3.0-generate-001` with the prompt.
    - Decode Base64 response to Image.
    - Save to file.

## Question
Do you want me to install the `google-generativeai` python package, or use raw HTTP requests to avoid dependencies?
(Raw HTTP is often cleaner for simple scripts).

*Recommendation: Raw HTTP via `requests` is robust and portable.*
