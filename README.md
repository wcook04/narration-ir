# Narration IR

**Help your animation agent understand what you're saying.**

Give your agent a recording or draft script, plus the sources that explain the
subject. With this skill, the agent writes a scene-by-scene brief: what each
sentence means, what viewers need to see, and when the visuals should change.
Your animation agent then uses that brief with your chosen video tools.

The skill is a **folder of instructions, examples and optional helper scripts**.
You can install it in Claude Code, Codex or another agent that supports skills.
Use it alongside Remotion, Manim, Motion Canvas or your existing editing workflow.

[Install the skill](#install-the-skill) · [Read the worked example](skills/narration-ir/examples/interview/walkthrough.md)

![Three stages: your words and sources; a brief explaining meaning and timing; a visual plan that removes a pause while preserving “I saved time for this interview.”](assets/readme/narration-to-visual-plan.png)

*An illustration of the fictional interview example below. The image shows a
planned edit, not a screenshot of an app or a rendered video.*

**IR** means *intermediate representation*: here, the written plan between your
narration and the animation.

## See the difference

Suppose an interviewee says: **“I saved time [pause] for this interview.”**

You want to show how you edited the recording, and narrate:
**“I remove the pause, but keep the qualification.”** The qualification is
“for this interview”: those words limit the claim to one interview.

Your animation agent needs that context before deciding what to draw.

| In the brief | What the animator needs to know |
| --- | --- |
| Meaning | Shorten silence while preserving “for this interview.” |
| Source | Where to find the original quote and proposed edit. |
| Risk | Removing “for this interview” would make the claim broader. |
| What to show | The same words before and after. Only the silence disappears. |
| Timing | The gap closes on **remove**; the qualification stays visible on **keep**. |
| Design choices | The animator chooses the layout, motion and typography. |

[Follow the complete eight-stage example](skills/narration-ir/examples/interview/walkthrough.md)
from opening question to answer, including a deliberately misleading visual
proposal and its correction. The interview and timestamps are invented for the
example; no real interview footage is included.

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

> Use narration-ir on my recording and source folder. Keep my recorded words.
> Explain what each sentence means and what viewers need to see. Tie visual
> changes to the words I say. Make sure each idea is introduced before I refer
> to it, then give my animation agent a brief for each scene.

For a script that is still changing, add: “Develop the script and pictures
together; timing remains provisional until I record.”

## Try the optional tools

The skill's instructions work without Python. If you want to validate a JSON
plan or generate a brief for one scene, the helper needs Python 3.10+ and
`jsonschema`. From the repo root:

<details>
<summary>Install and run the Python helper</summary>

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python skills/narration-ir/scripts/narration_ir.py validate skills/narration-ir/examples/interview/plan.json
.venv/bin/python skills/narration-ir/scripts/narration_ir.py packet skills/narration-ir/examples/interview/plan.json --beat b04
```

On Windows use `.venv\Scripts\python.exe`. The `validate` command validates the
example's structure, references and declared timing. The `packet` command prints
the brief for scene `b04`, including source excerpts, explanation and event times.

The example passes validation, with warnings that its timing is synthetic and
no audiovisual output has been reviewed. A valid plan still needs review for
meaning, readability and timing against real audio.

Import the `words` array from Whisper/WhisperX JSON with `import-whisper`; see
[the format and commands](skills/narration-ir/references/contract.md). Untimed
words are rejected. No transcription engine or renderer is bundled or installed.

</details>

## What belongs in the plan?

For the **whole video**, the agent records who it is for, the opening question,
the answer you will give, and the steps needed to explain that answer. It also
records which objects and visual conventions should stay consistent, and which
existing skills, components and assets could help.

For **each sentence**, the agent explains what you mean using the sources. It
records what viewers already know, what they should understand next, what they
might misunderstand, and what the picture must show. Each planned visual change
refers to a specific spoken word, so repeated words can be distinguished.

Ten-to-one elaboration can be useful when the speaker compresses substantial
background into a sentence. Ask for that level of detail when useful; more words
alone do not make an explanation better. Most spoken words can accompany the
same picture without another animation.

With an **accepted recording**, the agent plans around the existing words and
timing. With a **draft script**, you can revise the words and pictures together,
then align the visuals after recording. Transcription timestamps are estimates
until reviewed against the audio.

## Repository map

| Location | Purpose |
| --- | --- |
| [skills/narration-ir](skills/narration-ir/SKILL.md) | Complete installable skill; copy this folder. |
| [Worked example](skills/narration-ir/examples/interview/walkthrough.md) | Eight stages, sources, populated plan and a failed treatment. |
| [References](skills/narration-ir/references/contract.md) | Portable schema, review method and renderer handoff. |
| [README illustration](assets/readme/narration-to-visual-plan.png) | Generated explanation of the worked example. |
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

Apache-2.0. [License](LICENSE). A copy is included in the skill folder.
