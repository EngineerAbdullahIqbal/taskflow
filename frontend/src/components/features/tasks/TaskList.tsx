/**
 * TaskList Component (T068)
 *
 * Displays paginated list of tasks with:
 * - Loading skeleton states
 * - Empty state with icon and CTA
 * - Staggered FadeIn animations
 * - Pagination controls
 */

'use client';

import { useState } from 'react';
import { TaskItem } from './TaskItem';
import { Skeleton } from '@/components/ui/skeleton';
import { Button } from '@/components/ui/button';
import { useTasks } from '@/hooks/useTasks';
import { useCategories } from '@/hooks/useCategories';
import { Inbox, ChevronLeft, ChevronRight } from 'lucide-react';
import { motion } from 'framer-motion';

interface TaskListProps {
  onCreateTask?: () => void;
}

export function TaskList({ onCreateTask }: TaskListProps) {
  const [page, setPage] = useState(1);
  const { tasks, total, pageSize, isLoading, toggleCompletion } = useTasks({ page, pageSize: 20 });
  const { categories } = useCategories();

  const totalPages = Math.ceil(total / pageSize);

  // Build category lookup map
  const categoryMap = new Map(categories.map(cat => [cat.id, cat]));

  if (isLoading) {
    return <TaskListSkeleton />;
  }

  if (tasks.length === 0) {
    return (
      <EmptyState onCreateTask={onCreateTask} />
    );
  }

  return (
    <div className="space-y-6">
      {/* Task Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {tasks.map((task, index) => (
          <TaskItem
            key={task.id}
            task={task}
            category={task.category_id ? categoryMap.get(task.category_id) : undefined}
            onToggleComplete={toggleCompletion}
            delay={index * 0.05}
          />
        ))}
      </div>

      {/* Pagination */}
      {totalPages > 1 && (
        <div className="flex items-center justify-between pt-4">
          <p className="text-sm text-zinc-400">
            Showing {(page - 1) * pageSize + 1} - {Math.min(page * pageSize, total)} of {total} tasks
          </p>

          <div className="flex gap-2">
            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage(p => Math.max(1, p - 1))}
              disabled={page === 1}
              className="bg-zinc-800/50 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100 disabled:opacity-50"
            >
              <ChevronLeft className="w-4 h-4 mr-1" />
              Previous
            </Button>

            <div className="flex items-center gap-1 px-3 text-sm text-zinc-300">
              Page {page} of {totalPages}
            </div>

            <Button
              variant="outline"
              size="sm"
              onClick={() => setPage(p => Math.min(totalPages, p + 1))}
              disabled={page === totalPages}
              className="bg-zinc-800/50 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100 disabled:opacity-50"
            >
              Next
              <ChevronRight className="w-4 h-4 ml-1" />
            </Button>
          </div>
        </div>
      )}
    </div>
  );
}

/**
 * Loading skeleton for task list
 */
function TaskListSkeleton() {
  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
      {[...Array(6)].map((_, i) => (
        <div
          key={i}
          className="p-6 rounded-lg bg-zinc-900/50 backdrop-blur-md border border-white/10 space-y-3"
        >
          <Skeleton className="h-6 w-3/4 bg-zinc-800" />
          <div className="flex gap-2">
            <Skeleton className="h-5 w-16 bg-zinc-800" />
            <Skeleton className="h-5 w-20 bg-zinc-800" />
          </div>
          <Skeleton className="h-16 w-full bg-zinc-800" />
          <Skeleton className="h-4 w-32 bg-zinc-800" />
        </div>
      ))}
    </div>
  );
}

/**
 * Empty state with encouragement and CTA
 */
function EmptyState({ onCreateTask }: { onCreateTask?: () => void }) {
  return (
    <motion.div
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.4 }}
      className="flex flex-col items-center justify-center py-20 px-4"
    >
      <div className="w-20 h-20 mb-6 rounded-full bg-zinc-800/50 flex items-center justify-center">
        <Inbox className="w-10 h-10 text-zinc-500" />
      </div>

      <h3 className="text-2xl font-bold text-zinc-200 mb-2">
        No tasks yet
      </h3>

      <p className="text-zinc-400 text-center max-w-md mb-6">
        You haven't created any tasks. Start building your productivity system by creating your first task.
      </p>

      {onCreateTask && (
        <Button
          onClick={onCreateTask}
          className="bg-blue-500 hover:bg-blue-600 text-white"
        >
          Create Your First Task
        </Button>
      )}
    </motion.div>
  );
}
