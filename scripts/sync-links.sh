#!/usr/bin/env python3
"""Sync symlinks for all pstack skills into ~/.agents/skills and ~/.gemini/config/skills."""

import os

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PSTACK_SKILLS = os.path.join(REPO_ROOT, "skills")
AGENTS_SKILLS = os.path.expanduser("~/.agents/skills")
GEMINI_SKILLS = os.path.expanduser("~/.gemini/config/skills")

os.makedirs(AGENTS_SKILLS, exist_ok=True)
os.makedirs(GEMINI_SKILLS, exist_ok=True)

# 1. Prune any broken symlinks pointing into pstack
for base in (AGENTS_SKILLS, GEMINI_SKILLS):
    for name in os.listdir(base):
        p = os.path.join(base, name)
        if os.path.islink(p) and not os.path.exists(p):
            os.unlink(p)
            print(f"Pruned broken symlink: {p}")

# 2. Link every skill in pstack/skills/
linked = 0
aliased = []
for name in sorted(os.listdir(PSTACK_SKILLS)):
    src = os.path.join(PSTACK_SKILLS, name)
    if not os.path.isdir(src) or not os.path.exists(os.path.join(src, "SKILL.md")):
        continue

    target_agents = os.path.join(AGENTS_SKILLS, name)
    target_gemini = os.path.join(GEMINI_SKILLS, name)

    # Check if already linked to us
    if os.path.islink(target_agents) and os.path.realpath(target_agents) == os.path.realpath(src):
        if not os.path.exists(target_gemini):
            os.symlink(f"../../../.agents/skills/{name}", target_gemini)
        linked += 1
        continue

    # Collision with another non-pstack skill -> alias as pstack-<name>
    if os.path.exists(target_agents):
        alias = f"pstack-{name}"
        ta = os.path.join(AGENTS_SKILLS, alias)
        tg = os.path.join(GEMINI_SKILLS, alias)
        if os.path.islink(ta):
            os.unlink(ta)
        if not os.path.exists(ta):
            os.symlink(src, ta)
        if os.path.islink(tg):
            os.unlink(tg)
        if not os.path.exists(tg):
            os.symlink(f"../../../.agents/skills/{alias}", tg)
        aliased.append((name, alias))
    else:
        os.symlink(src, target_agents)
        if not os.path.exists(target_gemini):
            os.symlink(f"../../../.agents/skills/{name}", target_gemini)
        linked += 1

print(f"Synced {linked} skills directly; aliased {aliased}")
