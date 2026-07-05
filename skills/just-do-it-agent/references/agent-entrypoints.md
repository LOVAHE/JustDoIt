# Agent Entrypoints

Use this reference when creating, changing, automating, testing, documenting, or handing off a durable workflow.

## Durable Deliverables

A durable deliverable is an artifact expected to be reused, operated, tested, maintained, handed off, or extended after this task: app flow, UI, API, command, script, report, dashboard, spec, runbook, automation, data pipeline, or integration.

Durable deliverables should have both:

- Human-facing surface: what a person uses, reads, reviews, or decides from.
- Agent-facing entrypoint: the stable, explicit, machine-operable path another agent can use.

Document an existing agent-facing entrypoint by default when one is relevant. Add a new handle, key, selector, route, schema, registry entry, command, or runbook only when the requested work creates or materially changes a durable workflow, the project already has a compatible convention, or future operation would otherwise be unreliable.

## Proportional Ladder

1. Reuse and document an existing project convention: test id, API route, CLI, schema, manifest, route, command bus, event, runbook, or `JDI.md` note.
2. Add a lightweight stable key, selector, test hook, command option, or route when the workflow has no reliable agent handle and the addition stays inside scope.
3. Add a schema, manifest, action registry, automation command, or runbook only for workflows that will be reused or operated by agents.
4. If adding an entrypoint would change public behavior or exceed scope, describe the recommended entrypoint in the handoff.

Keep implementation notes, debug labels, prompt details, source provenance, and agent metadata out of user-facing product UI unless the user asks for a developer/debug view. Keep agent contracts in code, tests, hidden metadata, schemas, manifests, docs, `JDI.md`, or developer-facing comments.

## Contract Fields

When creating or changing a durable workflow, expose the contract fields that fit:

- Stable key: semantic identifier such as `settings.save`, `kanban.card.move`, `checkout.coupon.apply`, or `report.filter.dateRange`.
- Invocation path: command, API route, function, event, test selector, URL, action registry entry, CLI flag, manifest entry, automation script, or `JDI.md` section.
- Inputs: names, types, allowed values, defaults, required fields, and examples when useful.
- Preconditions: auth, state, selected item, loaded data, environment, feature flag, or permissions.
- Side effects: what changes, what persists, and what external systems are touched.
- Success signal: returned value, DOM state, event, route, file output, database row, log line, metric, or test assertion.
- Failure signal: error shape, validation message, exit code, retry behavior, rollback condition, or user-visible failure state.
- Verification: exact command, test, query, assertion, screenshot check, or inspection step another agent can run.

Use dot-namespaced keys for actions. Keep keys semantic and stable; avoid wording tied to button text, screen position, styling, or temporary implementation details.

## UI Work

For new or materially changed durable UI workflows, make the workflow operable without relying only on pointer clicks. Prefer existing project-approved handles first: accessible roles, tests, routes, API responses, command-palette actions, component methods, events, state attributes, keyboard paths, or selectors.

For drag, hover, drawing, timeline edits, or multi-step forms, provide a programmatic action or keyboard path in addition to pointer-only operation when it is reasonable for the product.

## Examples

Treat these examples as examples, not preferred conventions:

```json
{
  "agentKey": "settings.save",
  "invoke": "projectAction('settings.save', payload)",
  "input": { "displayName": "string", "theme": "light|dark" },
  "successSignal": "settings.saved event or persisted preference reloads",
  "verify": "Run the settings save test and assert the saved preference reloads"
}
```

```json
{
  "agentKey": "report.export",
  "invoke": "bin/report export --format json --out ./out/report.json",
  "input": { "format": "json|csv", "out": "path" },
  "successSignal": "exit code 0 and output file exists",
  "verify": "Run the export command and validate output schema"
}
```

Adapt examples to the project's language and framework. Do not introduce a global action registry if the existing system already has a better command, event, route, schema, or test automation pattern.
