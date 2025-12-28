/**
 * Task API Client
 *
 * Provides methods for interacting with task endpoints.
 * All requests automatically include JWT authentication headers.
 */

import { api } from './client';
import type {
  Task,
  CreateTaskRequest,
  UpdateTaskRequest,
  TaskListResponse
} from '@/types/task';

/**
 * Create a new task
 */
export async function createTask(data: CreateTaskRequest): Promise<Task> {
  return api.post<Task>('/api/tasks', data);
}

/**
 * Get paginated list of tasks for current user
 */
export async function getTasks(params?: {
  page?: number;
  page_size?: number;
  category_id?: string;
  completed?: boolean;
}): Promise<TaskListResponse> {
  const queryParams = new URLSearchParams();

  if (params?.page) queryParams.set('page', params.page.toString());
  if (params?.page_size) queryParams.set('page_size', params.page_size.toString());
  if (params?.category_id) queryParams.set('category_id', params.category_id);
  if (params?.completed !== undefined) queryParams.set('completed', params.completed.toString());

  const endpoint = `/api/tasks${queryParams.toString() ? `?${queryParams.toString()}` : ''}`;
  return api.get<TaskListResponse>(endpoint);
}

/**
 * Get single task by ID
 */
export async function getTaskById(taskId: string): Promise<Task> {
  return api.get<Task>(`/api/tasks/${taskId}`);
}

/**
 * Update an existing task
 */
export async function updateTask(
  taskId: string,
  data: UpdateTaskRequest
): Promise<Task> {
  return api.patch<Task>(`/api/tasks/${taskId}`, data);
}

/**
 * Delete a task
 */
export async function deleteTask(taskId: string): Promise<void> {
  return api.delete<void>(`/api/tasks/${taskId}`);
}

/**
 * Toggle task completion status
 */
export async function toggleTaskCompletion(taskId: string): Promise<Task> {
  return api.patch<Task>(`/api/tasks/${taskId}/toggle`, {});
}
