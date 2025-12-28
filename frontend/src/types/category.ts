/**
 * Category Type Definitions
 *
 * Categories are user-defined labels with custom colors for organizing tasks.
 * Each user can have up to 20 categories.
 */

export interface Category {
  id: string;
  user_id: string;
  name: string;
  color: string; // hex color (e.g., "#3b82f6")
  created_at: string;
  updated_at: string;
}

/**
 * Category creation payload
 */
export interface CreateCategoryRequest {
  name: string;
  color: string;
}

/**
 * Category update payload
 */
export interface UpdateCategoryRequest {
  name?: string;
  color?: string;
}

/**
 * Category list response
 */
export interface CategoryListResponse {
  categories: Category[];
  total: number;
}
