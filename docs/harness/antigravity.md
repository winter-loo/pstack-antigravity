# pstack in Antigravity

pstack is designed to run seamlessly with the Antigravity AI agent. This document describes the native tool mappings, model roles, and path conventions used by pstack within Antigravity.

## Tools and Primitives

| Generic Concept | Antigravity Native Equivalent |
| --- | --- |
| Subagent delegation (`Task`) | `invoke_subagent` (with `TypeName`, `Model`, `Role`, `Prompt`, `Workspace`) |
| Interactive user questions | `ask_question` (or direct prompt when simple) |
| Task planning / Todos | Antigravity artifacts / Markdown todo lists |
| Code search | Native MCP codebase graph tools (`search_graph`, `trace_path`, `get_code_snippet`) or `run_command` with `rg` / `git` |
| File editing | Native tools: `edit_file`, `write_file`, `read_file` |

## Subagent Configuration

| Capability | Antigravity Mapping |
| --- | --- |
| Subagent type | `TypeName: "self"` (default), or custom types defined with `define_subagent` (e.g. `poteto-agent`, `comment-sicko`) |
| Read-only exploration | `TypeName: "research"` or prompt with explicit read-only instructions |
| Workspace isolation | `Workspace: "branch"` or git worktree isolation |
| Background execution | Native asynchronous execution; Antigravity wakes automatically on subagent completion |
| Model selection | `Model: "pro"` (complex reasoning / judgment), `"flash"` (fast code execution), `"flash_lite"` (routine), or `"inherit"` |

## Model Configuration & Budget

pstack configures role-specific models in `~/.gemini/config/rules/pstack-models.md` (or workspace-level `.agents/rules/pstack-models.md`).

- **Defaults**:
  - Code delegates (feature, refactoring, bug-fix, perf, hillclimb): `flash`
  - Judgment, architecture, prose, synthesizers: `pro`
  - Swarm workers & explorers: `flash`
  - Review panels (arena runners, architect runners, interrogate reviewers): `pro`, `flash`
- **Reasoning Budgets**:
  - `unlimited` / `large`: `pro` for judgment and hardest tasks; `flash` for execution delegates.
  - `medium`: `flash` for standard workflows.
  - `small`: `flash_lite` for workers and routine steps; `flash` for judgment.

## Paths & Storage

| Path Category | Antigravity Path |
| --- | --- |
| Global plugin root | `~/.gemini/config/plugins/pstack/` |
| Global skills | `~/.gemini/config/skills/` |
| Workspace skills | `.agents/skills/` |
| Configuration rules | `~/.gemini/config/rules/pstack-models.md` or `.agents/rules/pstack-models.md` |
| Conversation transcripts | `<appDataDir>/brain/<conversation-id>/.system_generated/logs/transcript.jsonl` |
| Artifact directory | `<appDataDir>/brain/<conversation-id>/` |
