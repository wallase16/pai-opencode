#!/usr/bin/env python3
"""
Suno Song Creator - Chrome MCP Version
Uses chrome-mcp tools instead of puppeteer for browser automation
"""

import time
import json
import sys
import argparse
import csv
import os
from datetime import datetime
from typing import Dict, List, Optional, Tuple


class SunoSongCreatorChrome:
    """
    Suno Song Creator - Chrome MCP Version

    NOTE: This script is a reference implementation. It requires an active MCP client
    environment to execute the `_call_chrome_tool` methods. Running this script
    directly in a standard shell without a bridge will invoke the mock implementations.
    """

    def __init__(self):
        self.suno_url = "https://suno.com/create"
        self.suno_tab_id = None

        # Robust selectors (Verified Dec 2025)
        self.selectors = {
            # Verified placeholders
            "lyrics_textarea": 'textarea[placeholder*="Write some lyrics"]',
            "styles_textarea": 'textarea[placeholder*="fuerte"], textarea[placeholder*="Style"]',
            "song_title_input": 'input[placeholder*="Song Title"]',
            "create_button": 'button[aria-label="Create song"]',
            "custom_mode_toggle": 'button:contains("Custom")',  # Pseudo-selector for logic
            "waiting_room_indicator": "Waiting Room powered by Cloudflare",
            # Download selectors (To be verified)
            "more_actions_button": 'button[aria-label="More actions"], button[data-testid="more-actions"]',
            "download_menu_item": 'div[role="menuitem"]:contains("Download")',
            "download_audio_item": 'div[role="menuitem"]:contains("Audio")',
        }

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

    def download_song(self, share_link: str) -> bool:
        """
        Download the song using browser automation (More -> Download -> Audio).
        """
        try:
            print(f"Attempting download for: {share_link}")

            # 1. Navigate to song page (Wait for load)
            self._call_chrome_tool("mcp-chrome_chrome_navigate", {"url": share_link})
            time.sleep(3)  # Wait for page load

            # 2. Click "More" (...) button
            print("Clicking 'More Actions'...")
            more_res = self._call_chrome_tool(
                "mcp-chrome_chrome_click_element",
                {"selector": self.selectors["more_actions_button"]},
            )

            if more_res.get("status") != "success":
                print("Failed to click 'More' button")
                return False

            time.sleep(1)  # Wait for menu

            # 3. Click "Download" from dropdown
            print("Clicking 'Download' menu item...")
            dl_res = self._call_chrome_tool(
                "mcp-chrome_chrome_click_element",
                {"selector": self.selectors["download_menu_item"]},
            )

            if dl_res.get("status") != "success":
                print("Failed to click 'Download' option")
                return False

            time.sleep(1)  # Wait for submenu

            # 4. Click "Audio" (MP3)
            print("Clicking 'Audio' option...")
            audio_res = self._call_chrome_tool(
                "mcp-chrome_chrome_click_element",
                {"selector": self.selectors["download_audio_item"]},
            )

            if audio_res.get("status") != "success":
                print("Failed to click 'Audio' option")
                return False

            print("Download triggered successfully")
            # Wait for download to start/complete
            time.sleep(5)
            return True

        except Exception as e:
            print(f"Download failed: {e}")
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
            else:
                # Ensure we are on the create page if tab exists
                # Optional: Verify URL matches
                pass

            # Check blocking state (Cloudflare)
            is_blocked, block_msg = self.check_blocking_state()
            if is_blocked:
                return {"success": False, "error": block_msg}

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

            # Wait for generation (Increase wait time for testing)
            print("Waiting 20s for song generation to appear in list...")
            time.sleep(20)

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
        """Extract share links from the current browser page using JS injection (Most Robust)"""
        try:
            # Inject script to find all song links on the page
            # We look for anchor tags containing '/song/' in href
            # and return the unique absolute URLs.
            js_script = """
            (() => {
                const links = Array.from(document.querySelectorAll('a[href*="/song/"]'));
                const urls = links.map(a => a.href);
                // Deduplicate
                const uniqueUrls = [...new Set(urls)];
                // Filter out non-song links (if any) and ensure absolute
                return uniqueUrls.filter(u => u.includes('/song/'));
            })();
            """

            result = self._call_chrome_tool(
                "mcp-chrome_chrome_inject_script",
                {"jsScript": js_script, "type": "MAIN"},
            )

            if result.get("status") == "success":
                # Result structure depends on tool implementation, usually in 'result' field of the return
                # Checking mock implementation or actual return structure
                # Assuming 'result' contains the return value of the script
                # If not, we might need to parse 'content'

                # In standard MCP chrome server, inject_script returns result in 'result' key if successful
                found_urls = result.get("result", [])

                # Check if it returned structure inside content list (common in some MCP versions)
                if not found_urls and result.get("content"):
                    try:
                        content_json = json.loads(result["content"][0]["text"])
                        found_urls = content_json.get("result", [])
                    except:
                        pass

                if isinstance(found_urls, list):
                    # Clean and filter
                    share_links = []
                    seen = set()

                    for url in found_urls:
                        # Extract ID to deduplicate (handle query params)
                        try:
                            song_id = url.split("/song/")[-1].split("?")[0]
                            if song_id and song_id not in seen:
                                seen.add(song_id)
                                share_links.append(url)
                        except:
                            continue

                    # Return top N (most recent are usually at top of DOM for Suno)
                    top_links = share_links[:limit]
                    print(f"Extracted top {len(top_links)} links: {top_links}")
                    return top_links

            print("JS Injection failed or returned no links")
            return []

        except Exception as e:
            # Catch all errors
            print(f"Error extracting share links: {e}")
            return []

            # Convert to full URLs and deduplicate
            share_links = []
            seen = set()

            for el in found_elements:
                # The 'href' might be in the element info or text if it's a link
                # Since we selected 'a' tags, we hope 'href' is returned.
                # If not, we might need to parse the selector or use another method.
                # BUT: The tool output shows `href` is NOT directly in the default response fields for all elements,
                # however, for type 'link' it often is.
                # Let's check what the tool returned in previous steps:
                # It returned "text" and "selector" but not explicit href in the simple summary.
                # Wait, the tool output above shows "text" and "selector" but NO href attribute in the JSON.
                # This is a limitation of get_interactive_elements if it doesn't return attributes.

                # FALLBACK: Use the original Regex method but IMPROVED.
                # The issue might be that `chrome_get_web_content` returns innerText by default?
                # No, we requested `htmlContent=True`.
                pass

            # REVERTING STRATEGY: Improve Regex.
            # The previous regex `href="([^"]*?/song/[^"]*)"` expects double quotes.
            # Maybe attributes are single quoted or no quotes?
            # Also, standard `re` might miss if newlines or spaces.

            # Let's try getting ALL 'a' tags with hrefs via a script injection if possible,
            # OR just fix the regex to be more permissive.

            content = self._call_chrome_tool(
                "mcp-chrome_chrome_get_web_content", {"htmlContent": True}
            )
            html_content = content.get("content", "")

            import re

            # Matches href="/song/..." or href="https://suno.com/song/..."
            # Handles " or ' quotes
            song_pattern = r'href=["\'](/?(?:https://suno\.com)?/song/[^"\']+)["\']'
            matches = re.findall(song_pattern, html_content)

            # ... (rest of processing)
            share_links = []
            seen = set()

            for match in matches:
                full_url = match
                if match.startswith("/"):
                    full_url = f"https://suno.com{match}"

                # Clean up any potential query params or anchors if needed
                # (Suno links are usually clean ids)

                song_id = full_url.split("/song/")[-1].split("?")[0]

                if song_id and song_id not in seen:
                    seen.add(song_id)
                    share_links.append(full_url)

            # Return top N
            top_links = share_links[:limit]
            print(f"Extracted top {len(top_links)} links: {top_links}")
            return top_links

        except Exception as e:
            print(f"Error extracting share links: {e}")
            return []

    def save_share_links(self, result: Dict) -> None:
        """Save share links to a file"""
        try:
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
            with open(links_file, "a", encoding="utf-8") as f:
                f.write(content + "\n")

            print(f"Share links saved to: {links_file}")

        except Exception as e:
            print(f"Error saving share links: {e}")

    def process_batch_csv(self, csv_path: str, output_dir: str, download: bool) -> None:
        """Process a CSV file for batch song generation"""
        print(f"Processing batch CSV: {csv_path}")

        if not os.path.exists(csv_path):
            print(f"Error: CSV file not found: {csv_path}")
            sys.exit(1)

        rows = []
        with open(csv_path, "r", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            # Normalize field names (strip whitespace)
            if reader.fieldnames:
                reader.fieldnames = [name.strip() for name in reader.fieldnames]
                if "Style" not in reader.fieldnames:
                    print("Error: CSV must contain 'Style' column")
                    sys.exit(1)
            else:
                print("Error: Empty CSV or missing header")
                sys.exit(1)
            rows = list(reader)

        total = len(rows)
        print(f"Found {total} songs to process")

        # Process each row
        updated_rows = []
        for i, row in enumerate(rows, 1):
            title = row.get("Title", f"Batch Song {i}")
            style = row.get("Style", "")
            lyrics = row.get("Lyrics", "Instrumental")
            status = row.get("Status", "Pending")
            link = row.get("Share Link", "")

            print(f"\nProcessing {i}/{total}: {title} ({style})")

            # Skip if already done
            if link and "suno.com" in link:
                print("Skipping: Already generated")
                updated_rows.append(row)
                continue

            # Generate
            result = self.create_song(lyrics, style, title)

            if result.get("success"):
                links = result.get("share_links", [])
                link_str = ", ".join(links)
                row["Share Link"] = link_str
                row["Status"] = "Generated"

                # Download if requested
                if download and links:
                    for link in links:
                        self.download_song(link)
            else:
                row["Status"] = f"Failed: {result.get('error')}"

            updated_rows.append(row)

            # Write back to CSV immediately (Progress save)
            self._write_csv(csv_path, reader.fieldnames, updated_rows)

            # Wait between generations
            if i < total:
                print("Cooling down for 10 seconds...")
                time.sleep(10)

    def _write_csv(self, path: str, fieldnames: List[str], rows: List[Dict]) -> None:
        """Helper to write rows back to CSV"""
        try:
            # Ensure 'Status' and 'Share Link' are in fieldnames
            for field in ["Status", "Share Link"]:
                if field not in fieldnames:
                    fieldnames.append(field)

            with open(path, "w", encoding="utf-8", newline="") as f:
                writer = csv.DictWriter(f, fieldnames=fieldnames)
                writer.writeheader()
                writer.writerows(rows)
        except Exception as e:
            print(f"Error saving CSV progress: {e}")

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
        "--mode",
        choices=["single", "batch"],
        default="single",
        help="Operation mode: single song or batch CSV processing",
    )

    parser.add_argument("--csv", help="Path to CSV file for batch processing")

    parser.add_argument(
        "--output-dir", default="./downloads", help="Directory to save downloaded songs"
    )

    parser.add_argument(
        "--no-download", action="store_true", help="Skip downloading generated songs"
    )

    # Legacy arguments for single mode
    parser.add_argument(
        "lyrics",
        nargs="?",
        default="Verse 1: Walking down the sunny street\nChorus: Summer days are here to stay",
        help="Song lyrics (Single Mode)",
    )

    parser.add_argument(
        "style", nargs="?", default="upbeat pop", help="Song style/genre (Single Mode)"
    )

    parser.add_argument("title", nargs="?", default="", help="Song title (Single Mode)")

    args = parser.parse_args()

    creator = SunoSongCreatorChrome()

    if args.mode == "batch":
        if not args.csv:
            print("Error: --csv argument required for batch mode")
            sys.exit(1)

        creator.process_batch_csv(args.csv, args.output_dir, not args.no_download)
    else:
        # Single Mode
        result = creator.create_song(args.lyrics, args.style, args.title)

        # Save share links if successful
        if result.get("success", False):
            creator.save_share_links(result)

            if not args.no_download:
                links = result.get("share_links", [])
                for link in links:
                    creator.download_song(link)

        # Output result as JSON
        print("\nResult:")
        print(json.dumps(result, indent=2))
        sys.exit(0 if result.get("success", False) else 1)


if __name__ == "__main__":
    main()
