#!/usr/bin/env python3
"""Download royalty-free music from Pixabay for YouTube Shorts.

Usage:
    python scripts/download_music.py --count 10 --genre upbeat

Requires: requests library
    pip install requests
"""

import argparse
import sys
from pathlib import Path

try:
    import requests
except ImportError:
    print("Error: 'requests' library not found. Install with: pip install requests")
    sys.exit(1)


PIXABAY_API_BASE = "https://pixabay.com/api/audios/"
PIXABAY_API_KEY = None  # User must provide their own API key (get free key at pixabay.com/api/)

GENRE_KEYWORDS = {
    "upbeat": "upbeat energetic happy",
    "cinematic": "cinematic epic dramatic orchestral",
    "ambient": "ambient peaceful calm relaxation",
    "electronic": "electronic synth digital modern",
    "acoustic": "acoustic guitar acoustic piano",
    "background": "background music loop",
    "motivational": "motivational inspiring uplifting",
}


def download_pixabay_tracks(
    count: int = 10,
    genre: str = "upbeat",
    api_key: str = None,
) -> list[Path]:
    """Download tracks from Pixabay Music.

    Args:
        count: Number of tracks to download
        genre: Genre keyword (upbeat, cinematic, ambient, etc.)
        api_key: Pixabay API key (get free at pixabay.com/api/)

    Returns:
        List of downloaded file paths
    """

    if not api_key:
        print("\n⚠️  Pixabay API key required!")
        print("Get a free key at: https://pixabay.com/api/")
        print("Then set it via: --api-key YOUR_KEY_HERE")
        print("\nAlternatively, manually download from:")
        print("  → https://pixabay.com/music/")
        print("  → Save MP3s to: ~/projects/collabs/youtube-shorts-pipeline/music/")
        return []

    music_dir = Path(__file__).parent.parent / "music"
    music_dir.mkdir(exist_ok=True)

    keywords = GENRE_KEYWORDS.get(genre, genre)

    print(f"\n📥 Downloading {count} '{genre}' tracks from Pixabay...")
    print(f"   Keywords: {keywords}")

    try:
        response = requests.get(
            PIXABAY_API_BASE,
            params={
                "key": api_key,
                "q": keywords,
                "per_page": count,
                "min_length": 30,  # At least 30 seconds
                "max_length": 600,  # Up to 10 minutes
                "safesearch": "true",
                "order": "popular",
            },
            timeout=10,
        )
        response.raise_for_status()
    except requests.RequestException as e:
        print(f"❌ API error: {e}")
        return []

    data = response.json()
    if not data.get("hits"):
        print(f"❌ No tracks found for genre: {genre}")
        return []

    downloaded = []
    for i, track in enumerate(data["hits"][:count], 1):
        track_id = track["id"]
        title = track["title"] or f"track_{track_id}"
        url = track["preview_url"]

        filename = music_dir / f"{i:02d}_{title[:40]}.mp3"

        print(f"  {i}/{len(data['hits'])}: {title[:50]}...", end=" ")

        try:
            resp = requests.get(url, timeout=15)
            resp.raise_for_status()
            filename.write_bytes(resp.content)
            print("✓")
            downloaded.append(filename)
        except Exception as e:
            print(f"✗ ({e})")

    print(f"\n✓ Downloaded {len(downloaded)} tracks to {music_dir}")
    return downloaded


def create_dummy_tracks(count: int = 5) -> list[Path]:
    """Create dummy 1-minute MP3 files for testing (requires ffmpeg).

    Args:
        count: Number of dummy tracks to create

    Returns:
        List of created file paths
    """
    import subprocess

    music_dir = Path(__file__).parent.parent / "music"
    music_dir.mkdir(exist_ok=True)

    print(f"\n🎵 Creating {count} dummy tracks for testing...")

    created = []
    for i in range(1, count + 1):
        filename = music_dir / f"dummy_track_{i:02d}.mp3"

        # Create 60-second silence with ffmpeg (or tone if silence doesn't work)
        cmd = [
            "ffmpeg",
            "-f", "lavfi",
            "-i", f"sine=f=440:d=60",  # 60-second 440Hz sine wave
            "-q:a", "9",
            "-acodec", "libmp3lame",
            str(filename),
            "-y",
            "-loglevel", "quiet",
        ]

        try:
            subprocess.run(cmd, check=True, timeout=30)
            print(f"  {i}. {filename.name} (60s) ✓")
            created.append(filename)
        except Exception as e:
            print(f"  {i}. {filename.name} — skipped ({e})")

    print(f"\n✓ Created {len(created)} dummy tracks")
    return created


def main():
    parser = argparse.ArgumentParser(
        description="Download royalty-free music for YouTube Shorts"
    )
    parser.add_argument(
        "--count", type=int, default=10,
        help="Number of tracks to download (default: 10)"
    )
    parser.add_argument(
        "--genre", default="upbeat",
        choices=list(GENRE_KEYWORDS.keys()) + ["custom"],
        help="Music genre/mood (default: upbeat)"
    )
    parser.add_argument(
        "--api-key", default=None,
        help="Pixabay API key (get free at pixabay.com/api/)"
    )
    parser.add_argument(
        "--dummy", action="store_true",
        help="Create dummy test tracks instead (requires ffmpeg)"
    )

    args = parser.parse_args()

    if args.dummy:
        create_dummy_tracks(args.count)
    else:
        download_pixabay_tracks(
            count=args.count,
            genre=args.genre,
            api_key=args.api_key,
        )

    print("\n✓ Done! Music directory ready at: ~/projects/collabs/youtube-shorts-pipeline/music/")


if __name__ == "__main__":
    main()
