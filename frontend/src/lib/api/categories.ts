/**
 * Category API Client
 *
 * Provides methods for interacting with category endpoints.
 * All requests automatically include JWT authentication headers.
 */

import { api } from './client';
import type {
  Category,
  CreateCategoryRequest,
  UpdateCategoryRequest,
  CategoryListResponse
} from '@/types/category';

/**
 * Create a new category
 */
export async function createCategory(data: CreateCategoryRequest): Promise<Category> {
  return api.post<Category>('/api/categories', data);
}

/**
 * Get all categories for current user
 */
export async function getCategories(): Promise<CategoryListResponse> {
  return api.get<CategoryListResponse>('/api/categories');
}

/**
 * Get single category by ID
 */
export async function getCategoryById(categoryId: string): Promise<Category> {
  return api.get<Category>(`/api/categories/${categoryId}`);
}

/**
 * Update an existing category
 */
export async function updateCategory(
  categoryId: string,
  data: UpdateCategoryRequest
): Promise<Category> {
  return api.patch<Category>(`/api/categories/${categoryId}`, data);
}

/**
 * Delete a category
 */
export async function deleteCategory(categoryId: string): Promise<void> {
  return api.delete<void>(`/api/categories/${categoryId}`);
}
