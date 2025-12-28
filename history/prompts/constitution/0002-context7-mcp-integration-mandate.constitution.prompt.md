---
id: 0002
title: Context7 MCP Integration Mandate
stage: constitution
date: 2025-12-27
surface: agent
model: claude-sonnet-4-5
feature: none
branch: master
user: abdullahiqbal
command: constitution-update
labels: ["constitution", "context7", "mcp", "library-docs", "minor-version"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (constitution document)
---

## Prompt

User request: "we must use Context7 mcp server while making better auth authentication system. and also add it on constitution. after that we creating Some Strong Skills for All our phase-2 Recommend skills that we need to create and we integrate Context7 mcp server into the skills. we create all specs plan and tasks using skills."

Action: Update constitution to mandate Context7 MCP usage for all library integrations, then create Phase 2 skills with Context7 integration.

## Response snapshot

Successfully updated TaskFlow Constitution from v2.0.0 to v2.1.0 (MINOR version bump).

**Version Change Rationale:**
This is a MINOR version bump because we're expanding an existing principle (Full Documentation) with a new requirement for Context7 MCP usage, but not making backward-incompatible changes or removing features.

**Key Changes:**

1. **Added Library Documentation (Context7 MCP) subsection** to Principle IV (Full Documentation):
   - MUST use Context7 MCP server to fetch up-to-date documentation for all third-party libraries
   - Required before implementing integrations with Better Auth, Next.js, FastAPI, SQLModel, shadcn/ui, or any external library
   - Verify current API patterns from source documentation
   - Never rely solely on LLM knowledge for library-specific implementation
   - Document library versions and reference Context7 docs in ADRs and comments
   - Use `mcp__context7__resolve-library-id` and `mcp__context7__get-library-docs` tools

2. **Added two new General Forbidden Practices:**
   - ❌ No library integration without Context7 documentation verification
   - ❌ No outdated API patterns (verify current library APIs via Context7)

3. **Updated Sync Impact Report** with new follow-up TODOs:
   - Create Tier 1 Phase 2 skills with Context7 integration
   - Configure Better Auth using Context7 docs

**Rationale:**
Context7 MCP ensures we always use current, accurate library documentation instead of potentially outdated LLM knowledge. This is critical for Phase 2 where we're integrating multiple actively-maintained libraries (Better Auth, Next.js 16+, FastAPI, SQLModel, shadcn/ui). Using Context7 will prevent API mismatches, deprecated pattern usage, and implementation errors.

**Benefits:**
- ✅ Always use current library APIs
- ✅ Avoid deprecated patterns
- ✅ Reduce implementation errors
- ✅ Better library version compatibility
- ✅ Proper documentation of library usage in ADRs

**Next Steps:**
Moving to Option 2: Create Tier 1 Phase 2 skills with Context7 integration built-in.

## Outcome

- ✅ Impact: Constitution v2.1.0 with Context7 MCP mandate
- 🧪 Tests: N/A (constitution document)
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Create Tier 1 skills (spec-generator, plan-generator, auth-integrator, api-builder)
- 🧠 Reflection: Context7 integration in constitution ensures all Phase 2 skills and implementations will use current, accurate library documentation. This prevents technical debt from outdated patterns.

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): PASS - Constitution properly versioned, Context7 requirement clearly specified with tool references
- Prompt variant (if applicable): Standard constitution update workflow
- Next experiment (smallest change to try): Create first skill (phase2-spec-generator) with Context7 integration
