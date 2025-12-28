/**
 * Shared Types Export
 *
 * Central export point for all shared types between frontend and backend.
 */

export type {
  // User types
  UserResponse,
  // Task types
  Priority,
  TaskResponse,
  CreateTaskRequest,
  UpdateTaskRequest,
  // Category types
  CategoryResponse,
  CreateCategoryRequest,
  UpdateCategoryRequest,
  // Notification types
  NotificationResponse,
  UpdateNotificationRequest,
  // Notification Preference types
  NotificationPreferenceResponse,
  UpdateNotificationPreferenceRequest,
  // Auth types
  SignupRequest,
  LoginRequest,
  TokenResponse,
  // Error types
  ErrorDetail,
  ErrorResponse,
  // Health types
  HealthResponse,
} from "./api";
