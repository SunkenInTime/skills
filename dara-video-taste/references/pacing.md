# Pacing

## Target

Dara wants back-to-back phrases that feel almost as though he is cutting himself off, while every word stays legible. This applies even to calm delivery. The first transition and first five seconds need especially close attention. Keep pauses and laughter when they serve an intentional comedic beat. Establish this rhythm in the first delivered cut, even when the recorded take is tired or hesitant. Rebuild complete phrases from the best takes, remove repeated setup and weak connectors, and tighten internal hesitation so the source delivery does not dictate the finished beat.

## Raw cut

1. Select complete, intentional takes and remove abandoned starts, retakes, and dead air. Preserve the argument's meaning and continuity. Finish when each retained phrase belongs to the intended take and the sequence makes sense.
2. Tighten the spaces between phrases, then inspect the delivery inside each phrase: hesitation, redundant connecting language, stretched syllables, and dragged word endings. Preserve intelligible consonant onsets and endings when shortening a held vowel. Finish when each transition has been reviewed in context and each identified drag has been addressed or intentionally retained.
3. Review the opening, middle, and ending as a continuous rhythm. Bring a weak midsection up to the pace of later cuts Dara has approved. Targeted corrections should preserve those approved cuts unless the request calls for a global change.

Silence detection and word timestamps locate candidates; they do not decide the cut. Inspect the quiet heads and tails retained inside each clip, not just empty timeline gaps. Check the outgoing final syllable and consonant against the source before bringing in the next phrase; transcription can recognize a word whose ending was clipped. Inspect at least half a second beyond each proposed speech ending for a delayed syllable or quiet consonant. On the budget AI edit, the word-timed transcript ended "twenty" about 0.4 seconds before the actual sound finished. Preserve that sound, then tighten the incoming phrase. Treat isolated quiet fragments as possible speech, particularly fricatives; merge them back into their word before deciding whether to shorten a pause. A nearly gapless video can still feel slow because phrases take too long to land. Verify the rhythm in playback rather than treating a millisecond threshold, cut count, or reduced duration as proof of good pacing.

## Boundary review after take selection

Prefer one complete clean take. When a transcript merges a false start, silence, and a later clean take into one sentence, re-transcribe the individual takes with independent context before choosing. Inspect waveform context before every incoming phrase as well as after every outgoing phrase. A timestamp may begin inside a name or retain the tail of the previous failed take. Remove repeated syllables and restarted words editorially; ASR often normalizes them away.

Treat silence detection as annotations for review. Apply only reviewed phrase or word boundaries, then rerun the fragment check after all trimming and frame rounding. Every short clip must contain an intentionally retained complete word or phrase, with a recorded reason. Stray one- or two-frame speech remnants require repair, even when a transcript still reads correctly. Check the opening as a continuous sequence, including the transition into the first recommendation.

Use independent short-source transcripts to investigate uncertain wording. A larger model is a comparison, not proof: full-file Whisper large-v3 repeated hallucinated text through silence and missed later content on the September 20 rerecord. Keep model disagreements visible and resolve them against source context. Preserve the user's spoken wording unless an editorial change is required and understood; do not silently remove a stated count to repair an inferred factual discrepancy.

## When the cut still feels slow

Evaluate faster phrase delivery alongside further gap trims. Dara suggested 1.2x or 1.3x on the first video without choosing one there, then explicitly requested 1.2x for the September 20 budget rerecord. Preserve the rate chosen for the current project; neither example establishes a universal default. Preserve voice pitch and keep picture, graphics, and audio synchronized. Label comparisons clearly and retain the layered edit if creating flattened previews. Let actual feedback determine the preferred speed.

For the first edit, shortening a hesitant connector to "let's say Hermes agent" and tightening the held "chance" addressed specific feedback. Learn the pattern, not those words as automatic deletion targets.

## Practical starting point

Use calibration.md for the actual loose/tighter comparisons and speed candidates. The original cut planner combined editorially selected source ranges with quiet-gap candidates, then rounded boundaries to frames. Early retained pauses around 160 ms felt loose. A later trial retained roughly 20 ms on each side of a detected pause; use this only as an initial boundary candidate, then inspect complete syllables and intentional pauses. Never subtract handles blindly from every detected silence. Use the plan validation tools after editorial selection, and the review.md criteria after implementation.
