---
id: 003
title: Create quality-gate, tdd-enforcer, and python-scaffold skills
stage: misc
date: 2025-12-27
surface: agent
model: claude-opus-4-5-20251101
feature: none
branch: phase-1-console
user: abdullahiqbal
command: skill-creator
labels: ["skills", "quality-gate", "tdd-enforcer", "python-scaffold", "tooling"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/quality-gate/SKILL.md
  - .claude/skills/quality-gate/scripts/run_gates.py
  - .claude/skills/quality-gate/references/gates.md
  - .claude/skills/tdd-enforcer/SKILL.md
  - .claude/skills/tdd-enforcer/scripts/tdd_check.py
  - .claude/skills/tdd-enforcer/scripts/generate_tests.py
  - .claude/skills/tdd-enforcer/references/tdd_patterns.md
  - .claude/skills/python-scaffold/SKILL.md
  - .claude/skills/python-scaffold/scripts/scaffold.py
  - .claude/skills/python-scaffold/references/templates.md
tests:
  - Verified quality-gate runs all 4 gates (test, type, lint, doc)
  - Verified tdd-enforcer detects missing tests
  - Verified tdd-enforcer generates test templates
  - Verified python-scaffold creates module structure
  - Verified python-scaffold creates service structure
---

## Prompt

No use your @skill-creator skill for creating both 3 skills

(Context: User requested 3 skills - quality-gate, tdd-enforcer, python-scaffold - to be created using the skill-creator skill from the anthropic-agent-skills plugin. Skills should be placed in .claude/skills/ directory.)

## Response snapshot

Created 3 reusable skills for TaskFlow project:

1. **quality-gate** - Runs all code quality gates (tests, types, lint, docs) in one command
   - `scripts/run_gates.py` with --fix, --gate, --strict flags
   - Reports unified pass/fail status

2. **tdd-enforcer** - Enforces TDD workflow
   - `scripts/tdd_check.py` detects code without tests
   - `scripts/generate_tests.py` creates Arrange-Act-Assert test templates
   - References TDD patterns documentation

3. **python-scaffold** - Generates constitution-compliant Python structure
   - `scripts/scaffold.py module <name>` for modules
   - `scripts/scaffold.py service <name>` for services with protocols
   - Includes type hints, docstrings, and test stubs

All skills tested and verified working.

## Outcome

- ✅ Impact: Created 3 reusable skills that enforce constitution principles across Phase 1 and future phases
- 🧪 Tests: All 3 skills verified with dry-run and functional tests
- 📁 Files: 10 files created in .claude/skills/
- 🔁 Next prompts: /sp.tasks to generate implementation tasks, then TDD implementation
- 🧠 Reflection: Skills follow skill-creator best practices - minimal SKILL.md, scripts for automation, references for documentation

## Evaluation notes (flywheel)

- Failure modes observed: None - followed skill-creator workflow correctly
- Graders run and results (PASS/FAIL): PASS - all scripts have valid CLI interfaces and produce expected output
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Consider adding --quiet flag to quality-gate for CI usage
