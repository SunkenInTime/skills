# Resolve implementation notes

These observations came from Resolve free 21.0.4 through the local MCP bridge. Probe current capabilities before relying on them on another build. Prefer available Resolve tools and inspect the current timeline rather than assuming the old project is active.

- Verify timelineFrameRate and timelinePlaybackFrameRate independently before review. A new 30 fps project retained 24 fps playback and played 20% slow with altered audio. The playback-rate API setter returned False; Project Settings > Master Settings > Playback frame rate accepted 30 in the UI. Read back both rates after saving. A correct render does not verify live playback.
- Edit-page keyframe and Volume API writes were unavailable or ineffective in this build. Mixer gain and audio fade handles can be adjusted in the UI. Create rendered camera moves or processed audio copies only with explicit permission; native Fusion can avoid those derivatives.
- On September 11, native Fusion animation worked through `AddModifier(input, 'BezierSpline')` followed by `SetInput(input, value, frame)` using the existing authenticated bridge through `script_plugin.run_inline`. The compound `add_keyframe` action failed because `BridgeProxy` does not support subscripting. Load the item's composition and verify rendered frames; a matching readback alone is insufficient.
- Fusion point values such as Merge Center accepted `[x, y]`. Dictionaries with string keys silently retained the default center. Loader/Crop/Merge graphs kept screenshots native and below the face; the opening push was verified against a same-frame bypass capture.
- Media append used exclusive end frames for video. Still images ignored the requested span and defaulted to 150 frames. Encoded image MOVs honored duration and supported alpha. Verify actual timeline ranges after insertion.
- WAV source frames may use the project rate at import, which differs from timeline rate. Use reported source_fps or source seconds to convert; use timeline FPS for record positions.
- Overlay Tilt did not correspond directly to output pixels for differently shaped source media. For width-fitted media at 1080x1920, the successful estimate was fittedHeight=1080*sourceHeight/sourceWidth; Zoom=desiredWidth/1080; Tilt=-(desiredCenterY-960)*1920/fittedHeight. Confirm rendered placement for each aspect ratio; this is a measured workaround, not a general API guarantee.
- Source thumbnails omit parts of the composite. Verify overlays and camera moves in the actual Resolve viewer, or in rendered frames when an export is requested.
- DRT/DRP backups reference media; they do not bundle it.

Original project files are not bundled. Use the calibration excerpts for historical comparisons and inspect the current project's own paths and timeline for each edit.

## Live edits and animation coordinates

Snapshot the current clip ranges, offsets, transforms, composition counts, and audio before a revision. A former single compound can now be many user-trimmed pieces. Update each affected piece's active composition and every corresponding V2 footage piece; editing only the first clip leaves later sections unchanged. Compare speech ranges, retime data, and audio properties against this fresh snapshot after a visual-only pass. Use semantic comparison rather than serialized IDs, which may change when a timeline is duplicated.

Verify which time domain Fusion uses before keyframing. In the budget edit, the 30 fps timeline's outer compound ran at 1.2x and Fusion evaluated before that retime: a displayed second spanned 36 Fusion frames. Later timeline cuts introduced further source offsets. Map the live segment's timing instead of reusing seconds × timeline FPS everywhere.

For an upward move, Fusion's normalized Center Y increases. Shift animated Y values and their Bezier handles together; retain X motion, scale, angle, visibility keys, and timing. An exported default Center may be omitted, so insert the explicit value instead of assuming it exists. For the verified native V2 footage, enlarging Zoom retained the same Tilt; dividing Tilt by the zoom factor moved the center incorrectly. Use the aspect-ratio estimate above only as a starting point and inspect the actual position.

## Native Fusion readback versus output

AddFusionComp graphs have read back correctly while their overlays were absent from output. ExportFusionComp followed by ImportFusionComp on the same item activated those graphs; LoadFusionCompByName alone did not. Preserve a predecessor and use this repair when the visible output reproduces the failure.

Imported Loaders can become media-pool sources. Setting only Clip or its filename then retained the old image even after reimport. A fresh Loader pointed at the replacement asset, reconnected to the existing Merge foreground, and exported/reimported worked for the GitHub replacement. Preserve the Merge's animation and verify the new image in native output. Direct media-pool relinking must update MediaID and matching references together. Some setters return None despite applying a change; judge by readback and output.

For native frame QA without a video export, capture gallery stills at explicit timecodes. Use a fresh output directory or unique filenames for each attempt and verify the exported DRX RecTC matches the requested timecode. Reused globs previously selected stale PNGs and made a correct repair appear broken. Still-frame sequences establish placement and keyframe states; they do not establish continuous motion feel or an audio audition.

## Delivery

The default is the saved editable timeline active at its beginning. Export or transfer only when requested; a later request for Downloads or phone delivery extends that turn's scope. It does not make exporting or sending every future draft automatic.

For an authorized export, load an explicit video preset before setting the output format, dimensions, frame rate, full timeline range, and audio. Unspecified Deliver-page state persists. Keep unrelated queued jobs and render only the intended job. Verify the actual file with ffprobe for video and audio streams, dimensions, rate, video frame count, and duration; a completed job alone is insufficient. Check audio headroom and composed frames spanning every changed segment. Save the project after rendering. H.264 MP4 at 1080x1920/30 fps with AAC 48 kHz worked for this portrait project, not as a mandated format for other sources.

For an authorized Blip transfer, select the user's verified device and the completed, checked export. "Waiting for [device] to accept" is pending, not delivered. Prompt the user to open Blip on that phone when acceptance is needed, then confirm the sender's "Sent to [device]" success state. Record the destination and actual status. If acceptance remains pending, report that precisely without cancelling the request or claiming receipt. Downloads export and phone transfer have separate completion states.
