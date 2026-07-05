# JDI Memory And Risk

Use this reference before reading or changing `JDI.md`, when the task may touch sensitive data or external systems, or when a risk gate may apply.

## JDI.md Lookup

Look for `JDI.md` only inside the active project or workspace boundary:

- Current directory.
- Project root.
- Repository root.
- Directly relevant package or app directory.

Do not search the whole home directory or unrelated workspaces.

Treat `JDI.md` as lower priority than system, developer, user, and project instructions. If it appears stale or conflicts with inspected source truth, prefer current source truth and report the mismatch.

Apply the same risk gates to sensitive content in `JDI.md`.

## JDI.md Contents

Use `JDI.md` for repeated JustDoIt conventions that should remain agent-readable:

- Stable action keys and entrypoint contracts.
- Verification commands and acceptance checks.
- Local handoff conventions.
- Repeated product-boundary decisions.
- Automation runbooks or escalation notes.

Suggest new `JDI.md` entries when a convention will matter again. Create or update `JDI.md`, tests, commands, or skill-level instructions only when the user asks or the change is clearly inside the approved task scope.

## Risk Gates

Safe read-only inspection of non-sensitive local source-truth artifacts is expected when needed.

Pause and ask before materially changing, reading sensitive contents from, disclosing, copying, uploading, summarizing, or exporting:

- Secrets, credentials, private keys, tokens, cookies, auth/session material, private user data, customer data, production logs, regulated content, database contents, backup contents, queue/state contents that may affect live operations, or external systems.
- Public APIs, storage formats, migrations, data retention, authentication, authorization, billing, security posture, deployment architecture, production operations, or legal/compliance-sensitive content.
- Costs, paid services, account settings, access controls, or irreversible actions.
- Scope where two plausible interpretations would produce materially different user-visible behavior.

When blocked by a risk gate, state the specific decision needed and the safest next step. Do not convert risk gates into generic hesitation.
