/**
 * Shared API Type Definitions
 *
 * These types are shared between frontend and backend to ensure
 * type safety across the full stack.
 */

// ============================================================================
// User Types
// ============================================================================

export interface UserResponse {
  id: number;
  email: string;
  name: string;
  created_at: string;
  updated_at: string;
}

// ============================================================================
// Task Types
// ============================================================================

export type Priority = "low" | "medium" | "high" | "urgent";

export interface TaskResponse {
  id: number;
  user_id: number;
  title: string;
  story: string | null;
  priority: Priority;
  schedule: string | null; // JSON array for recurring days
  due_date: string | null;
  category_id: number | null;
  reminder_enabled: boolean;
  reminder_timing: number | null;
  reminder_channels: string | null; // "email,browser"
  completed: boolean;
  created_at: string;
  updated_at: string;
}

export interface CreateTaskRequest {
  title: string;
  story?: string;
  priority?: Priority;
  schedule?: string;
  due_date?: string;
  category_id?: number;
  reminder_enabled?: boolean;
  reminder_timing?: number;
  reminder_channels?: string;
}

export interface UpdateTaskRequest {
  title?: string;
  story?: string;
  priority?: Priority;
  schedule?: string;
  due_date?: string;
  category_id?: number;
  reminder_enabled?: boolean;
  reminder_timing?: number;
  reminder_channels?: string;
  completed?: boolean;
}

// ============================================================================
// Category Types
// ============================================================================

export interface CategoryResponse {
  id: number;
  user_id: number;
  name: string;
  color: string; // Hex color #RRGGBB
  created_at: string;
  updated_at: string;
}

export interface CreateCategoryRequest {
  name: string;
  color: string;
}

export interface UpdateCategoryRequest {
  name?: string;
  color?: string;
}

// ============================================================================
// Notification Types
// ============================================================================

export interface NotificationResponse {
  id: number;
  user_id: number;
  task_id: number | null;
  type: string;
  title: string;
  message: string;
  read: boolean;
  clicked: boolean;
  created_at: string;
}

export interface UpdateNotificationRequest {
  read?: boolean;
  clicked?: boolean;
}

// ============================================================================
// Notification Preference Types
// ============================================================================

export interface NotificationPreferenceResponse {
  id: number;
  user_id: number;
  reminder_email: string | null;
  email_notifications_enabled: boolean;
  browser_notifications_enabled: boolean;
  created_at: string;
  updated_at: string;
}

export interface UpdateNotificationPreferenceRequest {
  reminder_email?: string;
  email_notifications_enabled?: boolean;
  browser_notifications_enabled?: boolean;
}

// ============================================================================
// Auth Types
// ============================================================================

export interface SignupRequest {
  email: string;
  password: string;
  name: string;
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

// ============================================================================
// Error Types
// ============================================================================

export interface ErrorDetail {
  field: string;
  message: string;
}

export interface ErrorResponse {
  error: string;
  message: string;
  details?: ErrorDetail[] | Record<string, unknown> | null;
}

// ============================================================================
// Health Types
// ============================================================================

export interface HealthResponse {
  status: string;
  timestamp: string;
  version: string;
  environment: string;
}
