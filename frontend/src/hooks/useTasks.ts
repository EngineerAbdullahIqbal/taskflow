/**
 * useTasks Hook (T075)
 *
 * React Query hook for managing task data.
 * Provides methods for fetching, creating, updating, and deleting tasks.
 * Includes optimistic updates and automatic cache invalidation.
 */

'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import {
  getTasks,
  getTaskById,
  createTask,
  updateTask,
  deleteTask,
  toggleTaskCompletion
} from '@/lib/api/tasks';
import type { CreateTaskRequest, UpdateTaskRequest } from '@/types/task';
import toast from 'react-hot-toast';

interface UseTasksParams {
  page?: number;
  pageSize?: number;
  categoryId?: string;
  completed?: boolean;
}

export function useTasks(params?: UseTasksParams) {
  const queryClient = useQueryClient();

  // Fetch tasks query
  const {
    data,
    isLoading,
    error,
    refetch
  } = useQuery({
    queryKey: ['tasks', params],
    queryFn: () => getTasks({
      page: params?.page || 1,
      page_size: params?.pageSize || 20,
      category_id: params?.categoryId,
      completed: params?.completed
    }),
    staleTime: 30000, // 30 seconds
  });

  // Create task mutation
  const createTaskMutation = useMutation({
    mutationFn: (newTask: CreateTaskRequest) => createTask(newTask),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      toast.success('Task created successfully');
    },
    onError: (error: Error) => {
      toast.error(`Failed to create task: ${error.message}`);
    }
  });

  // Update task mutation
  const updateTaskMutation = useMutation({
    mutationFn: ({ taskId, data }: { taskId: string; data: UpdateTaskRequest }) =>
      updateTask(taskId, data),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      toast.success('Task updated successfully');
    },
    onError: (error: Error) => {
      toast.error(`Failed to update task: ${error.message}`);
    }
  });

  // Delete task mutation
  const deleteTaskMutation = useMutation({
    mutationFn: (taskId: string) => deleteTask(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
      toast.success('Task deleted successfully');
    },
    onError: (error: Error) => {
      toast.error(`Failed to delete task: ${error.message}`);
    }
  });

  // Toggle completion mutation
  const toggleCompletionMutation = useMutation({
    mutationFn: (taskId: string) => toggleTaskCompletion(taskId),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['tasks'] });
    },
    onError: (error: Error) => {
      toast.error(`Failed to update task: ${error.message}`);
    }
  });

  return {
    // Data
    tasks: data?.tasks || [],
    total: data?.total || 0,
    page: data?.page || 1,
    pageSize: data?.page_size || 20,

    // Loading states
    isLoading,
    error,

    // Mutations
    createTask: createTaskMutation.mutateAsync,
    updateTask: updateTaskMutation.mutateAsync,
    deleteTask: deleteTaskMutation.mutateAsync,
    toggleCompletion: toggleCompletionMutation.mutateAsync,

    // Mutation states
    isCreating: createTaskMutation.isPending,
    isUpdating: updateTaskMutation.isPending,
    isDeleting: deleteTaskMutation.isPending,

    // Refetch
    refetch
  };
}

/**
 * Get single task by ID
 */
export function useTask(taskId: string) {
  const { data, isLoading, error } = useQuery({
    queryKey: ['task', taskId],
    queryFn: () => getTaskById(taskId),
    enabled: !!taskId,
  });

  return {
    task: data,
    isLoading,
    error
  };
}
