from __future__ import annotations

import importlib.util
import json
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "skills" / "consultative-sales-communication"


class RepositoryTests(unittest.TestCase):
    def test_skill_package_exists(self) -> None:
        self.assertTrue((SKILL / "SKILL.md").is_file())
        self.assertTrue((SKILL / "agents" / "openai.yaml").is_file())

    def test_references_are_direct(self) -> None:
        references = SKILL / "references"
        self.assertTrue(references.is_dir())
        self.assertFalse(any(path.is_dir() for path in references.iterdir()))

    def test_no_template_placeholders(self) -> None:
        for path in SKILL.rglob("*.md"):
            text = path.read_text(encoding="utf-8")
            self.assertNotIn("TODO", text, path)
            self.assertNotIn("PLACEHOLDER", text, path)

    def test_public_tree_audit(self) -> None:
        script = ROOT / "scripts" / "audit_public_tree.py"
        spec = importlib.util.spec_from_file_location("audit_public_tree", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.main(), 0)

    def test_behavior_cases_are_well_formed(self) -> None:
        cases = json.loads((ROOT / "tests" / "cases.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(len(cases), 20)
        identifiers = {case["id"] for case in cases}
        self.assertEqual(len(identifiers), len(cases))
        for case in cases:
            self.assertIn(case["channel"], {"chat", "call", "meeting"})
            self.assertTrue(case["expected_decision"])
            self.assertTrue(case["required"])
            self.assertTrue(case["forbidden"])
            self.assertEqual(len(case["required"]), len(set(case["required"])))
            self.assertEqual(len(case["forbidden"]), len(set(case["forbidden"])))
            self.assertFalse(set(case["required"]) & set(case["forbidden"]))

    def test_message_linter(self) -> None:
        script = SKILL / "scripts" / "message_lint.py"
        spec = importlib.util.spec_from_file_location("message_lint", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        cases = json.loads((ROOT / "tests" / "linter_cases.json").read_text(encoding="utf-8"))
        for case in cases:
            with self.subTest(case=case["id"]):
                rules = {finding["rule"] for finding in module.lint(case["text"])}
                self.assertEqual(rules, set(case["expected_rules"]))

    def test_dependency_free_skill_validator(self) -> None:
        script = ROOT / "scripts" / "validate_skill.py"
        spec = importlib.util.spec_from_file_location("validate_skill", script)
        self.assertIsNotNone(spec)
        self.assertIsNotNone(spec.loader)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
        self.assertEqual(module.main(), 0)


if __name__ == "__main__":
    unittest.main()
