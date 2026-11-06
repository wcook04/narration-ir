# Sources and design decisions

Reviewed on 6 November 2026. This is a skill-first release: meaning, evidence,
audience state, chronology and word-bound obligations precede renderer choices.
The standalone helper and fictional example were authored for this repository.
There is no dependency on the author's private production system.

## Packaging sources

- [Agent Skills specification](https://agentskills.io/specification): adopt the
  `SKILL.md` entry with `name` and `description`, plus optional `references/`,
  `scripts/` and `agents/`. Keep resources inside the copied folder. This is format
  compatibility, not evidence that every host discovers the skill automatically.
- [Remotion skills](https://github.com/remotion-dev/skills/tree/a2824c67f8b4585c294a8101db9f9f0ad3c643f8):
  inspected the router entry. Adopt selective reference loading. Do not copy its
  renderer setup, API guidance or host-specific preview behavior. GitHub did not
  identify a repository-wide license at inspection; no payload was copied.
- [Manim video skill](https://github.com/vumichien/manim-skill/tree/70ccd68cf4dea135973f899b25fb408ddf5946c5):
  inspected `skills/manim-video/SKILL.md` and its Apache-2.0 license. Adopt the
  pattern of a concrete artifact handoff with validation. Do not require its
  four-role orchestration, voice services or Manim runtime. No payload was copied.
- [Chalkboard](https://github.com/nicglazkov/Chalkboard): examined the public
  project as adjacent work, not as an installed or benchmarked integration.

These projects informed packaging and boundaries; none is a required dependency.
The root layout gate and regression fixtures are copied unchanged from the
author's portable repository-organization tooling. The README's reader-first
ordering follows the reviewed Crafting Effective READMEs pattern; no template
prose or assets are redistributed.

## Creator evidence

The [supplied interview-editing explainer](https://www.youtube.com/watch?v=ZVcZsMrB1eI)
was inspected through its available caption track. The creator discusses
transcript-guided cut suggestions and editorial iteration;
later they describe a mistranslated word and the need to listen and review.
The adopted lesson is to preserve speaker qualifications and distinguish timing
from semantic acceptance. This release does not reproduce the creator's transcript,
assets or private correspondence. Visual frames and audio were not independently
reviewed, so the 01–08 display is the operator's supplied observation, not a claim
of our visual inspection. Our eight-stage example is new fictional material.

Public discussions such as [a creator's Remotion experience](https://www.reddit.com/r/ClaudeAI/comments/1syvi3p/i_used_claude_code_remotion_to_generate_my_apps/)
and [a timing-workflow discussion](https://www.reddit.com/r/vibecoding/comments/1vn4fbt/made_this_animation_with_claude_remotion/)
were discovery leads for the separation of editable timing and render/review.
They are anecdotal reports, not compatibility tests or evidence of improved
understanding. Technical choices were verified against the primary skill sources
above and the local regression suite.

## Deliberate scope

The opening question, development, payoff and optional stage indicator support
coherence within a video. Entertainment, educational and emotional value are
authoring prompts, not algorithmic ranking laws. No claim about three consecutive
uploads, watch-time thresholds or guaranteed virality is incorporated. Reposting,
multiple variants and distribution automation are outside this skill.

The optional helper validates declared facts about an IR; it cannot establish
that source interpretation is correct or that a finished visual communicates it.
No real-recording exporter, renderer adapter or finished-video benchmark is claimed.
A future integration should preserve source identities, occurrence IDs, output
clock and unresolved evidence rather than merely translating field names.
