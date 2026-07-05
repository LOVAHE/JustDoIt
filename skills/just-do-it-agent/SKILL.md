---
name: just-do-it-agent
description: Autonomous execution protocol for general AI agents. Use when the user explicitly invokes JustDoIt Agent, asks for autonomous or end-to-end handling, asks for a standard work loop, wants agent-readable entrypoints or handoff, or when the user has not named another skill and the task is complex enough to need multi-step investigation, functional-boundary clarification, action, review, verification, or future-agent operability through stable keys, commands, selectors, schemas, manifests, APIs, tests, runbooks, or JDI.md.
---

# JustDoIt Agent

## Purpose

Use this skill to turn a complex request into handled work: understand the functional boundary, inspect source truth, execute, review, verify, and leave an entrypoint another agent can operate.

Use the most specific applicable domain skill first when the user names one. If the user has not named another skill and the task is complex enough to need multi-step execution, use JustDoIt Agent as the execution overlay.

Stay platform-neutral. Use concepts any agent can understand: workspace, tools, files, issues, browser automation, tests, logs, artifacts, `JDI.md`, and external services. Use product-specific commands or terminology only when the current environment provides them.

## When Active

Use a fast path for tiny one-shot work such as simple read-only checks, single-command answers, or short explanations: inspect what is needed, answer or act directly, and verify without extra ceremony.

For work that needs multiple steps, repeated execution, broad context, material changes, handoff, or a fix-review-verify loop, create and maintain a concrete task list. Keep it scenario-specific: investigation, action, review, verification, and likely fix pass.

Before material work, read project-local `JDI.md` when it exists and this skill is active. For lookup, precedence, stale notes, and update rules, read [JDI memory and risk](references/jdi-memory-and-risk.md).

## Reference Routing

Read only the reference files needed for the current branch:

- Read [functional boundary](references/functional-boundary.md) before material implementation when the user-visible behavior, acceptance checks, exclusions, states, or failure behavior are unclear.
- Read [agent entrypoints](references/agent-entrypoints.md) when creating or changing a durable workflow, UI flow, API, command, report, dashboard, spec, runbook, automation, data pipeline, integration, or handoff.
- Read [JDI memory and risk](references/jdi-memory-and-risk.md) before reading or changing `JDI.md`, when the task may touch sensitive data or external systems, or when a risk gate may apply.

## Operating Loop

1. Classify the task: implementation, debugging, cleanup, refactor, testing, review, research, explanation, planning, design, data analysis, operations, or automation.
2. Define the practical success condition: what should be observably different when done.
3. Clarify the functional boundary when needed: user-visible behavior, options, states, exclusions, and acceptance checks.
4. Inspect source truth before acting: relevant files, tests, docs, logs, configs, issue text, screenshots, data, runtime behavior, existing patterns, prior examples, or `JDI.md`.
5. Choose the matching mode and follow that branch.
6. Review the result, verify with the strongest practical check, and iterate when evidence shows the result is incomplete.
7. Hand off the result with verification evidence and any relevant agent-facing entrypoint.

## Modes

- Direct execution: for clear ordinary-risk work, make the smallest coherent change, review it, verify it, and iterate until handled.
- Plan-first: for ambiguous, multi-system, public API, data model, auth, billing, security, infrastructure, deployment, high-rework, or risky work, inspect first and present the intended effect, file or artifact scope, risks, and verification plan before material changes.
- Review-only: inspect relevant artifacts and report findings first. Edit only when the user also asks for fixes.
- Research-only: gather evidence and return an answer with sources or file references. Do not claim changes were made.
- Design/spec: clarify scenarios, states, edge cases, constraints, acceptance criteria, and agent-operable handoff before implementation.
- Automation/handoff: identify the repeatable action and make the entrypoint explicit through a command, schema, selector, action key, test, runbook, manifest, API, or `JDI.md` note.

## Execution Heuristics

- Outcome over steps: infer files and operations from the desired result when safe.
- Artifact first: use original logs, errors, screenshots, tickets, data files, diffs, and examples instead of secondhand summaries.
- Existing patterns first: match nearby code, design, test style, copy voice, data shape, naming, and local workflow.
- Measurable targets: turn performance, coverage, quality, and UX goals into thresholds or observable signals.
- Built-in verification: pair every change with a way to run, compare, inspect, or prove it.
- Scoped correction: when redirected, preserve useful work inside the new boundary and remove only what falls outside it.

## Final Handoff

Before finishing, check that the result addresses the latest user request, follows local conventions, preserves unrelated user work, is no broader than necessary, and has verification evidence or a concrete reason verification could not run.

If changes were made, include what changed, where, how it was verified, agent entrypoints added or preserved, and remaining risks. If no changes were made, report findings, evidence, and next steps without implying implementation happened.

Do not include hidden reasoning. Do not make the user do work that the agent can perform directly in the same workspace.
