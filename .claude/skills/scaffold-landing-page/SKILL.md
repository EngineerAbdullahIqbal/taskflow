---
name: scaffold-landing-page
description: Generate high-conversion SaaS landing pages with Next.js 16, featuring hero sections, bento grid layouts, and glassmorphism design. Use when creating marketing pages, product landing pages, or SaaS homepages. Triggers on "create landing page", "scaffold landing page", "build landing page", "generate SaaS landing", or "landing page for [product]".
---

# Scaffold Landing Page

## Overview

Instantly generate production-ready SaaS landing pages with modern design patterns:
- **Hero Section:** Large typography, dual CTAs, gradient text
- **Bento Grid:** Asymmetric feature showcase with glassmorphism cards
- **Sticky Navbar:** Transparent with backdrop blur
- **Mobile-First:** Fully responsive from 375px to 4K displays

## Workflow

### Step 1: Gather Requirements

Ask the user for:

**Required Inputs:**
1. **product_name** - SaaS product name (e.g., "TaskFlow", "Acme Analytics")
2. **value_proposition** - Main headline (e.g., "Ship features faster with AI-powered development")
3. **features_list** - Array of 3-6 features, each with:
   - `title` (string) - Feature name
   - `description` (string) - 1-2 sentence explanation
   - `icon` (string) - Lucide icon name (e.g., "Zap", "Shield", "Users")

**Optional Inputs:**
4. **subtext** - Hero supporting text (defaults to expanded value prop)
5. **grid_pattern** - Bento grid layout: "hero", "balanced", "spotlight", "magazine" (see references/bento-grid-patterns.md)

**Example Request Format:**
```
User: "Create a landing page for TaskFlow"
Response: "I'll create a landing page for TaskFlow. I need a few details:
1. What's your main value proposition? (e.g., 'Organize your life with smart task management')
2. List 3-6 key features with descriptions and icons"
```

### Step 2: Load Template and References

1. **Read template:** `assets/landing-page-template.tsx`
2. **Review patterns:** `references/bento-grid-patterns.md` (if needed)
3. **Check best practices:** `references/landing-page-best-practices.md` (if needed)

### Step 3: Generate Code

**Process:**
1. Start with template from `assets/landing-page-template.tsx`
2. Replace all placeholders:
   - `{{PRODUCT_NAME}}` → user's product name
   - `{{VALUE_PROPOSITION}}` → user's headline
   - `{{SUBTEXT}}` → user's subtext or auto-generate from value prop
   - `{{FEATURE_ICONS}}` → comma-separated list of Lucide icon imports
   - `{{FEATURES}}` → Map features to JSX cards with grid areas

3. Apply bento grid pattern:
   - **3 features:** "hero" pattern (1 large, 2 small)
   - **4 features:** "balanced" pattern (2x2 grid)
   - **5 features:** "spotlight" pattern
   - **6 features:** "magazine" pattern

4. Ensure code quality:
   - All imports are valid (Button from shadcn/ui, icons from lucide-react)
   - TypeScript types are correct
   - No syntax errors
   - Mobile-first Tailwind classes
   - Glassmorphism aesthetic maintained

### Step 4: Output

Provide:
1. **Complete page.tsx file** ready to paste
2. **File path:** `app/(marketing)/page.tsx` or similar
3. **Required dependencies** (if not already installed):
   ```bash
   npx shadcn@latest add button
   npm install lucide-react
   ```
4. **Usage note:** Explain how to customize CTAs, add images, or modify grid

## Code Generation Example

**Input:**
```
product_name: "TaskFlow"
value_proposition: "Organize your life with smart task management"
features_list: [
  {title: "AI Prioritization", description: "Let AI sort your tasks by urgency", icon: "Sparkles"},
  {title: "Team Collaboration", description: "Share tasks and assign work", icon: "Users"},
  {title: "Smart Reminders", description: "Never miss a deadline", icon: "Bell"}
]
```

**Output Structure:**
```tsx
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { ArrowRight, Sparkles, Users, Bell } from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-zinc-950">
      {/* Sticky Navbar */}
      <nav className="sticky top-0 z-50 border-b border-white/10 bg-zinc-950/80 backdrop-blur-md">
        {/* ... */}
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:py-32">
        <h1 className="text-5xl md:text-6xl lg:text-7xl font-bold bg-gradient-to-r from-zinc-100 to-zinc-400 bg-clip-text text-transparent">
          Organize your life with smart task management
        </h1>
        {/* CTAs */}
      </section>

      {/* Bento Grid */}
      <section className="container mx-auto px-4 py-20">
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {/* Feature cards with proper grid areas */}
        </div>
      </section>

      {/* Bottom CTA */}
      <section className="container mx-auto px-4 py-20">
        {/* ... */}
      </section>
    </div>
  )
}
```

## Quality Checklist

Before delivering code, verify:

- [ ] Product name appears in navbar, footer, and bottom CTA
- [ ] Value proposition is in hero H1 with gradient
- [ ] Both CTAs are present (primary + secondary)
- [ ] All feature icons are imported from lucide-react
- [ ] Feature cards use glassmorphism classes
- [ ] Grid pattern matches number of features
- [ ] Mobile responsive (stacks on small screens)
- [ ] Navbar is sticky with backdrop-blur
- [ ] No TypeScript errors
- [ ] No placeholder text left in code

## Empty State Handling

If user provides no features or invalid data:

```tsx
{features.length === 0 ? (
  <div className="col-span-full text-center py-12">
    <Inbox className="h-12 w-12 mx-auto text-zinc-600 mb-4" />
    <p className="text-zinc-500">Add features to showcase your product</p>
  </div>
) : (
  // Render feature grid
)}
```

## Customization Tips

After generating the page, suggest:

1. **Add hero image/video:** Replace gradient background with product screenshot
2. **Add social proof:** Insert logos or testimonial section after hero
3. **Customize colors:** Replace `blue-600` with brand color
4. **Add animations:** Use framer-motion for scroll animations (see animation-interactions skill)
5. **Optimize metadata:** Add proper Next.js metadata for SEO

## Resources

### assets/landing-page-template.tsx
Base Next.js 16 component template with all placeholders marked `{{VARIABLE}}`.

### references/bento-grid-patterns.md
Visual diagrams and CSS Grid classes for 4 asymmetric layout patterns (hero, balanced, spotlight, magazine).

### references/landing-page-best-practices.md
Comprehensive guide on typography, CTAs, icons, colors, accessibility, and conversion optimization.
