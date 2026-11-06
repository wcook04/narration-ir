# Working on Narration IR

The product is the self-contained folder `skills/narration-ir/`. Keep all runtime
resources inside it. Root docs, tests and CI serve repository maintainers and
must not be runtime dependencies of an installed copy.

Preserve accepted speech, stable word occurrences, explicit timing provenance,
evidence boundaries and the distinction between obligations and treatments.
Do not add a renderer, hosted transcription service, telemetry, agent-specific
orchestration, or private project integration as an implicit dependency.

Use Python 3.10+ and `requirements.txt` for optional helper development.
Run `python3 scripts/verify.py`, including the copied-payload test, before commits.
Run the layout gate with `--index` after staging. New directory roles belong in
`docs/repository_layout.json`; keep the README map current. Preserve unrelated
changes and commit scoped paths. Describe mechanical validation separately from
acoustic, semantic, audiovisual and user evaluation.
