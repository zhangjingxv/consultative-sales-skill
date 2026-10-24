from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest


SCRIPT = Path(__file__).resolve().parents[1] / "skills/consultative-sales-communication/scripts/message_lint.py"
spec = importlib.util.spec_from_file_location("bilingual_linter", SCRIPT)
linter = importlib.util.module_from_spec(spec)
spec.loader.exec_module(linter)


class MessageLintTests(unittest.TestCase):
    def test_one_rule_retains_every_exact_match(self):
        text = "🙂 完全兼容，而且保证！ I guarantee it."
        findings = linter.lint(text)
        self.assertEqual(len(findings), 1)
        matches = findings[0]["matches"]
        self.assertEqual([m["match"] for m in matches], ["完全兼容", "保证", "guarantee"])
        for match in matches:
            self.assertEqual(text[match["start"]:match["end"]], match["match"])

    def test_negation_does_not_hide_next_claim(self):
        for text in ("不能保证交期，但保证兼容。", "I can’t guarantee delivery, but I guarantee compatibility."):
            with self.subTest(text=text):
                findings = linter.lint(text)
                self.assertEqual(len(findings), 1)
                matches = findings[0]["matches"]
                self.assertEqual(len(matches), 1)
                self.assertGreater(matches[0]["start"], text.index(",") if "," in text else text.index("，"))

    def test_internal_details_are_reviewed_even_when_negated(self):
        findings = linter.lint("No gross margin above 30% is approved.")
        self.assertEqual([f["rule"] for f in findings], ["internal-commercial-data"])

    def test_long_english_spellings_do_not_trigger_chinese_limit(self):
        self.assertEqual(linter.lint("documentation " * 30), [])
        self.assertEqual([f["rule"] for f in linter.lint("detail " * 81)], ["long-message"])
        self.assertEqual([f["rule"] for f in linter.lint("内容" * 121)], ["long-message"])
        self.assertEqual([f["rule"] for f in linter.lint("资料 " * 60 + "detail " * 41)], ["long-message"])

    def test_question_punctuation_is_not_an_extra_question(self):
        self.assertEqual(linter.lint("Would tomorrow work??"), [])
        self.assertEqual([f["rule"] for f in linter.lint("Which model? What date?")], ["multiple-questions"])

    def test_cli_stdin_keeps_unmatched_context_out_of_output(self):
        for text, expected_code in (("Synthetic customer ABC-947. I will update you tomorrow.", 0),
                                    ("Synthetic customer ABC-947. I guarantee delivery.", 1)):
            with self.subTest(code=expected_code):
                run = subprocess.run([sys.executable, str(SCRIPT)], input=text,
                                     capture_output=True, text=True)
                self.assertEqual(run.returncode, expected_code)
                result = json.loads(run.stdout)
                self.assertEqual(result["ok"], expected_code == 0)
                self.assertIn("not verified", result["scope"])
                self.assertNotIn("ABC-947", run.stdout + run.stderr)

    def test_cli_file_input(self):
        with tempfile.TemporaryDirectory() as directory:
            source = Path(directory) / "draft.txt"
            source.write_text("不能保证交期，但保证兼容。", encoding="utf-8")
            run = subprocess.run([sys.executable, str(SCRIPT), "--file", str(source)],
                                 capture_output=True, text=True)
            self.assertEqual(run.returncode, 1)
            self.assertEqual(json.loads(run.stdout)["findings"][0]["rule"], "unsupported-certainty")


if __name__ == "__main__":
    unittest.main()
