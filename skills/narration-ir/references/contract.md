# Contract and optional helper

`plan.schema.json` is the JSON Schema 2020-12 shape contract for `narration-ir/0.1`.
The bundled helper adds cross-reference, source-byte, chronology and timing rules.
This is a small portable profile, not an interchange standard for every editor.
Preserve richer native data when exporting a subset into this profile.

## Ownership

- `transcript` owns literal word occurrences, revision, provenance and seconds on
  one output clock. Times are nonnegative, ordered, nonoverlapping and bounded by
  `duration`. Overlapping speakers require an explicit editorial track selection
  before import; this profile does not flatten simultaneous speech silently.
- `transcript_sha256` binds the plan to **all** transcript fields, using UTF-8 JSON
  with sorted keys, compact separators and non-ASCII text preserved. The helper's
  `digest()` implements the algorithm. A new digest is an acknowledgement after
  review, not automatic permission to carry old meaning or cues to new speech.
- `global_plan` owns the audience, question, payoff beat, section route, viewer
  value, project profile and capability inventory. Empty capabilities are valid
  when no renderer has yet been inspected. Do not fabricate a successful trial.
- `sections` supplies the ordered route. Beats also carry a `paragraph` grouping.
- `concepts` declares introductions at particular word occurrences, including
  introductions within a sentence. `objects` declares persistent identity.
- `beats` owns the sentence/clause elaboration, before/after understanding,
  evidence, exclusions, knowledge states and obligations. Together, ordered beats
  cover each transcript word exactly once. `speech` joins their exact word text
  with spaces. The source transcription file should be retained separately if
  original punctuation spacing must be reproduced byte-for-byte.
- `events` supplies one possible timing treatment. Each event belongs to an
  obligation and an occurrence in that obligation's beat. Many words may hold the
  same image. An unassigned obligation is reported as a warning, not acceptance.
- `review` records separate semantic and audiovisual status and unresolved issues.
  These labels are declarations; the helper cannot verify that a review happened.

## Evidence

Each source is a UTF-8 text file relative to the plan directory, with SHA-256 and
an evidence kind: `fictional`, `primary`, `speaker_account`, or `secondary`.
Each beat carries source ID, human-readable locator and exact excerpt. The helper
verifies bytes and excerpt inclusion. A hash proves identity, not truth or support
for the interpretation. The locator and inference still require human/agent review.
Include only material you may distribute. For large papers or repositories, use
an authorized short excerpt plus a citation and version in that source file.

Absolute paths, escaping paths and symlink escapes are rejected. No URL fetching
or arbitrary shell execution occurs. Files intentionally stay within the plan
directory so scene packages can move together. This is path containment, not a
race-free sandbox for hostile concurrent filesystem mutation.

## Timing

For each event let `T` be the selected word edge plus `offset`, and `D` its duration:

| Sync | Transition starts | Result settles |
| --- | --- | --- |
| `onset` | T | T + D |
| `emphasis` | T − D/2 | T + D/2 |
| `settled` | T − D | T |

`hold` follows the settled result. All times are seconds; round to frames only in
the renderer adapter and record that rounding. “Emphasis” means the midpoint in
this profile; a nonlinear treatment must map its actual emphasis moment explicitly.

Transitions and holds must fit the owning beat interval. Beat bounds may include
silence around words. When a cue does not fit, simplify the treatment, prepare the
objects earlier, or revise the declared scene boundary with its adjacent handoff.
Do not silently clamp the event or change accepted speech. Event prerequisites
must be introduced by the **start of the transition**, preventing a settled cue
from starting its reveal before the referenced concept exists.

Use `untimed` provenance with null word, duration and beat times for a draft.
The helper validates occurrence order but emits no executable schedule. Synthetic
times are permitted only in `developing_script` mode and remain explicitly marked.
An accepted recording may have `asr_unreviewed` or `audio_reviewed` provenance;
the former always warns. Neither state establishes frame-exact alignment by itself.

## Commands

Run from the copied skill directory, with Python 3.10+ and `jsonschema` installed:

```sh
python scripts/narration_ir.py validate examples/interview/plan.json
python scripts/narration_ir.py packet examples/interview/plan.json --beat b04
python scripts/narration_ir.py import-whisper /path/to/whisper.json --revision take-1
```

Alternatively the PEP 723 header lets `uv run scripts/narration_ir.py ...` resolve
the helper's dependency. `uv` is optional and not bundled.

Whisper imports accept a top-level `words` array or `segments[].words`. Each word
needs `word` (or `text`), numeric `start`, and numeric `end`. Missing, reversed,
overlapping and non-finite times fail. IDs include the user-supplied revision and
ordinal occurrence. Re-importing a changed take requires a new revision and a
semantic rebind; IDs are not claimed to survive transcript edits automatically.
The imported duration is the last word end, not measured audio duration: set the
actual output duration from your audio before defining trailing visual holds.

The importer produces the transcript object only. Put it in an authored plan,
populate source and meaning fields, then bind its digest. The helper never invents
elaboration or automatically approves an edit. All commands print JSON; none
overwrites a plan. Exit codes: 0 successful operation, 1 invalid plan, 2 input or
dependency error. Warnings and open issues do not make a structurally valid plan
invalid; preserve them in production acceptance.
