/**
 * useCategories Hook (T076)
 *
 * React Query hook for managing category data.
 * Provides methods for fetching and creating categories.
 */

'use client';

import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { getCategories, createCategory } from '@/lib/api/categories';
import type { CreateCategoryRequest } from '@/types/category';
import toast from 'react-hot-toast';

export function useCategories() {
  const queryClient = useQueryClient();

  // Fetch categories query
  const {
    data,
    isLoading,
    error,
    refetch
  } = useQuery({
    queryKey: ['categories'],
    queryFn: getCategories,
    staleTime: 60000, // 1 minute (categories change less frequently)
  });

  // Create category mutation
  const createCategoryMutation = useMutation({
    mutationFn: (newCategory: CreateCategoryRequest) => createCategory(newCategory),
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['categories'] });
      toast.success('Category created successfully');
    },
    onError: (error: Error) => {
      toast.error(`Failed to create category: ${error.message}`);
    }
  });

  return {
    // Data
    categories: data?.categories || [],
    total: data?.total || 0,

    // Loading states
    isLoading,
    error,

    // Mutations
    createCategory: createCategoryMutation.mutateAsync,

    // Mutation states
    isCreating: createCategoryMutation.isPending,

    // Refetch
    refetch
  };
}
