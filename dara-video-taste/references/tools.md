# Reusable preparation and review tools

Use scripts/video_helpers.py from this skill with Python3, ffmpeg, and ffprobe on PATH. It uses only Python's standard library. Run --help or a subcommand's --help for exact arguments. These helpers produce local artifacts; use Resolve for the editable working timeline. Honor any current instruction to keep work native. The originals and existing output files are preserved.

## When to use a helper

Follow the stage workflow in SKILL.md and review.md. Analyze existing source media without changing the edit. Native Resolve operations are the default implementation. preview, audio-copy, still-clip, and frames create derivatives: use them only within current authorization and the delivery preferences in resolve.md. In particular, a request to review directly in Resolve does not authorize new review-video exports. Existing reference excerpts remain available for calibration.

## Source-range plan

One source file per plan, source-relative frames with exclusive ends, and plan FPS matching the source's nominal r_frame_rate. These are positions on that nominal time grid, as used by the first Resolve edit, rather than raw decoded-frame indices. preview conforms variable frame timing to this grid before trimming, keeping audio cuts at frame/FPS seconds. Record positions are cumulative. The helper rejects mixed-rate plans rather than guessing conversions. Each reason should express the editorial decision, especially an intentional pause or a shortened connector.

```json
{
  "source": "/absolute/path/source.mp4",
  "fps": 29.97002997002997,
  "ranges": [
    {"start_frame": 30, "end_frame": 90, "record_start_frame": 0, "reason": "Complete opening take"},
    {"start_frame": 120, "end_frame": 210, "record_start_frame": 60, "reason": "Next thought, quiet head removed"}
  ]
}
```

For a whole-composite speed comparison, make a single full-length range from the actual frame count. Additional trims must be explicit reviewed ranges. preview preserves voice pitch and time-compresses the composite, including its effects; for final production, consider native dialogue retiming with separately placed natural effect tails. Preview output is flattened, so retain the layered source timeline.

## Commands

Substitute absolute paths for the examples. Set HELPER in your shell to this skill's scripts/video_helpers.py path.

```sh
python3 "$HELPER" analyze /absolute/path/raw-cut.mp4
python3 "$HELPER" validate-plan /absolute/path/cut-plan.json
python3 "$HELPER" preview /absolute/path/cut-plan.json /absolute/path/review.mp4
python3 "$HELPER" preview /absolute/path/cut-plan.json /absolute/path/review-1.2x.mp4 --speed 1.2
python3 "$HELPER" layout --canvas 1080 1920 --asset 500 500 --logo --region 0 1210 1080 1760 --center 540 1480
python3 "$HELPER" layout --canvas 1080 1920 --asset 1090 510 --region 0 1210 1080 1760 --center 540 1480
python3 "$HELPER" audio-copy /absolute/path/dialogue.wav /absolute/path/dialogue-normalized.wav --mode dialogue
python3 "$HELPER" audio-copy /absolute/path/click.mp3 /absolute/path/click-balanced.wav --mode sfx --peak -11 --fade-start 1.18
python3 "$HELPER" still-clip /absolute/path/overlay.png /absolute/path/overlay.mov --duration 3 --fps 30000/1001
python3 "$HELPER" frames /absolute/path/render.mp4 /absolute/path/qa-frames --times 0.1 1.8 3.5 4
```

`layout` requires the usable region you chose after reserving space for the face and platform controls. The coordinates above illustrate the latest trial, not a verified platform specification. Supply different bounds for a different composition or UI; `--center` and `--max-size` preserve a chosen placement or focal-asset size. The calculation preserves aspect ratio and fits both the region and requested center. Inspect animation overshoot and native Resolve positioning separately.

analyze defaults to quiet intervals at least 0.12 seconds below -32 dB as candidates. preview consumes reviewed ranges and does not automatically cut them further. audio-copy keeps the full input duration, uses two-pass loudness processing for dialogue, or gain plus a quarter-sine tail for SFX. still-clip keeps alpha using PNG in a MOV, for environments where still durations are unreliable. frames extracts full-resolution composed images with time-labeled filenames.

## Limits that require judgment

This is not an automatic video editor. It does not pick retakes, decide which word is safe to shorten, infer sarcasm, choose a meme, or establish perceptual pacing. A transcript match cannot prove the final syllable survived. A fit calculation cannot prove the caption is readable. Use the skill's editorial criteria and the actual rendered result for those decisions.

## Speech boundary review without video exports

`scripts/speech_cut_review.py PLAN OUTPUT_DIR` accepts the existing source-range plan format. Run with numpy and Pillow available. It reads source audio, validates contiguous record ranges, draws both sides of every boundary with half a second of discarded context, and flags short fragments, quiet heads/tails, and energetic cut edges. It never trims automatically. Resolve each flag editorially; a clean report is not listening approval. The original project also used separate short-phrase transcriptions for comparing uncertain takes; those project-specific scripts are not bundled. Whole-file ASR can merge retakes and silently remove stumbles.

For independent disfluency evidence, `scripts/transcribe_speech_regions.py SOURCE REGIONS_JSON OUTPUT_JSON` uses local wav2vec2 CTC with approximate word spans. Run with numpy, transformers, and torch available. The first run downloads facebook/wav2vec2-base-960h from Hugging Face. REGIONS_JSON contains start/end seconds. On the September 20 source it exposed a repeated ten-dollar attempt and repeated is-a that Whisper normalized away. It misrecognizes names; compare with contextual ASR and source waveforms, and retain phoneme context around the reported word spans.
