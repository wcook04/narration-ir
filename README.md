# Narration IR

**Give your animation agent the meaning behind your words.**

Narration IR is a portable agent skill for turning a script or recording and its
sources into a grounded, word-timed visual explanation plan. The plan records
what you mean, what the viewer needs to understand, what a picture must show,
and which spoken words each visual event follows.

It is a planning skill with optional validation tools. Use it alongside your
existing Remotion, Manim, Motion Canvas, editing, or animation workflow.

## See the difference

You say: **“I remove the pause, but keep the qualification.”**

| The animator needs | The IR supplies |
| --- | --- |
| Meaning | Shorten silence while preserving “for this interview.” |
| Evidence | The original quote and proposed edit, with source locations. |
| Possible misunderstanding | A smoother edit can accidentally imply a broader claim. |
| Visual obligation | Show the same words before and after. Only the silence disappears. |
| Timing | The gap closes on **remove**; the qualification stays visible on **keep**. |
| Creative freedom | The animator chooses layout, motion, typography and treatment. |

[Follow the complete eight-stage example](skills/narration-ir/examples/interview/walkthrough.md)
from opening question to payoff. It includes a deliberately misleading treatment
and a repair. The case and timestamps are synthetic; this is an inspectable
planning example, not footage of a real interview or an evaluated video.

## Install the skill

With the optional [Skills CLI](https://github.com/vercel-labs/skills) (Node.js
22.20+), run this from the project where you want to use it and select your agent:

```sh
npx skills add wcook04/narration-ir --skill narration-ir
```

Or install manually without Node.js:

Clone this repository and copy **the whole `skills/narration-ir` folder** to the
skills location supported by your agent. It contains its own references, schema,
examples and helpers. It has no links back to this checkout at runtime.

```sh
git clone https://github.com/wcook04/narration-ir.git
```

For a project using Claude Code, from that project's directory:

```sh
mkdir -p .claude/skills
cp -R /path/to/narration-ir/skills/narration-ir .claude/skills/
```

For Codex, copy the same folder into `.agents/skills/` in your project or
`~/.agents/skills/` for personal use. These are the documented
[Codex locations](https://developers.openai.com/api/reference/cli); the Claude
locations are documented in [Claude Code skills](https://code.claude.com/docs/en/skills).
For another host, use its documented Agent Skills location.
If your host does not discover skills, ask it to read
`skills/narration-ir/SKILL.md` directly. Manual use needs no installer, API key,
Python environment, or renderer.

Then ask your agent:

> Use narration-ir on my recording and source folder. Keep the recorded words.
> Build the global explanation and sentence-level meaning, evidence, audience
> states, misconceptions and visual obligations. Anchor meaningful events to
> spoken words, review chronology, then give my animator a packet per scene.

For a script that is still changing, add: “Develop the script and pictures
together; timing remains provisional until I record.”

## Try the optional tools

Python 3.10+; `jsonschema` is the only runtime dependency. From the repo root:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python skills/narration-ir/scripts/narration_ir.py validate skills/narration-ir/examples/interview/plan.json
.venv/bin/python skills/narration-ir/scripts/narration_ir.py packet skills/narration-ir/examples/interview/plan.json --beat b04
```

On Windows use `.venv\Scripts\python.exe`. Validation reports structural and
timing errors separately from warnings and open review issues. The example
passes the mechanical rules and explicitly retains synthetic timing and an
unreviewed audiovisual result. The packet includes global purpose, sentence
meaning, word occurrences, source evidence, continuity and resolved events.

Import the `words` array from Whisper/WhisperX JSON with `import-whisper`; see
[the format and commands](skills/narration-ir/references/contract.md). Untimed
words are rejected. No transcription engine or renderer is bundled or installed.

## What belongs in the plan?

The **global plan** records audience, opening question, payoff, section route,
persistent objects, style preferences and available capabilities. The **local
plan** records literal speech, source-grounded elaboration, audience before/after,
misconceptions, exclusions, prerequisites and visual obligations. Word anchors
bind the explanation to a particular transcript revision.

Ten-to-one elaboration can be useful when the speaker compresses substantial
background into a sentence. It is a configurable depth target, not a quality
score. A word can retain the previous picture; it does not need a new animation.

The skill includes hook/development/payoff coherence and viewer orientation.
It makes no virality promises and includes no reposting or variant-farming workflow.

## Repository map

| Location | Purpose |
| --- | --- |
| [skills/narration-ir](skills/narration-ir/SKILL.md) | Complete installable skill; copy this folder. |
| [Worked example](skills/narration-ir/examples/interview/walkthrough.md) | Eight stages, sources, populated plan and a failed treatment. |
| [References](skills/narration-ir/references/contract.md) | Portable schema, review method and renderer handoff. |
| [tests](tests/test_narration_ir.py) | Timing, chronology, import and isolated-copy regression tests. |
| [scripts](scripts/verify.py) | Maintainer verification and repository layout enforcement. |
| [docs](docs/provenance.md) | Design sources, limitations and release evidence. |

Run `python3 scripts/verify.py` after installing `requirements.txt` in your active
environment. [Contributing](CONTRIBUTING.md) explains the same validation route.

## Origins and license

Developed by Will Cook from a workflow for giving animation agents the context
behind recorded explanations. The public example is newly authored and fictional;
no private recordings, transcripts, conversations or project data are included.
[Design sources and adoption decisions](docs/provenance.md) distinguish this
skill from renderer-specific skills and explain what was reused.

Apache-2.0. [License](LICENSE). The same license travels inside the copied skill.
