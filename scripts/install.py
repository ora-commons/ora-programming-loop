#!/usr/bin/env python3
"""Install only Programming Loop resources; never invoke a coding host or model."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shutil
import sys
import tempfile


HOSTS = {
    "codex": ".codex",
    "claude": ".claude",
    "zcode": ".zcode",
    "hermes": ".hermes",
    "qwen": ".qwen",
    "minimax": ".minimax",
}
PROFILE_HOSTS = {"claude", "zcode", "qwen"}
COMPONENT = "programming-loop"
PROFILE = "programming-loop-reviewer.md"
SOURCE = Path(__file__).resolve().parents[1]


class InstallationError(Exception):
    pass


def digest(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def host_directory(host: str, home: Path | None = None,
                   host_root: Path | None = None) -> Path:
    if host not in HOSTS:
        raise InstallationError(f"Unknown host: {host}")
    root = Path(host_root) if host_root else Path(home or Path.home()) / HOSTS[host]
    root = root.absolute()
    # Do not traverse a user-supplied link and write into another installation.
    for part in (root, *root.parents):
        if part.is_symlink():
            raise InstallationError(f"Installation path contains a symbolic link: {part}")
    return root


def regular_bytes(path: Path) -> bytes:
    if path.is_symlink() or not path.is_file():
        raise InstallationError(f"Missing or non-regular resource: {path}")
    return path.read_bytes()


def payload(source: Path, host: str) -> tuple[dict[str, bytes], bytes | None]:
    version = regular_bytes(source / "VERSION").decode("utf-8").strip()
    if not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?", version):
        raise InstallationError("VERSION must identify a release, such as 1.0.0")
    entry = regular_bytes(source / "skills/programming-loop/SKILL.md")
    framework_link = b"`../../frameworks/programming-loop.md`"
    adapter_link = b"`../../adapters/`"
    if entry.count(framework_link) != 1 or entry.count(adapter_link) != 1:
        raise InstallationError("The Programming Loop entry has unexpected resource links")
    entry = entry.replace(framework_link, b"`./frameworks/programming-loop.md`")
    entry = entry.replace(adapter_link, f"`./adapters/{host}.md`".encode())
    paths = {
        "VERSION": "VERSION",
        "frameworks/programming-loop.md": "frameworks/programming-loop.md",
        f"adapters/{host}.md": f"adapters/{host}.md",
        "README.md": "README.md",
        "LICENSE": "LICENSE",
        "NOTICE.md": "NOTICE.md",
    }
    files = {name: regular_bytes(source / path) for name, path in paths.items()}
    files["SKILL.md"] = entry
    if any(not value.strip() for value in files.values()):
        raise InstallationError("A required component resource is empty")
    profile = None
    if host in PROFILE_HOSTS:
        profile = regular_bytes(source / "profiles" / host / PROFILE)
        if not profile.strip():
            raise InstallationError("The required native reviewer profile is empty")
        files[f"profiles/{host}/{PROFILE}"] = profile
    identity = {
        "component": COMPONENT,
        "version": version,
        "source": COMPONENT,
        "host": host,
        "files": {name: digest(data) for name, data in files.items()},
        "reviewer_sha256": digest(profile) if profile is not None else None,
    }
    files["SOURCE.json"] = (json.dumps(identity, indent=2, sort_keys=True) + "\n").encode()
    return files, profile


def read_identity(skill: Path, host: str) -> dict:
    try:
        identity = json.loads(regular_bytes(skill / "SOURCE.json"))
    except (ValueError, InstallationError) as error:
        raise InstallationError(
            f"Unmanaged or incomplete installation at {skill}; no files changed. "
            "Select another host root or use the original installer to repair it."
        ) from error
    if (not isinstance(identity, dict) or identity.get("component") != COMPONENT
            or identity.get("source") != COMPONENT or identity.get("host") != host
            or not isinstance(identity.get("files"), dict)
            or not isinstance(identity.get("version"), str)
            or not re.fullmatch(r"\d+\.\d+\.\d+(?:[-+][A-Za-z0-9.-]+)?", identity["version"])):
        raise InstallationError(f"Mismatched source identity at {skill}; no files changed")
    required = {"SKILL.md", "VERSION", "frameworks/programming-loop.md",
                f"adapters/{host}.md", "README.md", "LICENSE", "NOTICE.md"}
    if host in PROFILE_HOSTS:
        required.add(f"profiles/{host}/{PROFILE}")
        if not isinstance(identity.get("reviewer_sha256"), str) or not re.fullmatch(
                r"[0-9a-f]{64}", identity["reviewer_sha256"]):
            raise InstallationError(f"Missing reviewer identity at {skill}")
    elif identity.get("reviewer_sha256") is not None:
        raise InstallationError(f"Unexpected reviewer identity at {skill}")
    if not required.issubset(identity["files"]):
        raise InstallationError(f"Incomplete installed resource identity at {skill}")
    for name, expected in identity["files"].items():
        path = PurePosixPath(name)
        if (not isinstance(name, str) or path.is_absolute() or ".." in path.parts
                or "\\" in name or str(path) != name or name == "SOURCE.json"
                or not isinstance(expected, str) or not re.fullmatch(r"[0-9a-f]{64}", expected)):
            raise InstallationError(f"Invalid installed file identity at {skill}")
    return identity


def ensure_plain_tree(path: Path) -> None:
    for item in (path, *path.parents):
        if item.is_symlink():
            raise InstallationError(f"Refusing symbolic-link installation path: {item}")
    if path.exists():
        for item in path.rglob("*"):
            if item.is_symlink():
                raise InstallationError(f"Preserve symbolic link before updating: {item}")


def inspect_installation(root: Path, host: str) -> dict:
    skill = root / "skills" / COMPONENT
    ensure_plain_tree(skill)
    identity = read_identity(skill, host)
    mismatches = []
    for name, expected in identity["files"].items():
        path = skill / name
        if not path.is_file() or digest(regular_bytes(path)) != expected:
            mismatches.append(str(path))
    expected_profile = identity.get("reviewer_sha256")
    if expected_profile is not None:
        profile = root / "agents" / PROFILE
        ensure_plain_tree(profile)
        if not profile.is_file() or digest(regular_bytes(profile)) != expected_profile:
            mismatches.append(str(profile))
    version_path = skill / "VERSION"
    if version_path.is_file() and regular_bytes(version_path).decode("utf-8").strip() != identity["version"]:
        mismatches.append(str(version_path))
    return {"identity": identity, "mismatches": mismatches}


def recover(root: Path) -> bool:
    """Restore the originals retained by an interrupted replacement."""
    backup = root / ".programming-loop-previous"
    if not backup.exists():
        return False
    ensure_plain_tree(backup)
    state = json.loads(regular_bytes(backup / "state.json"))
    if (state.get("component") != COMPONENT
            or set(state.get("originals", {})) != {"skill", "profile"}
            or not all(isinstance(value, bool) for value in state["originals"].values())):
        raise InstallationError(f"Unrecognized recovery directory: {backup}")
    targets = {"skill": root / "skills" / COMPONENT, "profile": root / "agents" / PROFILE}
    for name, target in targets.items():
        original = backup / name
        ensure_plain_tree(target)
        if original.exists():
            if target.exists():
                if name == "skill":
                    replacement = state["replacement"]
                    if json.loads(regular_bytes(target / "SOURCE.json")) != replacement:
                        raise InstallationError(f"Changed replacement retained at {target}")
                    old = read_identity(original, replacement["host"])
                    expected = {key: value for key, value in replacement["files"].items()}
                    expected["SOURCE.json"] = digest(regular_bytes(target / "SOURCE.json"))
                    for item in original.rglob("*"):
                        relative = str(item.relative_to(original))
                        if item.is_file() and relative not in old["files"] and relative != "SOURCE.json":
                            expected[relative] = digest(regular_bytes(item))
                    actual = {str(item.relative_to(target)): digest(regular_bytes(item))
                              for item in target.rglob("*") if item.is_file()}
                    if actual != expected:
                        raise InstallationError(f"User changes retained at {target}; originals remain at {backup}")
                elif digest(regular_bytes(target)) != state["replacement"].get("reviewer_sha256"):
                    raise InstallationError(f"Changed reviewer retained at {target}; original remains at {backup}")
            if target.is_dir():
                shutil.rmtree(target)
            elif target.exists():
                target.unlink()
            target.parent.mkdir(parents=True, exist_ok=True)
            os.replace(original, target)
        elif not state["originals"][name] and target.exists():
            # No previous target existed; remove only bytes this transaction installed.
            if name == "skill":
                current = json.loads(regular_bytes(target / "SOURCE.json"))
                if current != state["replacement"]:
                    raise InstallationError(f"Changed replacement retained at {target}")
                for relative, expected in current["files"].items():
                    if digest(regular_bytes(target / relative)) != expected:
                        raise InstallationError(f"Changed replacement retained at {target}")
                owned = set(current["files"]) | {"SOURCE.json"}
                actual = {str(p.relative_to(target)) for p in target.rglob("*") if p.is_file()}
                if actual != owned:
                    raise InstallationError(f"Additional files retained at {target}")
                shutil.rmtree(target)
            elif digest(regular_bytes(target)) == state["replacement"].get("reviewer_sha256"):
                target.unlink()
            else:
                raise InstallationError(f"Changed replacement retained at {target}")
    shutil.rmtree(backup)
    return True


def preflight_install(source: Path, host: str, home: Path | None = None,
                      host_root: Path | None = None) -> tuple:
    root = host_directory(host, home, host_root)
    skill = root / "skills" / COMPONENT
    reviewer = root / "agents" / PROFILE
    files, profile = payload(source, host)
    ensure_plain_tree(skill)
    ensure_plain_tree(reviewer)
    backup = root / ".programming-loop-previous"
    if backup.exists():
        raise InstallationError(f"Interrupted replacement retained at {backup}; run recover for this host root")
    if skill.exists():
        current = inspect_installation(root, host)
        if current["mismatches"]:
            raise InstallationError(
                "Installed files were changed or are missing; preserve or repair them before updating: "
                + ", ".join(current["mismatches"])
            )
        for name in files:
            if (name != "SOURCE.json" and name not in current["identity"]["files"]
                    and (skill / name).exists()):
                raise InstallationError(f"New package resource would overwrite a user addition: {skill / name}")
    else:
        current = None
        if profile is not None and reviewer.exists():
            raise InstallationError(f"Unowned reviewer profile retained at {reviewer}")
    return root, skill, reviewer, files, profile, current


def install(source: Path, host: str, home: Path | None = None,
            host_root: Path | None = None) -> Path:
    root, skill, reviewer, files, profile, current = preflight_install(
        source, host, home, host_root
    )
    backup = root / ".programming-loop-previous"
    root.mkdir(parents=True, exist_ok=True)
    staging = Path(tempfile.mkdtemp(prefix=".programming-loop-stage-", dir=root))
    try:
        staged_skill = staging / "skill"
        if skill.exists():
            shutil.copytree(skill, staged_skill)
            # Retire prior owned resources; unknown files remain in the staged copy.
            for name in current["identity"]["files"]:
                (staged_skill / name).unlink(missing_ok=True)
        else:
            staged_skill.mkdir()
        for name, data in files.items():
            target = staged_skill / name
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(data)
        if profile is not None:
            (staging / "profile").write_bytes(profile)
        # Validate the complete staged bytes before moving a working installation.
        for name, data in files.items():
            if regular_bytes(staged_skill / name) != data:
                raise InstallationError(f"Staged resource differs: {name}")
        state = {"component": COMPONENT,
                 "originals": {"skill": skill.exists(), "profile": reviewer.exists()},
                 "replacement": json.loads(files["SOURCE.json"])}
        staged_backup = staging / "previous"
        staged_backup.mkdir()
        (staged_backup / "state.json").write_text(json.dumps(state), encoding="utf-8")
        # Publish complete recovery metadata in one rename before moving a
        # working installation. An interruption cannot leave an empty backup
        # directory that blocks both retry and documented recovery.
        os.replace(staged_backup, backup)
        try:
            skill.parent.mkdir(parents=True, exist_ok=True)
            if skill.exists():
                os.replace(skill, backup / "skill")
            os.replace(staged_skill, skill)
            if profile is not None:
                reviewer.parent.mkdir(parents=True, exist_ok=True)
                if reviewer.exists():
                    os.replace(reviewer, backup / "profile")
                os.replace(staging / "profile", reviewer)
            if inspect_installation(root, host)["mismatches"]:
                raise InstallationError("Installed resources failed readback")
        except BaseException:
            try:
                recover(root)
            except Exception as error:
                raise InstallationError(f"Replacement stopped; originals retained at {backup}: {error}") from error
            raise
        shutil.rmtree(backup)
        return skill
    finally:
        shutil.rmtree(staging)


def preflight_remove(host: str, home: Path | None = None,
                     host_root: Path | None = None) -> tuple:
    root = host_directory(host, home, host_root)
    skill = root / "skills" / COMPONENT
    if (root / ".programming-loop-previous").exists():
        raise InstallationError("Recover the interrupted replacement before removal")
    ensure_plain_tree(skill)
    identity = read_identity(skill, host)
    mismatches = inspect_installation(root, host)["mismatches"]
    if mismatches:
        raise InstallationError(
            "Installed Programming Loop files were changed or are missing; "
            "preserve or repair them before removal: " + ", ".join(mismatches)
        )
    targets = [(skill / name, expected) for name, expected in identity["files"].items()]
    if identity.get("reviewer_sha256"):
        targets.append((root / "agents" / PROFILE, identity["reviewer_sha256"]))
    for target, expected in targets:
        ensure_plain_tree(target)
        if not target.is_file() or digest(regular_bytes(target)) != expected:
            raise InstallationError(f"Installed Programming Loop file changed before removal: {target}")
    return root, skill, root / "agents" / PROFILE, identity


def remove(host: str, home: Path | None = None,
           host_root: Path | None = None) -> list[str]:
    root, skill, reviewer, identity = preflight_remove(host, home, host_root)
    staging = Path(tempfile.mkdtemp(prefix=".programming-loop-remove-", dir=root))
    preserve_staging = False
    try:
        remaining = staging / "remaining-skill"
        shutil.copytree(skill, remaining)
        for name in identity["files"]:
            (remaining / name).unlink()
        (remaining / "SOURCE.json").unlink()
        for directory in sorted(
                (p for p in remaining.rglob("*") if p.is_dir()),
                key=lambda p: len(p.parts), reverse=True):
            if not any(directory.iterdir()):
                directory.rmdir()
        retained = [str(skill / p.relative_to(remaining))
                    for p in remaining.rglob("*") if p.is_file()]
        original_skill = staging / "original-skill"
        original_profile = staging / "original-profile"
        try:
            os.replace(skill, original_skill)
            if retained:
                os.replace(remaining, skill)
            if identity.get("reviewer_sha256"):
                os.replace(reviewer, original_profile)
        except BaseException:
            try:
                if skill.exists():
                    shutil.rmtree(skill)
                if original_skill.exists():
                    skill.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(original_skill, skill)
                if original_profile.exists():
                    if reviewer.exists():
                        reviewer.unlink()
                    reviewer.parent.mkdir(parents=True, exist_ok=True)
                    os.replace(original_profile, reviewer)
            except BaseException as error:
                preserve_staging = True
                raise InstallationError(
                    f"Removal stopped; originals retained at {staging}: {error}"
                ) from error
            raise
        return retained
    finally:
        if staging.exists() and not preserve_staging:
            shutil.rmtree(staging)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("operation", choices=("install", "remove", "status", "recover", "install-check", "remove-check"))
    parser.add_argument("--host", choices=HOSTS, required=True)
    parser.add_argument("--home", type=Path, help="User root (defaults to the current user's home)")
    parser.add_argument("--host-root", type=Path, help="Explicit selected host/profile root; overrides --home")
    parser.add_argument("--source", type=Path, default=SOURCE, help="Authoritative Programming Loop release root")
    args = parser.parse_args(argv)
    try:
        root = host_directory(args.host, args.home, args.host_root)
        if args.operation == "install-check":
            preflight_install(args.source, args.host, args.home, args.host_root)
            print("Programming Loop installation targets are ready.")
        elif args.operation == "remove-check":
            preflight_remove(args.host, args.home, args.host_root)
            print("Programming Loop removal targets are ready.")
        elif args.operation == "install":
            path = install(args.source, args.host, args.home, args.host_root)
            print(f"Installed Programming Loop at {path}. Restart the selected host to refresh skills.")
        elif args.operation == "remove":
            retained = remove(args.host, args.home, args.host_root)
            print("Removed Programming Loop files; projects, unrelated settings, and unowned additions are preserved.")
            if retained:
                print("Retained unowned additions:\n" + "\n".join(retained))
        elif args.operation == "recover":
            print("Restored the previous installation." if recover(root) else "No interrupted replacement to recover.")
        else:
            result = inspect_installation(root, args.host)
            print(json.dumps(result, indent=2, sort_keys=True))
            return 1 if result["mismatches"] else 0
    except (InstallationError, OSError, ValueError) as error:
        print(f"Programming Loop: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
