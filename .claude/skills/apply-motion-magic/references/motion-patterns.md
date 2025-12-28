# Motion API Patterns Reference

## Variants Object Pattern

Define variants **outside** the component function for performance and reusability:

```tsx
// ✅ GOOD: Outside component
const fadeIn = {
  hidden: { opacity: 0 },
  visible: { opacity: 1 }
}

export function Component() {
  return <motion.div variants={fadeIn} initial="hidden" animate="visible" />
}

// ❌ BAD: Inside component (recreated on every render)
export function Component() {
  const fadeIn = { hidden: { opacity: 0 }, visible: { opacity: 1 } }
  return <motion.div variants={fadeIn} initial="hidden" animate="visible" />
}
```

## GPU-Accelerated Properties

**Use these for 60fps performance:**
- `opacity` - Transparency
- `x`, `y` - Translation
- `scale`, `scaleX`, `scaleY` - Scaling
- `rotate`, `rotateX`, `rotateY` - Rotation

**Avoid these (cause layout reflows):**
- `top`, `left`, `right`, `bottom`
- `width`, `height`
- `margin`, `padding`

```tsx
// ✅ GOOD: GPU-accelerated
<motion.div animate={{ x: 100, scale: 1.2, opacity: 0.5 }} />

// ❌ BAD: Forces layout reflow
<motion.div animate={{ left: '100px', width: '200px' }} />
```

## Transition Configuration

### Duration
- **Quick feedback**: 150-200ms (buttons, toggles)
- **UI animations**: 300-400ms (cards, sections)
- **Page transitions**: 500ms (modals, route changes)

```tsx
const variants = {
  hidden: { opacity: 0 },
  visible: { 
    opacity: 1, 
    transition: { duration: 0.3, ease: 'easeOut' }
  }
}
```

### Easing Functions
- `easeOut` - Default, natural deceleration
- `easeInOut` - Smooth start and end
- `linear` - Constant speed (avoid for UI)
- `anticipate` - Slight overshoot (playful)

```tsx
transition={{ duration: 0.3, ease: [0.4, 0, 0.2, 1] }} // Custom cubic-bezier
```

## Stagger Pattern

Parent controls stagger timing, children just define their animation:

```tsx
const container = {
  hidden: { opacity: 0 },
  visible: {
    opacity: 1,
    transition: {
      staggerChildren: 0.1, // Delay between children
      delayChildren: 0.2,   // Delay before first child
      staggerDirection: 1   // 1 = forward, -1 = reverse
    }
  }
}

const item = {
  hidden: { opacity: 0, y: 20 },
  visible: { opacity: 1, y: 0 }
}

<motion.ul variants={container} initial="hidden" animate="visible">
  {items.map(item => (
    <motion.li key={item.id} variants={item}>
      {/* Children inherit parent's animate state */}
    </motion.li>
  ))}
</motion.ul>
```

## AnimatePresence for Exit Animations

Required for animating components when they're removed from the DOM:

```tsx
import { AnimatePresence } from 'motion/react'

const modal = {
  hidden: { opacity: 0, scale: 0.95 },
  visible: { opacity: 1, scale: 1 },
  exit: { opacity: 0, scale: 0.95 } // Exit animation
}

<AnimatePresence>
  {isOpen && (
    <motion.div
      variants={modal}
      initial="hidden"
      animate="visible"
      exit="exit" // Runs before unmounting
    >
      Modal content
    </motion.div>
  )}
</AnimatePresence>
```

**AnimatePresence modes:**
- `wait` - Exit completes before enter starts (default for single elements)
- `sync` - Exit and enter run simultaneously
- `popLayout` - Prevent layout shift during exit

```tsx
<AnimatePresence mode="wait">
  <motion.div key={selectedTab}>...</motion.div>
</AnimatePresence>
```

## Gestures

### whileHover
```tsx
<motion.button
  whileHover={{ 
    scale: 1.05, 
    backgroundColor: '#27272a' 
  }}
  transition={{ duration: 0.15 }}
>
  Hover me
</motion.button>
```

### whileTap
```tsx
<motion.button
  whileTap={{ scale: 0.95 }}
  transition={{ duration: 0.1 }}
>
  Click me
</motion.button>
```

### whileDrag
```tsx
<motion.div
  drag
  dragConstraints={{ left: 0, right: 300, top: 0, bottom: 0 }}
  whileDrag={{ scale: 1.1, cursor: 'grabbing' }}
>
  Drag me
</motion.div>
```

## Wrapping Custom Components

Use `motion.create()` to add motion to custom components:

```tsx
import { motion } from 'motion/react'
import { Button } from '@/components/ui/button'

const MotionButton = motion.create(Button)

<MotionButton whileHover={{ scale: 1.05 }}>
  Animated shadcn Button
</MotionButton>
```

## Accessibility: Respecting prefers-reduced-motion

Always check user's motion preferences:

```tsx
import { useReducedMotion } from 'motion/react'

export function Component() {
  const shouldReduceMotion = useReducedMotion()
  
  const variants = shouldReduceMotion
    ? { hidden: { opacity: 0 }, visible: { opacity: 1 } } // Only fade
    : { hidden: { opacity: 0, y: 20 }, visible: { opacity: 1, y: 0 } } // Fade + slide
  
  return <motion.div variants={variants} initial="hidden" animate="visible" />
}
```

Or use the `transition` prop:

```tsx
<motion.div
  animate={{ opacity: 1, y: 0 }}
  transition={{ 
    duration: shouldReduceMotion ? 0 : 0.3 // Instant if reduced motion
  }}
/>
```

## Layout Animations

Animate layout changes automatically:

```tsx
<motion.div layout> {/* Animates position/size changes */}
  {expanded && <p>Extra content</p>}
</motion.div>
```

**Layout props:**
- `layout` - Animates all layout changes
- `layoutId` - Shared element transitions between components

```tsx
// Card expands into modal with shared layoutId
<motion.div layoutId="card-1">
  {isExpanded ? <FullView /> : <CardView />}
</motion.div>
```

## Common Patterns

### Card Hover Effect
```tsx
const cardHover = {
  rest: { scale: 1 },
  hover: { 
    scale: 1.02, 
    y: -4,
    boxShadow: '0 10px 30px rgba(0,0,0,0.3)',
    transition: { duration: 0.2 }
  }
}

<motion.div 
  initial="rest" 
  whileHover="hover" 
  variants={cardHover}
>
  Card content
</motion.div>
```

### Page Transition
```tsx
const pageVariants = {
  initial: { opacity: 0, x: -20 },
  animate: { opacity: 1, x: 0 },
  exit: { opacity: 0, x: 20 }
}

<AnimatePresence mode="wait">
  <motion.div
    key={router.pathname}
    variants={pageVariants}
    initial="initial"
    animate="animate"
    exit="exit"
    transition={{ duration: 0.3 }}
  >
    {children}
  </motion.div>
</AnimatePresence>
```

### Skeleton Loader Pulse
```tsx
<motion.div
  className="h-4 w-32 bg-zinc-800 rounded"
  animate={{ opacity: [0.5, 1, 0.5] }}
  transition={{ 
    repeat: Infinity, 
    duration: 1.5,
    ease: 'easeInOut'
  }}
/>
```

## Performance Tips

1. **Use `will-change`** sparingly (Motion handles this automatically)
2. **Avoid animating** `box-shadow` directly - use scale + opacity instead
3. **Batch animations** with variants rather than multiple `animate` props
4. **Use `layoutId`** for shared element transitions (more performant than manual orchestration)
5. **Limit stagger count** - 20+ items may cause jank, consider virtualization

## Debugging

Enable debug mode to visualize animations:

```tsx
<motion.div
  animate={{ x: 100 }}
  onAnimationStart={() => console.log('Animation started')}
  onAnimationComplete={() => console.log('Animation complete')}
/>
```
