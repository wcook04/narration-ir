# Contributing

Keep the skill useful when copied alone into a different project. Demonstrate
changes with a small fictional or licensed example. Never commit recordings,
private transcripts, credentials, personal paths or unlicensed donor assets.

Create a virtual environment, install `requirements.txt`, and run:

```sh
python scripts/verify.py
git add <your-paths>
python scripts/check_layout.py --root . --index
```

Use a branch and pull request after the initial repository creation. Include a
concrete failure and repair when changing semantics. The optional helper does not
need to grow into a renderer. Preserve unknown evidence instead of fabricating
alignment, source support or viewer-review results.
