/**
 * Task Type Definitions
 *
 * Represents both one-time tasks and recurring habits in the TaskFlow system.
 * Tasks can have either a due_date (one-time) or schedule (recurring), never both.
 */

export type Priority = 'Low' | 'Medium' | 'High' | 'Urgent';

export interface Task {
  id: string;
  user_id: string;
  title: string;
  story?: string;
  priority: Priority;
  schedule?: string[]; // ['Mon', 'Wed', 'Fri'] for habits
  due_date?: string; // ISO date for one-time tasks
  category_id?: string;
  completed: boolean;
  created_at: string;
  updated_at: string;
}

/**
 * Task creation payload (excludes auto-generated fields)
 */
export interface CreateTaskRequest {
  title: string;
  story?: string;
  priority: Priority;
  schedule?: string[];
  due_date?: string;
  category_id?: string;
}

/**
 * Task update payload (all fields optional except id)
 */
export interface UpdateTaskRequest {
  title?: string;
  story?: string;
  priority?: Priority;
  schedule?: string[];
  due_date?: string;
  category_id?: string;
  completed?: boolean;
}

/**
 * Paginated task list response
 */
export interface TaskListResponse {
  tasks: Task[];
  total: number;
  page: number;
  page_size: number;
}
