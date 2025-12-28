---
name: apply-motion-magic
description: Inject Motion (Framer Motion) animations into existing static React code with proper variants, gestures, and animation patterns. Use when adding animations to components, making static UI interactive, or implementing page transitions. Triggers on "add animations", "apply motion", "animate component", "add framer motion", "make it animated", or "add transitions".
---

# Apply Motion Magic

## Overview

Transform static React components into animated, interactive experiences using Motion (Framer Motion successor). Automatically inject animations with proper variants, gestures, and performance optimizations.

## Workflow

### Step 1: Analyze Static Code

Identify elements to animate:
- Containers (div, section, main)
- Interactive elements (button, a)
- Lists and grids
- Conditional content (modals, dropdowns)

### Step 2: Choose Animation Pattern

Ask user for `animation_style`:
- **FadeIn**: opacity 0 → 1 (default for most content)
- **SlideUp**: y: 20 → 0 + opacity (cards, sections)
- **StaggerChildren**: Parent + children pattern (lists, grids)
- **ScaleIn**: scale 0.95 → 1 + opacity (modals, popups)
- **Custom**: User-defined variants

### Step 3: Apply Transformations

1. **Update imports:**
   ```tsx
   import { motion, AnimatePresence } from 'motion/react'
   ```

2. **Convert elements:**
   - `div` → `motion.div`
   - `button` → `motion.button`
   - Keep all existing props and className

3. **Add variants (outside component):**
   ```tsx
   const containerVariants = {
     hidden: { opacity: 0 },
     visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
   }
   ```

4. **Add motion props:**
   - `initial="hidden"`
   - `animate="visible"`
   - `variants={variantName}`

5. **For buttons, add gestures:**
   - `whileHover={{ scale: 1.05 }}`
   - `whileTap={{ scale: 0.95 }}`

6. **For conditional content, wrap with AnimatePresence:**
   ```tsx
   <AnimatePresence>{isOpen && <motion.div />}</AnimatePresence>
   ```

### Step 4: Output

Provide:
- Refactored component code
- Variants object definitions
- Import statements
- Performance notes (GPU-accelerated properties used)

## Animation Patterns

### FadeIn
```tsx
const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { duration: 0.3 } }
}
```

### SlideUp
```tsx
const slideUp = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0, transition: { duration: 0.4 } }
}
```

### StaggerChildren
```tsx
const container = {
  hidden: { opacity: 0 },
  visible: { opacity: 1, transition: { staggerChildren: 0.1 } }
}
const item = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}
```

### ScaleIn
```tsx
const scaleIn = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1, transition: { duration: 0.3 } }
}
```

## Best Practices

- **GPU Properties Only**: Use `x`, `y`, `scale`, `opacity` (not `top`, `left`, `width`)
- **Timing**: 150-500ms for UI (300ms default)
- **Accessibility**: Respect `prefers-reduced-motion`
- **Variants Outside**: Define variants outside component for performance
- **AnimatePresence**: Required for exit animations

## Examples

See assets/ for before/after code examples:
- `assets/fade-in-example.tsx` - Basic fade in animation
- `assets/slide-up-example.tsx` - Slide up with opacity
- `assets/stagger-children-example.tsx` - List stagger pattern
- `assets/button-gestures-example.tsx` - Interactive button

For detailed Motion API patterns, see `references/motion-patterns.md`.
