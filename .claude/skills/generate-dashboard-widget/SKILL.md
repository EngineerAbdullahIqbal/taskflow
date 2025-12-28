---
name: generate-dashboard-widget
description: Generate beautiful dashboard widgets (StatCard, List, Chart) with glassmorphism design, empty states, and skeleton loaders. Use when creating dashboard components, data visualization widgets, metric cards, or analytics panels. Triggers on "create dashboard widget", "generate widget", "build stat card", "create chart", or "dashboard for [metric]".
---

# Generate Dashboard Widget

## Overview

Create production-ready dashboard widgets in three types:
- **StatCard:** Display key metrics with trend indicators  
- **List:** Show recent items or activity feeds
- **Chart:** Data visualization

All widgets include glassmorphism, empty states, skeleton loaders, TypeScript typing, and mobile responsiveness.

## Workflow

### Step 1: Identify Type & Data

Ask user for widget_type ("StatCard"/"List"/"Chart"), title, and data structure.

### Step 2: Generate Component

Use glass card base:
```tsx
<Card className="bg-zinc-900/50 border-white/10 backdrop-blur-md">
  <CardHeader><CardTitle>{title}</CardTitle></CardHeader>
  <CardContent>{/* content */}</CardContent>
</Card>
```

### Step 3: Add States

Empty state: Lucide icon + message
Loading: Skeleton with pulsing animation

### Step 4: Output

Component + Skeleton + TypeScript interfaces + Usage example

## Widget Specs

**StatCard:** Metrics with trends (text-3xl values, color-coded change)
**List:** Scrollable items (max-h-[400px], dividers)  
**Chart:** Data viz (suggest Recharts, responsive container)

## Typography

- Title: `text-lg font-semibold text-foreground`
- Labels: `text-xs text-muted-foreground`
- Values: `text-3xl font-bold text-foreground`
- Trend+: `text-green-500` / Trend-: `text-red-500`
