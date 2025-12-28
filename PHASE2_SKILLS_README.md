# Phase 2 Development Skills

> **Automated spec, plan, and implementation generation for TaskFlow Phase 2 full-stack web application**

This repository includes 4 specialized Claude Code skills that automate the creation of specifications, implementation plans, authentication integration, and API development for TaskFlow Phase 2.

## 🎯 Overview

All skills enforce **Context7 MCP integration** to verify current library documentation and best practices before implementation.

### Available Skills

| Skill | Purpose | Triggers | Output |
|-------|---------|----------|--------|
| **phase2-spec-generator** | Create feature specifications | `/phase2-spec-generator`, "create spec", "write specification" | `specs/features/<feature-name>.md` |
| **phase2-plan-generator** | Generate implementation plans | `/phase2-plan-generator`, "create plan", "plan implementation" | `specs/<feature-name>/plan.md` |
| **phase2-auth-integrator** | Integrate Better Auth + JWT | `/phase2-auth-integrator`, "integrate auth", "setup authentication" | Auth routes, middleware, models, tests |
| **phase2-api-builder** | Build FastAPI CRUD APIs | `/phase2-api-builder`, "build api", "create api", "generate routes" | Models, schemas, services, routes, tests |

---

## 🚀 Quick Start

### 1. Verify Skills Are Installed

After restarting Claude Code, the skills should be available. Verify by typing:

```bash
/phase2-spec-generator
```

If the skill is recognized, you'll enter the specification generation workflow.

### 2. Complete Workflow Example

**Scenario**: Build a user authentication feature

```bash
# Step 1: Create specification
/phase2-spec-generator
# Input: "user authentication with signup, login, logout, JWT tokens"
# Output: specs/features/user-authentication.md

# Step 2: Generate implementation plan
/phase2-plan-generator
# Input: "user-authentication"
# Output: specs/user-authentication/plan.md

# Step 3: Integrate authentication
/phase2-auth-integrator
# Generates: Auth routes, middleware, User model, login/signup forms, protected routes, tests

# Step 4: Build related APIs (e.g., user profile API)
/phase2-api-builder
# Generates: User profile CRUD endpoints with service layer and tests
```

---

## 📚 Skill Details

### 1. phase2-spec-generator

**Purpose**: Generate comprehensive, constitution-compliant feature specifications.

**Workflow**:
1. Gather feature requirements (user stories, acceptance criteria)
2. **Context7 Verification**: Fetch current library docs for tech stack
3. Generate specification with:
   - Product vision
   - User stories with acceptance criteria
   - Technical stack (verified via Context7)
   - UI/UX requirements (WCAG 2.1 AA)
   - API contracts (TypeScript interfaces)
   - Database schema (SQLModel)
   - Security considerations
   - Performance requirements (Lighthouse ≥90)
   - Testing strategy (≥85% coverage)
   - 8 Quality gates checklist
4. Save to `specs/features/<feature-name>.md`
5. Validate completeness

**Context7 Libraries Used**:
- Next.js (`/vercel/next.js`)
- FastAPI (`/fastapi/fastapi`)
- Better Auth (`/better-auth/better-auth`)
- SQLModel (`/tiangolo/sqlmodel`)
- shadcn/ui (`/shadcn/ui`)

**Example**:
```
User: /phase2-spec-generator
Claude: What feature would you like to specify?
User: Task dashboard with filtering (all/pending/completed) and sorting (date/title)
Claude: [Fetches Context7 docs, generates complete spec]
Output: specs/features/task-dashboard.md
```

**References**:
- `constitution-excerpt.md` - Constitution standards
- `quality-gates-checklist.md` - 8 quality gates
- `example-specs.md` - Template examples

---

### 2. phase2-plan-generator

**Purpose**: Convert approved specifications into detailed implementation plans.

**Workflow**:
1. Verify approved specification exists
2. **Context7 Patterns**: Fetch implementation patterns from library docs
3. Design architecture (layered approach):
   - Frontend: `app/(auth)/` → `components/features/` → `lib/api/` → `hooks/` → `types/`
   - Backend: `routes/` → `services/` → `models/`
4. Define implementation sequence with dependencies:
   1. Database Layer (no deps)
   2. Backend Service (depends: Database)
   3. Backend API (depends: Service)
   4. Frontend Types (depends: API)
   5. Frontend API Client (depends: Types + API)
   6. Frontend Components (depends: API Client)
   7. Frontend Routes (depends: Components)
   8. E2E Tests (depends: All)
5. Suggest ADRs for architectural decisions
6. Generate `specs/<feature-name>/plan.md`
7. Validate completeness

**ADR Suggestion Criteria** (all 3 must be true):
- **Impact**: Long-term consequences?
- **Alternatives**: Multiple options considered?
- **Scope**: Cross-cutting influence?

**Example**:
```
User: /phase2-plan-generator
Claude: Which approved spec should I plan?
User: user-authentication
Claude: [Fetches Context7 patterns, designs architecture, generates plan]
Output: specs/user-authentication/plan.md
ADR Suggestion: "📋 JWT vs Session-based auth detected. Document? Run `/sp.adr jwt-strategy`"
```

**References**:
- `adr-checklist.md` - When to create ADRs

---

### 3. phase2-auth-integrator

**Purpose**: Integrate Better Auth with JWT authentication into TaskFlow.

**Workflow**:
1. Verify spec includes auth requirements
2. **Context7 Docs**: Fetch Better Auth JWT plugin documentation
3. **Backend Integration** (FastAPI):
   - Auth service (password hashing, JWT generation)
   - Auth routes (`/api/auth/signup`, `/login`, `/logout`, `/refresh`)
   - Auth middleware (JWT verification, protected routes)
4. **Database Models** (SQLModel):
   - User model with `password_hash` (bcrypt cost factor 12)
   - Migration: `create_users_table.py`
5. **Frontend Integration** (Next.js):
   - Auth context (Better Auth React hooks)
   - Auth API client (type-safe)
   - Auth components (LoginForm, SignupForm, ProtectedRoute)
   - Auth routes (`/login`, `/signup`)
6. **Environment Configuration**:
   - `.env.example` with `BETTER_AUTH_SECRET`, token expiration settings
7. **Testing**:
   - Backend tests (service, routes, middleware)
   - Frontend tests (form validation, API client)
   - E2E tests (signup → login → protected route flow)
8. Validate implementation

**Security Standards**:
- Passwords hashed with bcrypt (cost factor 12)
- JWT tokens signed with HS256 + env secret
- Session expires: 15 minutes (access), 7 days (refresh with "remember me")
- Rate limiting: 5 failed attempts per 15 minutes

**Example**:
```
User: /phase2-auth-integrator
Claude: [Verifies spec, fetches Better Auth docs, generates all auth files]
Output:
  backend/app/services/auth_service.py
  backend/app/routes/auth.py
  backend/app/middleware/auth.py
  backend/app/models/user.py
  frontend/lib/auth-context.tsx
  frontend/components/features/auth/LoginForm.tsx
  backend/tests/routes/test_auth.py
  .env.example
```

**References**:
- `auth-patterns.md` - JWT strategy, session management
- `protected-routes.md` - Middleware examples
- `password-security.md` - Hashing, validation, rate limiting

---

### 4. phase2-api-builder

**Purpose**: Generate production-ready FastAPI CRUD APIs with SQLModel.

**Workflow**:
1. Verify spec includes API contracts
2. **Context7 Docs**: Fetch FastAPI + SQLModel patterns
3. **Database Models** (SQLModel):
   - Model with proper indexes, relationships
   - Migration script
4. **Pydantic Schemas**:
   - Request schemas (input validation with `field_validator`)
   - Response schemas (output serialization)
5. **Service Layer**:
   - CRUD methods with ownership verification
   - Pagination support
6. **FastAPI Routes**:
   - `GET /api/<resource>` - List with pagination
   - `POST /api/<resource>` - Create (201)
   - `GET /api/<resource>/{id}` - Get by ID
   - `PATCH /api/<resource>/{id}` - Update
   - `DELETE /api/<resource>/{id}` - Delete (204)
   - Dependency injection (`get_current_user`, `get_session`)
7. **Tests**:
   - Service tests (CRUD operations)
   - Route tests (auth, validation, error responses)
8. Validate (≥85% coverage)

**API Error Format** (Constitution standard):
```json
{
  "detail": "Human-readable error message",
  "error_code": "MACHINE_READABLE_CODE"
}
```

**Example**:
```
User: /phase2-api-builder
Claude: What resource API should I build?
User: tasks - with title, description, completed status
Claude: [Fetches FastAPI docs, generates full API stack]
Output:
  backend/app/models/task.py
  backend/app/schemas/task.py
  backend/app/services/task_service.py
  backend/app/routes/task.py
  backend/tests/services/test_task_service.py
  backend/tests/routes/test_task.py
  backend/app/migrations/20251228_create_tasks_table.py
```

**References**:
- `fastapi-patterns.md` - Dependency injection, error handling, pagination
- `sqlmodel-relationships.md` - One-to-many, many-to-many, optimization
- `api-error-handling.md` - Standardized error responses

---

## 🔗 Context7 MCP Integration

All skills use **Context7 MCP server** to verify current library documentation before generating code.

### How It Works

1. **Resolve Library ID**:
   ```typescript
   mcp__context7__resolve-library-id("better-auth")
   // Returns: "/better-auth/better-auth"
   ```

2. **Fetch Documentation**:
   ```typescript
   mcp__context7__get-library-docs({
     context7CompatibleLibraryID: "/better-auth/better-auth",
     mode: "code",  // 'code' for API refs, 'info' for guides
     topic: "JWT plugin"
   })
   // Returns: Current API patterns, configuration examples
   ```

3. **Document Findings**:
   All specs and plans include a "Context7 Verification Notes" section documenting library versions and patterns used.

### Why Context7?

- **Current APIs**: Ensures code uses latest library patterns, not outdated LLM knowledge
- **Version Compatibility**: Verifies feature support in specified library versions
- **Best Practices**: Fetches recommended implementation patterns from source docs
- **Constitution Compliance**: Enforced in Principle IV (Full Documentation)

---

## 📋 Quality Standards

All generated code follows **TaskFlow Constitution v2.1.0**:

### 8 Quality Gates

1. ✅ **Specification Gate** - Complete, approved spec
2. ✅ **Design Gate** - UI/UX approved, accessibility checklist
3. ✅ **Architecture Gate** - System design reviewed, security considered
4. ✅ **Implementation Gate** - Tests passing, ≥85% coverage, no lint errors
5. ✅ **Security Gate** - Auth/authz defined, input validated, OWASP reviewed
6. ✅ **Performance Gate** - Lighthouse ≥90, API <200ms (p95)
7. ✅ **Accessibility Gate** - WCAG 2.1 AA compliant
8. ✅ **Deployment Gate** - Migrations tested, rollback plan, monitoring

### Core Principles

- **TDD**: Test coverage ≥85%
- **Type Safety**: TypeScript strict mode, Python mypy --strict
- **Graceful Degradation**: Error boundaries, loading states, friendly errors
- **Full Documentation**: OpenAPI, Storybook, ADRs, **Context7 verification**
- **Evolutionary Architecture**: Layered separation, no cross-layer leakage
- **Simplicity**: YAGNI, smallest viable implementation

---

## 📦 Installation (For Sharing)

These skills are bundled as `.skill` files for easy sharing:

```bash
# Copy .skill files to another project
cp phase2-*.skill /path/to/other-project/.claude/skills/

# Or extract manually
unzip phase2-spec-generator.skill -d ~/.claude/skills/phase2-spec-generator
```

**Skill Files**:
- `phase2-spec-generator.skill` (15 KB)
- `phase2-plan-generator.skill` (2.8 KB)
- `phase2-auth-integrator.skill` (7.9 KB)
- `phase2-api-builder.skill` (12 KB)

---

## 🎓 Example: Complete Feature Implementation

### Scenario: Build "Task Categories" Feature

#### 1. Create Specification
```bash
User: /phase2-spec-generator
Claude: What feature would you like to specify?
User: Task categories - users can create custom categories (e.g., Work, Personal, Shopping)
      and assign tasks to categories. Each category has a name and color.

Claude: [Fetches Next.js, FastAPI, SQLModel docs via Context7]
        [Generates comprehensive spec with user stories, API contracts, DB schema]

Output: specs/features/task-categories.md
```

**Generated Spec Includes**:
- User stories: Create category, assign task to category, filter by category
- API contracts: `POST /api/categories`, `GET /api/categories`, `PATCH /api/tasks/{id}/category`
- DB schema: `categories` table with `user_id`, `name`, `color`; `tasks.category_id` foreign key
- UI mockups: Category selector dropdown, category badge on task cards
- Acceptance criteria: Max 20 categories per user, unique category names, color validation

#### 2. Generate Plan
```bash
User: /phase2-plan-generator
Claude: Which approved spec should I plan?
User: task-categories

Claude: [Fetches FastAPI + SQLModel implementation patterns via Context7]
        [Designs architecture following layered approach]

Output: specs/task-categories/plan.md
ADR Suggestion: "📋 Category color validation (client vs server) - Document? Run `/sp.adr category-color-validation`"
```

**Generated Plan Includes**:
- File structure:
  - `backend/app/models/category.py`
  - `backend/app/services/category_service.py`
  - `frontend/components/features/categories/CategorySelector.tsx`
- Implementation sequence (8 phases)
- Acceptance criteria per phase

#### 3. Build Category API
```bash
User: /phase2-api-builder
Claude: What resource API should I build?
User: categories - name (1-50 chars), color (hex code), belongs to user

Claude: [Generates full API stack with validation]

Output:
  backend/app/models/category.py (SQLModel with user_id FK)
  backend/app/schemas/category.py (Pydantic with hex color validator)
  backend/app/services/category_service.py (max 20 categories per user)
  backend/app/routes/category.py (CRUD routes)
  backend/tests/services/test_category_service.py
  backend/tests/routes/test_category.py
```

#### 4. Run Quality Gates
```bash
# After implementation
User: /quality-gate

Claude: Running quality gates...
        ✅ Tests passing (87% coverage)
        ✅ Type checking passed
        ✅ Linting passed
        ✅ Security scan passed
        Ready to commit!
```

---

## 🛠️ Troubleshooting

### Skills Not Appearing

**Issue**: Skills don't show up after installation.

**Solution**: Skills are loaded at session start. Restart Claude Code:
```bash
exit
claude
```

### Context7 Errors

**Issue**: `mcp__context7__resolve-library-id` fails.

**Solution**: Ensure Context7 MCP server is configured in Claude Code settings.

### Validation Errors

**Issue**: Generated code fails quality gate.

**Solution**: Check constitution requirements in `.specify/memory/constitution.md`. Skills enforce constitution standards, but edge cases may need manual fixes.

---

## 📄 License

These skills are part of the TaskFlow project and follow the project's license.

---

## 🤝 Contributing

To improve or extend these skills:

1. Edit skill files in `.claude/skills/<skill-name>/SKILL.md`
2. Update reference files in `.claude/skills/<skill-name>/references/`
3. Test changes by restarting Claude Code
4. Re-package using:
   ```bash
   python3 ~/.claude/plugins/cache/anthropic-agent-skills/document-skills/*/skills/skill-creator/scripts/package_skill.py .claude/skills/<skill-name>
   ```

---

**Generated with TaskFlow Constitution v2.1.0 • Powered by Claude Code + Context7 MCP** 🚀
