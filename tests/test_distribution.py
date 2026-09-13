import importlib.util
import json
import os
from pathlib import Path
import shutil
import tempfile
import unittest
from unittest import mock


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location("loop_install", ROOT / "scripts/install.py")
installer = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(installer)


class DistributionTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="programming-loop-test-")
        self.addCleanup(self.temp.cleanup)
        self.base = Path(self.temp.name).resolve()
        self.home = self.base / "user space 雪"
        self.home.mkdir()

    def copy_source(self):
        source = self.base / "release"
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns("__pycache__"))
        return source

    def assert_no_staging(self, host):
        root = self.home / installer.HOSTS[host]
        self.assertEqual(list(root.glob(".programming-loop-*")), [])

    def tree_bytes(self, root):
        return {
            str(path.relative_to(root)): path.read_bytes()
            for path in root.rglob("*") if path.is_file()
        }

    def test_all_selected_hosts_load_complete_identified_method_without_calls(self):
        fake_bin = self.base / "fake-bin"
        fake_bin.mkdir()
        for executable in ("codex", "claude", "zcode", "hermes", "qwen", "mcode"):
            path = fake_bin / executable
            path.write_text("#!/bin/sh\nexit 89\n", encoding="utf-8")
            path.chmod(0o755)
        with mock.patch.dict(os.environ, {"PATH": str(fake_bin)}):
            for host in installer.HOSTS:
                with self.subTest(host=host):
                    skill = installer.install(ROOT, host, self.home)
                    identity = json.loads((skill / "SOURCE.json").read_text())
                    self.assertEqual(identity["component"], "programming-loop")
                    self.assertEqual(identity["source"], "programming-loop")
                    self.assertEqual(identity["host"], host)
                    self.assertEqual(identity["version"], (ROOT / "VERSION").read_text().strip())
                    for name in ("frameworks/programming-loop.md", f"adapters/{host}.md", "VERSION"):
                        self.assertEqual((skill / name).read_bytes(), (ROOT / name).read_bytes())
                    source_entry = (ROOT / "skills/programming-loop/SKILL.md").read_bytes()
                    installed_entry = (skill / "SKILL.md").read_bytes()
                    expected_entry = source_entry.replace(
                        b"`../../frameworks/programming-loop.md`",
                        b"`./frameworks/programming-loop.md`",
                    ).replace(b"`../../adapters/`", f"`./adapters/{host}.md`".encode())
                    self.assertEqual(installed_entry, expected_entry)
                    self.assertEqual(identity["files"]["SKILL.md"], installer.digest(installed_entry))
                    for resource in (skill / "frameworks/programming-loop.md",
                                     skill / f"adapters/{host}.md"):
                        self.assertTrue(resource.is_file(), resource)
                        self.assertTrue(resource.read_text(encoding="utf-8").strip(), resource)
                    self.assertEqual(list((skill / "adapters").glob("*.md")), [skill / f"adapters/{host}.md"])
                    self.assertFalse(installer.inspect_installation(self.home / installer.HOSTS[host], host)["mismatches"])
                    if host in installer.PROFILE_HOSTS:
                        self.assertEqual((self.home / installer.HOSTS[host] / "agents" / installer.PROFILE).read_bytes(),
                                         (ROOT / "profiles" / host / installer.PROFILE).read_bytes())
                    self.assert_no_staging(host)

    def test_update_switches_complete_resources_and_preserves_user_additions(self):
        source = self.copy_source()
        skill = installer.install(source, "claude", self.home)
        extra = skill / "user-notes.txt"
        extra.write_text("Keep my notes", encoding="utf-8")
        (source / "VERSION").write_text("1.0.1\n", encoding="utf-8")
        (source / "frameworks/programming-loop.md").write_text("# Replacement complete method\n", encoding="utf-8")
        installer.install(source, "claude", self.home)
        self.assertEqual(extra.read_text(), "Keep my notes")
        self.assertEqual((skill / "VERSION").read_text(), "1.0.1\n")
        self.assertEqual((skill / "frameworks/programming-loop.md").read_bytes(),
                         (source / "frameworks/programming-loop.md").read_bytes())
        self.assert_no_staging("claude")

    def test_failed_preparation_preserves_usable_installation(self):
        source = self.copy_source()
        skill = installer.install(source, "hermes", self.home)
        previous = (skill / "SOURCE.json").read_bytes()
        (source / "adapters/hermes.md").unlink()
        with self.assertRaises(installer.InstallationError):
            installer.install(source, "hermes", self.home)
        self.assertEqual((skill / "SOURCE.json").read_bytes(), previous)
        self.assertFalse(installer.inspect_installation(self.home / ".hermes", "hermes")["mismatches"])
        self.assert_no_staging("hermes")
        (skill / "adapters/hermes.md").unlink()
        self.assertTrue(installer.inspect_installation(self.home / ".hermes", "hermes")["mismatches"])
        damaged = self.tree_bytes(self.home / ".hermes")
        with self.assertRaisesRegex(installer.InstallationError, "changed or are missing"):
            installer.install(ROOT, "hermes", self.home)
        self.assertEqual(self.tree_bytes(self.home / ".hermes"), damaged)
        self.assertFalse((skill / "adapters/hermes.md").exists())
        (skill / "adapters/hermes.md").write_bytes((ROOT / "adapters/hermes.md").read_bytes())
        reviewer_skill = installer.install(source, "qwen", self.home)
        reviewer_identity = (reviewer_skill / "SOURCE.json").read_bytes()
        installed_profile = self.home / ".qwen/agents" / installer.PROFILE
        installed_profile.unlink()
        damaged = self.tree_bytes(self.home / ".qwen")
        with self.assertRaisesRegex(installer.InstallationError, "changed or are missing"):
            installer.install(ROOT, "qwen", self.home)
        self.assertEqual(self.tree_bytes(self.home / ".qwen"), damaged)
        self.assertFalse(installed_profile.exists())
        installed_profile.write_bytes((ROOT / "profiles/qwen" / installer.PROFILE).read_bytes())
        (source / "profiles/qwen" / installer.PROFILE).write_bytes(b"")
        with self.assertRaises(installer.InstallationError):
            installer.install(source, "qwen", self.home)
        self.assertEqual((reviewer_skill / "SOURCE.json").read_bytes(), reviewer_identity)
        self.assertFalse(installer.inspect_installation(self.home / ".qwen", "qwen")["mismatches"])

    def test_failed_profile_switch_restores_old_skill_and_profile(self):
        source = self.copy_source()
        skill = installer.install(source, "qwen", self.home)
        previous = (skill / "SOURCE.json").read_bytes()
        profile = self.home / ".qwen/agents" / installer.PROFILE
        old_profile = profile.read_bytes()
        (source / "VERSION").write_text("1.0.1\n", encoding="utf-8")
        (source / "profiles/qwen" / installer.PROFILE).write_text("new profile\n", encoding="utf-8")
        replace = os.replace
        failed = False

        def fail_once(src, dst):
            nonlocal failed
            if Path(src).parent.name.startswith(".programming-loop-stage-") and Path(src).name == "profile" and not failed:
                failed = True
                raise OSError("injected failed replacement")
            return replace(src, dst)

        with mock.patch.object(installer.os, "replace", side_effect=fail_once):
            with self.assertRaisesRegex(OSError, "injected failed replacement"):
                installer.install(source, "qwen", self.home)
        self.assertEqual((skill / "SOURCE.json").read_bytes(), previous)
        self.assertEqual(profile.read_bytes(), old_profile)
        self.assertFalse(installer.inspect_installation(self.home / ".qwen", "qwen")["mismatches"])
        self.assert_no_staging("qwen")

    def test_removal_refuses_edited_owned_content_and_rolls_back_failure(self):
        skill = installer.install(ROOT, "zcode", self.home)
        root = self.home / ".zcode"
        unrelated = root / "settings.json"
        unrelated.write_text("unrelated settings", encoding="utf-8")
        other = root / "skills/other/SKILL.md"
        other.parent.mkdir()
        other.write_text("other skill", encoding="utf-8")
        extra = skill / "notes.txt"
        extra.write_text("user note", encoding="utf-8")
        edited = skill / "adapters/zcode.md"
        original_edited = edited.read_bytes()
        edited.write_text("user edit", encoding="utf-8")

        with self.assertRaisesRegex(installer.InstallationError, "changed or are missing"):
            installer.remove("zcode", self.home)
        self.assertTrue((skill / "SKILL.md").is_file())
        self.assertTrue((skill / "SOURCE.json").is_file())
        self.assertTrue((root / "agents" / installer.PROFILE).is_file())
        self.assertEqual(extra.read_text(), "user note")
        edited.write_bytes(original_edited)

        replace = os.replace
        failed = False

        def fail_profile_removal(src, dst):
            nonlocal failed
            if Path(dst).name == "original-profile" and not failed:
                failed = True
                raise OSError("injected failed removal")
            return replace(src, dst)

        with mock.patch.object(installer.os, "replace", side_effect=fail_profile_removal):
            with self.assertRaisesRegex(OSError, "injected failed removal"):
                installer.remove("zcode", self.home)
        self.assertFalse(installer.inspect_installation(root, "zcode")["mismatches"])
        self.assertEqual(extra.read_text(), "user note")
        self.assert_no_staging("zcode")

        retained = installer.remove("zcode", self.home)
        self.assertIn(str(extra), retained)
        self.assertEqual(unrelated.read_text(), "unrelated settings")
        self.assertEqual(other.read_text(), "other skill")
        self.assertEqual(extra.read_text(), "user note")
        self.assertFalse((skill / "SKILL.md").exists())
        self.assertFalse((root / "agents" / installer.PROFILE).exists())

    def test_unmanaged_or_edited_install_is_never_overwritten(self):
        skill = self.home / ".codex/skills/programming-loop"
        skill.mkdir(parents=True)
        entry = skill / "SKILL.md"
        entry.write_text("unmanaged user skill", encoding="utf-8")
        with self.assertRaises(installer.InstallationError):
            installer.install(ROOT, "codex", self.home)
        self.assertEqual(entry.read_text(), "unmanaged user skill")
        installed = installer.install(ROOT, "minimax", self.home)
        method = installed / "frameworks/programming-loop.md"
        method.write_text("user's edited method", encoding="utf-8")
        with self.assertRaises(installer.InstallationError):
            installer.install(ROOT, "minimax", self.home)
        self.assertEqual(method.read_text(), "user's edited method")
        metadata_path = installed / "SOURCE.json"
        metadata = json.loads(metadata_path.read_text())
        metadata["files"] = {}
        metadata_path.write_text(json.dumps(metadata), encoding="utf-8")
        with self.assertRaises(installer.InstallationError):
            installer.inspect_installation(self.home / ".minimax", "minimax")
        clean = installer.install(ROOT, "hermes", self.home)
        extra = clean / "future-resource.md"
        extra.write_text("user-owned future collision", encoding="utf-8")
        real_payload = installer.payload

        def new_payload(source, host):
            files, profile = real_payload(source, host)
            files["future-resource.md"] = b"new package content"
            return files, profile

        with mock.patch.object(installer, "payload", side_effect=new_payload):
            with self.assertRaises(installer.InstallationError):
                installer.install(ROOT, "hermes", self.home)
        self.assertEqual(extra.read_text(), "user-owned future collision")

    def test_explicit_profile_root_and_symbolic_link_preservation(self):
        root = self.base / "Hermes profile"
        skill = installer.install(ROOT, "hermes", host_root=root)
        self.assertEqual(skill, root / "skills/programming-loop")
        self.assertEqual(installer.remove("hermes", host_root=root), [])
        self.assertFalse(skill.exists())
        if hasattr(os, "symlink"):
            real = self.base / "unrelated-directory"
            real.mkdir()
            link = self.home / ".claude"
            try:
                link.symlink_to(real, target_is_directory=True)
            except OSError:
                return  # The OS may require explicit symlink privileges.
            with self.assertRaises(installer.InstallationError):
                installer.install(ROOT, "claude", self.home)
            self.assertEqual(list(real.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
