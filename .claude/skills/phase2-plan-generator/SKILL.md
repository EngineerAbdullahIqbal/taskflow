---
name: phase2-plan-generator
description: Generate implementation plans from approved Phase 2 feature specifications for TaskFlow. Use when converting approved specs into detailed implementation plans with architecture decisions, file structure, component hierarchy, API routes, database migrations, and implementation sequence. Triggers on "create plan", "generate plan", "plan implementation", or "/phase2-plan-generator". Requires existing approved specification file.
---

# Phase 2 Plan Generator

Generate detailed implementation plans from approved TaskFlow Phase 2 feature specifications.

## Overview

This skill reads an approved feature specification and generates a comprehensive implementation plan in `specs/<feature-name>/plan.md`. The plan includes architectural decisions, file structure, implementation sequence with dependencies, and ADR suggestions for significant technical choices.

**Key Feature**: Uses Context7 MCP to fetch current implementation patterns and best practices from library documentation.

## Workflow

### 1. Verify Approved Specification

Check that `specs/features/<feature-name>.md` exists and is approved. If not approved:

```
❌ Cannot create plan: Specification not approved.
Please complete spec approval first, then run /phase2-plan-generator.
```

### 2. Fetch Implementation Patterns (Context7)

Use Context7 MCP to get patterns from library documentation:

**Context7 Query Process**:
1. Use `mcp__context7__resolve-library-id` for: Next.js, FastAPI, Better Auth, SQLModel, shadcn/ui
2. Use `mcp__context7__get-library-docs` with `mode='code'` to fetch:
   - File structure recommendations
   - Integration patterns
   - Configuration requirements
3. Document findings for plan

### 3. Design Architecture

Design following constitution layered approach:

**Frontend**: `app/(auth)/` → `components/features/` → `lib/api/` → `hooks/` → `types/`

**Backend**: `routes/` → `services/` → `models/` (+ `schemas/`)

### 4. Define Implementation Sequence

Break into phases with dependencies:

1. Database Layer (no deps)
2. Backend Service (depends: Database)
3. Backend API (depends: Service)
4. Frontend Types (depends: API)
5. Frontend API Client (depends: Types + API)
6. Frontend Components (depends: API Client)
7. Frontend Routes (depends: Components)
8. E2E Tests (depends: All)

### 5. Suggest ADRs

Test for architectural significance (all 3 must be true):
- Impact: Long-term consequences?
- Alternatives: Multiple options considered?
- Scope: Cross-cutting influence?

Common ADR topics: Auth approach, State management, DB schema, API pagination, File uploads, Real-time updates

### 6. Generate plan.md

Create comprehensive plan with sections: Overview, Architecture Decisions, File Structure, Implementation Sequence (with acceptance criteria per phase), ADR Suggestions, Context7 Notes, Testing Strategy, Deployment Checklist

### 7. Validate & Report

Check completeness and constitution compliance, then inform user of next steps.

## Context7 Libraries

| Library | ID | Patterns to Fetch |
|---------|-----|-------------------|
| Next.js | `/vercel/next.js` | App Router structure, middleware |
| FastAPI | `/fastapi/fastapi` | Dependency injection, route org |
| Better Auth | `/better-auth/better-auth` | JWT plugin, protected routes |
| SQLModel | `/tiangolo/sqlmodel` | Relationships, queries |
| shadcn/ui | `/shadcn/ui` | Component composition |

## References

See `references/` for:
- `architecture-patterns.md` - Constitution architecture standards
- `implementation-sequence-examples.md` - Example sequences
- `adr-checklist.md` - When to create ADRs
