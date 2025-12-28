# ADR Decision Checklist

## When to Create an ADR

All 3 criteria must be met:

1. **Impact**: Long-term consequences (framework, data model, API, security, platform)
2. **Alternatives**: Multiple viable options were considered
3. **Scope**: Cross-cutting and influences system design

## Common ADR Topics in Phase 2

- Authentication approach (session vs JWT, token refresh strategy)
- State management (Context vs Zustand vs Redux)
- Database schema design (normalization decisions)
- API pagination (offset vs cursor)
- File uploads (direct vs presigned URL vs cloud storage)
- Real-time updates (polling vs WebSockets vs SSE)
- Caching strategy (client vs server, invalidation approach)
- Error tracking (Sentry vs alternatives)

## ADR Template

```markdown
# ADR [Number]: [Title]

**Status**: Proposed | Accepted | Deprecated | Superseded

**Date**: YYYY-MM-DD

## Context

[What is the issue motivating this decision?]

## Decision

[What is the change being proposed?]

## Alternatives Considered

1. **[Alternative 1]**: [Pros/Cons]
2. **[Alternative 2]**: [Pros/Cons]

## Consequences

**Positive**:
- [Benefit 1]

**Negative**:
- [Tradeoff 1]

**Risks**:
- [Risk 1]

## References

- [Link to spec]
- [Link to library documentation]
```

## Suggestion Format

```markdown
📋 Architectural decision detected: [Brief Description]

**Decision**: [What was chosen]
**Alternatives Considered**: [What else was evaluated]
**Impact**: [Why this matters long-term]

Document reasoning and tradeoffs? Run `/sp.adr [decision-title]`
```
