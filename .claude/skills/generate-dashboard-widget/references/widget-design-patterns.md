# Widget Design Patterns

## Empty States

Use semantic Lucide icons:
- Inbox: Lists/feeds
- BarChart3: Charts/analytics
- AlertCircle: Errors
- Info: Informational

## Loading Patterns

Skeleton: Pulsing gray boxes matching content structure
```tsx
<div className="h-4 w-24 bg-zinc-800 animate-pulse rounded" />
```

## Color Coding

- Positive trends: `text-green-500`
- Negative trends: `text-red-500`
- Neutral/muted: `text-zinc-400` or `text-muted-foreground`
