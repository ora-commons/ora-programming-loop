# ZCode adapter

Use this adapter only when ZCode is the initiating and coordinating host. The
universal framework supplies every workflow rule.

## Fresh workers

Start each executor and reviewer with a new native Agent call using the general
purpose worker type. A fresh Agent has no coordinator conversation, so include
the whole task-local packet. Use the installed `programming-loop-reviewer`
profile for review when profile selection is available.

Set tool access explicitly for the assignment. Reviewer profiles omit ordinary
write/edit tools, but the coordinator still verifies the actual host tool list
and states the read-only boundary. Run the executor and the acceptance reviewer
serially; the framework's supervision runs while the executor is busy.

## Completion and waiting

Collect the worker's complete returned content. An `async_launched` or similar
launch acknowledgement is not an implementation or review result. Use native
completion and messaging operations to retrieve the result, then inspect the
working tree before continuing.

Use the host's actual concurrent supervision and stop/report operations under
the framework; a check queued until a busy executor returns is insufficient.
Report unavailable operations rather than inventing them. End task-owned
supervision with the Loop; never select another provider as a hidden fallback.
