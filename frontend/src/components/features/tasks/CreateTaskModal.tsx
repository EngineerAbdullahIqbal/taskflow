/**
 * CreateTaskModal Component (T072)
 *
 * Modal dialog for creating new tasks with full validation.
 * Uses React Hook Form with Zod schema validation.
 * Includes ScheduleSelector and CategorySelector components.
 */

'use client';

import { useForm } from 'react-hook-form';
import { zodResolver } from '@hookform/resolvers/zod';
import { z } from 'zod';
import { motion, AnimatePresence } from 'framer-motion';
import {
  Dialog,
  DialogContent,
  DialogHeader,
  DialogTitle,
  DialogDescription,
} from '@/components/ui/dialog';
import { Button } from '@/components/ui/button';
import { Input } from '@/components/ui/input';
import { Textarea } from '@/components/ui/textarea';
import { Label } from '@/components/ui/label';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { ScheduleSelector } from './ScheduleSelector';
import { CategorySelector } from '../categories/CategorySelector';
import { useTasks } from '@/hooks/useTasks';
import { useCategories } from '@/hooks/useCategories';
import type { Priority } from '@/types/task';
import { Loader2 } from 'lucide-react';

interface CreateTaskModalProps {
  open: boolean;
  onOpenChange: (open: boolean) => void;
}

// Validation schema
const taskSchema = z.object({
  title: z.string().min(1, 'Title is required').max(200, 'Title too long'),
  story: z.string().max(2000, 'Story too long').optional(),
  priority: z.enum(['Low', 'Medium', 'High', 'Urgent']),
  schedule: z.array(z.string()).optional(),
  due_date: z.string().optional(),
  category_id: z.string().optional(),
}).refine(
  (data) => {
    // XOR validation: schedule and due_date cannot both be set
    const hasSchedule = data.schedule && data.schedule.length > 0;
    const hasDueDate = data.due_date && data.due_date.length > 0;
    return !(hasSchedule && hasDueDate);
  },
  {
    message: 'Cannot set both schedule and due date',
    path: ['schedule'],
  }
);

type TaskFormData = z.infer<typeof taskSchema>;

export function CreateTaskModal({ open, onOpenChange }: CreateTaskModalProps) {
  const { createTask, isCreating } = useTasks();
  const { categories, isLoading: categoriesLoading, createCategory, isCreating: isCategoryCreating } = useCategories();

  const {
    register,
    handleSubmit,
    formState: { errors },
    reset,
    watch,
    setValue
  } = useForm<TaskFormData>({
    resolver: zodResolver(taskSchema),
    defaultValues: {
      priority: 'Medium',
      schedule: undefined,
      due_date: undefined,
    }
  });

  const onSubmit = async (data: TaskFormData) => {
    try {
      await createTask(data);
      reset();
      onOpenChange(false);
    } catch (error) {
      // Error handling is done in the hook
      console.error('Create task error:', error);
    }
  };

  const handleCancel = () => {
    reset();
    onOpenChange(false);
  };

  const handleCreateCategory = async (name: string, color: string) => {
    const newCategory = await createCategory({ name, color });
    setValue('category_id', newCategory.id);
  };

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <AnimatePresence>
        {open && (
          <DialogContent
            className="bg-zinc-900 border-zinc-800 text-zinc-100 max-w-2xl max-h-[90vh] overflow-y-auto"
            asChild
          >
            <motion.div
              initial={{ scale: 0.95, opacity: 0 }}
              animate={{ scale: 1, opacity: 1 }}
              exit={{ scale: 0.95, opacity: 0 }}
              transition={{ duration: 0.2 }}
            >
              <DialogHeader>
                <DialogTitle className="text-2xl font-bold text-zinc-100">
                  Create New Task
                </DialogTitle>
                <DialogDescription className="text-zinc-400">
                  Create a one-time task or recurring habit. Fill in the details below.
                </DialogDescription>
              </DialogHeader>

              <form onSubmit={handleSubmit(onSubmit)} className="space-y-6 mt-6">
                {/* Title */}
                <div className="space-y-2">
                  <Label htmlFor="title" className="text-sm font-medium text-zinc-300">
                    Title *
                  </Label>
                  <Input
                    id="title"
                    {...register('title')}
                    placeholder="Enter task title"
                    className="bg-zinc-900/50 border-zinc-700 text-zinc-100 focus:border-blue-500/50"
                  />
                  {errors.title && (
                    <p className="text-sm text-red-400">{errors.title.message}</p>
                  )}
                </div>

                {/* Story */}
                <div className="space-y-2">
                  <Label htmlFor="story" className="text-sm font-medium text-zinc-300">
                    Story / Description
                  </Label>
                  <Textarea
                    id="story"
                    {...register('story')}
                    placeholder="Add details, notes, or markdown formatting..."
                    rows={4}
                    className="bg-zinc-900/50 border-zinc-700 text-zinc-100 focus:border-blue-500/50 resize-none"
                  />
                  {errors.story && (
                    <p className="text-sm text-red-400">{errors.story.message}</p>
                  )}
                </div>

                {/* Priority */}
                <div className="space-y-2">
                  <Label htmlFor="priority" className="text-sm font-medium text-zinc-300">
                    Priority *
                  </Label>
                  <Select
                    value={watch('priority')}
                    onValueChange={(value) => setValue('priority', value as Priority)}
                  >
                    <SelectTrigger className="bg-zinc-900/50 border-zinc-700 text-zinc-100">
                      <SelectValue />
                    </SelectTrigger>
                    <SelectContent className="bg-zinc-900 border-zinc-700">
                      {['Low', 'Medium', 'High', 'Urgent'].map((priority) => (
                        <SelectItem
                          key={priority}
                          value={priority}
                          className="text-zinc-100 focus:bg-zinc-800 focus:text-zinc-100"
                        >
                          {priority}
                        </SelectItem>
                      ))}
                    </SelectContent>
                  </Select>
                </div>

                {/* Schedule Selector */}
                <ScheduleSelector
                  schedule={watch('schedule')}
                  dueDate={watch('due_date')}
                  onScheduleChange={(schedule) => setValue('schedule', schedule)}
                  onDueDateChange={(dueDate) => setValue('due_date', dueDate)}
                />
                {errors.schedule && (
                  <p className="text-sm text-red-400">{errors.schedule.message}</p>
                )}

                {/* Category Selector */}
                {!categoriesLoading && (
                  <CategorySelector
                    categories={categories}
                    selectedCategoryId={watch('category_id')}
                    onCategorySelect={(categoryId) => setValue('category_id', categoryId)}
                    onCreateCategory={handleCreateCategory}
                    isCreatingCategory={isCategoryCreating}
                  />
                )}

                {/* Actions */}
                <div className="flex gap-3 pt-4">
                  <Button
                    type="button"
                    variant="outline"
                    onClick={handleCancel}
                    disabled={isCreating}
                    className="flex-1 bg-zinc-800/50 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100"
                  >
                    Cancel
                  </Button>
                  <Button
                    type="submit"
                    disabled={isCreating}
                    className="flex-1 bg-blue-500 hover:bg-blue-600 text-white disabled:opacity-50"
                  >
                    {isCreating ? (
                      <>
                        <Loader2 className="w-4 h-4 mr-2 animate-spin" />
                        Creating...
                      </>
                    ) : (
                      'Create Task'
                    )}
                  </Button>
                </div>
              </form>
            </motion.div>
          </DialogContent>
        )}
      </AnimatePresence>
    </Dialog>
  );
}
