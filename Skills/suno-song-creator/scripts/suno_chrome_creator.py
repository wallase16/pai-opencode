#!/usr/bin/env python3
"""
Suno Song Creator - Chrome MCP Version
Uses chrome-mcp tools instead of puppeteer for browser automation
"""

import time
import json
import sys
import argparse
from typing import Dict, List, Optional, Tuple


class SunoSongCreatorChrome:
    def __init__(self):
        self.suno_url = "https://suno.com/create"
        self.suno_tab_id = None

        # Updated selectors based on current Suno page structure (2025)
        self.selectors = {
            "lyrics_textarea": "body > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div > div > div > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(2) > div > div:nth-of-type(2) > div > div:nth-of-type(1) > div:nth-of-type(1) > div > textarea",
            "styles_textarea": 'textarea[placeholder*="indie, electronic, synths"]',
            "song_title_input": "body > div:nth-of-type(1) > div:nth-of-type(1) > div:nth-of-type(2) > div:nth-of-type(1) > div > div > div > div > div > div > div > div:nth-of-type(1) > div > div:nth-of-type(2) > div:nth-of-type(2) > div:nth-of-type(5) > div > div > div > div > div:nth-of-type(1) > input",
            "create_button": 'button[aria-label="Create song"]',
        }

    def find_suno_tab(self) -> Optional[int]:
        """Find existing Suno tab or return None"""
        try:
            # Get all windows and tabs
            windows_data = self._call_chrome_tool("mcp-chrome_get_windows_and_tabs", {})

            # Look for Suno tab
            for window in windows_data.get("windows", []):
                for tab in window.get("tabs", []):
                    if "suno.com" in tab.get("url", ""):
                        self.suno_tab_id = tab["tabId"]
                        print(f"Found existing Suno tab: {tab['tabId']}")
                        return tab["tabId"]

            print("No existing Suno tab found")
            return None

        except Exception as e:
            print(f"Error finding Suno tab: {e}")
            return None

    def navigate_to_create(self) -> bool:
        """Navigate to Suno create page"""
        try:
            # Navigate to create page (opens new tab if none exists)
            result = self._call_chrome_tool(
                "mcp-chrome_chrome_navigate",
                {"url": self.suno_url, "newWindow": self.suno_tab_id is None},
            )

            if result.get("status") == "success":
                print("Successfully navigated to Suno create page")
                # If we opened a new window, we need to find the tab ID
                if self.suno_tab_id is None:
                    time.sleep(2)  # Wait for tab to open
                    self.find_suno_tab()
                return True
            else:
                print(f"Failed to navigate: {result}")
                return False

        except Exception as e:
            print(f"Error navigating to create page: {e}")
            return False

    def check_login_status(self) -> Tuple[bool, str]:
        """Check if user is logged in by examining current URL"""
        try:
            content = self._call_chrome_tool(
                "mcp-chrome_chrome_get_web_content", {"textContent": True}
            )

            current_url = content.get("url", "")

            if "/login" in current_url or "/signin" in current_url:
                return False, "User not logged in - redirected to login page"

            return True, "Logged in successfully"

        except Exception as e:
            return False, f"Error checking login status: {e}"

    def fill_song_form(self, lyrics: str, style: str, title: str = "") -> bool:
        """Fill the song creation form with lyrics, style, and title"""
        try:
            print("Filling song creation form...")

            # Scroll down to make form visible
            print("Scrolling to form...")
            scroll_result = self._call_chrome_tool(
                "mcp-chrome_chrome_keyboard", {"keys": "PageDown"}
            )
            if not scroll_result.get("status") == "success":
                print("Warning: Scroll failed, proceeding anyway")

            # Wait a moment for scroll to complete
            import time

            time.sleep(1)

            # Fill lyrics
            result = self._call_chrome_tool(
                "mcp-chrome_chrome_fill_or_select",
                {"selector": self.selectors["lyrics_textarea"], "value": lyrics},
            )
            if not result.get("status") == "success":
                print("Failed to fill lyrics")
                return False

            # Fill styles textarea directly
            result = self._call_chrome_tool(
                "mcp-chrome_chrome_fill_or_select",
                {"selector": self.selectors["styles_textarea"], "value": style},
            )
            if not result.get("status") == "success":
                print("Failed to fill styles")
                return False

            # Fill title if provided
            if title:
                result = self._call_chrome_tool(
                    "mcp-chrome_chrome_fill_or_select",
                    {"selector": self.selectors["song_title_input"], "value": title},
                )
                if not result.get("status") == "success":
                    print("Failed to fill title")
                    return False

            print("Form filled successfully")
            return True

        except Exception as e:
            print(f"Error filling form: {e}")
            return False

    def submit_song_creation(self) -> bool:
        """Click the create button to start song generation"""
        try:
            print("Submitting song creation...")

            result = self._call_chrome_tool(
                "mcp-chrome_chrome_click_element",
                {"selector": self.selectors["create_button"]},
            )

            if result.get("status") == "success":
                print("Song creation submitted successfully")
                return True
            else:
                print("Failed to submit song creation")
                return False

        except Exception as e:
            print(f"Error submitting creation: {e}")
            return False

    def create_song(self, lyrics: str, style: str, title: str = "") -> Dict:
        """Main method to create a song"""
        try:
            print(f"Starting song creation with style: {style}")
            print(f"Lyrics preview: {lyrics[:100]}...")

            # Find or open Suno tab
            if not self.find_suno_tab():
                print("Opening new Suno tab...")
                if not self.navigate_to_create():
                    return {"success": False, "error": "Failed to navigate to Suno"}

            # Check login status
            logged_in, login_message = self.check_login_status()
            if not logged_in:
                return {"success": False, "error": login_message}

            # Fill the form
            if not self.fill_song_form(lyrics, style, title):
                return {"success": False, "error": "Failed to fill song form"}

            # Submit creation
            if not self.submit_song_creation():
                return {"success": False, "error": "Failed to submit song creation"}

            # Wait for generation (would need polling implementation)
            print("Waiting for song generation to complete...")

            # Extract actual share links from browser content
            # Per Suno workflow: only extract the top 2 most recently generated songs
            share_links = self.extract_share_links(limit=2)

            result = {
                "success": True,
                "message": "Song created successfully",
                "lyrics": lyrics,
                "style": style,
                "title": title,
                "share_links": share_links,
                "songs_generated": len(share_links),
            }

            # Save share links to file
            self.save_share_links(result)

            return result

        except Exception as e:
            error_msg = f"Song creation failed: {e}"
            print(error_msg)
            return {
                "success": False,
                "error": error_msg,
                "lyrics": lyrics,
                "style": style,
                "title": title,
            }

    def extract_share_links(self, limit: int = 2) -> List[str]:
        """Extract share links from the current browser page

        Per Suno workflow: Extract only the top N most recently generated songs.
        Suno always puts the most recently generated songs at the top of the library.
        """
        try:
            # Get HTML content from the page
            content = self._call_chrome_tool(
                "mcp-chrome_chrome_get_web_content", {"htmlContent": True}
            )

            html_content = content.get("content", "")

            # Parse HTML to find song links
            # Look for href attributes containing "/song/"
            import re

            song_pattern = r'href="([^"]*?/song/[^"]*)"'
            matches = re.findall(song_pattern, html_content)

            # Convert to full URLs and deduplicate
            share_links = []
            seen = set()

            for match in matches:
                if match.startswith("/"):
                    full_url = f"https://suno.com{match}"
                elif match.startswith("http"):
                    full_url = match
                else:
                    continue

                # Extract song ID for deduplication
                song_id = (
                    full_url.split("/song/")[-1] if "/song/" in full_url else full_url
                )
                if song_id and song_id not in seen:
                    seen.add(song_id)
                    share_links.append(full_url)

            # Return only the top N most recent songs (per Suno workflow)
            top_links = share_links[:limit]
            print(
                f"Extracted top {len(top_links)} most recent share links (per Suno workflow): {top_links}"
            )
            return top_links

        except Exception as e:
            print(f"Error extracting share links: {e}")
            return []

    def save_share_links(self, result: Dict) -> None:
        """Save share links to a file"""
        try:
            import os
            from datetime import datetime

            # Create output directory if it doesn't exist
            output_dir = os.path.dirname(os.path.abspath(__file__))
            links_file = os.path.join(output_dir, "generated_song_links.txt")

            # Format the content
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            content = f"# Generated Song Links - {timestamp}\n"
            content += f"# Style: {result.get('style', 'unknown')}\n"
            content += f"# Lyrics preview: {result.get('lyrics', '')[:100]}...\n\n"

            share_links = result.get("share_links", [])
            if share_links:
                content += "Share Links:\n"
                for i, link in enumerate(share_links, 1):
                    content += f"{i}. {link}\n"
            else:
                content += "No share links available\n"

            # Save to file
            with open(links_file, "w", encoding="utf-8") as f:
                f.write(content)

            print(f"Share links saved to: {links_file}")

        except Exception as e:
            print(f"Error saving share links: {e}")

    def _call_chrome_tool(self, tool_name: str, params: Dict) -> Dict:
        """Call a chrome-mcp tool and return the result"""
        # This is a placeholder - in actual implementation, this would call
        # the appropriate chrome-mcp function
        print(f"Calling {tool_name} with params: {params}")

        # For now, return a mock response structure
        return {
            "status": "success",
            "content": "",
            "elements": [],
            "url": "https://suno.com/create",
        }


def main():
    parser = argparse.ArgumentParser(
        description="Suno Song Creator - Chrome MCP Version"
    )

    parser.add_argument(
        "lyrics",
        nargs="?",
        default="Verse 1: Walking down the sunny street\nChorus: Summer days are here to stay",
        help="Song lyrics",
    )

    parser.add_argument(
        "style", nargs="?", default="upbeat pop", help="Song style/genre"
    )

    parser.add_argument("title", nargs="?", default="", help="Song title (optional)")

    args = parser.parse_args()

    # Create and run
    creator = SunoSongCreatorChrome()
    result = creator.create_song(args.lyrics, args.style, args.title)

    # Save share links if successful
    if result.get("success", False):
        creator.save_share_links(result)

    # Output result as JSON
    print("\nResult:")
    print(json.dumps(result, indent=2))

    sys.exit(0 if result.get("success", False) else 1)


if __name__ == "__main__":
    main()
