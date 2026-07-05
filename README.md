# JustDoIt Agent

JustDoIt Agent is a portable skill for complex work that should be finished, checked, and left usable by the next agent.

It is not a domain expert. It is an execution overlay.

## Why

Most agent work stops at "looks done." JustDoIt Agent makes done mean:

- A human can verify the result.
- A future agent can continue from a stable entrypoint.

That entrypoint might be a command, test, API, selector, schema, runbook, action key, or `JDI.md` note.

## Use It When

Use it when a task needs autonomous end-to-end handling, a standard work loop, or agent-readable handoff.

Tiny one-shot checks and short explanations should stay lightweight.

## Install

Copy the skill folder into an agent runtime that supports file-based skills:

```text
skills/just-do-it-agent
```

For a Codex-style local setup, copy it to:

```text
~/.codex/skills/just-do-it-agent
```

Then invoke it by name, or let the agent select it for complex tasks where no other skill is named.

## What's Inside

```text
skills/just-do-it-agent/
  SKILL.md
  agents/openai.yaml
  references/
    agent-entrypoints.md
    functional-boundary.md
    jdi-memory-and-risk.md
```

`SKILL.md` is the portable core. `references/` holds details that are loaded only when needed. `agents/openai.yaml` is optional UI metadata for OpenAI-compatible skill lists.

## Status

License: CC BY-NC-SA 4.0. Non-commercial, share-alike.

The license covers this skill and its docs. It does not automatically apply to things people create while using the skill.
