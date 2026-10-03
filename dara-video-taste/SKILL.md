---
name: dara-video-taste
description: Edit Dara's short-form videos in his established style, including new raw cuts, pacing repairs, framing, supporting images, sound effects, and learning from review feedback. Use for short-form video work in DaVinci Resolve when the user wants Dara's style.
---

# Dara's video editing

The first delivered pass should already reflect Dara's corrections. Use near-interrupting but complete speech, a deliberate opening push when doing visuals, and readable contextual assets below his face and clear of platform controls. Preserve intentional comedy. Source performance and automated timestamps are inputs to editorial judgment, not the finished rhythm.

This package preserves Dara's editing preferences and examples. When another creator uses it, apply the style to their footage and treat references to Dara's face, feedback, or approval as references to the current creator. Their explicit direction overrides these defaults. See [README.md](README.md) for setup.

## 1. Establish scope and current state

Identify the requested stage: raw cut, visual/sound pass, targeted repair, or discussion. A new raw cut goes to Dara before VFX; an explicit full-pass request authorizes the requested stages. Caption-only discussion leaves the project untouched. Default review delivery is the saved, active Resolve timeline; create video exports only when requested.

Inspect the live project, every affected timeline segment, its Fusion layers, and audio tracks. The live timeline takes precedence over saved plans: Dara may have trimmed or split clips since the previous pass. Preserve those edits and manual gains, and duplicate or back up that live state before mutations.

Done when the working timeline, requested changes, preserved user edits, and delivery mode are recorded in the project's edit notes. Use available context rather than asking Dara to repeat it.

## 2. Calibrate before making editorial decisions

Read [calibration.md](references/calibration.md) and inspect its relevant reference media. This is required on a fresh video, a fresh task taking over an edit, and after feedback that the result feels wrong. Within the same task, reuse completed calibration unless the requested style changes.

Load only the pass you are implementing:

- Speech selection or pacing: [pacing.md](references/pacing.md).
- Framing, camera moves, images, or effects: [visuals-and-sound.md](references/visuals-and-sound.md), including its two reference images.
- Resolve work, exports, or phone delivery: [resolve.md](references/resolve.md), including split clips, retimed Fusion, native-output verification, and delivery completion.
- Reusable preparation or analysis: [tools.md](references/tools.md). Helpers support the edit; they do not select takes or prove good pacing.
- Conflicting feedback or skill maintenance: [learning.md](references/learning.md).

Done when the notes identify which examples were actually inspected, what they establish, and the specific choices this new source needs. Missing playback capability remains an explicit review limitation; text or waveform analysis must not be described as listening.

## 3. Build the requested pass against the reference

For speech, select the clean complete take before tightening boundaries. Record why a reconstruction is necessary when using pieces of separate takes. Preserve meaning and word endings while removing stumbles, empty heads/tails, and weak connectors. Check the opening as a continuous hook before propagating the cutting approach through the rest.

For visuals and sound, write a compact beat plan before filling the timeline: spoken phrase, asset/effect, timing, transition purpose, and bounds clear of both the face and platform UI. Establish one representative placement and opening move in the actual composite before applying the treatment throughout. Keep existing effects that support their beats.

Done when every requested section has been addressed, and edits remain native and adjustable wherever supported. Follow the pass reference for exact treatment and numeric starting points.

## 4. Review before delivery

Complete the applicable checks in [review.md](references/review.md). Inspect the resulting timeline/composite, not merely the requested property values. Fix failures before presenting the first pass. Checkpoints are internal work, not additional permission requests.

Done when the project notes contain the review evidence and remaining limitations, the correct timeline is saved and active at its start, and the user receives a concise change summary. Call it a review version until Dara approves it. A successful export, matching transcript, or gapless timeline is not approval.

## 5. Learn without accumulating conflicting rules

Update the authoritative pass reference when corrective feedback changes future decisions. Store the dated supporting evidence and unresolved choices in learning.md. Keep numeric experiments provisional unless Dara selects them. Latest explicit direction overrides the baseline. Keep project-specific ranges with the project; add a portable example only when it teaches a distinct judgment the existing references cannot show.
