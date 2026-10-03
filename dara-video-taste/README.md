# Dara's video editing skill

My short-form editing workflow for DaVinci Resolve: tight, complete speech; supporting imagery below the face; native effects; and review against actual examples.

## Install

Clone this repo and copy the whole `dara-video-taste` folder into your agent's skills directory. Keep its references, scripts, and assets together. The entry point is [SKILL.md](SKILL.md).

For a project-scoped install, put it at `.agents/skills/dara-video-taste/` in your editing project. You can also give an agent the path to `SKILL.md` directly.

Example request:

> Use dara-video-taste to cut this talking-head video in DaVinci Resolve. Start with the speech pass and leave the editable timeline ready for review.

The preferences come from my edits. Apply them to your own footage, and override them with your own direction. The examples include rejected cuts and unselected speed comparisons so the agent can learn the differences. Their status is recorded in the calibration manifest.

## What you need

- DaVinci Resolve and an agent integration that can inspect and edit the live timeline. I used [Samuel Gursky's Resolve MCP](https://github.com/samuelgursky/davinci-resolve-mcp). Install that separately using its setup instructions and check compatibility with your Resolve version.
- Python 3, `ffmpeg`, and `ffprobe` for the bundled helpers. `video_helpers.py` uses Python's standard library.
- Optional speech-boundary review: `numpy` and `Pillow`.
- Optional CTC transcription: `numpy`, `torch`, and `transformers`. Its first run downloads `facebook/wav2vec2-base-960h` from Hugging Face.

Install optional Python dependencies in a virtual environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install numpy Pillow
# Only if you want the independent transcription helper:
python -m pip install torch transformers
```

Run helper commands from this skill's directory, or pass their full paths. [Tools](references/tools.md) documents the source-range plan and commands. Transcription regions use a JSON list such as `[{"start": 0, "end": 6}]`, in source seconds.

## Included

- Pacing, composition, sound, Resolve implementation, and review guidance.
- Five short calibration videos and two layout reference images.
- Media analysis, cut-plan validation, preview, layout, audio, still-clip, and frame-extraction helpers.
- Speech-boundary waveform review and independent CTC transcription helpers.

Full projects, original footage, the broader meme and sound library, and machine configuration are not included. The calibration clips are reference material. Resolve integration observations are version-specific; verify them on your installation.
