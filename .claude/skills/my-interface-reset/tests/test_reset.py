"""Exercise reset mutations only in disposable project directories."""

import copy
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

import yaml


SCRIPT = Path(__file__).resolve().parents[1] / "scripts" / "reset.py"
OUTPUTS = ("backend", "frontend", "database", "developer")


class ResetTests(unittest.TestCase):
    def fixture(self, root, as_mapping=False):
        config = root / ".interface/config"
        config.mkdir(parents=True)
        tasks = [
            {"id": "T1", "status": "done", "title": "Keep", "log": ["verified"]},
            {"id": "T2", "status": "blocked", "blocker": "B1", "depends_on": ["T1"]},
        ]
        if as_mapping:
            tasks = {t["id"]: t for t in tasks}
        task = {"content": {"task_states": {"states": {"todo": "Not started"}},
                "plans": {"P1": {"id": "P1", "groups": {"G1": {"task_count": 2, "tasks": tasks}}},
                          "P2": {"id": "P2", "groups": {}}}}}
        state = {"content": {"active": {"mode": "development", "phase": "P1"},
                             "blockers": {"B1": {"what_is_missing": "Input"}},
                             "open_questions": {"Q1": {"question": "Keep?"}}}}
        for name, data in (("task", task), ("state", state)):
            (config / f"{name}.yaml").write_text(yaml.safe_dump(data))
        (config / "other.yaml").write_text("keep: true\n")
        for name in OUTPUTS + ("keep",):
            (root / name).mkdir()
            (root / name / "artifact").write_text("keep until reset")
        return config, task, state

    def run_reset(self, root, stage, apply=False):
        return subprocess.run([sys.executable, str(SCRIPT), stage] + (["--apply"] if apply else []),
                              cwd=root, capture_output=True, text=True)

    def snapshot(self, root):
        return {str(p.relative_to(root)): p.read_bytes() for p in root.rglob("*") if p.is_file()}

    def test_stages_and_collection_shapes(self):
        for stage in ("1", "2", "3"):
            for as_mapping in (False, True):
                with self.subTest(stage=stage, mapping=as_mapping), tempfile.TemporaryDirectory() as directory:
                    root = Path(directory)
                    config, task, state = self.fixture(root, as_mapping)
                    before = self.snapshot(root)
                    result = self.run_reset(root, stage)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertEqual(before, self.snapshot(root))
                    for name in OUTPUTS:
                        self.assertIn(f"Delete root directory: {name}/", result.stdout)
                    result = self.run_reset(root, stage, apply=True)
                    self.assertEqual(result.returncode, 0, result.stderr)
                    self.assertTrue((root / "keep/artifact").is_file())
                    for name in OUTPUTS:
                        self.assertFalse((root / name).exists())
                    if stage == "1":
                        self.assertTrue(config.is_dir())
                        self.assertEqual(list(config.iterdir()), [])
                        continue
                    actual = yaml.safe_load((config / "task.yaml").read_text())
                    actual_state = yaml.safe_load((config / "state.yaml").read_text())["content"]
                    expected = copy.deepcopy(task)
                    if stage == "2":
                        for plan in expected["content"]["plans"].values():
                            plan["groups"] = {}
                    else:
                        tasks = expected["content"]["plans"]["P1"]["groups"]["G1"]["tasks"]
                        for item in tasks.values() if as_mapping else tasks:
                            item["status"] = "todo"
                            item.pop("blocker", None)
                    self.assertEqual(actual, expected)
                    self.assertEqual(actual_state["active"]["mode"], "not set" if stage == "2" else "planning")
                    self.assertIsNone(actual_state["active"]["phase"])
                    for key in ("blockers", "open_questions"):
                        self.assertEqual(actual_state[key], state["content"][key])
                    self.assertEqual((config / "other.yaml").read_text(), "keep: true\n")

    def test_interpreter_handles_malformed_config_and_preserves_link_target(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config, _, _ = self.fixture(root)
            (config / "task.yaml").write_text("invalid: [")
            (config / "nested").mkdir()
            (config / "nested/value").write_text("remove")
            (config / "external").symlink_to(root / "keep", target_is_directory=True)
            result = self.run_reset(root, "1", apply=True)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(list(config.iterdir()), [])
            self.assertTrue((root / "keep/artifact").is_file())

    def test_invalid_input_never_mutates(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            config, task, _ = self.fixture(root)
            task["content"]["plans"]["P1"]["groups"]["G1"]["tasks"] = "invalid"
            (config / "task.yaml").write_text(yaml.safe_dump(task))
            for stage in ("2", "3", "0", "4", "interpreter", "task", "plan", "develop", "planning", "development"):
                before = self.snapshot(root)
                result = self.run_reset(root, stage, apply=True)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(before, self.snapshot(root))


if __name__ == "__main__":
    unittest.main()
