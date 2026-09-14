# Programming Loop

Programming Loop is a portable method for completing bounded repository work
with separate implementation and review contexts. It turns an approved outcome
into a protected change, exact checks, independent review, correction, and the
agreed delivery endpoint without introducing a workflow service or run ledger.

The component is host-neutral. One framework defines the method; a small
adapter explains how to perform fresh dispatch and handback in each supported
AI coding host. The installer copies the framework, exactly one matching
adapter, and the host entry files into the user's normal configuration.

## What it guarantees

When its prerequisites are met, the Loop requires the coordinator to:

- inspect the real repository and agree on a bounded plan before editing;
- preserve unrelated and explicitly protected work;
- give each executor and reviewer a complete, self-contained assignment;
- keep implementation and review in separate fresh contexts;
- run only the checks approved for the change;
- correct every material in-scope defect and review the cumulative result;
- use Git as the rollback record when the project uses Git; and
- stop with an honest status when authority, access, or a user decision is
  missing.

It does not guarantee that a host, model, credential, repository, or remote is
available. It never grants authority to publish, deploy, purchase, message,
delete data, use credentials, or change a repository merely because the
component is installed.

## Package map

| Path | Purpose |
|---|---|
| `frameworks/programming-loop.md` | The complete host-neutral workflow. |
| `adapters/` | One short mapping for each supported host. |
| `skills/programming-loop/SKILL.md` | The native skill entry that loads the framework and adapter. |
| `profiles/` | Read-only-oriented reviewer profiles for hosts that use profile files. |
| `scripts/install.py` | Transactional install, update, and removal command. |
| `VERSION` | Component release identity. |

The private `Golfplan18/ora-programming-loop` repository is the sole authoritative
Programming Loop source. The
[ora-commons/ora-programming-loop](https://github.com/ora-commons/ora-programming-loop)
repository is its public source and update route. Public releases, product-embedded
snapshots, and installed copies retain available provenance, but are not canonical
authorities and should not be hand-edited as mirrors.

## Supported hosts

The distribution installer recognizes six hosts:

| Host | Adapter | Reviewer profile |
|---|---|---|
| Codex | `adapters/codex.md` | Uses a fresh native subagent assignment. |
| Claude Code | `adapters/claude.md` | `profiles/claude/programming-loop-reviewer.md` |
| ZCode | `adapters/zcode.md` | `profiles/zcode/programming-loop-reviewer.md` |
| Hermes | `adapters/hermes.md` | Uses a fresh delegated task. |
| Qwen Code | `adapters/qwen.md` | `profiles/qwen/programming-loop-reviewer.md` |
| MiniMax Code | `adapters/minimax.md` | Uses a stateless one-shot task. |

Support means the package has an installation target and an explicit native
mechanism. It is not a claim that every host version, model, provider, or
permission mode has passed live end-to-end qualification. Always inspect the
installed host's current tool descriptions before dispatch.

## Install

Run the installer from this component directory:

```sh
python3 scripts/install.py install --host codex
```

Replace `codex` with `claude`, `zcode`, `hermes`, `qwen`, or `minimax`. The
default destination is the selected host's normal user configuration. Use
`--host-root PATH` to install into another host configuration root, such as an
isolated test or managed environment.

The installer validates every source file, writes an atomic release directory,
then switches the host entry points. If replacement fails, the previous
installation remains recoverable. It does not contact a provider or start a
model session.

To update an existing installation from this component:

```sh
python3 scripts/install.py install --host codex
```

The `install` operation recognizes an existing owned installation and replaces
it transactionally; there is no separate update operation.

To remove only files owned by the installed release:

```sh
python3 scripts/install.py remove --host codex
```

Removal preserves a host entry when the user changed it after installation.
Read the command's result before deleting any remaining user-owned file.

## Use

Ask the host to use **Programming Loop** for a repository task. The coordinator
loads the universal framework and its installed adapter, inspects the project,
and proposes the small scope lock described by the framework. Editing begins
only after the user approves that plan.

If native skill discovery is unavailable, open and provide these two files to
the coordinating session:

1. `frameworks/programming-loop.md`
2. the one adapter matching the initiating host

Do not provide all adapters to a worker. The initiating host controls dispatch;
a model used for an optional external review is a review target, not a reason
to substitute that target's host adapter.

## Portability and extension

To add a host, first determine whether it can create a genuinely fresh worker,
return the complete worker result, and keep coordinator authority separate. A
new adapter should name only the exact native operations, isolation limits,
completion signal, and safe wait behavior. It must not restate or alter the
universal method. Add installer wiring and a focused distribution check only
when that new host is an actual supported product outcome.

A host without a safe fresh-worker mechanism can still use the framework by
manual copy-and-paste, but it must disclose that implementation or review
isolation is unestablished. Never route silently through another provider.

## Operational truth

The installer and automated distribution checks establish file integrity,
transactional replacement, supported destinations, and generated-resource
parity. They do not open a host, exercise a subscription, or certify live model
behavior. A maintainer should describe those layers separately: “packaged and
mechanically checked” is not “live-qualified.”

The Loop stores no run history of its own. Current conversation, repository
state, Git commits, and check output are the working evidence. If the host ends
mid-run, resume from those sources and the approved plan. Do not infer success
from an installed profile, a task identifier, or a stale status field.

The selected adapter always follows the initiating host. For example, a Codex
coordinator asking an authorized Claude model for an optional second opinion
still uses the Codex adapter; Claude is the review target, not the dispatcher.
This distinction prevents incorrect tool instructions and hidden provider
switches.

## License

The component is dedicated to the public domain under CC0 1.0 Universal. See
`LICENSE` and `NOTICE.md`.
