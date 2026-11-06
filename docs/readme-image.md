# README illustration

`assets/readme/narration-to-visual-plan.png` illustrates the existing fictional
interview example in `skills/narration-ir/examples/interview/`. The unchanged
words in the before/after strips are the explanation: remove silence while
preserving the scope of the speaker's claim.

Generated on 6 November 2026 with the built-in image-generation tool. The image
is an illustration, not an app screenshot or evidence of rendered animation.
No third-party images or private media were supplied. The original generated
1663 × 946 PNG is copied unchanged into the repository. The asset is used only
by the README and is not a dependency of the installable skill.

The shortened narration in the illustration is an explanatory paraphrase; the
worked plan retains its original literal sentence. All before/after interview
words agree with the fictional source. The gap disappears; the words
“for this interview” remain in both strips.

## Generation prompt

```text
Use case: infographic-diagram.
Create a polished editorial illustration for the README of Narration IR, a portable AI-agent skill. Wide landscape image, approximately 1800 by 1000. The purpose is to show the actual method: recorded words plus source context become a meaning-and-timing plan before an animator chooses visuals. This is a conceptual illustration, not an app screenshot. Use a quiet warm-white paper background, black/charcoal typography, restrained golden-yellow annotations and muted teal for retained content. Elegant precise print design, generous margins, clear typographic hierarchy, crisp flat shapes with a little tactile paper texture. No robots, brains, magic sparkles, decorative code, glowing gradients, logos or invented UI.

Adapt this existing worked example exactly: a fictional interviewee says "I saved time [pause] for this interview". The editor removes only silence; the qualification "for this interview" remains. This example is about preserving scope of meaning.

Composition: three numbered stages across the page, connected by two simple arrows. Large headings exactly:
"01  YOUR WORDS"
"02  THE MEANING"
"03  THE VISUAL PLAN"

Stage 1: a neatly typeset speech note containing the exact narration "Remove the pause. Keep the meaning." Beneath it, a short recorded waveform with a clearly visible flat silence interval, and one small source page. One large label under the source page: "Read the source".
Stage 2: an annotated brief on a paper sheet, containing only these three large lines:
"Cut the silence"
"Keep the qualification"
"Time the change to the words"
Use one clear yellow underline and one restrained margin annotation mark; no tiny filler text.
Stage 3: an actual before/after explanatory comparison rather than a generic screen icon. Two horizontal strips labeled "Before" and "After". BEFORE strip contains three aligned blocks in order: "I saved time", a small golden yellow empty gap labeled "pause", and a muted-teal block "for this interview". AFTER strip contains exactly the same two text blocks "I saved time" and "for this interview" adjacent, with no pause. Both teal blocks must contain the identical words. A subtle alignment guide makes the retained qualifier recognizable. The yellow gap disappears; words never disappear. Underneath: "Same words. Less silence."

All text must be verbatim, properly spelled, large and comfortably readable at 900px displayed width. Keep total copy limited to the supplied labels. No extra title, footer, headings or claims. Make the relation immediately clear to someone unfamiliar with AI animation.
```

## Review

The generated image was inspected for text accuracy, the unchanged qualification,
the removed silence interval and the left-to-right sequence. The README repeats
the example in selectable text and provides descriptive alt text. It does not
require readers to decode the image to install or use the skill.

The README prose was revised using the humanizer method: explain the input,
agent action and resulting brief before introducing “IR”; define “qualification”
using the actual words; keep optional Python instructions separate from skill use.

