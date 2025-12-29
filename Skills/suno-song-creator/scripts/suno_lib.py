#!/usr/bin/env python3
"""
Suno Song Creator - Library Version
Adapted for use by Master Controller
"""

import time
import json
import sys
import argparse
import csv
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


# Mock MCP bridge if running as library without bridge injected
def mock_mcp_call(tool_name: str, params: Dict) -> Dict:
    print(f"[MOCK] Calling {tool_name} with {params}")
    return {"status": "success", "content": "", "url": "https://suno.com/create"}


class SunoSongCreator:
    def __init__(self, mcp_client=None):
        self.suno_url = "https://suno.com/create"
        self.suno_tab_id = None
        # Allow injection of real MCP client
        self.mcp_client = mcp_client

        self.selectors = {
            "lyrics_textarea": 'textarea[placeholder*="Write some lyrics"]',
            "styles_textarea": 'textarea[placeholder*="fuerte"], textarea[placeholder*="Style"]',
            "song_title_input": 'input[placeholder*="Song Title"]',
            "create_button": 'button[aria-label="Create song"]',
            "custom_mode_toggle": 'button:contains("Custom")',
            "waiting_room_indicator": "Waiting Room powered by Cloudflare",
            "more_actions_button": 'button[aria-label="More actions"], button[data-testid="more-actions"]',
            "download_menu_item": 'div[role="menuitem"]:contains("Download")',
            "download_audio_item": 'div[role="menuitem"]:contains("Audio")',
        }

    def _call_chrome_tool(self, tool_name: str, params: Dict) -> Dict:
        """Call chrome tool via injected client or mock"""
        if self.mcp_client:
            return self.mcp_client.call_tool(tool_name, params)
        else:
            return mock_mcp_call(tool_name, params)

    def check_blocking_state(self) -> Tuple[bool, str]:
        """Check if access is blocked by Cloudflare Waiting Room or other blockers"""
        try:
            content = self._call_chrome_tool(
                "mcp-chrome_chrome_get_web_content", {"textContent": True}
            )
            title = content.get("title", "")
            text = content.get("textContent", "")

            if (
                self.selectors["waiting_room_indicator"] in title
                or self.selectors["waiting_room_indicator"] in text
            ):
                return True, "Blocked: Cloudflare Waiting Room active"

            return False, "Access Clear"
        except Exception as e:
            return False, f"Error checking blocking state: {e}"

    def find_suno_tab(self) -> Optional[int]:
        """Find existing Suno tab or return None"""
        try:
            windows_data = self._call_chrome_tool("mcp-chrome_get_windows_and_tabs", {})
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
            result = self._call_chrome_tool(
                "mcp-chrome_chrome_navigate",
                {"url": self.suno_url, "newWindow": self.suno_tab_id is None},
            )
            if result.get("status") == "success":
                print("Successfully navigated to Suno create page")
                if self.suno_tab_id is None:
                    time.sleep(2)
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
            self._call_chrome_tool("mcp-chrome_chrome_keyboard", {"keys": "PageDown"})
            time.sleep(1)

            # Fill lyrics
            result = self._call_chrome_tool(
                "mcp-chrome_chrome_fill_or_select",
                {"selector": self.selectors["lyrics_textarea"], "value": lyrics},
            )
            if not result.get("status") == "success":
                print("Failed to fill lyrics")
                return False

            # Fill styles
            result = self._call_chrome_tool(
                "mcp-chrome_chrome_fill_or_select",
                {"selector": self.selectors["styles_textarea"], "value": style},
            )
            if not result.get("status") == "success":
                print("Failed to fill styles")
                return False

            # Fill title
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

    def download_song(self, share_link: str) -> bool:
        """Download the song using browser automation (More -> Download -> Audio)."""
        try:
            print(f"Attempting download for: {share_link}")
            self._call_chrome_tool("mcp-chrome_chrome_navigate", {"url": share_link})
            time.sleep(3)

            # Click "More"
            more_res = self._call_chrome_tool(
                "mcp-chrome_chrome_click_element",
                {"selector": self.selectors["more_actions_button"]},
            )
            if more_res.get("status") != "success":
                print("Failed to click 'More' button")
                return False
            time.sleep(1)

            # Click "Download"
            dl_res = self._call_chrome_tool(
                "mcp-chrome_chrome_click_element",
                {"selector": self.selectors["download_menu_item"]},
            )
            if dl_res.get("status") != "success":
                print("Failed to click 'Download' option")
                return False
            time.sleep(1)

            # Click "Audio"
            audio_res = self._call_chrome_tool(
                "mcp-chrome_chrome_click_element",
                {"selector": self.selectors["download_audio_item"]},
            )
            if audio_res.get("status") != "success":
                print("Failed to click 'Audio' option")
                return False

            print("Download triggered successfully")
            time.sleep(5)
            return True
        except Exception as e:
            print(f"Download failed: {e}")
            return False

    def extract_share_links(self, limit: int = 2) -> List[str]:
        """Extract share links using JS injection"""
        try:
            js_script = """
            (() => {
                const links = Array.from(document.querySelectorAll('a[href*="/song/"]'));
                const urls = links.map(a => a.href);
                const uniqueUrls = [...new Set(urls)];
                return uniqueUrls.filter(u => u.includes('/song/'));
            })();
            """
            result = self._call_chrome_tool(
                "mcp-chrome_chrome_inject_script",
                {"jsScript": js_script, "type": "MAIN"},
            )

            # Logic to parse result would go here (simplified for library)
            return [
                "https://suno.com/song/mock123"
            ]  # Placeholder for library version until integrated with real extraction logic
        except Exception as e:
            print(f"Error extracting share links: {e}")
            return []

    def generate_song(self, lyrics: str, style: str, title: str) -> Dict:
        """Library method to generate a song"""
        try:
            if not self.find_suno_tab():
                if not self.navigate_to_create():
                    return {"success": False, "error": "Navigation Failed"}

            is_blocked, msg = self.check_blocking_state()
            if is_blocked:
                return {"success": False, "error": msg}

            logged_in, msg = self.check_login_status()
            if not logged_in:
                return {"success": False, "error": msg}

            if not self.fill_song_form(lyrics, style, title):
                return {"success": False, "error": "Form Fill Failed"}

            if not self.submit_song_creation():
                return {"success": False, "error": "Submission Failed"}

            print("Waiting for generation...")
            # Real implementation would poll
            time.sleep(5)

            links = self.extract_share_links()
            return {"success": True, "share_links": links}

        except Exception as e:
            return {"success": False, "error": str(e)}


if __name__ == "__main__":
    pass
