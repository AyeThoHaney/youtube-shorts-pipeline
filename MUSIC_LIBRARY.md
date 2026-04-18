# Music Library Setup

The YouTube Shorts pipeline automatically selects background music from the `music/` directory and ducks the volume during speech regions.

## Current Status

✅ **Test tracks ready** — 5 dummy tracks (60s each) for development  
📝 **Production tracks pending** — Replace test tracks with real royalty-free music

## How to Add Real Music

### Option 1: Pixabay Music (Easiest)

1. Get a free API key at https://pixabay.com/api/
2. Run the download script:
   ```bash
   python scripts/download_music.py \
     --api-key YOUR_KEY \
     --genre upbeat \
     --count 20
   ```
3. Script will download 20 upbeat tracks to `music/`

Available genres:
- `upbeat` — Energetic, happy, motivational
- `cinematic` — Epic, dramatic, orchestral
- `ambient` — Peaceful, calm, relaxation
- `electronic` — Synth, digital, modern
- `acoustic` — Guitar, piano, organic
- `background` — Loops, subtle, unobtrusive
- `motivational` — Inspiring, uplifting

### Option 2: Manual Download (YouTube Audio Library)

1. Go to https://www.youtube.com/audiolibrary
2. Download 10-20 royalty-free tracks as MP3s
3. Save to: `~/projects/collabs/youtube-shorts-pipeline/music/`
4. That's it! Pipeline picks them up automatically

### Option 3: Bulk Download from Free Sites

- **Pixabay Music**: https://pixabay.com/music/ (2,000+ tracks)
- **Incompetech**: https://incompetech.com/ (10+ years of music)
- **Free Music Archive**: https://freemusicarchive.org/ (15,000+ tracks)

## How the System Uses Music

1. **Selection**: Randomly picks one track from the music directory
2. **Duration**: Loops track to match voiceover duration
3. **Ducking**: Lowers volume during speech, full volume during gaps
   - Speech volume: 12% (configurable)
   - Gap volume: 25% (configurable)
   - Smooth transitions: ±0.3s crossfade

## Configuration

Edit `verticals/config.py` to customize:

```python
MUSIC_DUCK_SPEECH = 0.12  # Volume during speech (0.0 = mute, 1.0 = full)
MUSIC_DUCK_GAP = 0.25     # Volume during gaps
MUSIC_MERGE_GAP_THRESHOLD = 0.5  # Silence threshold (seconds)
```

## Testing

Run a complete produce cycle with music:

```bash
python -m verticals produce \
  --draft /path/to/draft.json \
  --lang en
```

Check the log for:
- `[music] selected track: test_track_01.mp3`
- `[assemble] Video assembled: ...verticals_JOB_ID_en.mp4`

If no music directory: pipeline falls back to voiceover-only (no background music)

## File Format Requirements

- **Format**: MP3 (required, no other formats supported)
- **Bitrate**: 128 kbps or higher recommended
- **Sample rate**: 44.1 kHz or 48 kHz
- **Duration**: Any length (will loop to match voiceover)

## Troubleshooting

**"No tracks found"**
- Verify `music/` directory exists
- Check that tracks are `.mp3` files
- Use: `python -c "from verticals.music import _find_tracks; print(_find_tracks())"`

**"Music too loud during speech"**
- Lower `MUSIC_DUCK_SPEECH` in config (try 0.08)
- Increase `MUSIC_DUCK_GAP` to increase contrast (try 0.35)

**"Music selection always the same"**
- Add more tracks to the directory (random pick from all)
- Currently 5 test tracks (all play ~equally)

