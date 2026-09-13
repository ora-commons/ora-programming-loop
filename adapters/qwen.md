# Qwen Code adapter

Use this adapter only when Qwen Code coordinates Programming Loop. Do not
replace the universal framework with host defaults.

## Fresh workers

Create each executor and reviewer with a new native Agent invocation and a
complete self-contained assignment. Request explicit return mode so the full
worker response comes back to the coordinator. Do not fork or resume the
executor as the reviewer.

Select the installed `programming-loop-reviewer` profile for review when custom
agents are available. Set the native tool allowlist explicitly. Parent automatic
or approval modes may override a child profile's apparent permissions, so the
coordinator must inspect the effective mode and the resulting repository state.

## Completion and waiting

Read the full returned result and inspect the real diff. A launch or success
status without content is not the handback. Use bounded native waiting and do
not detach a poller.

Use only the provider and model authorized in the current session. Do not route
through another provider or a paid fallback without the user's prior approval.
