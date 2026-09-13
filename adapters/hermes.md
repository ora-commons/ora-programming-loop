# Hermes adapter

Use this adapter only when Hermes coordinates Programming Loop. The universal
framework defines the method and outcomes.

## Fresh workers

Create each executor and reviewer with a separate `delegate_task` call and a
complete self-contained prompt. Do not reuse the executor task for review. Set
the narrowest available tool and repository permissions consistent with the
assigned slice.

Retrieve the delegated task's full saved result before deciding what happened.
A delegation acknowledgement, task name, or status transition is not evidence
that the assignment succeeded.

## Provider and waiting limits

Hermes children may inherit provider and fallback configuration from the
coordinator. Inspect that configuration before dispatch. If it could use an
unauthorized or paid fallback, change the authorized local configuration or
use a disclosed manual handoff; never allow a silent provider switch.

Use bounded native result collection. Do not detach shell pollers. If the host
cannot establish a fresh isolated worker or return its result, report that limit
and keep review or execution unverified.
