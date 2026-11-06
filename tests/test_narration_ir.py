import copy
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills/narration-ir"
SPEC = importlib.util.spec_from_file_location("narration_ir", SKILL / "scripts/narration_ir.py")
ir = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(ir)


class PlanTests(unittest.TestCase):
    def setUp(self):
        self.base = SKILL / "examples/interview"
        self.plan = ir.read_json(self.base / "plan.json")

    def result(self):
        return ir.validate(self.plan, self.base)

    def reject(self, text):
        result = self.result()
        self.assertFalse(result["valid"], result)
        self.assertIn(text, "\n".join(result["errors"]))

    def test_example_and_explicit_limits(self):
        result = self.result()
        self.assertTrue(result["valid"], result)
        self.assertEqual(len(result["events"]), 9)
        self.assertIn("synthetic", " ".join(result["warnings"]))
        self.assertIn("not been reviewed", " ".join(result["warnings"]))

    def test_stale_revision(self):
        self.plan["transcript"]["revision"] = "changed"
        self.reject("stale transcript")

    def test_modified_spoken_word(self):
        self.plan["transcript"]["words"][0]["text"] = "Why"
        self.reject("speech differs")

    def test_duplicate_word(self):
        self.plan["transcript"]["words"][1]["id"] = self.plan["transcript"]["words"][0]["id"]
        self.reject("duplicate word")

    def test_missing_word_coverage(self):
        self.plan["beats"][0]["word_ids"].pop()
        self.reject("cover every word")

    def test_unknown_word(self):
        self.plan["beats"][0]["word_ids"][0] = "absent"
        self.reject("unknown word")

    def test_anchor_from_wrong_beat(self):
        self.plan["events"][3]["anchor_word"] = self.plan["beats"][0]["word_ids"][0]
        self.reject("outside the owning beat")

    def test_obligation_from_wrong_beat(self):
        self.plan["events"][0]["obligation"] = "o02"
        self.reject("not owned by its beat")

    def test_duplicate_obligation(self):
        self.plan["beats"][1]["obligations"][0]["id"] = "o01"
        self.reject("duplicate obligation")

    def test_undeclared_concept(self):
        self.plan["beats"][0]["introduces"] = []
        self.reject("exactly one declaring beat")

    def test_later_prerequisite(self):
        self.plan["beats"][0]["requires"] = ["c08"]
        self.reject("has not been introduced")

    def test_premature_transition_even_when_target_is_later(self):
        event = self.plan["events"][3]
        event["requires"] = ["c04"]
        self.reject("premature reveal")

    def test_same_beat_late_introduction(self):
        event = self.plan["events"][3]
        event["requires"] = ["c04"]
        self.plan["concepts"][3]["introduced_at"] = self.plan["beats"][3]["word_ids"][-1]
        self.reject("premature reveal")

    def test_onset_and_settled_differ(self):
        words = {w["id"]: w for w in self.plan["transcript"]["words"]}
        event = copy.deepcopy(self.plan["events"][3])
        settled = ir.resolve_event(event, words)
        event["sync"] = "onset"
        onset = ir.resolve_event(event, words)
        self.assertEqual(settled["settled"], onset["start"])
        self.assertAlmostEqual(onset["settled"] - settled["settled"], .4)

    def test_emphasis_midpoint(self):
        words = {w["id"]: w for w in self.plan["transcript"]["words"]}
        event = dict(self.plan["events"][0], sync="emphasis")
        time = ir.resolve_event(event, words)
        self.assertAlmostEqual(time["target"] - time["start"], .2)

    def test_hold_exceeds_available_time(self):
        self.plan["events"][0]["hold"] = 100
        self.reject("exceeds its beat")

    def test_source_bytes_changed(self):
        self.plan["sources"][0]["sha256"] = "0" * 64
        self.reject("source digest changed")

    def test_fabricated_source_excerpt(self):
        self.plan["beats"][0]["source_refs"][0]["excerpt"] = "AI edits perfectly."
        self.reject("excerpt absent")

    def test_source_escape(self):
        self.plan["sources"][0]["path"] = "../outside.md"
        self.reject("must stay within")

    def test_source_symlink_escape(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            base = root / "case"
            base.mkdir()
            (root / "secret.md").write_text("private")
            (base / "source.md").symlink_to(root / "secret.md")
            result = ir.validate(self.plan, base)
            self.assertIn("must stay within", " ".join(result["errors"]))

    def test_unknown_object(self):
        self.plan["beats"][0]["objects"] = ["unknown"]
        self.reject("unknown persistent object")

    def test_route_mismatch_is_diagnostic(self):
        self.plan["global_plan"]["route"] = ["unknown"]
        self.reject("section order")

    def test_synthetic_recording_is_rejected(self):
        self.plan["mode"] = "accepted_recording"
        self.reject("requires imported recording")

    def test_untimed_script_has_no_schedule(self):
        self.plan["transcript"].update(provenance="untimed", duration=None)
        for word in self.plan["transcript"]["words"]:
            word.update(start=None, end=None)
        for beat in self.plan["beats"]:
            beat.update(start=None, end=None)
        self.plan["transcript_sha256"] = ir.digest(self.plan["transcript"])
        report = self.result()
        self.assertTrue(report["valid"], report)
        self.assertEqual(report["events"], [])
        self.assertIn("no executable schedule", " ".join(report["warnings"]))

    def test_non_finite_event_is_rejected(self):
        self.plan["events"][0]["duration"] = float("inf")
        self.reject("non-finite")

    def test_wrong_shape_is_diagnostic(self):
        self.plan["beats"] = "bad"
        self.reject("shape")

    def test_packet_includes_context_and_issues(self):
        packet = ir.packet(self.plan, "b04", self.result())
        self.assertEqual(packet["timing_provenance"], "synthetic")
        self.assertTrue(packet["beat"]["source_refs"][0]["excerpt"])
        self.assertEqual(len(packet["resolved_events"]), 2)
        self.assertTrue(packet["previous_handoff"])
        self.assertTrue(packet["next_speech"])
        self.assertEqual(packet["review"]["issues"], self.plan["review"]["issues"])


class ImportTests(unittest.TestCase):
    def test_repeated_words_have_distinct_occurrence_ids(self):
        data = {"segments": [{"words": [{"word": " same", "start": 0, "end": .2},
                                          {"word": " same", "start": .5, "end": .7}]}]}
        result = ir.import_whisper(data, "r1")
        self.assertNotEqual(result["words"][0]["id"], result["words"][1]["id"])
        self.assertEqual(result["provenance"], "asr_unreviewed")

    def test_untimed_word_does_not_get_interpolated(self):
        with self.assertRaisesRegex(ValueError, "missing"):
            ir.import_whisper({"words": [{"word": "number", "start": 1}]}, "r")

    def test_segment_only_is_rejected(self):
        with self.assertRaises(ValueError):
            ir.import_whisper({"segments": [{"text": "Hello", "start": 0, "end": 1}]}, "r")

    def test_partial_segments_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "partial"):
            ir.import_whisper({"segments": [{"text": "one", "words": [{"word": "one", "start": 0, "end": 1}]}, {"text": "two"}]}, "r")

    def test_bad_inputs_raise_explanations(self):
        for data in ([], {"words": "bad"}, {"segments": ["bad"]}, {"words": [{"word": "x", "start": True, "end": 2}]}):
            with self.subTest(data=data), self.assertRaises(ValueError):
                ir.import_whisper(data, "r")

    def test_overlapping_words_are_rejected(self):
        with self.assertRaisesRegex(ValueError, "overlapping"):
            ir.import_whisper({"words": [{"word": "a", "start": 0, "end": 2}, {"word": "b", "start": 1, "end": 3}]}, "r")


class PortableTests(unittest.TestCase):
    def test_copied_skill_runs_without_checkout_or_home_configuration(self):
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            # Rename the staged donor out of existence after copying; execution
            # has no source checkout on sys.path, cwd, or HOME.
            donor = root / "donor"
            shutil.copytree(SKILL, donor, ignore=shutil.ignore_patterns("__pycache__"))
            installed = root / "installed/narration-ir"
            shutil.copytree(donor, installed)
            shutil.rmtree(donor)
            home = root / "empty-home"
            home.mkdir()
            env = {"PATH": os.environ.get("PATH", ""), "HOME": str(home)}
            script = installed / "scripts/narration_ir.py"
            plan = installed / "examples/interview/plan.json"
            for args in (("validate", str(plan)), ("packet", str(plan), "--beat", "b04")):
                result = subprocess.run([sys.executable, "-I", str(script), *args], cwd=root,
                                        env=env, capture_output=True, text=True)
                self.assertEqual(result.returncode, 0, result.stderr + result.stdout)
                output = json.loads(result.stdout)
                self.assertNotIn(str(ROOT), result.stdout)
                self.assertTrue(output)
            self.assertTrue((installed / "LICENSE").is_file())
            self.assertTrue((installed / "NOTICE").is_file())


if __name__ == "__main__":
    unittest.main()
