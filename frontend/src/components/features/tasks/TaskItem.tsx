/**
 * TaskItem Component (T069)
 *
 * Glassmorphism card displaying a single task with:
 * - Title and truncated story
 * - Priority badge
 * - Category badge (if assigned)
 * - Schedule/Due date display
 * - FadeIn animation on mount
 */

'use client';

import { motion } from 'framer-motion';
import { PriorityIndicator } from './PriorityIndicator';
import { CategoryBadge } from './CategoryBadge';
import { Checkbox } from '@/components/ui/checkbox';
import { cn } from '@/lib/utils';
import { Calendar, Repeat } from 'lucide-react';
import type { Task } from '@/types/task';
import type { Category } from '@/types/category';

interface TaskItemProps {
  task: Task;
  category?: Category;
  onToggleComplete?: (taskId: string) => void;
  delay?: number;
}

export function TaskItem({ task, category, onToggleComplete, delay = 0 }: TaskItemProps) {
  const handleToggle = () => {
    onToggleComplete?.(task.id);
  };

  // Format schedule display
  const scheduleDisplay = task.schedule?.join(', ');

  // Format due date display
  const dueDateDisplay = task.due_date
    ? formatDate(new Date(task.due_date), 'MMM d, yyyy')
    : null;

  // Truncate story to 120 characters
  const truncatedStory = task.story
    ? task.story.length > 120
      ? `${task.story.slice(0, 120)}...`
      : task.story
    : null;

  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      exit={{ opacity: 0, y: -20 }}
      transition={{ duration: 0.3, delay }}
      className={cn(
        'group relative p-6 rounded-lg',
        'bg-zinc-900/50 backdrop-blur-md border border-white/10',
        'hover:bg-zinc-900/70 hover:border-white/20',
        'transition-all duration-200',
        task.completed && 'opacity-60'
      )}
    >
      <div className="flex items-start gap-4">
        {/* Checkbox */}
        <Checkbox
          checked={task.completed}
          onCheckedChange={handleToggle}
          className="mt-1"
          aria-label={`Mark task "${task.title}" as ${task.completed ? 'incomplete' : 'complete'}`}
        />

        {/* Content */}
        <div className="flex-1 min-w-0 space-y-3">
          {/* Header: Title + Badges */}
          <div className="space-y-2">
            <h3
              className={cn(
                'text-lg font-semibold text-zinc-100',
                task.completed && 'line-through'
              )}
            >
              {task.title}
            </h3>

            <div className="flex flex-wrap items-center gap-2">
              <PriorityIndicator priority={task.priority} />

              {category && <CategoryBadge category={category} />}

              {/* Schedule/Due Date Indicator */}
              {task.schedule && task.schedule.length > 0 && (
                <div className="flex items-center gap-1.5 text-xs text-zinc-400">
                  <Repeat className="w-3.5 h-3.5" />
                  <span>{scheduleDisplay}</span>
                </div>
              )}

              {task.due_date && (
                <div className="flex items-center gap-1.5 text-xs text-zinc-400">
                  <Calendar className="w-3.5 h-3.5" />
                  <span>{dueDateDisplay}</span>
                </div>
              )}
            </div>
          </div>

          {/* Story/Description */}
          {truncatedStory && (
            <p className="text-sm text-zinc-400 leading-relaxed">
              {truncatedStory}
            </p>
          )}

          {/* Metadata */}
          <div className="text-xs text-zinc-500">
            Created {formatDate(new Date(task.created_at), 'MMM d, yyyy')}
          </div>
        </div>
      </div>

      {/* Hover Border Glow Effect */}
      <div
        className="absolute inset-0 rounded-lg opacity-0 group-hover:opacity-100 transition-opacity pointer-events-none"
        style={{
          background: 'linear-gradient(90deg, rgba(59, 130, 246, 0.1) 0%, rgba(139, 92, 246, 0.1) 100%)',
        }}
      />
    </motion.div>
  );
}

/**
 * Helper function to safely format dates
 */
function formatDate(date: Date, formatStr: string): string {
  try {
    // Simple date formatting without external library
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const month = months[date.getMonth()];
    const day = date.getDate();
    const year = date.getFullYear();

    if (formatStr === 'MMM d, yyyy') {
      return `${month} ${day}, ${year}`;
    }

    return date.toLocaleDateString();
  } catch {
    return 'Invalid date';
  }
}
