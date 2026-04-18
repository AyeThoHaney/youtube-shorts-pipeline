import React from "react";
import { Composition } from "remotion";
import { KineticCaption } from "./KineticCaption";
import { VerticalIntro } from "./VerticalIntro";

export const RemotionRoot: React.FC = () => {
  return (
    <>
      <Composition
        id="VerticalIntro"
        component={VerticalIntro}
        durationInFrames={60}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          title: "This Changes Everything",
          niche: "AI",
          accentColor: "#00E5C0",
          bgColor: "#111111",
        }}
      />
      <Composition
        id="KineticCaption"
        component={KineticCaption}
        durationInFrames={900}
        fps={30}
        width={1080}
        height={1920}
        defaultProps={{
          words: [
            { text: "Sample", startMs: 0, endMs: 500 },
            { text: "caption", startMs: 500, endMs: 1000 },
          ],
          duration: 30,
          accentColor: "#FFD600",
        }}
      />
    </>
  );
};
