# ADR-004: Monorepo Structure with Independent Frontend and Backend Workspaces

> **Scope**: Clustered decision covering repository organization, workspace separation, package management strategy, and type sharing approach for Phase 2 full-stack development.

- **Status:** Accepted
- **Date:** 2025-12-28
- **Feature:** 001-ps2-fullstack-web-foundation
- **Context:** Phase 2 transitions from Phase 1 console app to full-stack web application requiring both Next.js frontend and FastAPI backend. Need to balance code sharing (especially TypeScript types for API contracts) with workspace independence and deployment flexibility.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Determines project structure, CI/CD workflow, deployment strategy
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Polyrepo, monorepo unified, monorepo independent
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Affects all engineers, all features, all deployments
-->

## Decision

**Monorepo with Independent Workspaces**

Structure and tooling:

- **Repository Layout**:
  - `frontend/` - Next.js 16+ application (TypeScript, pnpm)
  - `backend/` - FastAPI application (Python 3.13+, UV package manager)
  - `shared/` - Shared TypeScript types only (minimal, consumed by frontend)
  - `.github/workflows/` - Separate CI pipelines for frontend and backend

- **Package Management**:
  - Frontend: **pnpm** (fast, disk-efficient, strict dependency resolution)
  - Backend: **UV** (modern Python package manager, Cargo-inspired)
  - No workspace-level package manager (workspaces are independent)

- **Type Sharing Strategy**:
  - API contract types defined in `shared/types/api.ts`
  - Frontend imports from `../shared/types/api`
  - Backend generates OpenAPI schemas, frontend consumes via codegen (future)
  - **Discipline required**: No frontend → backend imports, no backend → frontend imports

- **Deployment**:
  - Frontend: Vercel (serverless, automatic previews)
  - Backend: Render or Railway (container-based, background worker support)
  - Independent deployment pipelines

## Consequences

### Positive

- **Type Safety Across Stack**: Shared API types eliminate contract drift - frontend and backend use same `TaskResponse`, `UserResponse` interfaces
- **Atomic Commits**: Single commit can update both frontend and backend for cross-stack features (e.g., add new task field → update API + UI in one PR)
- **Simplified CI/CD**: Single repository for GitHub Actions workflows, easier branch management, no cross-repo synchronization
- **Developer Experience**: Clone once, work on full feature (API + UI) without switching repos
- **Easier Feature Development**: No need for coordinating PRs across multiple repositories, reviewing full feature in one place
- **Constitution Compliance**: Aligns with TaskFlow Constitution "Monorepo Structure Standards" section

### Negative

- **Discipline Required**: Must avoid `import from '../../backend'` in frontend code - enforced via ESLint rules and code review
- **Build Complexity**: CI must detect which workspace changed to skip unnecessary builds (GitHub Actions path filters)
- **Deployment Coordination**: Frontend and backend deploy independently - requires versioned API contracts or feature flags for breaking changes
- **Workspace Isolation**: No shared linting config or test utilities without duplication (intentional tradeoff for independence)
- **Learning Curve**: Team must understand monorepo best practices (workspace boundaries, import restrictions, deployment sequencing)

## Alternatives Considered

**Alternative 1: Separate Repositories (Polyrepo)**
- Approach: `taskflow-frontend` and `taskflow-backend` as independent GitHub repos
- Pros: Maximum isolation, independent versioning, clearer ownership boundaries
- Cons:
  - Type duplication (copy-paste `TaskResponse` between repos) or published shared package overhead
  - Cross-repo PRs for features (update backend API → wait for deploy → update frontend)
  - Two clones, two CI configs, two sets of branch management
- **Why Rejected**: Type duplication unacceptable, cross-repo PR friction slows iteration, overkill for 2-person hackathon team

**Alternative 2: Monorepo with Unified Package Manager (Turborepo/Nx)**
- Approach: Workspace-level package manager (pnpm workspaces or Nx) orchestrating frontend + backend
- Pros: Shared build cache, task dependencies, unified scripts (`npm run build:all`)
- Cons:
  - Forces same package manager for Python and Node.js (unnatural)
  - Tight coupling - backend changes trigger frontend rebuilds unnecessarily
  - Overhead for small team (Turborepo/Nx config complexity)
- **Why Rejected**: Python + Node.js don't benefit from shared workspace manager, independence preferred for deployment flexibility

**Alternative 3: Backend-Driven Monolith (FastAPI serves Next.js build)**
- Approach: FastAPI serves static Next.js build at `/`, API at `/api`
- Pros: Single deployment, simplified CORS, single URL
- Cons:
  - Loses Next.js serverless benefits (ISR, edge functions)
  - Frontend changes require backend rebuild/redeploy
  - No Vercel preview deployments
  - Mixing Python and Node.js build processes in one container
- **Why Rejected**: Sacrifices Next.js strengths, deployment inflexibility, Phase 2 hackathon suggests Vercel frontend hosting

## References

- Feature Spec: `specs/001-ps2-fullstack-web-foundation/spec.md` (Section "Deployment Requirements")
- Implementation Plan: `specs/001-ps2-fullstack-web-foundation/plan.md` (Section "Project Structure")
- TaskFlow Constitution: `.specify/memory/constitution.md` (Section "Monorepo Structure Standards")
- Related ADRs: ADR-003 (JWT Auth - shared types for auth state)
- Tooling Choices:
  - pnpm: Fast, disk-efficient package manager with strict resolution
  - UV: Modern Python package manager (https://github.com/astral-sh/uv)
