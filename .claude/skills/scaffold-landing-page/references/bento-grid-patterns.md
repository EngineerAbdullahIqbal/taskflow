# Bento Grid Layout Patterns

Asymmetric grid layouts that create visual interest while maintaining structure.

## Pattern 1: Hero Feature (3 features)

```
┌─────────────────────┬─────────┐
│                     │    2    │
│         1           ├─────────┤
│     (2 cols)        │    3    │
└─────────────────────┴─────────┘
```

**Grid Areas:**
- Feature 1: `md:col-span-2 md:row-span-2`
- Feature 2: `md:col-span-1`
- Feature 3: `md:col-span-1`

## Pattern 2: Balanced (4 features)

```
┌───────────┬───────────┐
│     1     │     2     │
├───────────┼───────────┤
│     3     │     4     │
└───────────┴───────────┘
```

**Grid Areas:**
- All features: Default grid

## Pattern 3: Spotlight (5 features)

```
┌─────────────────────┬─────────┐
│                     │    2    │
│         1           ├─────────┤
│     (2 cols)        │    3    │
├───────────┬─────────┴─────────┤
│     4     │         5         │
└───────────┴───────────────────┘
```

**Grid Areas:**
- Feature 1: `lg:col-span-2 lg:row-span-2`
- Feature 2: `lg:col-span-1`
- Feature 3: `lg:col-span-1`
- Feature 4: `lg:col-span-1`
- Feature 5: `lg:col-span-2`

## Pattern 4: Magazine (6 features)

```
┌─────────────────────┬─────────┐
│                     │    2    │
│         1           ├─────────┤
│     (2 cols)        │    3    │
├───────────┬─────────┴─────────┤
│     4     │         5         │
├───────────┴───────────────────┤
│            6 (full)           │
└───────────────────────────────┘
```

**Grid Areas:**
- Feature 1: `lg:col-span-2 lg:row-span-2`
- Feature 2: `lg:col-span-1`
- Feature 3: `lg:col-span-1`
- Feature 4: `lg:col-span-1`
- Feature 5: `lg:col-span-2`
- Feature 6: `lg:col-span-3`

## Mobile Strategy

All patterns stack vertically on mobile (< 768px):
```tsx
className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4"
```

## Glassmorphism Card Style

```tsx
className="
  rounded-lg
  border border-white/10
  bg-zinc-900/50
  backdrop-blur-md
  p-6
  transition-all
  hover:border-white/20
  hover:bg-zinc-900/70
"
```

## Icon Container

```tsx
<div className="inline-flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600/10 mb-4">
  <Icon className="h-6 w-6 text-blue-500" />
</div>
```
