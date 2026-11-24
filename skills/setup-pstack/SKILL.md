---
name: setup-pstack
description: Configure which models pstack uses per role and at what reasoning budget. Detects your available models and writes an always-applied rule that overrides the skill defaults. Use for /setup-pstack, "configure pstack models", "pstack budget", or changing pstack's model choices.
---

# Setup pstack

Write `~/.gemini/config/rules/pstack-models.md`, an always-applied rule that sets pstack's model per role in Antigravity.

## Steps

### 1. Detect available models

Enumerate the model tiers you can pass to `invoke_subagent` in this session: `pro`, `flash`, `flash_lite`, or `inherit`. The aliases `inherit` and `auto` are always valid.

### 2. Load current state

The default role-to-model mapping is the rule shape shown in step 5 below. If `~/.gemini/config/rules/pstack-models.md` already exists, read it and treat its `# budget` line and its role values as the current choices. Otherwise start from those defaults. Drop any line whose role is not in step 5.

### 3. Budget, map, and confirm

**(a) Ask for a budget.** Prefer `ask_question` over free text. Offer these three options and name the current budget when the rule records one. With no rule, say that `large` matches the skill defaults:

- `large — pro for judgment & code delegates, flash for fast workers`
- `medium — flash across all roles`
- `small — flash_lite for workers, flash for judgment`

**(b) Apply it.** Build the working table from the skill defaults:
- `large`: `pro` for code delegates, judgment, and prose; `flash` for swarm workers; `pro, flash` for review panels.
- `medium`: `flash` for all roles.
- `small`: `flash_lite` for workers, `flash` for judgment.

**(c) Show the roles and confirm.** Show every role with its model. Ask whether to accept as-is or change specific roles, offering `pro`, `flash`, `flash_lite`, and `inherit` as options via `ask_question`. For panel roles (`arena runners`, `interrogate reviewers`) the value is a list and one subagent runs per entry.

### 4. Validate

Confirm that every chosen value is valid for `invoke_subagent` (`pro`, `flash`, `flash_lite`, or `inherit`).

### 5. Write the rule

Write `~/.gemini/config/rules/pstack-models.md` with `# defaults: 3`, a `# budget` line, and one line per role. Overwrite the whole file so re-runs stay idempotent. Shape:

```markdown
# pstack model configuration. One line per role. Delete a line to fall back to the skill default.
# `inherit` runs the role on the parent chat model.
# defaults: 3
# budget: large
feature, refactoring: pro
bug-fix: pro
perf-issue: pro
hillclimb: pro
judgment and prose: pro
arena runners: pro, flash
arena cross-judge pool: pro, flash
swarm workers: flash
interrogate reviewers: pro, flash
```

### 6. Confirm

Tell the user the rule was written and that it applies to new sessions. Re-running this skill updates it.

### 7. Offer a verification skill (optional)

Check whether the project has a way to drive the real app for proof (a `verify-*` skill, or an existing harness). If not, offer once: "Want a project-local verification skill, so agents can drive the app the way a user does and prove changes work? I can generate one with /create-verification-skill." On yes, invoke `/create-verification-skill`. On no, move on without pushing.

### 8. Offer a formal verification skill (optional)

Check whether the project already has a formal verification skill (a project skill that runs a model checker, a proof, or another verifier against the code). If not, offer once: "Want a formal verification skill, so agents can prove a key property of your code holds in every case in scope, not only the cases tests reach? I can generate one with /create-formal-verification-skill." On yes, invoke `/create-formal-verification-skill`. On no, move on without pushing.
