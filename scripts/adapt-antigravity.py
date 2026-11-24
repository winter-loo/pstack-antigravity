#!/usr/bin/env python3
"""Idempotently adapt pstack files for the Antigravity AI agent.

Removes Cursor / Grok / Claude / Opus / Fable / Bugbot references and maps
models, subagent primitives, rules, and paths to native Antigravity equivalents.
"""

import json
import os
import re
import shutil
import sys

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def read(rel: str) -> str:
    with open(os.path.join(ROOT, rel), "r", encoding="utf-8") as f:
        return f.read()


def write(rel: str, text: str) -> None:
    p = os.path.join(ROOT, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8") as f:
        f.write(text)


def remove_if_exists(rel: str) -> None:
    p = os.path.join(ROOT, rel)
    if os.path.isdir(p):
        shutil.rmtree(p)
    elif os.path.exists(p):
        os.remove(p)


def adapt_plugin_json() -> None:
    data = json.loads(read("plugin.json"))
    version = data.get("version", "0.15.48")
    out = {
        "$schema": "https://agent-plugins.org/schemas/1.0.0/plugin.schema.json",
        "name": "pstack",
        "version": version,
        "description": "If you want to go fast, go deep first. pstack helps you write less, but higher quality code. Rigorous Antigravity agent workflows you can parallelize with confidence.",
        "author": {"name": "Lauren Tan"},
        "homepage": "https://github.com/poteto/pstack",
        "license": "MIT",
        "keywords": [
            "pstack",
            "poteto-mode",
            "antigravity",
            "workflow",
            "principles",
            "agent-style",
            "subagents",
            "unslop",
        ],
    }
    write("plugin.json", json.dumps(out, indent=2) + "\n")


def adapt_poteto_agent() -> None:
    p = "agents/poteto-agent.md"
    if not os.path.exists(os.path.join(ROOT, p)):
        return
    text = read(p)
    text = re.sub(r"^model:.*\n", "", text, flags=re.MULTILINE)
    text = text.replace("~/.cursor/plugins/", "~/.gemini/config/plugins/")
    text = text.replace(".cursor-plugin/plugin.json", "plugin.json")
    text = text.replace("Task spawn", "subagent spawn")
    write(p, text)


def adapt_setup_pstack() -> None:
    content = """---
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
"""
    write("skills/setup-pstack/SKILL.md", content)


def adapt_poteto_mode() -> None:
    text = read("skills/poteto-mode/SKILL.md")
    text = text.replace(
        "- Before commit → `/deslop` from the `cursor-team-kit` plugin. Before review → **no-comments**.",
        "- Before commit → deslop the diff (`/deslop` or `/unslop`). Before review → **no-comments**.",
    )
    text = text.replace(
        "- Shipping UI / IDE / CLI → `control-ui` or `control-cli` from `cursor-team-kit`.",
        "- Shipping UI / IDE / CLI → drive the real surface with an automated UI or CLI test driver.",
    )
    text = text.replace(
        "- PR status → the **Babysit** playbook, not Cursor's built-in babysit skill. Landing a green stack → the **Shipping** playbook.",
        "- PR status → the **Babysit** playbook. Landing a green stack → the **Shipping** playbook.",
    )
    text = text.replace(
        "Starting any agent, whether a Task subagent or a Project worker",
        "Starting any subagent via `invoke_subagent`",
    )

    old_subagents = re.search(
        r"## Subagents\n.*?(?=\n## Writing the reply)", text, flags=re.DOTALL
    )
    if old_subagents:
        new_subagents = """## Subagents

**Use `invoke_subagent` with `TypeName: "poteto-agent"` (or `"self"`) for any subagent you spawn directly inside a playbook step.** The chat that receives `/poteto-mode` runs the playbook itself. Routed workflow skills (`interrogate`, `swarm`) set their own subagent roles. Respect them.

**Defaults for every `invoke_subagent` call.** Subagents run asynchronously in the background. Pass file pointers instead of inlining large context, and set an explicit `Model` per role. `/setup-pstack` writes `~/.gemini/config/rules/pstack-models.md`, whose per-role lines override the defaults below and the role models in routed skills (`arena`, `swarm`, `interrogate`). A role with no line keeps its default. A line of `inherit` or `auto` runs the role on the parent model (`Model: "inherit"`). Each code playbook reads its own line (`feature, refactoring`, `bug-fix`, `perf-issue`, or `hillclimb`), prose and judgment read `judgment and prose`, and trivial mechanical edits or verification read `swarm workers`.

- Code, prose, and judgment: `pro`.
- Trivial mechanical edits and verification workers: `flash`.
- Diverse review and design panels: `pro` and `flash`.

**Match the model to the job.** Start from the role's line or default and pick the tier the job needs (`pro` for hard/subtle reasoning, `flash` for fast execution and verification, `flash_lite` for routine checks, `inherit` to match the parent session).

You own every subagent's work. Review the diff and write your own summary. A second opinion is the same prompt against a second model tier.

**Fresh subagents by default.** Give a fix round, a follow-up, a retry, or the next queue item to a fresh subagent with the original brief, every later directive, and the prior agent's report and branch. Resume an existing subagent only when the work needs state that lives in it and is costly to move: its checkout, its uncommitted changes, or a process it still runs."""
        text = text[: old_subagents.start()] + new_subagents + text[old_subagents.end() :]

    write("skills/poteto-mode/SKILL.md", text)


def adapt_arena_and_swarm() -> None:
    arena = read("skills/arena/SKILL.md")
    arena = re.sub(
        r"3\. Pick the runners from the `arena runners` line.*?(?=\n4\.)",
        "3. Pick the runners from the `arena runners` line in `~/.gemini/config/rules/pstack-models.md`, by default `pro` and `flash`. An `auto` or `inherit` entry runs on the parent model (`Model: \"inherit\"`). Spawn runners via `invoke_subagent`, keeping at least two runners. Spawn more for multiple design directions, and repeat one model when the work is generation-bound, not judgment-sensitive.",
        arena,
        flags=re.DOTALL,
    )
    arena = re.sub(
        r"After all Phase B candidates complete, spawn one readonly judge.*?(?=\n## Phase D)",
        "After all Phase B candidates complete, spawn one readonly judge from the `arena cross-judge pool` line in `~/.gemini/config/rules/pstack-models.md`, by default `pro` and `flash`. Pick a tier different from the parent where possible, or `pro` by default. While you read in Phase D, the judge scores each candidate, by path label, on each rubric criterion and recommends a base.\n",
        arena,
        flags=re.DOTALL,
    )
    arena = arena.replace("/tmp/arena-<slug>/", "/var/tmp/arena-<slug>/")
    write("skills/arena/SKILL.md", arena)

    swarm = read("skills/swarm/SKILL.md")
    swarm = re.sub(
        r"3\. Pick the worker model from the `swarm workers` line.*?(?=\n4\.)",
        "3. Pick the worker model from the `swarm workers` line in `~/.gemini/config/rules/pstack-models.md`. If the rule or that line is missing, use `flash`. For `auto` or `inherit`, use `Model: \"inherit\"` so the workers run on the parent model. For a model race, name each arm's model up front.",
        swarm,
        flags=re.DOTALL,
    )
    write("skills/swarm/SKILL.md", swarm)


def adapt_readme() -> None:
    text = read("README.md")
    text = text.replace("at Meta, Netflix, and Cursor.", "at Meta, Netflix, and other tech companies.")
    text = text.replace(
        "ship high quality code at Cursor. this turns cursor into a real engineering team.",
        "ship high quality code. this turns Antigravity into a real engineering team.",
    )
    text = text.replace(
        "**cursor gives you the best of all worlds.**",
        "**antigravity gives you the best of all worlds.**",
    )
    text = re.sub(
        r"## install\n.*?(?=\n## get started)",
        """## install

In Antigravity, pstack is installed locally as a native plugin:
- Plugin directory: `~/.gemini/config/plugins/pstack/`
- Global skills directory: `~/.gemini/config/skills/`
- Configuration rule: `~/.gemini/config/rules/pstack-models.md`

The [Antigravity adapter](./docs/harness/antigravity.md) maps Antigravity tools, subagents, and model roles.
""",
        text,
        flags=re.DOTALL,
    )
    text = re.sub(
        r"out of the box, code delegates.*?(?=\[`/setup-pstack`\])",
        "out of the box, code delegates (feature, refactoring, bug fix, perf, hillclimb), prose, and judgment go to `pro`, and fast verification workers go to `flash`. the default review panel is `pro` / `flash`. ",
        text,
        flags=re.DOTALL,
    )
    text = text.replace(
        "pick `/poteto-mode` from the `/` menu before you type your task, so cursor attaches the skill to the message.",
        "pick `/poteto-mode` from the `/` menu or type `/poteto-mode` before your task.",
    )
    text = re.sub(
        r"to keep \[`/poteto-mode`\]\(\./skills/poteto-mode/SKILL\.md\) on across turns.*?(?=\n## skills)",
        "[`/poteto-mode`](./skills/poteto-mode/SKILL.md) works across turns and with iterative loops or `/goal`. you can make Antigravity work for many hours without sacrificing rigor.\n",
        text,
        flags=re.DOTALL,
    )
    text = text.replace("wake a Grok Bot over a webhook", "wake an AI bot over a webhook")
    text = re.sub(
        r"## not shipped here\n.*?(?=\n## why are there no planning skills\?)",
        """## not shipped here

a few things `poteto-mode` references:

- `/deslop` and `/unslop` strip narrating comments, unsupported guards, and dead code.
- UI and CLI verification drivers can be run via automated scripts or browser skills.
- Skill authoring follows Antigravity skill conventions (`agy-customizations`). For PR status, `poteto-mode` routes directly to the [babysit playbook](./skills/poteto-mode/playbooks/babysit.md).
""",
        text,
        flags=re.DOTALL,
    )
    text = text.replace(
        "cursor already has a great plan mode which works great with pstack.",
        "Antigravity has planning capabilities which work great with pstack.",
    )
    text = text.replace(
        "to set it up, point cursor at [`FOR_AGENTS.md`](./automations/benny/FOR_AGENTS.md). setup copies the pack into the target repository at `.cursor/automations/benny/`, enables pstack there for shared skills, and keeps user configuration outside the copied pack. benny runs on cursor automations, so it is cursor-only.",
        "to set it up, point Antigravity at [`FOR_AGENTS.md`](./automations/benny/FOR_AGENTS.md). setup copies the pack into the target repository at `.agents/automations/benny/`, enables pstack there for shared skills, and keeps user configuration outside the copied pack.",
    )
    write("README.md", text)


def adapt_markdown_sweep() -> None:
    """Apply consistent Antigravity replacements across all markdown and yaml files."""
    replacements = [
        ("~/.cursor/rules/pstack-models.mdc", "~/.gemini/config/rules/pstack-models.md"),
        ("pstack-models.mdc", "pstack-models.md"),
        ("https://github.com/cursor/plugins/blob/main/pstack/", "https://github.com/poteto/pstack/blob/main/"),
        (".cursor/automations/benny/", ".agents/automations/benny/"),
        (".cursor/benny/", ".agents/benny/"),
        (".cursor/settings.json", ".agents/config.json"),
        (".cursor/skills/", ".agents/skills/"),
        ("~/.cursor/skills/", "~/.gemini/config/skills/"),
        ("~/.cursor/plugins/", "~/.gemini/config/plugins/"),
        (".cursor/worktrees/", ".agents/worktrees/"),
        ("~/Library/Application Support/Cursor", "~/.gemini/antigravity-cli"),
        ("~/.cursor/projects/*/", "<appDataDir>/brain/*/"),
        ("claude-opus-5-5-xhigh-fast", "pro"),
        ("claude-opus-5-5-high-fast", "flash"),
        ("claude-opus-5-5-medium-fast", "flash_lite"),
        ("claude-opus-5-5-low-fast", "flash_lite"),
        ("claude-opus-5-5-xhigh", "pro"),
        ("claude-fable-5-2-high", "pro"),
        ("grok-4.7-xhigh-fast", "flash"),
        ("Grok Bot", "AI bot"),
        ("Cursor's built-in `create-skill`", "Antigravity skill authoring (`agy-customizations`)"),
        ("Cursor's built-in babysit skill", "standard babysit tools"),
        ("Cursor's `/loop` command (a built-in, not a pstack skill)", "the `/loop` or `/goal` command"),
        ("Cursor's `/loop` command", "`/loop` or `/goal`"),
        ("Each owner is a Cursor cloud agent", "Each owner is an Antigravity subagent"),
        ("a Cursor cloud agent", "an independent subagent"),
        ("the `deslop` skill from the `cursor-team-kit` plugin (`/deslop`)", "the `/deslop` or `/unslop` pass"),
        ("Run `/deslop` from `cursor-team-kit`", "Run `/deslop` or `/unslop`"),
        ("`/deslop` ships in the `cursor-team-kit` plugin, not in pstack.", "Use `/unslop` or deslop the code directly."),
        ("such as `control-ui` or `control-cli` from `cursor-team-kit`", "such as an automated UI or CLI test driver"),
        ("`control-ui` or `control-cli` from `cursor-team-kit`", "an automated UI or CLI test driver"),
        ("from `cursor-team-kit`", ""),
        ("cursor-team-kit", "Antigravity tools"),
        ("two cursor automations", "two agent automations"),
        ("Cursor automations", "agent automations"),
        ("pointing cursor at", "pointing Antigravity at"),
        ("pointing Cursor at", "pointing Antigravity at"),
        ("restart Cursor", "restart Antigravity"),
        ("A [Cursor Project](https://cursor.com/blog/projects) gives one coordinator agent a persistent thread. The coordinator doesn't write code. It directs subagents, which run in the cloud by default, so the work continues when your laptop is closed.", "Antigravity orchestration gives one coordinator agent a persistent thread. The coordinator directs subagents across isolated workspaces."),
        ("In a Cursor chat, run:", "In Antigravity, pstack is installed locally in `~/.gemini/config/plugins/pstack`."),
        ("Cursor confirms the plugin is installed.", "The plugin is discovered and active."),
        ("In Claude Code, run `/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`. Claude Code prefixes plugin commands, so each command in this guide takes a `pstack:` prefix there, such as `/pstack:setup-pstack`, which writes its model rule to `~/.claude/rules/pstack-models.md`. The [Claude Code adapter](../harness/claude-code.md) covers the other differences.", "See the [Antigravity adapter](../harness/antigravity.md) for tool mappings, model roles, and path conventions."),
        ("To keep `/poteto-mode` on for the whole chat, pick it from the `/` menu with Option+Enter (Mac) or Alt+Enter (Windows) instead of Enter. That makes it a [Custom Mode](https://cursor.com/docs/skills#using-a-skill-as-a-custom-mode), which stays in context on every turn until you exit it. Custom Modes are available in the Agents Window and the CLI. Plain Enter attaches the skill to one message, and it fades as the chat moves on.", "Invoke `/poteto-mode` at the start of any complex task to ground execution in proven playbooks."),
        ("- `/loop` is Cursor's built-in wake mechanism, not a pstack skill.", "- `/loop` or `/goal` automates recurring iteration and long-running execution."),
        ("pstack is built for Cursor, and it also installs in Claude Code with `/plugin marketplace add cursor/plugins`, then `/plugin install pstack@cursor-plugins`. There, each command takes a `pstack:` prefix, such as `/pstack:poteto-mode`. The [Claude Code adapter](../../docs/harness/claude-code.md) maps the Cursor names, and a step that needs a Cursor-only feature, such as Bugbot or Automations, is skipped with a one-line note.", "pstack is built for Antigravity, running natively with Antigravity subagents and tools. The [Antigravity adapter](../../docs/harness/antigravity.md) maps tools and workflows."),
        ("Other tools can read the skills, because they use the Agent Skills format. But most workflow skills, including `/poteto-mode`, `/how`, and `/teach`, spawn Cursor subagents, some with per-role models, and Custom Modes and `/loop` are Cursor features, so those parts may not work there.", "pstack skills use the standard Agent Skills format. Workflow skills spawn Antigravity subagents via `invoke_subagent` with per-role models configured in `~/.gemini/config/rules/pstack-models.md`."),
        ("Cursor's docs list Custom Modes in the Agents Window and the CLI. Elsewhere, start each new task with `/poteto-mode`.", "Start each new task with `/poteto-mode`."),
        ("Link [Cursor's skills docs](https://cursor.com/docs/skills) when this comes up. ", ""),
        ("Without `/poteto-mode`, a phrase such as \"babysit this pr\" can start Cursor's own skill for the same job instead.", "Using `/poteto-mode` ensures the rigorous babysit playbook runs."),
        ("Cursor's Plan Mode works alongside it.", "Antigravity planning features work alongside it."),
        ("- `/deslop`, `control-cli`, and `control-ui` ship in the `Antigravity tools` plugin.\n- `/loop` and `/create-skill` are Cursor built-ins.", "- Code deslopping is handled via `/deslop` or `/unslop`.\n- Skill authoring follows Antigravity skill guidelines (`agy-customizations`)."),
        ("bugbot-triage.md", "review-bot-triage.md"),
        ("address the bugbot comments", "address the review bot comments"),
        ("Bugbot", "review bot"),
        ("bugbot", "review bot"),
    ]

    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules", "scripts")]
        for fname in files:
            if not fname.endswith((".md", ".yaml", ".yml")):
                continue
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, ROOT)
            text = read(rel)
            orig = text
            for old, new in replacements:
                text = text.replace(old, new)
            # Clean up any leftover 01-setup Opus/Fable/Gemini paragraph
            if rel == "docs/guide/01-setup.md":
                text = re.sub(
                    r"The defaults are the same as the `large` budget\..*?spend fewer tokens\.",
                    "The default budget runs `pro` for code delegates, architecture, and judgment, and `flash` for fast workers. `medium` uses `flash` across roles, and `small` lowers workers to `flash_lite`.",
                    text,
                    flags=re.DOTALL,
                )
            if rel == "skills/poteto-mode/playbooks/session-pickup.md":
                text = text.replace(
                    "A local transcript under the active workspace's `agent-transcripts/` directory (the system prompt names the path. Do not glob across `<appDataDir>/brain/*/`, that crosses workspace boundaries and reads private chats from unrelated projects), a cloud-agent URL, or a pushed branch.",
                    "A local transcript under `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl`, a prior subagent result, or a pushed branch.",
                )
            if text != orig:
                write(rel, text)


def adapt_scripts_pkg() -> None:
    for rel in [
        "skills/poteto-mode/scripts/package.json",
        "skills/poteto-mode/scripts/bun.lock",
        "skills/statechart/scripts/package.json",
    ]:
        if os.path.exists(os.path.join(ROOT, rel)):
            t = read(rel)
            t = t.replace("@cursor-skill/", "@antigravity-skill/")
            write(rel, t)


def audit() -> int:
    pat = re.compile(r"\b(cursor|grok|claude|opus|fable|composer)\b", re.IGNORECASE)
    hits = []
    for root, dirs, files in os.walk(ROOT):
        dirs[:] = [d for d in dirs if d not in (".git", "node_modules")]
        for fname in sorted(files):
            full = os.path.join(root, fname)
            rel = os.path.relpath(full, ROOT)
            if rel.startswith("scripts/"):
                continue
            try:
                with open(full, "r", encoding="utf-8", errors="ignore") as f:
                    lines = f.readlines()
            except Exception:
                continue
            for idx, line in enumerate(lines, 1):
                clean = line.replace("endCursor", "").replace("pageInfo.endCursor", "")
                if pat.search(clean):
                    hits.append(f"{rel}:{idx}: {line.strip()[:120]}")
    print(f"Audit remaining matches: {len(hits)}")
    for h in hits:
        print(" ", h)
    return len(hits)


def main() -> int:
    remove_if_exists(".cursor-plugin")
    remove_if_exists("docs/harness/claude-code.md")
    adapt_plugin_json()
    adapt_poteto_agent()
    adapt_setup_pstack()
    adapt_poteto_mode()
    adapt_arena_and_swarm()
    adapt_readme()
    adapt_markdown_sweep()
    adapt_scripts_pkg()
    return 0 if audit() == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
