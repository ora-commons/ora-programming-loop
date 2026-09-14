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
        shutil.copytree(ROOT, source, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        return source

    def package_entries(self, source):
        return {
            name: (
                (source / name).read_bytes(),
                bool((source / name).stat().st_mode & 0o111),
            )
            for name in installer.PRODUCT_PATHS
        }

    def write_vendored_identity(self, source):
        entries = self.package_entries(source)
        tree = installer.git_tree_id(entries)
        commit = (
            f"tree {tree}\n"
            "author Programming Loop Test <test@example.invalid> 0 +0000\n"
            "committer Programming Loop Test <test@example.invalid> 0 +0000\n"
            "\npackage fixture\n"
        ).encode()
        identity = {
            "authoritative_repository": installer.AUTHORITATIVE_REPOSITORY,
            "component": "programming-loop",
            "files": {name: installer.digest(data) for name, (data, _mode) in entries.items()},
            "public_release_repository": installer.PUBLIC_REPOSITORY_IDENTIFIER,
            "source": "programming-loop",
            "source_revision": installer.git_object_id("commit", commit).hex(),
            "source_tree": tree,
            "vendored_snapshot": installer.VENDORED_SNAPSHOT,
            "version": (source / "VERSION").read_text().strip(),
        }
        (source / "SOURCE.json").write_text(json.dumps(identity), encoding="utf-8")
        return identity

    def write_public_manifest(self, source):
        manifest = {
            "version": 1,
            "files": [
                {
                    "path": name,
                    "sha256": installer.digest(data),
                    "executable": executable,
                }
                for name, (data, executable) in sorted(self.package_entries(source).items())
            ],
        }
        raw = (json.dumps(manifest, indent=2, sort_keys=True) + "\n").encode()
        (source / installer.PUBLIC_MANIFEST).write_bytes(raw)
        return manifest, raw

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
                    self.assertEqual(identity["public_release_repository"], installer.PUBLIC_REPOSITORY)
                    self.assertEqual(identity["source_kind"], "development-checkout")
                    self.assertIsNone(identity["source_manifest_sha256"])
                    self.assertIsNone(identity["source_revision"])
                    self.assertIsNone(identity["source_tree"])
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
                    self.assertIn(installer.PUBLIC_REPOSITORY,
                                  (skill / "README.md").read_text(encoding="utf-8"))
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
        legacy_identity = json.loads((skill / "SOURCE.json").read_text())
        for name in ("public_release_repository", "source_kind", "source_manifest_sha256",
                     "source_revision", "source_tree"):
            legacy_identity.pop(name)
        (skill / "SOURCE.json").write_text(json.dumps(legacy_identity), encoding="utf-8")
        (source / "VERSION").write_text("1.0.1\n", encoding="utf-8")
        (source / "frameworks/programming-loop.md").write_text("# Replacement complete method\n", encoding="utf-8")
        installer.install(source, "claude", self.home)
        self.assertEqual(extra.read_text(), "Keep my notes")
        self.assertEqual((skill / "VERSION").read_text(), "1.0.1\n")
        self.assertEqual((skill / "frameworks/programming-loop.md").read_bytes(),
                         (source / "frameworks/programming-loop.md").read_bytes())
        self.assert_no_staging("claude")

    def test_installed_identity_retains_available_package_provenance(self):
        source = self.copy_source()
        source_identity = self.write_vendored_identity(source)

        vendored = installer.install(source, "codex", self.home)
        identity = json.loads((vendored / "SOURCE.json").read_text())
        self.assertEqual(identity["public_release_repository"], installer.PUBLIC_REPOSITORY)
        self.assertEqual(identity["source_kind"], "vendored-snapshot")
        self.assertEqual(identity["source_revision"], source_identity["source_revision"])
        self.assertEqual(identity["source_tree"], source_identity["source_tree"])
        self.assertIsNone(identity["source_manifest_sha256"])
        self.assertNotIn("authoritative_repository", identity)

        public_source = self.base / "public-release"
        shutil.copytree(ROOT, public_source,
                        ignore=shutil.ignore_patterns("__pycache__", ".git"))
        _manifest, manifest_bytes = self.write_public_manifest(public_source)
        released = installer.install(public_source, "hermes", self.home)
        identity = json.loads((released / "SOURCE.json").read_text())
        self.assertEqual(identity["public_release_repository"], installer.PUBLIC_REPOSITORY)
        self.assertEqual(identity["source_kind"], "public-release")
        self.assertEqual(identity["source_manifest_sha256"], installer.digest(manifest_bytes))
        self.assertIsNone(identity["source_revision"])
        self.assertIsNone(identity["source_tree"])

    def test_public_release_ignores_root_git_metadata_but_preserves_destination_on_extra(self):
        root = self.home / installer.HOSTS["minimax"]
        for kind in ("directory", "gitfile"):
            with self.subTest(kind=kind):
                source = self.base / f"public-clone-{kind}"
                shutil.copytree(ROOT, source,
                                ignore=shutil.ignore_patterns("__pycache__", ".git"))
                self.write_public_manifest(source)
                git_metadata = source / ".git"
                if kind == "directory":
                    git_metadata.mkdir()
                else:
                    git_metadata.write_text("gitdir: /test/repository\n", encoding="utf-8")

                skill = installer.install(source, "minimax", self.home)
                self.assertTrue(skill.is_dir())
                self.assertEqual(
                    json.loads((skill / "SOURCE.json").read_text())["source_kind"],
                    "public-release",
                )
                preserved = self.tree_bytes(root)
                (source / "unexpected.txt").write_text("not package content\n", encoding="utf-8")
                with self.assertRaisesRegex(installer.InstallationError, "unexpected resource"):
                    installer.install(source, "minimax", self.home)
                self.assertEqual(self.tree_bytes(root), preserved)
                self.assert_no_staging("minimax")

    def test_public_release_rejects_nested_git_metadata_before_replacement(self):
        root = self.home / installer.HOSTS["minimax"]
        installer.install(ROOT, "minimax", self.home)
        preserved = self.tree_bytes(root)

        source = self.copy_source()
        self.write_public_manifest(source)
        (source / "subdir" / ".git").mkdir(parents=True)

        with self.assertRaisesRegex(installer.InstallationError, "nested Git control metadata"):
            installer.install(source, "minimax", self.home)
        self.assertEqual(self.tree_bytes(root), preserved)
        self.assert_no_staging("minimax")

    def test_untrusted_package_provenance_is_rejected_before_replacement(self):
        root = self.home / installer.HOSTS["minimax"]
        installer.install(ROOT, "minimax", self.home)
        preserved = self.tree_bytes(root)

        def assert_rejected(source, pattern):
            with self.assertRaisesRegex(installer.InstallationError, pattern):
                installer.install(source, "minimax", self.home)
            self.assertEqual(self.tree_bytes(root), preserved)
            self.assert_no_staging("minimax")

        cases = []

        incomplete = self.base / "incomplete-vendored"
        shutil.copytree(ROOT, incomplete, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        metadata = self.write_vendored_identity(incomplete)
        metadata.pop("source_revision")
        (incomplete / "SOURCE.json").write_text(json.dumps(metadata), encoding="utf-8")
        cases.append(("incomplete vendored identity", incomplete, "does not identify"))

        self_attested = self.base / "self-attested-vendored"
        shutil.copytree(ROOT, self_attested,
                        ignore=shutil.ignore_patterns("__pycache__", ".git"))
        metadata = self.write_vendored_identity(self_attested)
        metadata["source_tree"] = "2" * 40
        (self_attested / "SOURCE.json").write_text(json.dumps(metadata), encoding="utf-8")
        cases.append(("invented source tree", self_attested, "source tree does not match"))

        for field, wrong in (
                ("authoritative_repository", "ora-commons/ora-programming-loop"),
                ("public_release_repository", installer.PUBLIC_REPOSITORY),
                ("vendored_snapshot", "programming-loop")):
            wrong_repository = self.base / f"wrong-{field}"
            shutil.copytree(ROOT, wrong_repository,
                            ignore=shutil.ignore_patterns("__pycache__", ".git"))
            metadata = self.write_vendored_identity(wrong_repository)
            metadata[field] = wrong
            (wrong_repository / "SOURCE.json").write_text(
                json.dumps(metadata), encoding="utf-8"
            )
            cases.append((f"wrong {field}", wrong_repository, "does not identify"))

        tampered = self.base / "tampered-vendored"
        shutil.copytree(ROOT, tampered, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        metadata = self.write_vendored_identity(tampered)
        (tampered / "README.md").write_text("tampered but rehashed\n", encoding="utf-8")
        metadata["files"]["README.md"] = installer.digest((tampered / "README.md").read_bytes())
        (tampered / "SOURCE.json").write_text(json.dumps(metadata), encoding="utf-8")
        cases.append(("tampered content with rewritten hash", tampered,
                      "source tree does not match"))

        missing = self.base / "missing-vendored"
        shutil.copytree(ROOT, missing, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        metadata = self.write_vendored_identity(missing)
        (missing / "adapters/zcode.md").unlink()
        metadata["files"].pop("adapters/zcode.md")
        (missing / "SOURCE.json").write_text(json.dumps(metadata), encoding="utf-8")
        cases.append(("missing file and identity", missing, "missing package resources"))

        extra = self.base / "extra-vendored"
        shutil.copytree(ROOT, extra, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        metadata = self.write_vendored_identity(extra)
        (extra / "untracked.txt").write_text("not part of the package\n", encoding="utf-8")
        metadata["files"]["untracked.txt"] = installer.digest(
            (extra / "untracked.txt").read_bytes()
        )
        (extra / "SOURCE.json").write_text(json.dumps(metadata), encoding="utf-8")
        cases.append(("extra file and identity", extra, "unexpected resource"))

        linked = self.base / "symlinked-vendored"
        shutil.copytree(ROOT, linked, ignore=shutil.ignore_patterns("__pycache__", ".git"))
        self.write_vendored_identity(linked)
        (linked / "adapters/zcode.md").unlink()
        (linked / "adapters/zcode.md").symlink_to("codex.md")
        cases.append(("symbolic-link resource", linked, "symbolic link"))

        mode_changed = self.base / "mode-vendored"
        shutil.copytree(ROOT, mode_changed,
                        ignore=shutil.ignore_patterns("__pycache__", ".git"))
        self.write_vendored_identity(mode_changed)
        (mode_changed / "README.md").chmod(0o755)
        cases.append(("changed file mode", mode_changed, "source tree does not match"))

        public_missing = self.base / "public-missing-entry"
        shutil.copytree(ROOT, public_missing,
                        ignore=shutil.ignore_patterns("__pycache__", ".git"))
        manifest, _raw = self.write_public_manifest(public_missing)
        manifest["files"].pop()
        (public_missing / installer.PUBLIC_MANIFEST).write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        cases.append(("incomplete public manifest", public_missing,
                      "exact Programming Loop package"))

        public_mode = self.base / "public-mode-mismatch"
        shutil.copytree(ROOT, public_mode,
                        ignore=shutil.ignore_patterns("__pycache__", ".git"))
        manifest, _raw = self.write_public_manifest(public_mode)
        manifest["files"][0]["executable"] = not manifest["files"][0]["executable"]
        (public_mode / installer.PUBLIC_MANIFEST).write_text(
            json.dumps(manifest), encoding="utf-8"
        )
        cases.append(("public manifest mode mismatch", public_mode, "wrong file mode"))

        for label, rejected_source, pattern in cases:
            with self.subTest(case=label):
                assert_rejected(rejected_source, pattern)

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
