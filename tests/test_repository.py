from __future__ import annotations

import importlib.util
import json
import subprocess
import sys
import tempfile
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
        self.assertGreaterEqual(len(cases), 28)
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

    def test_force_install_keeps_backup_outside_skill_discovery(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skills_dir = Path(temp_dir) / "skills"
            command = [sys.executable, str(ROOT / "scripts" / "install.py"), "--skills-dir", str(skills_dir)]
            subprocess.run(command, check=True, capture_output=True, text=True)
            subprocess.run([*command, "--force"], check=True, capture_output=True, text=True)
            self.assertTrue((skills_dir / SKILL.name / "SKILL.md").is_file())
            self.assertEqual([path.name for path in skills_dir.iterdir()], [SKILL.name])
            backups = list((Path(temp_dir) / "skill-backups").iterdir())
            self.assertEqual(len(backups), 1)
            self.assertTrue((backups[0] / "SKILL.md").is_file())

    def test_language_installation_and_unrelated_skill_preservation(self) -> None:
        for language, names in (
            ("en", {SKILL.name + "-en"}),
            ("both", {SKILL.name, SKILL.name + "-en"}),
        ):
            with self.subTest(language=language), tempfile.TemporaryDirectory() as temp_dir:
                skills_dir = Path(temp_dir) / "skills"
                unrelated = skills_dir / "unrelated"
                unrelated.mkdir(parents=True)
                marker = unrelated / "marker.txt"
                marker.write_text("retain unrelated data")
                command = [sys.executable, str(ROOT / "scripts/install.py"),
                           "--skills-dir", str(skills_dir), "--language", language]
                subprocess.run(command, check=True, capture_output=True, text=True)
                self.assertEqual({p.name for p in skills_dir.iterdir()}, names | {"unrelated"})
                for name in names:
                    self.assertTrue((skills_dir / name / "references" / "essential-methods.md").is_file())
                subprocess.run([*command, "--force"], check=True, capture_output=True, text=True)
                self.assertEqual(len(list((Path(temp_dir) / "skill-backups").iterdir())), len(names))
                self.assertEqual(marker.read_text(), "retain unrelated data")

    def test_both_install_preflights_before_mutating(self) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            skills_dir = Path(temp_dir) / "skills"
            english = skills_dir / (SKILL.name + "-en")
            english.mkdir(parents=True)
            marker = english / "marker.txt"
            marker.write_text("existing English installation")
            result = subprocess.run([sys.executable, str(ROOT / "scripts/install.py"),
                                     "--skills-dir", str(skills_dir), "--language", "both"],
                                    capture_output=True, text=True)
            self.assertNotEqual(result.returncode, 0)
            self.assertFalse((skills_dir / SKILL.name).exists())
            self.assertEqual(marker.read_text(), "existing English installation")

    def test_language_packages_have_matching_rules_and_reference_coverage(self) -> None:
        import re
        english = SKILL.with_name(SKILL.name + "-en")
        self.assertEqual({p.name for p in (SKILL / "references").glob("*.md")},
                         {p.name for p in (english / "references").glob("*.md")})
        for skill in (SKILL, english):
            text = (skill / "references" / "essential-methods.md").read_text()
            identifiers = re.findall(r"^\| (M\d{2}) ", text, flags=re.M)
            self.assertEqual(identifiers, [f"M{i:02d}" for i in range(1, 27)])


if __name__ == "__main__":
    unittest.main()
