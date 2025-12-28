# ADR-003: JWT Authentication with Better Auth and FastAPI Verification

> **Scope**: Clustered decision covering authentication framework, token strategy, session management, and backend verification for Phase 2 full-stack web application.

- **Status:** Accepted
- **Date:** 2025-12-28
- **Feature:** 001-ps2-fullstack-web-foundation
- **Context:** Phase 2 requires secure multi-user authentication for web application with seamless integration between Next.js frontend (Better Auth) and FastAPI backend. Must balance security, scalability, and developer experience while minimizing database load.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security? ✅ YES - Affects entire auth flow, security model, and scalability
     2) Alternatives: Multiple viable options considered with tradeoffs? ✅ YES - Session-based, OAuth providers, Better Auth JWT
     3) Scope: Cross-cutting concern (not an isolated detail)? ✅ YES - Impacts frontend, backend, database, deployment
-->

## Decision

**Authentication Strategy: Better Auth with Stateless JWT**

Components of this integrated authentication solution:

- **Frontend Framework**: Better Auth (framework-agnostic TypeScript auth library)
- **Token Strategy**: Stateless JWT (JSON Web Tokens)
  - Access tokens: 15-minute expiration (HS256 signing)
  - Refresh tokens: 7-day expiration
  - Shared secret between Next.js and FastAPI
- **Backend Verification**: FastAPI middleware with python-jose JWT decoding
- **Password Security**: bcrypt hashing (cost factor 12)
- **Session Storage**: No database-backed sessions (stateless)

## Consequences

### Positive

- **Scalability**: Stateless JWT eliminates session database table, reducing database load and enabling horizontal scaling without session affinity
- **Performance**: No database lookup per request - JWT verification is CPU-only operation (sub-millisecond)
- **Type Safety**: Better Auth provides type-safe React hooks (`useSession()`, `signIn()`, `signOut()`)
- **Developer Experience**: Shared secret enables seamless JWT verification across stack with minimal configuration
- **Security Balance**: 15-minute access tokens limit exposure window while 7-day refresh tokens reduce re-login friction
- **Framework Agnostic**: Better Auth works with Next.js today, could support other frameworks in future phases

### Negative

- **Token Revocation Complexity**: Stateless tokens cannot be invalidated before expiration - requires workarounds:
  - Short access token expiration (15 min) limits damage window
  - Refresh token blacklist (database table) for logout/ban scenarios
  - No "instant logout" across all devices without additional infrastructure
- **Secret Management**: Shared JWT secret (`BETTER_AUTH_SECRET`) must be securely stored in environment variables and synchronized between frontend and backend deployments
- **Token Size**: JWT payload includes user claims, increasing request size vs session ID (typically 200-500 bytes vs 32 bytes)
- **Learning Curve**: Team must understand JWT lifecycle, refresh token rotation, and edge cases (token expiration during long-running operations)

## Alternatives Considered

**Alternative 1: Session-Based Authentication with Database Storage**
- Approach: Store session ID in cookie, lookup session data in PostgreSQL `sessions` table
- Pros: Instant revocation, smaller cookie size, simpler security model
- Cons: Database query per request (adds latency), session affinity required for load balancing, scaling complexity
- **Why Rejected**: Database load and latency unacceptable for Phase 2 performance targets (API < 300ms p95)

**Alternative 2: OAuth 2.0 with Third-Party Provider (Auth0/Clerk)**
- Approach: Delegate authentication to managed service, use provider's tokens
- Pros: No auth code to maintain, built-in MFA/SSO, compliance features
- Cons: Vendor lock-in, recurring cost ($25-100/month), external dependency (downtime risk), privacy concerns (user data shared with third party)
- **Why Rejected**: Phase 2 hackathon requirements specify custom authentication, cost constraints, desire for full control

**Alternative 3: Passkeys/WebAuthn with Better Auth**
- Approach: Passwordless authentication using device biometrics
- Pros: Superior UX (no passwords), phishing-resistant, modern standard
- Cons: Browser support inconsistencies (Safari issues), fallback complexity, Phase 2 scope creep
- **Why Rejected**: Deferred to Phase 3+ - email/password sufficient for MVP, passkeys can be added via Better Auth plugin later

## References

- Feature Spec: `specs/001-ps2-fullstack-web-foundation/spec.md` (FR-001 to FR-010: Authentication & Authorization)
- Implementation Plan: `specs/001-ps2-fullstack-web-foundation/plan.md` (Phase 0 Task #1: Better Auth + JWT Integration Pattern)
- Context7 Documentation: `/better-auth/better-auth` (2,333 code snippets, benchmark score 74)
- Related ADRs: ADR-002 (Monorepo Structure - shared types for auth state)
- Security Requirements: spec.md Section "Security Considerations" (bcrypt cost 12, JWT HS256, rate limiting)
