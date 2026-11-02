# Ora Programming Loop framework

## Purpose and authority

Ora Programming Loop completes bounded repository work through one approved plan, fresh implementation, independent review, correction, and the agreed delivery endpoint. The session running this framework is the **coordinator**.

- The coordinator owns the plan, dispatch sequence, evidence, and final handback; it does not pretend that preparing a prompt or opening a worker proves that work happened.
- Use the adapter for the initiating host together with this framework; the adapter supplies native tool names and isolation facts only.
- If adapter text conflicts with this method, this framework controls unless a higher-priority user, repository, or host instruction says otherwise.
- An approved plan authorizes only the outcome, scope, checks, and effects it actually names.
- Installation or invocation of the Loop grants no permission to edit, spend money, use a credential, contact a provider, publish, deploy, message another person, delete data, or perform an irreversible action.

## Roles

The Loop uses three responsibilities:

- **Coordinator:** inspects, proposes the plan, obtains approval, protects the repository, dispatches work, interprets reviewer outcomes, and performs only the approved finish line.
- **Executor:** works in a fresh context on one coherent implementation or correction slice. It may inspect the whole repository but changes only the approved component and runs only the assigned checks.
- **Reviewer:** works in a different fresh context. It independently inspects the plan, cumulative candidate, repository, and current evidence, and returns one of the four defined outcomes.

Separation:

- One person or session may coordinate small work, but executor and reviewer contexts remain separate.
- Do not let a reviewer validate its own implementation and do not reuse an executor conversation as a review context.

## 1. Establish the task

### Read before asking

Read the user's current request, every named source of truth, and applicable repository instructions. Inspect enough of the actual project to understand:

- the current user-visible behavior and desired result;
- relevant architecture, entry points, call sites, data, and dependencies;
- existing focused checks and delivery behavior;
- Git branch, commit, worktrees, staged, unstaged, untracked, and symlink state;
- unrelated or explicitly protected work; and
- live automation or external effects that constrain safe execution.

Discovery rules:

- Stop discovery once the evidence supports a safe plan.
- Ask only for a fact or decision that could materially change the result, scope, risk, authority, cost, external effect, or finish line.
- Resolve ordinary reversible technical choices by inspection and professional judgment.
- When a simpler approach produces the same outcome, show it and recommend it.
- If sources contradict one another and the current user has not resolved the conflict: show the concrete alternatives and wait. Do not combine them or pick the newest-looking document.
- A current direct user correction overrides older material and should be acknowledged plainly.

### Agree on one plan

Before non-trivial editing, present a compact scope lock containing:

1. the user-visible outcome;
2. the component or content in scope;
3. explicit non-goals and protected work;
4. the expected change shape and meaningful milestones;
5. the exact authorized checks—the complete testing ceiling;
6. authorized external, destructive, or irreversible effects; and
7. the observable completion and Git finish line, if any.

- Obtain one explicit approval.
- That approval covers: normal repository-local, reversible implementation; the named checks; independent review; in-scope correction; and the named delivery steps.
- Do not return for per-file choices or routine implementation decisions.
- Ask again only when evidence requires a materially different outcome, non-goal, architecture, dependency, authority, external effect, migration, data loss, or inseparable interaction with user work.

Reader-facing artifacts:

- For a reader-facing artifact whose content shape is material, include: current and projected line and character counts; replacement versus append behavior; material exclusions; and the rollback point.
- Preserve the bytes and ask again before writing if a major new section or artifact type, or material expansion beyond that approved shape, becomes necessary.

## 2. Protect the working state

- Immediately before editing: reread the governing sources and repository rules; record the baseline commit and branch; reinspect staged, unstaged, untracked, ignored when relevant, and symlink work — repository state can change after the plan was approved.
- For automated Git editing, use a task branch in a task-owned worktree unless the user or repository explicitly approves another safe arrangement.
- Never stash, reset, overwrite, stage, commit, or absorb unrelated work.
- A protected path overrides a broad component description.
- Edit a dirty in-scope file only when its existing changes can be preserved and separated; if safe separation is impossible, stop and ask the user.
- Use Git commits as rollback points when the project uses Git.
- Do not add a second state database, checkpoint format, receipt store, ledger, manager process, or workflow service; temporary files must have a deletion point.

Adapter and dispatch:

- Before dispatch, choose the adapter matching the host that will create and coordinate workers; confirm the actual native capability exists.
- An adapter is not permission to install a tool, authenticate, choose a paid provider, or use a fallback provider.
- If native dispatch is unavailable, a disclosed manual handoff is acceptable, but isolation and execution remain unestablished until the receiving context returns evidence.

Vibe assignments:

- For a Vibe assignment, honor the supplied Ora Programming ownership-transfer rule instead of asking the user to manage worker conversations.
- Carry the exact supplied governing instructions, Specification, references, retained decisions, and acceptance criteria into every executor, reviewer, and supervisor packet.
- Require each recipient to open required materials before dependent work; report missing access.

## 3. Dispatch a clean executor

### Assignment integrity

- The executor packet is a boundary, not a summary of the coordinator's memory.
- Include governing text verbatim when exact wording controls the outcome; identify quoted repository data separately from instructions.
- A path is useful only when the worker can access it; for remote or isolated workers, provide the permitted content or disclose the access limit.
- Never silently truncate an input or imply that an unavailable artifact was inspected.
- Name the owner and return destination so the worker can report directly.
- Identify the document custodian when the task changes requirements or maintained documentation.
- State whether the worker may make ordinary reversible choices and which decisions remain with the user.
- A worker should not pause for routine file choices already inside approved scope, and should not guess about a reserved product choice.

Shared mechanisms and mirrors:

- When a shared mechanism changes, the executor enumerates its real call sites before wiring and either updates them consistently or gives a principled reason each excluded call site is unaffected. This is part of implementing the approved behavior, not permission for opportunistic cleanup.
- Unrelated defects remain untouched unless they prevent the approved result and cannot be separated safely.
- For generated or mirrored artifacts: identify the canonical source and existing generator before editing; change the canonical source; run only the approved generation route; verify source-to-output parity. Never hand-maintain both copies or introduce a second synchronization system merely to make the current patch pass.

### The fresh worker

Create a fresh worker using the initiating host's adapter. Do not fork the coordinator's full conversation or pass hidden reasoning. Supply a complete, self-contained executor packet containing only what the worker needs:

- repository path, task branch, and applicable repository instructions;
- the approved plan and current milestone verbatim;
- baseline or latest accepted commit;
- factual protected work and current relevant state;
- exact authority limits and prohibited effects;
- reviewer defects when this is a correction slice;
- checks assigned to this slice; and
- required handback: changed paths, result, exact checks and output, remaining work, cleanup state, and any genuine blocker.

Executor limits:

- Permit whole-repository reading because the worker may need to trace call sites, but authorize edits only inside the approved component and its necessary direct consequences.
- Require real repository edits, not a proposed patch in chat.
- Do not let the worker stage, commit, change branches, push, deploy, publish, use credentials, or message externally unless the approved plan explicitly assigns that action to it.
- The executor completes one coherent, reviewable slice. It stops when the slice is implemented and its assigned checks are complete, or when the approved outcome cannot be reached without changed authority.
- A worker reaching a token or time boundary returns exact state to the coordinator; it does not call a partial draft complete.

### Failure behavior

- Optional enrichment, decoration, or supplementary lookup should normally fail open with a visible warning when its loss does not endanger the accepted result.
- Publication, release, permissions, security, authentication, and data-integrity gates retain their explicit failure behavior.
- The executor may not weaken a safety gate or convert it to a warning to obtain a passing check.
- If an edit or generator fails: preserve the previous recoverable artifact and remove only task-owned staging.
- If a command starts a background process: record it and end it as soon as its output is no longer needed; never create an unbounded detached wait loop.
- A process belonging to another task is reported, not killed.
- Use one writer for a coupled foundation until independent acceptance; thereafter use only path-exclusive parallel lanes and one writer per shared integration surface. Freeze all edit lanes before cumulative review.

## 4. Collect evidence

- Read the worker's actual returned result through the host mechanism.
- Not the result: a launch acknowledgement, task identifier, process exit, notification, or absence of an error.
- Inspect the real working tree. Capture:
  - raw cumulative diff from the baseline, including uncommitted task work;
  - concise diff statistics and exact changed paths;
  - staged, unstaged, untracked, and symlink state;
  - output from only the authorized checks; and
  - any direct artifact inspection the plan requires.
- Do not accept a worker's summary in place of the candidate.
- Do not run a full suite, build, lint, audit, benchmark, or extra reassurance check unless it is named in the approved testing ceiling.
- An additional or repeated check must satisfy the supplied task's necessity rule; a material-risk label alone is not proof. Obtain any necessary authority change before running it.
- Tests: simple checks that something happened or didn't are fine. Do not add elaborate tests for rare, unimportant outcomes. A finding alone does not justify a test. Judge a test's whole addition, setup included.

## 5. Dispatch an independent reviewer

### Review packet integrity

- The cumulative diff must cover every task change from the recorded baseline, including accepted earlier slices and current uncommitted correction.
- If multiple repositories participate in one atomic outcome, provide each repository, baseline, raw diff, and relevant check evidence.
- Do not reduce review to the latest hunk when earlier accepted work affects the current behavior.
- Give the reviewer source material needed to decide each criterion, but exclude implementation discussion, executor transcripts, intended fixes, and coordinator conclusions. This prevents anchoring and keeps the review reproducible from the actual candidate.
- A reviewer may use read-only repository inspection to follow code paths outside the diff; whole-repository access does not enlarge the approved product scope.
- The reviewer checks truth as well as mechanics: documentation must match the active behavior; generated records must describe the real source; model or provider attribution must reflect what actually ran; a status must not claim a later endpoint than the evidence establishes.
- Bookkeeping cannot overrule functioning code or real output; repair bookkeeping when it cannot represent reality.

### The fresh reviewer

Create a different fresh worker through the same initiating-host adapter. Never resume the executor or seed the reviewer with the executor conversation, intended fix, suspected defect, or coordinator verdict. Give the reviewer:

- the exact approved plan;
- the milestone identifier, or `FINAL`;
- repository path, branch, and baseline commit;
- protected pre-existing work;
- raw cumulative diff and current working state;
- current authorized check output;
- whole-repository read access; and
- authority to run only review checks already in the approved ceiling.

Reviewer conduct:

- The reviewer directly inspects the repository and candidate.
- When acceptance depends on an image, interface, audio, video, PDF, remote source, or live state, it inspects that evidence with an appropriate available tool; a description or executor claim is not a substitute.
- If required evidence is inaccessible, the criterion remains unverified.

### Reviewer rule

The reviewer examines widely. It records potential issues and why they do or do not warrant a change, including close calls. Good review work means finding real errors and explaining why other issues don't justify code or a test. "No findings" is full success.

Every finding states: input or situation; actual result; expected result; evidence (command output or a traced code path); who is harmed and how; size of the smallest fix.

- Actionable only with evidence of a result contrary to the approved plan in a way that changes the result the user asked for, or a real error with identified harm.
- Severe failures are unrecoverable data loss, security exposure, and unauthorized or erroneous spending, sending or publishing. For these, a traced path from an actual permitted input to the harm is sufficient; do not cause the harm to prove it.
- Not actionable, so record it and move on: "could", "might" or "in theory" with no demonstrated case; rare conditions with unimportant results; errors nobody would notice and nothing depends on; fixes bigger than the harm, except on severe failures; hardening or style with no proven harm.

A finding against the plan itself must show a user harm or a contradiction with the owner's decision. Do not invent requirements; recommend removing unnecessary ones or correcting contradictions with the owner's decisions.

### Builder disposition

When a reviewer disagrees with a decision, it gives its reasoning and, if one is available, a reasonable alternative. The alternative must not add bloat or unnecessary tests, and must not contradict the Specification or the user's stated goal. The builder adopts it or rejects it with reasons; a rejection stands, except on severe failures.

- The builder fixes actionable findings the smallest way.
- The builder may reject a finding as unnecessary, recording its reasons. A rejection stands, except on severe failures.
- A finding does not expand authority or require a test.

### Outcomes

Require exactly one leading outcome and concise evidence:

- `CONTINUE` — this slice is sound and approved work remains.
- `FIX` — correctable actionable findings remain within approved scope.
- `DONE` — the complete approved outcome is independently established.
- `ASK USER` — responsible continuation needs changed authority, inaccessible human-only input, resolution of conflicting instructions, or another user-reserved decision.

Every completed review report and correction result also carries exactly one current line:

```text
Review disposition: SETTLED
```

- `SETTLED` — review finished; every finding was fixed or rejected with reasons; no unresolved severe finding remains. Continue toward delivery.
- `CORRECTION` — review finished and findings require builder decisions. Run correction.
- `SEVERE` — a demonstrated severe finding remains unresolved. Preserve the candidate and return the necessary decision to the owner.
- `INCOMPLETE` — review or correction did not finish. Preserve its work; use the existing operational recovery route. Never complete.
- `ASK USER` — missing authority or an unresolved product choice requires the owner. Preserve this route.

Read exactly one disposition line from the **current completed report**, outside quotations and examples. Missing, duplicate, unknown or contradictory declarations mean `INCOMPLETE`. "No severe finding stated" means an affirmative, completed `SETTLED` or `CORRECTION` declaration, whose instructions expressly require identifying every severe finding; it never means an absent severity declaration. A previously recorded severe finding cannot disappear through rejection: settlement requires a recorded fix and evidence that its harmful path was removed.

Outcome rules:

- A final `CONTINUE` is not completion; treat it as `FIX` because final review must establish the whole outcome.
- A missing check or inaccessible required artifact cannot become `DONE` or `SETTLED` through confident prose; its disposition is `INCOMPLETE`.

## 6. Continue by evidence

### Changes to governing inputs

- If the user changes a material goal, constraint, fact, authority, or approval while work is active: stop affected work, update the one governing plan or requirement source, and send the accepted meaning to every affected fresh worker.
- Do not append an amendment history; do not let a consultant's answer silently replace the plan.
- Unaffected authorized work may continue when it is safely independent.
- A newly discovered missing product decision returns to the user or the workflow that owns product definition.
- A missing implementation direction may be resolved through the approved planning authority.
- Neither becomes an ordinary code choice just because implementation has begun.
- A reviewer preference about style or architecture cannot reopen a settled product decision without a concrete material defect.

### Staging and accepted slices

- Before any authorized commit: inspect the complete staged diff and confirm only task-owned changes are staged.
- Compare actual artifact size and scope with any approved projection.
- Generated outputs, manifests, and legal notices are part of this inspection when they are in scope.
- A materially expanded reader artifact is preserved but not committed until the user accepts the new shape.
- An accepted slice commit is a recovery point, not proof that the project is complete; later cumulative review may find a defect spanning slices.
- Correct spanning defects against the same baseline and review the whole current result.
- Never reset away accepted or user-owned work to simplify correction.

### Outcome handling

- On `FIX`: consolidate the complete current defect list and dispatch a new clean executor with the same plan and authority; never resume the rejected executor for correction. Rejected implementation is evidence, not a code donor, except for items identified in independent acceptance evidence. The builder then fixes or rejects each finding with reasons. A settled correction — every finding fixed or reasonably rejected with recorded reasons, and no unresolved severe finding — permits milestone progress without another approval review. An unresolved severe finding preserves the candidate and returns the necessary decision to the owner.
- On `CONTINUE`: commit the accepted coherent slice when the approved Git path allows it, then dispatch the next milestone from that rollback point. Never commit a rejected slice merely to make the working tree tidy.
- On `DONE`: confirm the candidate, checks, preservation, and cleanup, then perform only the plan's remaining finish line. A review pass is a checkpoint, not permission to invent a push, merge, deployment, publication, or release.
- On `ASK USER`: return the exact unresolved decision or missing authority with the candidate preserved. Show the real alternatives, their cost and risk, whether they are reversible, and a recommendation.
- On `INCOMPLETE` or a missing, duplicate, unknown or contradictory disposition: preserve the review's work and use the existing operational recovery route. Never complete from an unfinished review; a transport failure must never erase a recorded severe finding.

### Convergence

- Continue while evidence improves: checks pass, failures narrow, causes become known, defects decrease, a milestone completes, or material uncertainty is removed.
- Rejected non-severe findings do not force another review or prevent completion. There is no compulsory correction round and no reviewer-agreement gate.
- Before declaring a blocker, exhaust safe alternatives inside the approved plan. Unresolved severe findings go to the owner.

## 7. Supervise long-running work

- Assign one independent supervisor using the reviewer responsibility (Vibe’s verifier role), outside the executing task. Use existing host operations so it can inspect and request a stop while the executor is busy; do not substitute a queued check inside that busy session. Confirm the actual stop/report route before dispatch; report a concrete host limitation if it is unavailable.
- At each named milestone, require a safe stopping point before inspection; use the confirmed host stop route if that point is missed or active work stalls without progress. Preserve recoverable work and confirm task-owned writers and mutating commands have stopped before inspection; interrupting an agent alone is not proof.
- Inspect the cumulative diff and candidate against governing materials: drift, production/test growth, repeated check invocations, reference fidelity, rejected executor reuse, and attempted gate bypass. Every added component and test must serve an approved behavior; remove or consolidate unnecessary duplicate paths, replacement architecture, speculative helpers, compatibility layers, scaffolding, and private-detail tests through the executor.
- Use existing check output to count invocations. A named test file is not unlimited authority. Additional or repeated checks must meet the governing task's proof and authority rules; stop when authorized checks and material review are satisfied.
- Resume healthy work automatically after inspection. Route findings that warrant change through the existing correction procedure; involve the user only for an unresolved retained decision, necessary material deviation, or retained final inspection.
- Keep the supervisor read-only: no product edits, tests, or commits. Use bounded host operations, no permanent service or detached poller, and end task-owned supervision when execution ends.

## 8. Finish, deliver, and recover

### Final verification and correction

- Before finishing, run one cumulative independent verification of the whole candidate. It receives the review record — findings, rejections, pushback and reversals — as material to examine, while independently inspecting the candidate.
- Verification checks the record as a third reader and may recommend reversing any decision, with reasons.
- Final correction fixes or rejects each recommendation with reasons, and its result carries the disposition line. Rejected non-severe findings do not force another review or prevent completion. Unresolved severe findings go to the owner.
- The coordinator accepts a settled (`SETTLED`) final correction without another correctness review. Completion after final correction says **completed after correction**, without inventing a subsequent verification pass.

### Removal-only pass

- Before landing, dispatch one fresh reviewer whose only job is to recommend what can be removed while still meeting the stated user function.
- The builder applies each recommendation or rejects it with reasons.

### Record

- Findings, rejections, pushback and reversals are retained as ordinary project files committed to Git, with the supplied instructions and conversations. Add no separate persistence system — no runtime, database, or installer mechanism; the Loop is an instructed method. Include no credentials or secrets. They are not sent to the owner.

Completion requires all of the following:

- the requested behavior works end to end;
- unrelated behavior and important content remain intact;
- the exact checks pass and required direct inspection is complete;
- cumulative final verification is complete and final correction settled every recommendation with reasons, with no unresolved severe finding;
- the approved delivery endpoint is actually reached;
- temporary scaffolding and task-owned background processes are removed; and
- no accepted output is parked unused.

Git path:

- For Git work, follow the exact approved repository path.
- A common path is: commit, push, pull-request review, merge to the default branch, deployment verification when merging deploys, and deletion of only the merged task branch and task-owned worktree.
- Do not assume that path where the user or repository selected a shorter endpoint.
- Never force-push, rewrite history, delete an unmerged branch, or bypass unrelated protections without explicit authority.

Recovery:

- Recovery uses the approved branch, commits, current diff, and check output.
- Revert delivered commits in reverse order when that is the project's safe rollback.
- Do not delete user work or create a custom recovery system.
- If work stops unfinished: report the exact retained state and next action without calling the project complete.

Final handback:

- The final handback states: the outcome in plain language; exact changed paths; accepted commits and delivery state; checks with results; preservation and cleanup facts; credible rollback route; remaining work; and whether user input is genuinely required.
- Contact the coordinating task directly; do not depend on the user to relay a worker's result.

## Optional external review targets

- A coordinator may use an approved external model or review service only when: the plan authorizes that call; the route is available; and its cost and data exposure are acceptable.
- The external target is a reviewer capability, not the initiating host.
- Continue to use the initiating host's adapter for dispatch, waiting, and result collection; do not swap adapters because the selected reviewer model is associated with another vendor.
- Supply the external reviewer the same bounded review packet; require its actual result and truthful model attribution when the route provides attribution.
- A transport success, selected alias, or provider acknowledgement does not prove which model answered.
- When attribution is missing, ambiguous, or mismatched: disclose that the requested reviewer identity is unverified and do not claim its approval.
- An optional external review failure must not erase a valid local candidate or block an independently sufficient approved fallback.
- Preserve the failure message, use only an already authorized fallback, and state which route actually produced the accepted evidence.
- Never discover keys, install provider tooling, or switch to a paid route as an implicit recovery step.

## Adapting the method to another host

- Keep one universal method.
- A host adapter is justified only when the host can initiate work and needs unique instructions for fresh context, tool permissions, result retrieval, bounded waiting, or a known isolation limitation.
- An adapter contains no project policy, reviewer rubric, Git workflow, scope rules, or duplicate lifecycle prose.
- Before calling a host supported, verify all of: installation has a deterministic destination; the entry loads this framework and exactly one adapter; a fresh executor can change the intended repository; a separate reviewer can inspect it; full results return to the coordinator; and removal preserves user changes.
- Package-level checks may establish deterministic wiring; live qualification must be reported separately and never inferred from fixtures.
- If a host lacks one of those mechanics: document the precise limitation and offer manual copy-and-paste where it remains useful.
- Do not emulate another host's tool names, hide a provider hop, or add a universal launcher.
- The smallest correct extension is one adapter plus necessary installer and distribution wiring, all governed by the same framework.
