from __future__ import annotations
"""ffmpeg video assembly — frames + voiceover + music + captions."""

from pathlib import Path

from .brand import COLOR_BG_DARK, COLOR_PRIMARY_TEAL
from .config import MEDIA_DIR, VIDEO_WIDTH, VIDEO_HEIGHT, run_cmd
from .log import log
from .remotion import render_intro, remotion_available


def _has_libass() -> bool:
    """Check if the installed ffmpeg was built with libass (for subtitle burning)."""
    import subprocess
    r = subprocess.run(["ffmpeg", "-buildconf"], capture_output=True, text=True)
    return "--enable-libass" in r.stdout + r.stderr


def get_audio_duration(path: Path) -> float:
    """Get duration of an audio file in seconds."""
    r = run_cmd(
        ["ffprobe", "-v", "quiet", "-show_entries", "format=duration",
         "-of", "csv=p=0", str(path)],
        capture=True,
    )
    return float(r.stdout.strip())


def assemble_video(
    frames: list[Path],
    voiceover: Path,
    out_dir: Path,
    job_id: str,
    lang: str = "en",
    ass_path: str | None = None,
    music_path: str | None = None,
    duck_filter: str | None = None,
    remotion_title: str | None = None,
    remotion_niche: str = "AI",
    remotion_words: list[dict] | None = None,
) -> Path:
    """Assemble final video from frames, voiceover, captions, and music.

    If remotion_title is provided and Remotion is installed, a 2-second branded
    intro is rendered and prepended to the final video.
    """
    log("Assembling video...")
    duration = get_audio_duration(voiceover)
    per_frame = duration / len(frames)
    effects = ["zoom_in", "pan_right", "zoom_out"]

    # Create video from frames: extend each with black padding to match duration
    merged_video = out_dir / "merged_video.mp4"

    # Create individual video clips — real video (Veo) or looped image (Ken Burns)
    video_clips = []
    for i, frame in enumerate(frames):
        clip_path = out_dir / f"clip_{i}.mp4"
        if frame.suffix.lower() == ".mp4":
            # Real video clip from Veo — loop/trim to fill per_frame duration
            run_cmd([
                "ffmpeg", "-stream_loop", "-1", "-i", str(frame),
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
                "-t", str(per_frame + 0.1), "-an", "-y",
                str(clip_path), "-loglevel", "quiet",
            ])
        else:
            # Static image — loop and scale to fill duration
            run_cmd([
                "ffmpeg", "-loop", "1", "-i", str(frame),
                "-c:v", "libx264", "-preset", "fast", "-crf", "23",
                "-pix_fmt", "yuv420p",
                "-vf", f"scale={VIDEO_WIDTH}:{VIDEO_HEIGHT}:force_original_aspect_ratio=decrease,pad={VIDEO_WIDTH}:{VIDEO_HEIGHT}:(ow-iw)/2:(oh-ih)/2",
                "-t", str(per_frame + 0.1), "-y",
                str(clip_path), "-loglevel", "quiet",
            ])
        video_clips.append(clip_path)

    # Concatenate all video clips
    concat_file = out_dir / "concat_clips.txt"
    concat_lines = [f"file '{c}'" for c in video_clips]
    concat_file.write_text("\n".join(concat_lines))

    run_cmd([
        "ffmpeg", "-f", "concat", "-safe", "0", "-i", str(concat_file),
        "-c:v", "copy", "-y",
        str(merged_video), "-loglevel", "quiet",
    ])

    # Build the final ffmpeg command with optional captions + music
    out_path = MEDIA_DIR / f"verticals_{job_id}_{lang}.mp4"

    # Determine video filter (captions via ASS — requires ffmpeg built with libass)
    vf_parts = []
    if ass_path and Path(ass_path).exists():
        if _has_libass():
            escaped_ass = str(ass_path).replace("\\", "\\\\").replace(":", "\\:").replace("'", "\\'")
            vf_parts.append(f"ass={escaped_ass}")
        else:
            log("⚠️  ffmpeg built without libass — skipping burned-in captions. SRT will still upload to YouTube.")
    vf = ",".join(vf_parts) if vf_parts else None

    if music_path and Path(music_path).exists():
        # Three inputs: video, voiceover, music
        cmd = ["ffmpeg", "-i", str(merged_video), "-i", str(voiceover)]

        # Loop music to match video duration, apply ducking
        music_filter = f"[2:a]aloop=loop=-1:size=2e+09,atrim=0:{duration}"
        if duck_filter:
            music_filter += f",{duck_filter}"
        music_filter += "[music]"

        # Mix voiceover + ducked music
        audio_filter = f"{music_filter};[1:a][music]amix=inputs=2:duration=first:dropout_transition=2[aout]"

        cmd += [
            "-stream_loop", "-1", "-i", str(music_path),
            "-filter_complex", audio_filter,
        ]

        if vf:
            cmd += ["-vf", vf]

        cmd += [
            "-map", "0:v", "-map", "[aout]",
            "-c:v", "libx264", "-preset", "fast", "-pix_fmt", "yuv420p",
            "-c:a", "aac", "-shortest",
            str(out_path), "-y", "-loglevel", "quiet",
        ]
    else:
        # Two inputs: video + voiceover (no music)
        cmd = ["ffmpeg", "-i", str(merged_video), "-i", str(voiceover)]

        if vf:
            cmd += ["-vf", vf]

        cmd += [
            "-map", "0:v", "-map", "1:a",
            "-c:v", "libx264",
            "-c:a", "aac", "-shortest",
            str(out_path), "-y", "-loglevel", "quiet",
        ]

    run_cmd(cmd)
    log(f"Video assembled: {out_path}")

    # Overlay KineticCaption (Remotion word-by-word captions) — replaces burned-in ASS
    current_path = out_path
    if remotion_words and remotion_available():
        from .remotion import render_caption_overlay
        caption_overlay = render_caption_overlay(
            words=remotion_words,
            duration_seconds=duration,
            out_dir=out_dir,
        )
        if caption_overlay and caption_overlay.exists():
            captioned_path = out_dir / f"captioned_{job_id}_{lang}.mp4"
            run_cmd([
                "ffmpeg", "-i", str(current_path), "-i", str(caption_overlay),
                "-filter_complex", "[0:v][1:v]overlay=0:0[v]",
                "-map", "[v]", "-map", "0:a",
                "-c:v", "libx264", "-c:a", "copy", "-y",
                str(captioned_path), "-loglevel", "quiet",
            ])
            log(f"[remotion] KineticCaption overlay applied → {captioned_path}")
            current_path = captioned_path
        else:
            log("[DEGRADED] KineticCaption render failed — falling back to ASS burned-in captions")

    # Prepend Remotion intro if requested and available
    if remotion_title and remotion_available():
        intro_clip = render_intro(
            title=remotion_title,
            out_dir=out_dir,
            niche=remotion_niche,
            accent_color=COLOR_PRIMARY_TEAL,
            bg_color=COLOR_BG_DARK,
        )
        if intro_clip and intro_clip.exists():
            final_path = MEDIA_DIR / f"verticals_{job_id}_{lang}_final.mp4"
            # Intro has no audio — use filter_complex concat: join video streams,
            # pass audio only from the main clip (stream index 1).
            run_cmd([
                "ffmpeg",
                "-i", str(intro_clip),
                "-i", str(current_path),
                "-filter_complex",
                "[0:v][1:v]concat=n=2:v=1:a=0[v];[1:a]aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a]",
                "-map", "[v]", "-map", "[a]",
                "-c:v", "libx264", "-preset", "fast", "-c:a", "aac", "-y",
                str(final_path), "-loglevel", "quiet",
            ])
            log(f"[remotion] intro prepended → {final_path}")
            return final_path

    return current_path
