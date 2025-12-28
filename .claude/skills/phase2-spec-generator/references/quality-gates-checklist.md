# Phase 2 Quality Gates Checklist

All features MUST pass these 8 gates before merge. Include relevant gates in feature specifications.

## 1. Specification Gate

**Purpose**: Ensure feature is fully specified before implementation begins.

**Checklist for Specs**:
- [ ] Feature has approved specification in `specs/features/`
- [ ] User flows documented with diagrams
- [ ] API contracts defined (request/response schemas)
- [ ] UI mockups or wireframes provided
- [ ] Database schema defined
- [ ] Security considerations documented
- [ ] Performance requirements specified
- [ ] Accessibility requirements included

**Deliverables**:
- Complete `specs/features/<feature-name>.md`
- Approval signatures from Product Owner and Tech Lead

---

## 2. Design Gate

**Purpose**: Validate UI/UX design before implementation.

**Checklist for Specs**:
- [ ] UI/UX designs approved by designer or product owner
- [ ] Component inventory complete (list of reusable components)
- [ ] Accessibility considerations documented (WCAG 2.1 AA)
- [ ] Mobile and desktop designs provided
- [ ] User flows show happy path and error paths
- [ ] Design system usage confirmed (shadcn/ui)

**Deliverables**:
- Wireframes/mockups in spec or design tool
- Component inventory in spec
- Accessibility checklist completed

---

## 3. Architecture Gate

**Purpose**: Ensure technical approach is sound before coding.

**Checklist for Specs**:
- [ ] System design reviewed (data flow, layer separation)
- [ ] Technology stack confirmed (no unapproved dependencies)
- [ ] Performance implications considered
- [ ] Security review completed
- [ ] Database schema follows conventions
- [ ] API design follows RESTful standards
- [ ] Frontend/backend integration plan clear

**Deliverables**:
- Architecture section in spec
- Data flow diagrams
- API contract definitions
- Database schema with indexes

---

## 4. Implementation Gate

**Purpose**: Validate code quality before merge.

**Checklist for Implementation** (include testing requirements in spec):
- [ ] Code review passed (minimum 1 reviewer)
- [ ] All tests passing (unit, integration, E2E)
- [ ] No linting errors (ESLint for frontend, Ruff for backend)
- [ ] Type checking passed (TypeScript, mypy --strict)
- [ ] Test coverage ≥85%
- [ ] No commented-out code
- [ ] No TODOs without issue references

**Testing Requirements in Spec**:
- Unit tests: Component tests (React Testing Library), Service tests (pytest)
- Integration tests: API endpoint tests, Database tests, Auth flow tests
- E2E tests: Critical user flows (Playwright)

---

## 5. Security Gate

**Purpose**: Prevent security vulnerabilities.

**Checklist for Specs** (Security Considerations section):
- [ ] Authentication requirements defined (JWT, Better Auth)
- [ ] Authorization rules specified (resource ownership)
- [ ] Input validation approach documented (Pydantic schemas)
- [ ] OWASP Top 10 considerations reviewed
- [ ] Sensitive data handling defined (encryption, secure cookies)
- [ ] Rate limiting requirements specified
- [ ] CORS configuration documented

**Security Checklist**:
- [ ] No known vulnerabilities (npm audit, safety check)
- [ ] Secrets not in code (environment variables)
- [ ] XSS prevention (HTML sanitization)
- [ ] SQL injection prevention (SQLModel parameterized queries)
- [ ] HTTPS only in production
- [ ] Secure cookies (httpOnly, Secure flags)

---

## 6. Performance Gate

**Purpose**: Ensure application meets performance targets.

**Checklist for Specs** (Performance Requirements section):
- [ ] Frontend performance targets defined:
  - Page load time < 2s (Lighthouse FCP)
  - Largest Contentful Paint (LCP) < 2.5s
  - Lighthouse score ≥90
  - Bundle size < 200KB (gzipped)
- [ ] Backend performance targets defined:
  - API response time < 200ms (p95) for CRUD
  - List endpoints < 300ms (p95)
  - Search queries < 500ms (p95)
- [ ] Database optimization planned:
  - Indexes on frequently queried columns
  - N+1 query prevention strategy
  - Pagination for lists (max 100 items)
- [ ] Caching strategy defined

**Performance Checklist**:
- [ ] Lighthouse score ≥90 measured on staging
- [ ] No performance regressions vs baseline
- [ ] API response times meet targets
- [ ] Database queries optimized

---

## 7. Accessibility Gate

**Purpose**: Ensure WCAG 2.1 AA compliance.

**Checklist for Specs** (UI/UX Requirements → Accessibility section):
- [ ] Semantic HTML with proper heading hierarchy
- [ ] Keyboard navigation support defined (Tab, Enter, Escape, arrows)
- [ ] Screen reader labels specified (ARIA)
- [ ] Color contrast requirements met (≥4.5:1 for text, ≥3:1 for large text)
- [ ] Focus indicators visible
- [ ] Touch targets ≥44px × 44px
- [ ] Alt text for images
- [ ] Form labels and error messages accessible

**Accessibility Checklist**:
- [ ] WCAG 2.1 AA compliance verified
- [ ] Keyboard navigation tested
- [ ] Screen reader tested (NVDA or VoiceOver)
- [ ] Color contrast verified (WebAIM checker)
- [ ] Lighthouse Accessibility score ≥90

---

## 8. Deployment Gate

**Purpose**: Ensure safe deployment to production.

**Checklist for Specs** (Deployment Considerations section):
- [ ] Environment variables documented
- [ ] Database migrations defined (Alembic scripts)
- [ ] Rollback plan specified
- [ ] Monitoring alerts planned
- [ ] Health check endpoints defined (`/health`, `/api/health`)
- [ ] Deployment sequence documented

**Deployment Checklist**:
- [ ] Successful deployment to staging
- [ ] Health check endpoints passing
- [ ] Database migrations applied successfully
- [ ] Smoke tests passed (critical flows work)
- [ ] Monitoring configured (Sentry, Vercel Analytics)
- [ ] Rollback tested

---

## Spec Template Integration

When writing specs, include sections that address these gates:

```markdown
## Testing Strategy (Gate 4)
- Unit tests: [describe]
- Integration tests: [describe]
- E2E tests: [describe]

## Security Considerations (Gate 5)
- Authentication & Authorization: [describe]
- Input Validation: [describe]
- Data Protection: [describe]

## Performance Requirements (Gate 6)
- Frontend: [targets]
- Backend: [targets]
- Caching: [strategy]

## Accessibility (WCAG 2.1 AA) (Gate 7)
- [ ] Semantic HTML
- [ ] Keyboard navigation
- [ ] Screen reader labels
- [ ] Color contrast ≥4.5:1
- [ ] Focus indicators
- [ ] Touch targets ≥44px

## Deployment Considerations (Gate 8)
- [ ] Environment variables documented
- [ ] Database migrations tested
- [ ] Rollback plan defined
- [ ] Monitoring configured
```

---

## Gate Progression

**Typical Flow**:
1. **Specification Gate** → Feature fully specified
2. **Design Gate** → UI/UX approved
3. **Architecture Gate** → Technical approach validated
4. **Implementation Gate** → Code complete, tests passing
5. **Security Gate** → No vulnerabilities
6. **Performance Gate** → Meets performance targets
7. **Accessibility Gate** → WCAG 2.1 AA compliant
8. **Deployment Gate** → Production-ready

**Key Principle**: Each gate builds on the previous. Cannot skip gates or proceed without passing.
