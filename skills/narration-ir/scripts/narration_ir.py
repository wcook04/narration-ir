#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = ["jsonschema>=4.23,<5"]
# ///
"""Local validation, occurrence timing and scene packets; no renderer or network."""
from __future__ import annotations

import argparse
from collections import Counter
import hashlib
import json
import math
from pathlib import Path
import sys


SKILL = Path(__file__).resolve().parents[1]


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                    separators=(",", ":"), allow_nan=False).encode()).hexdigest()


def read_json(path):
    def reject(value):
        raise ValueError(f"Non-finite JSON number: {value}")
    return json.loads(Path(path).read_text(encoding="utf-8"), parse_constant=reject)


def resolve_event(event, words):
    """Emphasis uses the transition midpoint; settled uses its end, not onset."""
    word = words[event["anchor_word"]]
    anchor = word[event["anchor_edge"]]
    if anchor is None:
        return None
    target = anchor + event["offset"]
    duration = event["duration"]
    progress = {"onset": 0, "emphasis": 0.5, "settled": 1}[event["sync"]]
    start = target - progress * duration
    return {"id": event["id"], "start": round(start, 6), "target": round(target, 6),
            "settled": round(start + duration, 6),
            "hold_until": round(start + duration + event["hold"], 6)}


def validate(plan, base):
    try:
        json.dumps(plan, allow_nan=False)
    except ValueError:
        return {"valid": False, "errors": ["non-finite number in plan"], "warnings": [], "events": []}
    try:
        from jsonschema import Draft202012Validator
    except ImportError as exc:
        raise ValueError("Optional helper needs jsonschema: python -m pip install 'jsonschema>=4.23,<5'") from exc
    errors, warnings = [], []
    schema = read_json(SKILL / "references/plan.schema.json")
    for error in Draft202012Validator(schema).iter_errors(plan):
        errors.append(f"shape {'.'.join(map(str, error.absolute_path)) or '$'}: {error.message}")
    if errors:
        return {"valid": False, "errors": errors, "warnings": warnings, "events": []}

    def unique(rows, label):
        counts = Counter(row["id"] for row in rows)
        errors.extend(f"duplicate {label} ID: {key}" for key, n in counts.items() if n > 1)
        return {row["id"]: row for row in rows}

    transcript = plan["transcript"]
    try:
        current_digest = digest(transcript)
    except ValueError:
        return {"valid": False, "errors": ["transcript has non-finite numbers"], "warnings": [], "events": []}
    if plan["transcript_sha256"] != current_digest:
        errors.append("stale transcript binding: review and rebind the plan to the changed transcript")
    words = unique(transcript["words"], "word")
    beats = unique(plan["beats"], "beat")
    sections = unique(plan["sections"], "section")
    sources = unique(plan["sources"], "source")
    concepts = unique(plan["concepts"], "concept")
    objects = unique(plan["objects"], "object")
    unique(plan["events"], "event")
    obligations = unique([o for b in plan["beats"] for o in b["obligations"]], "obligation")
    positions = {w["id"]: i for i, w in enumerate(transcript["words"])}
    previous = 0
    untimed = transcript["provenance"] == "untimed"
    if untimed != (transcript["duration"] is None):
        errors.append("untimed provenance requires null duration; timed provenance requires a duration")
    for word in transcript["words"]:
        start, end = word["start"], word["end"]
        if untimed:
            if start is not None or end is not None:
                errors.append(f"{word['id']}: untimed transcript must use null word times")
        elif start is None or end is None:
            errors.append(f"{word['id']}: timed transcript has missing word times")
        elif not (previous <= start < end <= (transcript["duration"] or 0)):
            errors.append(f"{word['id']}: word times overlap, regress, or exceed duration")
        if end is not None:
            previous = end
    if plan["mode"] == "accepted_recording" and transcript["provenance"] in ("synthetic", "untimed"):
        errors.append("accepted_recording requires imported recording times, not synthetic or untimed data")
    if transcript["provenance"] != "audio_reviewed":
        warnings.append(f"timing provenance: {transcript['provenance']}; acoustic precision is not established")

    source_text = {}
    for source in sources.values():
        relative = Path(source["path"])
        path = (base / relative).resolve()
        if relative.is_absolute() or not path.is_relative_to(base.resolve()):
            errors.append(f"{source['id']}: source must stay within the plan directory")
            continue
        try:
            data = path.read_bytes()
            if hashlib.sha256(data).hexdigest() != source["sha256"]:
                errors.append(f"{source['id']}: source digest changed")
            source_text[source["id"]] = data.decode("utf-8")
        except (OSError, UnicodeError):
            errors.append(f"{source['id']}: cannot read UTF-8 source {source['path']}")

    for concept in concepts.values():
        if concept["introduced_at"] not in words:
            errors.append(f"{concept['id']}: unknown introduction word")
    route = plan["global_plan"]["route"]
    if route != [s["id"] for s in plan["sections"]]:
        errors.append("global route must match the declared section order")
    payoff = plan["global_plan"]["payoff_beat"]
    if payoff not in beats:
        errors.append("unknown payoff beat")
    coverage, prior_end, prior_section = [], 0, -1
    for beat in plan["beats"]:
        bid = beat["id"]
        if beat["section"] not in sections:
            errors.append(f"{bid}: unknown section")
        else:
            section_index = list(sections).index(beat["section"])
            if section_index < prior_section:
                errors.append(f"{bid}: section order regresses")
            prior_section = section_index
        ids = beat["word_ids"]
        coverage.extend(ids)
        if any(w not in words for w in ids):
            errors.append(f"{bid}: unknown word occurrence")
            continue
        if beat["speech"] != " ".join(words[w]["text"] for w in ids):
            errors.append(f"{bid}: speech differs from the bound word occurrences")
        if untimed:
            if beat["start"] is not None or beat["end"] is not None:
                errors.append(f"{bid}: untimed beat must use null bounds")
        elif beat["start"] is None or beat["end"] is None:
            errors.append(f"{bid}: missing timed beat bounds")
        else:
            if not (prior_end <= beat["start"] < beat["end"] <= (transcript["duration"] or 0)):
                errors.append(f"{bid}: beat bounds overlap, regress, or exceed duration")
            if any(words[w]["start"] is None or words[w]["end"] is None or
                   not (beat["start"] <= words[w]["start"] < words[w]["end"] <= beat["end"]) for w in ids):
                errors.append(f"{bid}: words outside the beat interval")
            prior_end = beat["end"]
        for cid in beat["requires"]:
            if cid not in concepts:
                errors.append(f"{bid}: unknown prerequisite {cid}")
            elif positions.get(concepts[cid]["introduced_at"], math.inf) >= positions[ids[0]]:
                errors.append(f"{bid}: prerequisite {cid} has not been introduced before this beat")
        for cid in beat["introduces"]:
            if cid not in concepts or concepts[cid]["introduced_at"] not in ids:
                errors.append(f"{bid}: introduction {cid} is not bound to this beat")
        for oid in beat["objects"]:
            if oid not in objects:
                errors.append(f"{bid}: unknown persistent object {oid}")
        for ref in beat["source_refs"]:
            sid = ref["source_id"]
            if sid not in sources:
                errors.append(f"{bid}: unknown source {sid}")
            elif sid in source_text and ref["excerpt"] not in source_text[sid]:
                errors.append(f"{bid}: excerpt absent from source {sid}")
    if coverage != list(words):
        errors.append("beats must cover every word exactly once in transcript order")
    introduced = Counter(c for b in plan["beats"] for c in b["introduces"])
    if set(introduced) != set(concepts) or any(n != 1 for n in introduced.values()):
        errors.append("every concept needs exactly one declaring beat")

    resolved, assigned = [], set()
    for event in plan["events"]:
        eid = event["id"]
        beat = beats.get(event["beat"])
        if beat is None:
            errors.append(f"{eid}: unknown owning beat")
            continue
        if event["obligation"] not in {o["id"] for o in beat["obligations"]}:
            errors.append(f"{eid}: obligation is not owned by its beat")
        else:
            assigned.add(event["obligation"])
        if event["anchor_word"] not in beat["word_ids"] or event["anchor_word"] not in words:
            errors.append(f"{eid}: anchor is outside the owning beat")
            continue
        timing = resolve_event(event, words)
        if timing is not None:
            resolved.append(timing)
            if beat["start"] is None or beat["end"] is None or timing["start"] < beat["start"] - 1e-6 or timing["hold_until"] > beat["end"] + 1e-6:
                errors.append(f"{eid}: transition or hold exceeds its beat interval")
        for cid in event["requires"]:
            concept = concepts.get(cid)
            if concept is None or concept["introduced_at"] not in words:
                errors.append(f"{eid}: unknown event prerequisite {cid}")
                continue
            intro = words[concept["introduced_at"]]
            if timing is not None and intro["start"] is not None:
                if timing["start"] < intro["start"] - 1e-6:
                    errors.append(f"{eid}: premature reveal before {cid} is introduced")
            elif positions[concept["introduced_at"]] > positions[event["anchor_word"]]:
                errors.append(f"{eid}: prerequisite {cid} is introduced after its anchor")
    for oid in obligations.keys() - assigned:
        warnings.append(f"{oid}: no timed event assigned; explain the deliberate hold or add a cue")
    if untimed:
        warnings.append("no executable schedule: record and align the script before rendering")
    warnings.extend(f"open review issue: {issue}" for issue in plan["review"]["issues"])
    if plan["review"]["audiovisual"] == "unreviewed":
        warnings.append("audiovisual output has not been reviewed")
    return {"valid": not errors, "errors": errors, "warnings": warnings,
            "events": resolved, "scope": "structure, references, source bytes and declared chronology only"}


def packet(plan, beat_id, report):
    index = next(i for i, b in enumerate(plan["beats"]) if b["id"] == beat_id)
    beat = plan["beats"][index]
    events = [e for e in plan["events"] if e["beat"] == beat_id]
    source_ids = {r["source_id"] for r in beat["source_refs"]}
    word_ids = set(beat["word_ids"])
    return {"schema": "narration-ir/scene-packet/0.1", "transcript_sha256": plan["transcript_sha256"],
            "timing_provenance": plan["transcript"]["provenance"], "global_plan": plan["global_plan"],
            "section": next(s for s in plan["sections"] if s["id"] == beat["section"]),
            "beat": beat, "words": [w for w in plan["transcript"]["words"] if w["id"] in word_ids],
            "sources": [s for s in plan["sources"] if s["id"] in source_ids],
            "objects": [o for o in plan["objects"] if o["id"] in beat["objects"]],
            "concepts": plan["concepts"], "events": events,
            "resolved_events": [e for e in report["events"] if e["id"] in {x["id"] for x in events}],
            "previous_handoff": plan["beats"][index-1]["handoff"] if index else "Opening: no prior scene.",
            "next_speech": plan["beats"][index+1]["speech"] if index+1 < len(plan["beats"]) else None,
            "review": plan["review"], "warnings": report["warnings"]}


def import_whisper(data, revision):
    if not isinstance(data, dict):
        raise ValueError("Whisper input must be a JSON object")
    raw = data.get("words")
    if raw is None:
        segments = data.get("segments", [])
        if not isinstance(segments, list) or any(not isinstance(s, dict) for s in segments):
            raise ValueError("Whisper segments must be objects")
        if any(not isinstance(s.get("words", []), list) for s in segments):
            raise ValueError("Whisper segment words must be arrays")
        if any(s.get("text", "").strip() and not s.get("words") for s in segments):
            raise ValueError("A nonempty segment lacks word timestamps; refusing a partial transcript")
        raw = [w for segment in segments for w in segment.get("words", [])]
    if not isinstance(raw, list) or any(not isinstance(w, dict) for w in raw):
        raise ValueError("Whisper words must be objects in an array")
    if not raw:
        raise ValueError("No word timestamps. Re-transcribe/align; segment times cannot establish word times.")
    words, previous = [], 0
    for i, word in enumerate(raw):
        start, end, value = word.get("start"), word.get("end"), word.get("word", word.get("text"))
        if (isinstance(start, bool) or isinstance(end, bool) or not isinstance(start, (int, float))
                or not isinstance(end, (int, float)) or not math.isfinite(start) or not math.isfinite(end)
                or not previous <= start < end or not isinstance(value, str) or not value.strip()):
            raise ValueError(f"Word {i+1} has missing, overlapping or invalid timing/text; resolve it against audio.")
        words.append({"id": f"{revision}:w{i+1:05d}", "text": value.strip(), "start": start, "end": end})
        previous = end
    return {"revision": revision, "provenance": "asr_unreviewed", "duration": previous, "words": words}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)
    for name in ("validate", "packet"):
        command = sub.add_parser(name)
        command.add_argument("plan", type=Path)
        if name == "packet":
            command.add_argument("--beat", required=True)
    command = sub.add_parser("import-whisper")
    command.add_argument("input", type=Path)
    command.add_argument("--revision", required=True)
    args = parser.parse_args(argv)
    try:
        if args.command == "import-whisper":
            result = import_whisper(read_json(args.input), args.revision)
        else:
            plan = read_json(args.plan)
            report = validate(plan, args.plan.parent)
            result = report
            if args.command == "packet" and report["valid"]:
                if args.beat not in {b["id"] for b in plan["beats"]}:
                    raise ValueError(f"Unknown beat: {args.beat}")
                result = packet(plan, args.beat, report)
            print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
            return 0 if report["valid"] else 1
        print(json.dumps(result, indent=2, ensure_ascii=False, allow_nan=False))
        return 0
    except (OSError, ValueError, TypeError, KeyError) as exc:
        print(json.dumps({"error": str(exc)}, ensure_ascii=False), file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
