/**
 * CategoryBadge Component (T071)
 *
 * Displays category name with dynamic color indicator.
 * Color is applied as a left border accent.
 */

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { Category } from '@/types/category';

interface CategoryBadgeProps {
  category: Category;
  className?: string;
}

export function CategoryBadge({ category, className }: CategoryBadgeProps) {
  return (
    <Badge
      variant="outline"
      className={cn(
        'text-xs font-medium px-2 py-0.5 bg-zinc-800/50 text-zinc-300 border-zinc-700',
        'transition-colors hover:bg-zinc-800',
        className
      )}
      style={{
        borderLeftColor: category.color,
        borderLeftWidth: '3px'
      }}
      aria-label={`Category: ${category.name}`}
    >
      {category.name}
    </Badge>
  );
}
