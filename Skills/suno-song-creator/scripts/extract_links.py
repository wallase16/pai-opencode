# Suno Share Link Extractor
# Processes HTML content to extract actual share links from our test

import re
import json


def extract_suno_links_from_html(html_content, limit=2):
    """Extract Suno song links from HTML content

    According to Suno workflow, the two most recently generated songs
    are always at the top of the library/results page.
    """
    # Pattern to match href attributes containing /song/
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
        song_id = full_url.split("/song/")[-1] if "/song/" in full_url else full_url
        if song_id and song_id not in seen:
            seen.add(song_id)
            share_links.append(full_url)

    # Return only the top N most recent songs (default: 2)
    # Suno puts the most recently generated songs at the top
    return share_links[:limit]


# HTML content from our actual test (truncated for brevity)
test_html = """
href="/song/a5044751-ffef-4341-8c2d-05b7c689fb56"
href="/song/e45fed37-db0c-47b3-93e4-af4f0b26fb95"
href="/song/ce5c29c7-8f15-49a4-a7d2-76e428e6bc55"
href="/song/36b89a62-eeca-478c-a764-c6f04f257dff"
href="/song/e089a545-fe09-437b-ba25-9e0e72875a5d"
href="/song/de89215a-fad5-4b8c-86e9-dff6b8eeca62"
href="/song/4dd9359d-86f0-4e81-8dda-61a258c0c412"
href="/song/1b20003a-bd69-41da-9c90-4158f0a53f7e"
href="/song/df166b98-353f-48af-8107-ad4856761bd5"
href="/song/29587468-ac91-4c08-8485-6491c9b1cd03"
"""

if __name__ == "__main__":
    # Extract only the top 2 most recent songs (as per Suno workflow)
    links = extract_suno_links_from_html(test_html, limit=2)
    print(f"Extracted top {len(links)} most recent share links (per Suno workflow):")
    for i, link in enumerate(links, 1):
        print(f"{i}. {link}")

    # Save to file
    result = {
        "success": True,
        "message": "Top 2 most recent share links extracted from test HTML (per Suno workflow)",
        "share_links": links,
        "songs_generated": len(links),
        "extraction_method": "top_2_recent",
        "workflow_note": "Suno always puts the 2 most recently generated songs at the top of the library",
    }

    with open("extracted_links.json", "w") as f:
        json.dump(result, f, indent=2)

    print(f"\nResults saved to extracted_links.json")
    print(f"Note: Only extracting top 2 links as per Suno workflow instructions")
