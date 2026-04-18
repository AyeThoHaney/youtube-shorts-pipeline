/**
 * KineticCaption — Full-video word-by-word caption overlay for YouTube Shorts.
 *
 * Props (passed via --props JSON):
 *   words      - Array of { text, startMs, endMs } from Whisper output
 *   duration   - Total video duration in seconds
 *   accentColor - Highlight color for the active word (default: "#FFD600")
 *   bgColor    - Background color for caption pill (default: "#000000CC")
 */

import { AbsoluteFill, useCurrentFrame, useVideoConfig } from "remotion";

interface WordTiming {
  text: string;
  startMs: number;
  endMs: number;
}

interface CaptionProps {
  words: WordTiming[];
  duration: number;
  accentColor?: string;
}

export const KineticCaption: React.FC<CaptionProps> = ({
  words,
  accentColor = "#FFD600",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();
  const currentMs = (frame / fps) * 1000;

  // Group words into lines of ~5 words
  const LINE_SIZE = 5;
  const lines: WordTiming[][] = [];
  for (let i = 0; i < words.length; i += LINE_SIZE) {
    lines.push(words.slice(i, i + LINE_SIZE));
  }

  // Find which line is currently active
  const activeLineIdx = lines.findIndex((line) => {
    const lineStart = line[0].startMs;
    const lineEnd = line[line.length - 1].endMs;
    return currentMs >= lineStart && currentMs <= lineEnd + 300;
  });

  if (activeLineIdx === -1) return <AbsoluteFill />;

  const activeLine = lines[activeLineIdx];

  return (
    <AbsoluteFill
      style={{
        display: "flex",
        alignItems: "flex-end",
        justifyContent: "center",
        paddingBottom: 220,
        fontFamily: "'Inter', 'Helvetica Neue', sans-serif",
      }}
    >
      <div
        style={{
          backgroundColor: "#000000CC",
          borderRadius: 16,
          padding: "16px 24px",
          display: "flex",
          flexWrap: "wrap",
          justifyContent: "center",
          gap: 8,
          maxWidth: 900,
        }}
      >
        {activeLine.map((word, i) => {
          const isActive = currentMs >= word.startMs && currentMs <= word.endMs;
          const isPast = currentMs > word.endMs;
          return (
            <span
              key={i}
              style={{
                fontSize: 58,
                fontWeight: 800,
                letterSpacing: "-0.02em",
                color: isActive ? accentColor : isPast ? "#FFFFFF99" : "#FFFFFFCC",
                textShadow: isActive ? `0 0 20px ${accentColor}66` : "none",
                transform: isActive ? "scale(1.05)" : "scale(1)",
                display: "inline-block",
                transition: "all 0.05s",
              }}
            >
              {word.text}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
