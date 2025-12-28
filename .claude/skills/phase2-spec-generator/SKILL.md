---
name: phase2-spec-generator
description: Generate comprehensive Phase 2 feature specifications for TaskFlow full-stack web application. Use when creating specifications for new features that require UI/UX design, API contracts, database schema, security considerations, performance requirements, and WCAG 2.1 AA accessibility standards. Triggers on "create spec", "generate spec", "write specification", or "/phase2-spec-generator".
---

# Phase 2 Spec Generator

Generate complete feature specifications for TaskFlow Phase 2 (Full-Stack Web Application) following constitutional standards.

## Overview

This skill creates comprehensive feature specifications in `specs/features/<feature-name>.md` with all required Phase 2 sections: Product Vision, User Stories, Acceptance Criteria, UI/UX Requirements, API Contracts, Database Schema, Security Considerations, Performance Requirements, and Accessibility Standards.

**Key Feature**: Integrates Context7 MCP to verify library compatibility and fetch current API patterns before spec creation.

## Workflow

### 1. Gather Requirements

Ask the user for:
- **Feature name** (required) - kebab-case, e.g., "user-authentication", "task-dashboard"
- **Feature description** (required) - What the feature does and why it's needed
- **Target personas** (optional) - Defaults to constitution personas if not specified
- **Priority** (optional) - Critical, High, Medium, Low

If information is missing, ask targeted questions:
```
For the [feature-name] feature:
1. What problem does this solve for users?
2. Who will use this feature? (Individual Professionals, Small Teams, Students)
3. What are the key capabilities users need?
```

### 2. Verify Library Compatibility (Context7)

Before writing the spec, use Context7 MCP to verify compatibility and fetch current API patterns:

```markdown
**Libraries to verify for Phase 2:**
- Next.js (frontend framework)
- FastAPI (backend framework)
- Better Auth (authentication)
- SQLModel (ORM)
- shadcn/ui (UI components)
- Tailwind CSS (styling)
```

**Context7 Workflow:**
1. Use `mcp__context7__resolve-library-id` to find library IDs:
   ```
   - Next.js: /vercel/next.js
   - FastAPI: /fastapi/fastapi
   - Better Auth: /better-auth/better-auth
   - SQLModel: /tiangolo/sqlmodel
   ```

2. Use `mcp__context7__get-library-docs` with `mode='code'` to fetch:
   - Current API patterns for the feature type
   - Required dependencies
   - Integration examples
   - Version compatibility notes

3. Document findings in spec's "Technical Stack" section

### 3. Generate Specification

Create `specs/features/<feature-name>.md` using this structure:

```markdown
# Feature: [Feature Name]

## Product Vision

**Problem Statement**: [What user problem this solves]

**Solution Overview**: [How this feature solves it]

**Success Metrics**: [Measurable outcomes]

## User Stories

### Story 1: [Primary User Goal]
**As a** [persona]
**I want** [capability]
**So that** [benefit]

**Acceptance Criteria**:
- [ ] [Testable criterion 1]
- [ ] [Testable criterion 2]
- [ ] [Testable criterion 3]

[Repeat for 3-5 user stories]

## Technical Stack

**Frontend**:
- Next.js 16+ (App Router) - [Context7 verified version]
- shadcn/ui components - [List specific components needed]
- Tailwind CSS - [Custom utility requirements]

**Backend**:
- FastAPI routes - [Endpoint patterns from Context7]
- SQLModel models - [ORM patterns from Context7]
- Better Auth - [Auth patterns from Context7]

**Context7 Verification Notes**:
- [Library compatibility findings]
- [API pattern references]
- [Integration considerations]

## UI/UX Requirements

### Wireframes/Mockups
[Describe or link to designs]

### Component Inventory
- **[ComponentName]** - Purpose, props, states
- [List all UI components needed]

### User Flows
1. [Primary flow step-by-step]
2. [Alternative flow]
3. [Error flow]

### Responsive Design
- Mobile (< 640px): [Behavior]
- Tablet (640px - 1024px): [Behavior]
- Desktop (> 1024px): [Behavior]

### Accessibility (WCAG 2.1 AA)
- [ ] Semantic HTML with proper heading hierarchy
- [ ] Keyboard navigation (Tab, Enter, Escape)
- [ ] Screen reader labels (ARIA)
- [ ] Color contrast ≥4.5:1 for text
- [ ] Focus indicators visible
- [ ] Touch targets ≥44px × 44px

## API Contracts

### Endpoint 1: [HTTP Method] /api/[path]

**Request**:
```typescript
interface [RequestName] {
  field1: type
  field2: type
}
```

**Response (200)**:
```typescript
interface [ResponseName] {
  field1: type
  field2: type
}
```

**Error Responses**:
- `400 Bad Request`: [When and why]
- `401 Unauthorized`: [When and why]
- `404 Not Found`: [When and why]

**Authentication**: Requires JWT token in Authorization header

[Repeat for all endpoints]

## Database Schema

### Table: [table_name]

```python
class [ModelName](SQLModel, table=True):
    __tablename__ = "[table_name]"

    id: int = Field(default=None, primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    [field_name]: [type] = Field([constraints])
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Indexes**:
- `user_id` (for filtering by user)
- `[field]` (for [reason])

**Migrations**:
- Migration: `[YYYYMMDD]_create_[table_name]_table.py`
- Alembic upgrade/downgrade required

[Repeat for all tables]

## Security Considerations

### Authentication & Authorization
- [ ] All endpoints require valid JWT token
- [ ] Users can only access their own data
- [ ] Resource ownership validated

### Input Validation
- [ ] All inputs validated with Pydantic schemas
- [ ] HTML sanitized to prevent XSS
- [ ] SQL injection prevented via SQLModel

### Data Protection
- [ ] Sensitive data encrypted at rest
- [ ] HTTPS only in production
- [ ] Secure cookies (httpOnly, Secure flags)

## Performance Requirements

### Frontend
- [ ] Page load time < 2s (Lighthouse FCP)
- [ ] Largest Contentful Paint (LCP) < 2.5s
- [ ] Lighthouse Performance score ≥90
- [ ] Bundle size < 200KB (gzipped)

### Backend
- [ ] API response time < 200ms (p95) for CRUD
- [ ] Database queries optimized (indexes, no N+1)
- [ ] Pagination for list endpoints (max 100 items)

### Caching Strategy
- [Describe caching approach]

## Testing Strategy

### Unit Tests (≥85% coverage)
- [ ] Frontend: Component tests (React Testing Library)
- [ ] Backend: Service tests (pytest)
- [ ] Database: Model tests (SQLModel)

### Integration Tests
- [ ] API endpoint tests
- [ ] Database integration tests
- [ ] Authentication flow tests

### E2E Tests (Playwright)
- [ ] Critical user flow: [describe]
- [ ] Error handling flow: [describe]

## Dependencies

**New NPM Packages**:
- [package-name@version] - [purpose]

**New Python Packages**:
- [package-name==version] - [purpose]

## Deployment Considerations

- [ ] Environment variables documented
- [ ] Database migrations tested
- [ ] Rollback plan defined
- [ ] Monitoring alerts configured

## Out of Scope (Phase 2)

- [Features explicitly not included]
- [Future enhancements]

## Open Questions

1. [Question 1]
2. [Question 2]

## Approval

- [ ] Product Owner: _______________
- [ ] Tech Lead: _______________
- [ ] Date: _______________
```

### 4. Validate Specification

Before saving, check:

✅ **Completeness**:
- [ ] All sections present (Product Vision → Approval)
- [ ] At least 3 user stories with acceptance criteria
- [ ] UI/UX requirements include accessibility
- [ ] API contracts define all CRUD endpoints
- [ ] Database schema follows naming conventions
- [ ] Security considerations address auth, validation, data protection
- [ ] Performance requirements specify targets
- [ ] Testing strategy covers unit, integration, E2E

✅ **Quality**:
- [ ] User stories follow "As a [persona], I want [goal], so that [benefit]"
- [ ] Acceptance criteria are testable (use checkboxes)
- [ ] API contracts use TypeScript interfaces
- [ ] Database schema uses SQLModel patterns
- [ ] Context7 verification notes included

✅ **Constitution Compliance**:
- [ ] Aligned with Product Vision & Mission
- [ ] Follows all 6 Core Principles
- [ ] Meets all 8 Quality Gates
- [ ] No Forbidden Practices
- [ ] Library versions verified via Context7

### 5. Save Specification

Write the file to `specs/features/<feature-name>.md`

### 6. Next Steps

After spec creation, inform the user:

```
✅ Feature specification created: specs/features/[feature-name].md

**Next Steps:**
1. Review and approve the specification
2. Run `/phase2-plan-generator` to create implementation plan
3. Run `/phase2-task-breaker` to generate tasks
4. Begin implementation following TDD workflow

**Constitution Compliance:**
- ✅ Specification Gate: Ready for review
- ⏳ Remaining gates: Design, Architecture, Implementation, Security, Performance, Accessibility, Deployment
```

## Context7 Library References

Use these library IDs with Context7 MCP:

| Library | Context7 ID | When to Fetch |
|---------|-------------|---------------|
| Next.js | `/vercel/next.js` | Frontend features |
| FastAPI | `/fastapi/fastapi` | Backend API routes |
| Better Auth | `/better-auth/better-auth` | Authentication features |
| SQLModel | `/tiangolo/sqlmodel` | Database models |
| shadcn/ui | `/shadcn/ui` | UI component features |
| Tailwind CSS | `/tailwindlabs/tailwindcss` | Custom styling needs |
| React Hook Form | `/react-hook-form/react-hook-form` | Form-heavy features |
| Zod | `/colinhacks/zod` | Validation schemas |

**Fetch Mode**:
- Use `mode='code'` for API references, code examples, integration patterns
- Use `mode='info'` for conceptual guides, architecture decisions

## Common Patterns

### Authentication Feature
- Fetch: Better Auth JWT plugin, Next.js middleware, FastAPI dependencies
- Sections: Login/Signup flows, JWT handling, protected routes, session management

### CRUD Feature
- Fetch: FastAPI route patterns, SQLModel relationships, React Query/SWR
- Sections: List/Create/Update/Delete flows, pagination, filtering, sorting

### Dashboard Feature
- Fetch: Next.js data fetching, shadcn/ui charts, Tailwind responsive patterns
- Sections: Data visualization, real-time updates, responsive layouts

## References

This skill includes additional reference material in `references/`:

- `constitution-excerpt.md` - Relevant constitution requirements for specs
- `quality-gates-checklist.md` - Checklist for 8 quality gates
- `example-specs.md` - Example specifications for common features

Read these as needed during spec generation.
