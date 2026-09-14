# Codex adapter

Use this adapter only when Codex is the session coordinating Programming Loop.
The universal framework remains authoritative.

## Fresh workers

Create executors and reviewers with the native collaboration subagent tool and
`fork_turns: "none"`. Put the complete self-contained assignment in the initial
message. A full-history fork is not an independent context.

Use a distinct subagent for every review. Use direct messages for updates and
handback, and a follow-up task only to resume an already identified worker with
current instructions. Read the returned final result; a spawn response proves
only that dispatch began.

## Waiting and limits

Use the host's bounded wait operation rather than shell sleep loops or detached
pollers. Desktop child agents may have narrower sandbox or UI access than the
coordinator, so state access limits in the assignment and keep unavailable
evidence unverified.

Do not select another provider or paid route as a fallback. A model choice is
separate from the executor/reviewer role and follows current user authority and
the host's available subscription.
