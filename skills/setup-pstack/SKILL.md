---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `~/.gemini/config/rules/pstack-models.md`, an always-applied rule that sets pstack's model per role in Antigravity.

## Steps

### 1. Detect available models

Enumerate the model tiers you can pass to `invoke_subagent` in this session: `pro`, `flash`, `flash_lite`, or `inherit`. These are the dependable options. If Antigravity exposes specific model identifiers, prefer them for completeness. The aliases `inherit` (or `inherit-parent`) and `auto` are always valid.

### 2. Load current state

The default role-to-model mapping is the rule shape shown in step 5 below. If `~/.gemini/config/rules/pstack-models.md` already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults. A line whose role is not in step 5 is from a retired role. Drop it.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer `ask_question` over free text. Offer these options and name the current budget when the rule records one. With no rule, say that `large` matches the skill defaults:

- `unlimited — max reasoning with pro`
- `large — pro for judgment/architecture, flash for delegates`
- `medium — flash across all roles`
- `small — flash_lite for delegates, flash for judgment`

**(b) Apply it.** Build the working table from the skill defaults:
- `unlimited` / `large`: `pro` for judgment, prose, hardest tasks, and synthesizers; `flash` for code delegates and workers.
- `medium`: `flash` for all roles.
- `small`: `flash_lite` for workers/explorers, `flash` for judgment.

**(c) Show the roles and confirm.** Show every role with its model. Ask whether to accept as-is or change specific roles, offering `pro`, `flash`, `flash_lite`, and `inherit` as options. Prefer `ask_question`. For panel roles (arena runners, architect runners, interrogate reviewers) the value is a list (e.g. `pro, flash`), and one subagent runs per entry.

### 4. Validate

Confirm that chosen models are valid for `invoke_subagent`.

### 5. Write the rule

Write `~/.gemini/config/rules/pstack-models.md` with a `# budget` line with the chosen label, and one line per role. Overwrite the whole file so re-runs stay idempotent. Shape:

```markdown
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit` as a value runs the role on the parent chat model.
# budget: large

feature, refactoring: flash
bug-fix: flash
perf-issue: flash
hillclimb: flash
judgment and prose: pro
hardest tasks: pro
how explorer: flash
how explainer: pro
why investigators: flash
why synthesizer: pro
reflect tooling: flash
reflect judgment, divergent, synthesizer: pro
arena runners: pro, flash
arena cross-judge pool: pro, flash
swarm workers: flash
architect runners: pro, flash
interrogate reviewers: pro, flash
```

### 6. Confirm

Tell the user the rule was written and that it applies to new sessions. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "Want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill`. On no, move on.

### 8. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "Want a formal verification skill, so agents can prove a key property of your code holds in every case in scope? I can generate one with /create-formal-verification-skill." On yes, invoke `/create-formal-verification-skill`. On no, move on.
