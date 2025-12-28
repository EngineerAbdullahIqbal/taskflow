/**
 * PriorityIndicator Component (T070)
 *
 * Color-coded priority badge with glassmorphism styling.
 * Uses semantic color gradients with opacity/20 backgrounds.
 */

import { Badge } from '@/components/ui/badge';
import { cn } from '@/lib/utils';
import type { Priority } from '@/types/task';

interface PriorityIndicatorProps {
  priority: Priority;
  className?: string;
}

const priorityStyles: Record<Priority, string> = {
  Low: 'bg-blue-500/20 text-blue-400 border-blue-500/30 hover:bg-blue-500/30',
  Medium: 'bg-yellow-500/20 text-yellow-400 border-yellow-500/30 hover:bg-yellow-500/30',
  High: 'bg-orange-500/20 text-orange-400 border-orange-500/30 hover:bg-orange-500/30',
  Urgent: 'bg-red-500/20 text-red-400 border-red-500/30 hover:bg-red-500/30'
};

export function PriorityIndicator({ priority, className }: PriorityIndicatorProps) {
  return (
    <Badge
      variant="outline"
      className={cn(
        'text-xs font-medium px-2 py-0.5 transition-colors',
        priorityStyles[priority],
        className
      )}
      aria-label={`Priority: ${priority}`}
    >
      {priority}
    </Badge>
  );
}
