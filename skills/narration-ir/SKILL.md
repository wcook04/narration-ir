---
name: narration-ir
description: Plan grounded visual explanations from a script or recording. Use when preparing word-timed animation briefs, explaining the meaning behind narration, reviewing visual chronology, or handing a video to an animation agent.
license: Apache-2.0
metadata:
  version: "0.1.0"
---

# Narration IR

Give the animator the meaning behind the words, the evidence for that meaning,
and the understanding the picture must produce. Keep the visual treatment open
where several pictures could explain the same thing.

An **intermediate representation (IR)** is the editable explanation plan between
the narration and the animation. This skill produces that plan and scene briefs.
Rendering uses the user's existing tools. No specific agent, model, renderer,
account, service, operating system, or other installed skill is required.

## Establish the input

Read the supplied script or transcript, relevant source files, and any existing
video plan before authoring. Infer audience and purpose from the request; ask
only for information that would change the explanation.

- **Accepted recording:** preserve the words and audio clock. Use a word-timed
  transcript from the available transcription/alignment tool. Whisper or WhisperX
  are options, not requirements. Listen around important anchors and uncertain
  recognition. ASR timestamps are estimates, not exact acoustic truth. Keep
  corrections separate from literal speech. Never invent word timing from an SRT.
- **Developing script:** revise narration and pictures together. The speaker can
  refer to an already planned transformation: “this surviving clip still contains
  the qualification.” Leave timings provisional until recorded, then rebind cues.

Reuse the project's existing format if it already carries these meanings. For a
new machine-readable plan, use [the contract](references/contract.md) and
[the worked example](examples/interview/plan.json). A small project may use the
same fields in Markdown; the optional validator accepts the JSON format only.

## Build the global understanding

Record the audience's starting knowledge, the question the video opens, its
promised answer, the explanatory steps between them, and the closing payoff.
Choose a real source or worked instance that makes the answer inspectable.

Record persistent objects, what each represents, and continuity rules. Read
previous videos or brand references when supplied; extract reusable meanings,
colours and motifs into a project profile rather than imposing this example's
style. A small section indicator can keep viewers oriented (for example 01–08);
use it when the stages are meaningful, not to imply progress without explanation.

Inventory available skills, cloned repos, components and assets by capability.
For each useful candidate record location, inspected version, license, intended
use, availability, and actual trial result. Load only the candidates relevant to
the next passage. Discovery, installation, a successful sample, and suitability
for this scene are different findings. Prefer adapting existing implementation.
If none exists, record the gap and let the renderer workflow resolve it.

Use hook → development → payoff as a coherence aid. Name the value for the viewer
(educational, entertaining, emotional, or a combination). These are authoring
choices, not promises of retention or virality. Do not add repost schedules,
variant farming, platform-ranking claims, or distribution experiments unless
the user separately requests them.

## Elaborate locally before choosing pictures

Work by section, paragraph and sentence; split a sentence into beats when its
meaning changes. Bind each beat to literal spoken occurrences, not a text search
for a repeated word. Give every spoken word a stable ID; every word needs a
place in the plan, but most words do not need their own animation.

For each beat record:

- What the speaker means, grounded in exact source locations; distinguish a
  speaker's account, an illustrative example, observed behavior and established fact.
- What the audience knows before, should understand after, and may misunderstand.
- What the statement does **not** establish or imply.
- Which concepts must already have been introduced; which objects persist or
  change; what the narrator, viewer and depicted actor each know.
- What must become visible for the sentence to work: the object, operation,
  result, intended inference, and enough time to inspect that result.
- Which spoken occurrence triggers each meaningful change; specify onset,
  emphasis or settled-result timing, duration, and hold separately.
- Uncertainties, source disagreements, and editorial decisions still needed.

Use the speaker's requested elaboration budget (for example ten explanatory
words per spoken word). Otherwise deepen ambiguous or consequential passages
until the animator can explain them without guessing. Length is a planning
budget, never proof of understanding. Do not pad with paraphrases or display the
elaboration as on-screen text. Label deductions and unsupported interpretations.

Distinguish a **visual obligation** (“retain the qualification when removing the
pause”) from a **treatment** (“use these two timeline lanes”). Assign treatments
after the obligations are understood. Sound, music, captions, framing and colours
belong to the project profile and treatment, not universal rules of this skill.

## Review chronology adversarially

Read the sequence with later information hidden. At each cue ask: can a newcomer
identify the referenced object, understand the operation, and state what remains
unknown? Does the picture reveal an answer before the narration or depicted actor
has obtained it? Does an example accidentally imply a general claim?

Use [the review guide](references/review.md). Review the opening promise against
the actual ending. Record concrete defects and repairs. If another reviewer is
available and authorized, they can test the plan without the author's explanation;
otherwise label the pass self-review. Do not equate either with a viewer study.

## Hand off and inspect

Supply a bounded packet per scene: global purpose, local literal speech and word
anchors, source excerpts/locations, elaboration, audience states, obligations,
continuity, previous/next handoff, selected reusable implementations, and unresolved
issues. Tell the animator to satisfy the obligations using their renderer skills.
See [renderer handoff](references/handoff.md). Do not silently resolve uncertainty.

After implementation, inspect real transitions and holds at delivery size and
the intended player size; listen to the final mix. Structural validation cannot
establish truth, visual readability, acoustic accuracy, or viewer understanding.
When only planning is requested, deliver the plan and explicitly leave audiovisual
acceptance unreviewed.

## Optional helpers

Paths below are relative to **this skill folder**, not the user's project.
The entire folder is portable; copying only `SKILL.md` drops the linked resources.
Packaging sources and license context are in [origins](references/origins.md).
The instructions work without Python. Helpers use Python 3.10+ and `jsonschema`:

```sh
python -m pip install 'jsonschema>=4.23,<5'
python scripts/narration_ir.py validate examples/interview/plan.json
python scripts/narration_ir.py packet examples/interview/plan.json --beat b04
python scripts/narration_ir.py import-whisper whisper.json --revision take-1
```

Commands write JSON to stdout. Redirect into a new project file when wanted.
`import-whisper` accepts timed words, not segment-only captions. It imports a
transcript, not a completed explanation. Read [the contract](references/contract.md)
for digest binding, source verification and timing limits.
