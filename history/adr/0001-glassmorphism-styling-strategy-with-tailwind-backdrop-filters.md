# ADR-0001: Glassmorphism Styling Strategy with Tailwind Backdrop Filters

> **Scope**: Document decision clusters, not individual technology choices. Group related decisions that work together (e.g., "Frontend Stack" not separate ADRs for framework, styling, deployment).

- **Status:** Accepted
- **Date:** 2025-12-29
- **Feature:** 001-ps2-fullstack-web-foundation (Landing Page)
- **Context:** The Task-Flow landing page requires a modern, visually appealing aesthetic to attract users and convey professionalism. Glassmorphism (translucent, blurred glass-like UI elements) has emerged as a contemporary design trend that aligns with our brand identity goal of a "Great Modern Reliable and Attractive fast Landing Page." We must decide how to implement glassmorphism effects across landing page components (HeroSection, BentoGrid, FeatureCard, Navbar) while maintaining performance, browser compatibility, and code maintainability within our existing Tailwind CSS + Next.js 16 stack.

<!-- Significance checklist (ALL must be true to justify this ADR)
     1) Impact: Long-term consequence for architecture/platform/security?
        ✅ Yes - Establishes visual design patterns for all landing page components, impacts browser support matrix, affects performance on lower-end devices, and sets precedent for future UI styling approaches.
     2) Alternatives: Multiple viable options considered with tradeoffs?
        ✅ Yes - Tailwind backdrop-filter utilities vs. custom CSS with @supports vs. CSS-in-JS solutions vs. pre-built glassmorphism libraries.
     3) Scope: Cross-cutting concern (not an isolated detail)?
        ✅ Yes - Affects all landing page components, requires Tailwind configuration changes, impacts browser compatibility testing, and influences component API design (e.g., glass effect props).
-->

## Decision

We will implement glassmorphism effects using **Tailwind CSS `backdrop-filter` utilities** as the primary styling approach for the Task-Flow landing page.

**Implementation Details:**
- **Core Utilities**: Use Tailwind's built-in `backdrop-blur-{size}` (e.g., `backdrop-blur-md`, `backdrop-blur-lg`) for blur effects
- **Transparency Layers**: Combine with Tailwind opacity utilities like `bg-white/10` (10% opacity white) and `border-white/20` for translucent backgrounds and borders
- **Responsive Variants**: Apply glassmorphism conditionally using responsive prefixes (`sm:`, `md:`, `lg:`) to reduce effects on smaller screens if performance is impacted
- **Tailwind Configuration**: Extend `tailwind.config.ts` with custom backdrop-blur values if default sizes (sm, md, lg, xl, 2xl, 3xl) are insufficient
- **Browser Fallbacks**: Provide graceful degradation for unsupported browsers using Tailwind's `@supports` directive or conditional class application
- **Component Pattern**: Establish reusable class combinations (e.g., `glass-card`, `glass-nav`) as Tailwind `@layer components` for consistency

**Example Usage:**
```tsx
// HeroSection.tsx
<div className="backdrop-blur-lg bg-white/10 border border-white/20 rounded-2xl shadow-2xl">
  {/* Hero content */}
</div>
```

## Consequences

### Positive

1. **Zero Additional Dependencies**: Leverages existing Tailwind CSS infrastructure without introducing new libraries or build complexity
2. **Consistent Utility-First Approach**: Aligns perfectly with the project's Tailwind-based styling strategy, reducing context switching for developers
3. **Excellent Developer Experience**: Tailwind's IntelliSense, class sorting, and purging work seamlessly with backdrop utilities
4. **Performance Optimization**: Tailwind's PurgeCSS automatically removes unused backdrop utilities, keeping bundle size minimal
5. **Easy Maintenance**: Changes to glassmorphism effects require only updating Tailwind classes, no custom CSS files to manage
6. **Responsive by Default**: Tailwind's responsive prefixes make it trivial to adjust glassmorphism intensity across breakpoints
7. **Hardware Acceleration**: `backdrop-filter` is GPU-accelerated in modern browsers, ensuring smooth animations when combined with Framer Motion

### Negative

1. **Browser Compatibility Constraints**: `backdrop-filter` requires modern browsers (Chrome 76+, Safari 9+, Firefox 103+). IE11 and older browsers will not display glassmorphism effects, requiring fallback styles
2. **Performance on Low-End Devices**: Backdrop blur is computationally expensive on older mobile devices and can cause jank during animations if overused
3. **Accessibility Considerations**: Heavy blur combined with low-contrast text can fail WCAG 2.1 AA contrast ratios (≥4.5:1). Requires careful color contrast testing
4. **Limited Customization**: Tailwind's default backdrop-blur scale (sm to 3xl) may not provide granular control compared to custom CSS `blur(10px)` values
5. **Debugging Difficulty**: Stacked backdrop effects (e.g., nested glassmorphism cards) can create unexpected visual artifacts that are hard to debug via DevTools
6. **Vendor Prefix Management**: Older browsers may require `-webkit-backdrop-filter` prefixes, though Tailwind + Autoprefixer handle this automatically

## Alternatives Considered

### Alternative 1: Custom CSS with @supports Detection
**Approach**: Write custom CSS classes with `@supports (backdrop-filter: blur(10px))` to provide fallbacks.

**Pros**:
- Fine-grained control over blur pixel values (e.g., `blur(8px)`, `blur(15px)`)
- Explicit fallback styles for unsupported browsers
- No dependency on Tailwind's backdrop utilities

**Cons**:
- Breaks utility-first consistency, requiring CSS files alongside Tailwind
- Manual prefixing for `-webkit-backdrop-filter` (unless using PostCSS plugins)
- No automatic purging; unused custom CSS remains in bundle
- Harder to maintain as effects evolve across components

**Why Rejected**: Introduces CSS file sprawl and deviates from the project's Tailwind-first philosophy without providing significant benefits over Tailwind's built-in utilities.

### Alternative 2: CSS-in-JS with styled-components or Emotion
**Approach**: Use `styled-components` or `emotion` to define glassmorphism effects with JavaScript template literals.

**Pros**:
- Full control over CSS properties via JavaScript
- Dynamic styling based on component props (e.g., `blurIntensity={10}`)
- Scoped styles prevent global CSS collisions

**Cons**:
- Adds 30-50KB to bundle size (styled-components runtime)
- Runtime CSS generation impacts performance (vs. Tailwind's compile-time CSS)
- Context switching between Tailwind (for layout) and CSS-in-JS (for glassmorphism)
- Hydration overhead for server-rendered components

**Why Rejected**: Violates the "zero additional dependencies" goal and introduces runtime performance overhead inconsistent with the landing page's < 2s load time requirement.

### Alternative 3: Pre-built Glassmorphism Library (e.g., glassmorphism-ui)
**Approach**: Use a third-party library like `glassmorphism-ui` or similar that provides pre-made glassmorphism components.

**Pros**:
- Ready-made components with tested glassmorphism effects
- Consistent API across components

**Cons**:
- External dependency with maintenance risk (library may become unmaintained)
- Limited customization to match Task-Flow brand identity
- Bloat from unused library components
- Potential conflicts with Tailwind's utility classes

**Why Rejected**: Introduces unnecessary abstraction and dependency risk for a styling pattern that can be achieved with 2-3 Tailwind utility classes.

### Alternative 4: SVG Filters for Glassmorphism
**Approach**: Use SVG `<feGaussianBlur>` filters applied via CSS `filter: url(#blur-filter)`.

**Pros**:
- Better browser support (works in IE10+ with fallbacks)
- Precise control over blur radius and color matrix

**Cons**:
- Requires inline SVG in HTML, increasing markup complexity
- Performance worse than `backdrop-filter` on modern browsers
- Difficult to integrate with Tailwind's utility-first approach
- Harder to debug and maintain

**Why Rejected**: Overengineered solution for a use case where modern browser support (95%+ via caniuse.com) is acceptable with graceful degradation.

## References

- Feature Spec: `specs/001-ps2-fullstack-web-foundation/spec.md` (User Story 8, FR-091: "Landing page MUST implement glassmorphism design aesthetic")
- Implementation Plan: `specs/001-ps2-fullstack-web-foundation/plan.md` (lines 1470, 1517: Tailwind CSS glassmorphism implementation)
- Related ADRs: ADR-004 (Monorepo Structure) - ensures Tailwind config is shared across frontend workspace
- Tailwind Backdrop Filter Docs: https://tailwindcss.com/docs/backdrop-blur
- Browser Compatibility: https://caniuse.com/css-backdrop-filter (95.8% global support as of Dec 2025)
- WCAG 2.1 Contrast Guidelines: https://www.w3.org/WAI/WCAG21/Understanding/contrast-minimum.html
