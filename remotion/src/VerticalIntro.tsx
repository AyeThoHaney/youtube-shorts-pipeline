/**
 * VerticalIntro — 2-second branded animated intro for YouTube Shorts (1080×1920).
 *
 * Props (passed via --props JSON):
 *   title      - Main topic text (e.g. "Claude Code Is Changing Everything")
 *   niche      - Niche label shown as a tag (e.g. "AI Tools")
 *   accentColor - Hex color for accent elements (default: "#00E5FF")
 *   bgColor    - Hex background color (default: "#0A0A0F")
 */

import { AbsoluteFill, interpolate, spring, useCurrentFrame, useVideoConfig } from "remotion";

interface IntroProps {
  title: string;
  niche?: string;
  accentColor?: string;
  bgColor?: string;
}

export const VerticalIntro: React.FC<IntroProps> = ({
  title,
  niche = "AI",
  accentColor = "#00E5C0",
  bgColor = "#111111",
}) => {
  const frame = useCurrentFrame();
  const { fps } = useVideoConfig();

  // Tag slides in from left at frame 3
  const tagX = spring({ frame: frame - 3, fps, config: { damping: 14, stiffness: 180 } });
  const tagTranslate = interpolate(tagX, [0, 1], [-300, 0]);
  const tagOpacity = interpolate(frame, [3, 12], [0, 1], { extrapolateRight: "clamp" });

  // Title word-by-word reveal starting at frame 10
  const words = title.split(" ");
  const wordDelay = 4; // frames between each word

  // Accent bar scales up at frame 5
  const barScale = spring({ frame: frame - 5, fps, config: { damping: 12, stiffness: 200 } });
  const barWidth = interpolate(barScale, [0, 1], [0, 120]);

  // Overall fade-out in last 8 frames
  const totalFrames = fps * 2; // 2 seconds
  const fadeOut = interpolate(frame, [totalFrames - 8, totalFrames - 1], [1, 0], {
    extrapolateLeft: "clamp",
    extrapolateRight: "clamp",
  });

  return (
    <AbsoluteFill
      style={{
        background: `radial-gradient(ellipse at 30% 20%, #1A1A1A 0%, ${bgColor} 70%)`,
        fontFamily: "'Inter', 'Helvetica Neue', sans-serif",
        opacity: fadeOut,
        display: "flex",
        flexDirection: "column",
        alignItems: "center",
        justifyContent: "center",
        padding: "60px 50px",
      }}
    >
      {/* Cronduit wordmark — top center */}
      <div
        style={{
          position: "absolute",
          top: 80,
          left: 0,
          right: 0,
          textAlign: "center",
          color: "#FFFFFF44",
          fontSize: 26,
          fontWeight: 700,
          letterSpacing: "0.3em",
          textTransform: "uppercase",
        }}
      >
        CRONDUIT
      </div>
      {/* Niche tag */}
      <div
        style={{
          transform: `translateX(${tagTranslate}px)`,
          opacity: tagOpacity,
          backgroundColor: accentColor + "22",
          border: `2px solid ${accentColor}`,
          borderRadius: 100,
          padding: "10px 28px",
          marginBottom: 28,
          display: "inline-flex",
          alignItems: "center",
          gap: 8,
        }}
      >
        <div
          style={{
            width: 8,
            height: 8,
            borderRadius: "50%",
            backgroundColor: accentColor,
            boxShadow: `0 0 8px ${accentColor}`,
          }}
        />
        <span
          style={{
            color: accentColor,
            fontSize: 28,
            fontWeight: 700,
            letterSpacing: "0.12em",
            textTransform: "uppercase",
          }}
        >
          {niche}
        </span>
      </div>

      {/* Accent bar */}
      <div
        style={{
          width: barWidth,
          height: 4,
          backgroundColor: accentColor,
          borderRadius: 2,
          marginBottom: 32,
          boxShadow: `0 0 20px ${accentColor}99, 0 0 40px #00B8FF44`,
        }}
      />

      {/* Title — word by word */}
      <div
        style={{
          textAlign: "center",
          lineHeight: 1.2,
        }}
      >
        {words.map((word, i) => {
          const startFrame = 10 + i * wordDelay;
          const wordProgress = spring({
            frame: frame - startFrame,
            fps,
            config: { damping: 18, stiffness: 220 },
          });
          const wordY = interpolate(wordProgress, [0, 1], [40, 0]);
          const wordOpacity = interpolate(frame, [startFrame, startFrame + 6], [0, 1], {
            extrapolateRight: "clamp",
            extrapolateLeft: "clamp",
          });
          return (
            <span
              key={i}
              style={{
                display: "inline-block",
                color: "#FFFFFF",
                fontSize: 72,
                fontWeight: 800,
                transform: `translateY(${wordY}px)`,
                opacity: wordOpacity,
                marginRight: "0.25em",
                textShadow: "0 2px 20px rgba(0,0,0,0.5)",
              }}
            >
              {word}
            </span>
          );
        })}
      </div>
    </AbsoluteFill>
  );
};
