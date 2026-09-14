# Claude Code adapter

Use this adapter only when Claude Code coordinates Programming Loop. Apply the
universal framework without copying it into the adapter.

## Fresh workers

In Claude Code 2.1.251, create each executor and reviewer with a fresh non-fork
native `Agent` invocation, not by resuming a prior agent. Include the complete
assignment because a fresh subagent does not inherit the coordinator
conversation. For review, select the installed `programming-loop-reviewer`
profile when the current Claude Code version exposes custom agents.

The profile limits ordinary authoring tools, but a profile or plugin permission
is not a security boundary. The coordinator must still state allowed checks,
prohibited effects, and repository scope in the prompt and inspect the result.

## Completion and waiting

Read the agent's full returned response. A task identifier or completion
notification is only a signal to collect the result. Schedule waits at natural
slice boundaries; do not run executor and reviewer concurrently or detach an
unbounded poller.

Use only the configured authorized Claude route. Never switch silently to an
API key, paid fallback, or different provider.
