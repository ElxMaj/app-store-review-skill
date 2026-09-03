# Apple-design review for native apps

Use this reference to review the product itself. `references/visual-report-design.md` governs the separate HTML report artifact.

This lens adapts Emil Kowalski's `apple-design` skill to evidence-based iOS and iPadOS review. It preserves the external skill's principles while expressing them as native, framework-neutral outcomes. Do not paste web CSS, Pointer Events code, or JavaScript physics into a SwiftUI, UIKit, React Native, Expo, or Flutter recommendation.

## Classification boundary

Apple design quality and App Review compliance overlap, but they are not the same claim.

- Tag a current statement from Apple's Human Interface Guidelines, accessibility guidance, or App Review Guidelines `OFFICIAL` and link the exact page when network access is available.
- Introduce an optional design judgment with `Craft recommendation:`. Keep any material rationale within the allowed evidence-confidence system from `references/evidence-policy.md`.
- Treat a runtime failure as submission risk only to the degree it makes a feature broken, incomplete, misleading, inaccessible, or difficult for a reviewer to operate. Do not imply that every HIG preference is an independent rejection rule.
- Never convert polish into approval odds. Improved craft reduces observed friction; it cannot make approval likely or guaranteed.

Screenshots can establish hierarchy, clipping, contrast evidence, and visible states. They cannot establish gesture tracking, velocity, interruption, haptic timing, or frame smoothness. Source can reveal intent but does not prove the shipped feel. Mark those conclusions `MANUAL CHECK` until supported by a build, device run, or supplied recording.

## Map Apple's principles into the existing grades

Keep the five Mode C grades. Do not add an Apple-likeness score.

| Principle | Review question | Primary Mode C destination |
|---|---|---|
| Purpose | Does each feature earn attention by advancing the app's specific job? | Product distinction; Product page |
| Agency | Can people choose, cancel, reverse, undo, and recover without being trapped? | Microcopy and states |
| Responsibility | Does the product protect privacy, safety, accessibility, and truthful expectations? | Visual identity and accessibility; Microcopy and states |
| Familiarity | Do standard controls, gestures, navigation, and metaphors behave predictably? | Visual identity and accessibility |
| Flexibility | Does the app adapt to content size, device, orientation, input method, language, and ability? | Visual identity and accessibility |
| Simplicity | Is the common path obvious, with advanced options one level deeper and necessary context present? | Product distinction; Microcopy and states |
| Craft | Are type, spacing, alignment, icons, materials, motion, and states coherent at every supported size? | Visual identity and accessibility |
| Delight | Does the experience produce calm confidence or useful joy after the other principles are sound? | Product distinction; Visual identity and accessibility |

Use safety and predictability, understanding, achievement, and joy as the human outcomes behind these principles. Delight is earned by the rest; confetti, bounce, glass, and haptics do not establish it.

## Interaction and motion

Walk each primary interaction on a real supported device when possible.

### Response and direct manipulation

- Look for visible response when contact begins, followed by commitment when the action completes. A control that appears inert until a delayed network result creates uncertainty.
- A dragged object should track continuously with the touch or pointer and preserve the original grab offset. Flag dead time, jumps to the object's center, and feedback that appears only after release.
- Keep feedback near the object or action it describes. Distinguish status, completion, warning, and error instead of using one generic toast for all four.
- Check cancellation behavior. A press can normally be cancelled by moving away; a direct manipulation should not trap the person after intent changes.

### Interruptibility and momentum

- A new gesture should be able to take over while motion is in flight. Flag disabled input, queued gestures, and transitions that must finish before reversal.
- On interruption, continue from the current visible presentation state, not the previous logical start or final target. A jump on re-grab is evidence that state and presentation diverged.
- Preserve release direction and velocity when a drag becomes an animation. Choose a detent or snap target from the platform or framework's predicted end position when momentum is meaningful, not release position alone.
- Carry velocity through retargeting instead of hard-cutting it. Treat horizontal and vertical motion independently when their velocities differ.

### Springs, spatial consistency, and boundaries

- Use restrained, critically damped motion as the ordinary starting point. Bounce belongs to an interaction that carried momentum; repeated navigation, loading, and routine state changes rarely justify overshoot.
- Calibration values from the source skill, not App Review requirements: damping ratio `1.0` and response `0.3-0.4` seconds are useful neutral starting points; damping near `0.8` can suit a momentum-driven release. Verify on device rather than copying numbers blindly.
- Enter and exit along the same spatial path. Anchor a surface to its trigger or source, and make intermediate frames indicate the destination.
- At a drag boundary, maintain continuity with progressive resistance instead of a frozen hard stop.
- Use a modest intent threshold before committing a drag direction, but minimize disambiguation delay. Detect plausible gestures together until intent is clear.
- Review fast motion frame by frame or in slow motion. Check supported lower-performance devices for hitches, flashes, strobing, and layout work on the animation path.

## Visual hierarchy, materials, and type

### Wayfinding and grouping

Each screen should make location, available destinations, content, and exit clear. Put a control close to what it changes. Proximity, order, spacing, contrast, and alignment should communicate grouping before explanatory labels are needed. Prefer direct destinations such as `Cues` or `Reports` over vague labels such as `Home`.

Use system conventions unless a tested product need justifies a custom pattern. Familiar does not mean generic: specific content, hierarchy, workflow, and interaction can make standard controls distinctive.

### Materials and depth

- Use translucency to communicate a functional floating layer, not as decoration.
- Avoid stacking light translucent surfaces where content from multiple depths competes for legibility.
- Match material weight and separation to surface size and hierarchy. A blocking modal needs clear separation; a parallel panel can preserve surrounding context.
- Keep text and controls legible over every real background. Test light and dark appearances, Increase Contrast, and Reduce Transparency. Provide a solid or more opaque fallback when requested.
- Use color as a secondary cue. Pair status color with text, shape, symbol, or another perceivable distinction.

### Typography

- Prefer system text styles and optical sizing. A custom typeface is valid when it serves the product, but it still needs a deliberate hierarchy and accessible behavior.
- Test every supported Dynamic Type size with long, localized, and multiline content. Controls and primary tasks must remain available without overlap or severe clipping.
- Treat tracking and leading as size-dependent. Large display type can be tighter; small or dense text needs legibility. Do not force one spacing value across all sizes.
- Scale layout spacing with text where appropriate. Verify truncation, line limits, scrolling, and reflow instead of assuming font scaling alone is sufficient.

## Feedback, sound, and haptics

Feedback should have causality, harmony, and utility.

- Causality: the person can tell which action or state caused it.
- Harmony: visual, audio, and haptic feedback describe the same event at the same moment.
- Utility: reserve prominent feedback for a meaningful selection, threshold, commit, completion, warning, or error.

Flag one identical haptic on every tap, sound or vibration without a visible equivalent, and feedback whose timing disagrees with the state change. Use documented system meanings where available and keep the app usable when haptics or audio are unavailable or disabled.

## Accessibility variants

Reduced motion does not mean removing all feedback.

- With Reduce Motion, remove gratuitous parallax, depth travel, zoom, blur transitions, elastic overshoot, and large-axis movement. Prefer a brief cross-fade, tighter settle, or immediate state change while preserving status and continuity.
- Direct manipulation can continue to track a person's gesture under Reduce Motion; avoid adding autonomous motion after release when it is unnecessary.
- With Reduce Transparency, make layered materials more opaque or solid and remove blur that harms legibility.
- With Increase Contrast, strengthen separation and test all semantic colors and materials.
- Verify VoiceOver names, values, hints, reading order, focus return, and announcements for asynchronous completion or failure.
- Verify comfortable target sizes and spacing, non-color communication, Full Keyboard Access where relevant, and explicit dismissal for information that otherwise disappears on a timer.

On iPad, also test rotation, supported multitasking widths, pointer, keyboard, and the relationship between a popover or inspector and its source. A stretched phone layout or full-width sheet is evidence to investigate, not an automatic defect.

## Audit and intervention contract

For each material observation, record:

1. `Evidence:` path, screen, supplied timestamp, setting, or device run.
2. `Principle:` the specific design or accessibility principle affected.
3. `Classification:` `OFFICIAL` guidance or `Craft recommendation:`.
4. `Impact:` reviewer-visible failure, accessibility gap, workflow friction, or optional refinement.
5. `Verify:` an observable device test, including the relevant accessibility setting or interruption case.

Rank interventions in this order unless the evidence justifies a different order:

1. broken, unreadable, inaccessible, unsafe, or unrecoverable primary paths
2. weak product purpose or agency
3. delayed, inconsistent, or non-interruptible interaction and feedback
4. typography, material, alignment, and platform adaptation
5. optional delight

If product distinction is `HIGH RISK`, the substantive product change still leads. Do not let animation, icon, material, or microcopy polish disguise a thin product.

Useful verification gestures include slow drag, fast flick, reversal, grab during settle, overdrag at every boundary, cancel and retry, background and foreground interruption, and repeated use with Reduce Motion enabled.

## Sources and attribution

Design sources verified 2026-09-03:

- Emil Kowalski, [`apple-design`](https://github.com/emilkowalski/skills/blob/main/skills/apple-design/SKILL.md)
- Apple, [Human Interface Guidelines](https://developer.apple.com/design/human-interface-guidelines/)
- Apple, [Design principles](https://developer.apple.com/design/human-interface-guidelines/design-principles)
- Apple, [Motion](https://developer.apple.com/design/human-interface-guidelines/motion), [Gestures](https://developer.apple.com/design/human-interface-guidelines/gestures), [Feedback](https://developer.apple.com/design/human-interface-guidelines/feedback), and [Playing haptics](https://developer.apple.com/design/human-interface-guidelines/playing-haptics)
- Apple, [Accessibility](https://developer.apple.com/design/human-interface-guidelines/accessibility) and [The details of UI typography](https://developer.apple.com/videos/play/wwdc2020/10175/)

The adapted source is MIT licensed:

```text
MIT License
Copyright (c) 2026 Emil Kowalski
Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
```
