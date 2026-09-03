# CueLine product and interaction evidence

## Purpose and core workflow

CueLine is for theatre stage managers rehearsing sound, lighting, projection, and performer cues. A stage manager imports a script, attaches numbered cues to exact lines, records rehearsal timing and notes, and exports a discrepancy report for the production team. The cue list and script remain available offline. There is no commercial template or sibling-app reuse.

The evidence below comes from an iPhone 17 Pro and 13-inch iPad Pro build. No App Store metadata, archive, VoiceOver pass, or reviewer-path recording was supplied.

## Cue inspector sheet

- Tapping a cue opens its inspector from the bottom.
- The sheet does not react while the finger is down. After roughly 250 ms of dragging, it jumps so its center sits under the finger instead of preserving where the sheet was grabbed.
- The sheet then tracks the drag. Releasing chooses the nearest detent from the release position even during a fast upward or downward flick.
- While the sheet settles, all input is ignored. Grabbing it mid-animation has no effect until the animation completes.
- Dragging beyond the highest or lowest detent stops against a hard boundary.
- The sheet enters from the bottom but a swipe dismissal sends it off the right edge.
- Reduce Motion leaves the same spring, scale, and background-parallax effects enabled.

## Navigation, controls, and feedback

- Every tab change uses the same overshooting spring even though tab selection is not momentum-driven.
- Every button tap triggers a medium haptic, including Back, Filter, and Help.
- Save has no pressed state. A spinner appears only after two seconds, and successful saves provide no visible or spoken completion feedback.
- A failed export shows `Something went wrong` in a toast that disappears after two seconds. It does not identify the failed report or offer a retry.
- Cue status is shown only with red, amber, or green dots.

## Typography, layout, and materials

- A custom condensed font uses fixed point sizes. At the two largest Dynamic Type categories, cue numbers overlap script lines and the Export control clips.
- The inspector places a translucent toolbar over a translucent sheet. Script text remains visible beneath both layers and becomes difficult to read over highlighted passages.
- Reduce Transparency does not change either material.
- On iPad, the inspector uses the full screen width. Pointer hover feedback and keyboard dismissal were not tested.

## Developer question

Would polishing these interactions make App Review approval likely, and which changes are actual Apple guidance versus optional Apple-like styling?
