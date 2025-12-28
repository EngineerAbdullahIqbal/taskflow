# Landing Page Best Practices

## Hero Section Requirements

### Typography Hierarchy

```tsx
// Main headline: Large, gradient, attention-grabbing
<h1 className="
  text-5xl md:text-6xl lg:text-7xl
  font-bold
  bg-gradient-to-r from-zinc-100 to-zinc-400
  bg-clip-text text-transparent
">

// Supporting text: Readable, muted
<p className="
  text-lg md:text-xl
  text-zinc-400
  mt-6 lg:mt-8
">
```

### Dual CTA Strategy

**Primary CTA:** High contrast, action-oriented
- Color: Blue/Primary brand color
- Text: "Start Free Trial", "Get Started", "Try for Free"
- Icon: Arrow right with hover animation

**Secondary CTA:** Lower contrast, exploratory
- Style: Outline button
- Text: "Watch Demo", "Learn More", "See How It Works"
- No icon or subtle play icon

```tsx
<div className="flex flex-col sm:flex-row gap-4 justify-center">
  <Button size="lg" className="group">
    Start Free Trial
    <ArrowRight className="ml-2 transition-transform group-hover:translate-x-1" />
  </Button>
  <Button size="lg" variant="outline">
    Watch Demo
  </Button>
</div>
```

## Navbar Design

### Sticky Positioning with Glassmorphism

```tsx
<nav className="
  sticky top-0 z-50
  border-b border-white/10
  bg-zinc-950/80
  backdrop-blur-md
">
```

### Content Hierarchy
1. Logo/Brand (left)
2. Navigation links (center) - Optional on landing pages
3. Sign In (right)
4. Primary CTA button (right)

## Feature Grid

### Feature Card Structure

```tsx
<div className="glass-card">
  {/* Icon container */}
  <div className="icon-container">
    <Icon />
  </div>

  {/* Title */}
  <h3 className="text-xl font-semibold mb-2">
    Feature Title
  </h3>

  {/* Description */}
  <p className="text-sm text-zinc-400">
    Feature description that explains the value clearly.
  </p>
</div>
```

### Icon Selection

Use Lucide React icons that match the feature semantically:
- Zap (Performance/Speed)
- Shield (Security)
- Users (Collaboration)
- BarChart (Analytics)
- Lock (Privacy)
- Sparkles (AI/Magic)
- Layers (Integration)
- Clock (Time-saving)

## Empty State Handling

If features_list is empty or has fewer than 3 features, show helpful message:

```tsx
{features.length === 0 ? (
  <div className="col-span-full text-center py-12">
    <Inbox className="h-12 w-12 mx-auto text-zinc-600 mb-4" />
    <p className="text-zinc-500">
      Add features to showcase your product's capabilities
    </p>
  </div>
) : (
  // Feature grid
)}
```

## Responsive Breakpoints

```
Mobile:  < 768px  (1 column, stacked layout)
Tablet:  768px+   (2 columns)
Desktop: 1024px+  (3 columns for bento grid)
Large:   1280px+  (Same as desktop but more padding)
```

## Color Palette (Dark Mode SaaS)

```tsx
// Backgrounds
bg-zinc-950      // Page background
bg-zinc-900/50   // Glass panels (semi-transparent)
bg-zinc-900      // Solid panels

// Text
text-zinc-100    // Primary text
text-zinc-400    // Secondary text
text-zinc-500    // Muted text

// Borders
border-white/10  // Subtle borders
border-white/20  // Hover borders

// Accents
bg-blue-600      // Primary CTAs
bg-blue-600/10   // Icon backgrounds
```

## Conversion Optimization

1. **Above-the-fold CTA:** Primary CTA visible without scrolling
2. **Social Proof:** Add "Join 10,000+ teams" if applicable
3. **Clear Value Prop:** What problem does it solve? (1-2 sentences max)
4. **Feature Hierarchy:** Most important feature gets larger grid space
5. **Bottom CTA:** Repeat primary CTA after features
6. **Trust Signals:** Logos, testimonials, or security badges (if applicable)

## Accessibility

```tsx
// Semantic HTML
<nav>, <main>, <section>, <footer>

// ARIA labels for icon-only buttons
<Button aria-label="Sign up for free trial">

// Focus states (automatic with shadcn/ui)
// Keyboard navigation support
```

## Performance

- **Use Next.js Image component** for hero images (if added)
- **Lazy load** below-the-fold sections
- **Optimize fonts** with next/font
- **Minimize JavaScript** - Use Server Components by default
