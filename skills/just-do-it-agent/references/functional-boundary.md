# Functional Boundary

Use this reference when a task may need clarification before material implementation.

## Definition

A functional boundary is the observable product or artifact contract that makes "done" verifiable. It covers behavior, options, states, exclusions, and acceptance checks. It is not the internal implementation approach.

If the boundary can be resolved by inspecting code, docs, tickets, logs, screenshots, tests, or surrounding behavior, inspect instead of asking. If meaningful user-visible behavior remains undefined, ask a concise batch of questions with recommended defaults when useful.

## Question Dimensions

Shape questions toward:

- Goals: what user-visible outcome distinguishes done from almost done.
- Acceptance: how a machine or reviewer can verify the behavior.
- Boundaries: what adjacent behavior, screen, data, workflow, or artifact is out of scope.
- States and failures: empty, loading, error, permission, rollback, retry, skip, cancel, timeout, and partial-success behavior.
- Assumptions: product facts, permissions, persistence, failure handling, data sensitivity, or deployment constraints being guessed.
- Alternatives: choices that change user-visible behavior, risk, cost, delivery constraints, or long-term operability.

Bring implementation choices into the conversation when they affect the product contract, constrain verification, create meaningful long-term tradeoffs, or cannot be inferred from the workspace.

## Example

For "add automatic updates," ask whether users need "skip this version," "remind me later," "check now," rollback/failure messaging, and where update status is visible.

Discuss scheduler, updater library, or storage choices only when they affect product behavior, deployment constraints, reliability, or verification.
