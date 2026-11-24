---
name: pstack
description: Full engineering suite for rigorous, verified, and unslopped development in Antigravity. Use for /pstack, "pstack", or learning how to apply pstack workflows, poteto-mode, and engineering principles.
disable-model-invocation: true
---

# pstack for Antigravity

**If you want to go fast, go deep first.**

pstack is a complete engineering suite designed to turn Antigravity into a rigorous engineering team. It prioritizes verified correctness, domain modeling, minimalism, and disciplined delegation over maximizing lines of code.

## Core Entry Points

1. **[`/poteto-mode`](../poteto-mode/SKILL.md)**: The primary entry point for any non-trivial task. It matches your task against 23 proven playbooks and executes with strict verification and unslopped prose.
2. **[`/setup-pstack`](../setup-pstack/SKILL.md)**: Configures per-role subagent models (`pro`, `flash`, `inherit`) and reasoning budgets, writing the configuration rule to `~/.gemini/config/rules/pstack-models.md`.
3. **[`/poteto-help`](../poteto-help/SKILL.md)**: Interactive guidance to help you pick the right skill, playbook, or principle for your current task.

## Key Skills Overview

- **Understanding & Architecture**:
  - [`/how`](../how/SKILL.md): Subsystem architecture walkthrough and runtime flow.
  - [`/why`](../why/SKILL.md): Deep dive into motivations, historical commits, and MCP evidence.
  - [`/reframe`](../reframe/SKILL.md): Learn the expert terminology and neighboring-field framing for what you are building.
  - [`/architect`](../architect/SKILL.md): Multi-candidate interface and module sketch before coding.
  - [`/arena`](../arena/SKILL.md): Parallel solution bake-off with cross-judging and component grafting.

- **Execution & Quality**:
  - [`/unslop`](../unslop/SKILL.md): Strips AI tells, fluff, and superficial pleasantries from text.
  - [`/no-comments`](../no-comments/SKILL.md): Spawns Comment Sicko to purge dead comments and enforce obvious code.
  - [`/technical-writing`](../technical-writing/SKILL.md): Diátaxis-aligned technical documentation standard.
  - [`/tdd`](../tdd/SKILL.md): Red-green-refactor for testable bug fixes.

- **Parallel Delegation & Swarms**:
  - [`/swarm`](../swarm/SKILL.md): Parallel matrix coverage, model races, and test gauntlets via subagents.
  - [`/interrogate`](../interrogate/SKILL.md): Adversarial multi-model review to actively break patches before landing.

- **Verification**:
  - [`/create-verification-skill`](../create-verification-skill/SKILL.md): Generates a project-local `verify-*` skill with an executable feature map.
  - [`/benchmark-checklist`](../benchmark-checklist/SKILL.md): Rigorous measurement sanity checks.
  - [`/show-me-your-work`](../show-me-your-work/SKILL.md): Generates an auditable decision trail (TSV).
