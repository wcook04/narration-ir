# Release validation

The first release is a portable planning skill. It has no rendered-video demo,
audio-alignment evaluation, agent behavior benchmark or viewer-learning result.

## Executed locally

- Python 3.12: 34 IR, import and isolated-copy test methods passed.
- Portable repository gate: 22 regression test methods passed, including working
  versus staged contents, missing owners and directory placement.
- The fictional example validates with 97 word occurrences, eight beats and nine
  timed events. Synthetic timing and unreviewed audiovisual output remain warnings.
- The Agent Skills metadata validator accepts `skills/narration-ir`.
- Skills CLI 1.7.6 installs the local repository for Codex and Claude Code with
  `--copy`. All 13 maintained skill payload files match in both installed copies;
  their helper runs successfully from outside the repository.
- The isolated-copy test removes its temporary donor, uses an empty home, and
  executes with Python's isolated mode. It validates the example and generates
  a scene packet without source-checkout imports or host configuration.
- Local relative Markdown links resolve. The public tree contains no personal
  filesystem paths or private project imports. Gitleaks scans the initial Git
  history and working directory without detected secrets.
- A fresh `git clone --no-local` of implementation commit `66749e0` into a separate
  checkout passed the README's virtual-environment installation, full verification
  command and `b04` scene-packet command with no inherited `PYTHONPATH`.

`python scripts/verify.py` is the maintained validation command. Hosted CI runs
the same command on Python 3.10, 3.12 and 3.13; see the live Actions results for
the commit being consumed rather than treating this dated local record as CI proof.

The README underwent an author self-review: it identifies the input, outputs,
first example, installation unit, optional dependencies and the limit of a
passing validator. This is not an independent reader study or a test of automatic
skill activation inside every supported host.
