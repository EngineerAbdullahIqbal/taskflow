/**
 * CategorySelector Component (T073)
 *
 * Dropdown for selecting existing categories with inline creation.
 * Shows "+ Create New" option with color picker.
 * Max 20 categories per user.
 */

'use client';

import { useState } from 'react';
import { Label } from '@/components/ui/label';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import {
  Select,
  SelectContent,
  SelectItem,
  SelectTrigger,
  SelectValue,
} from '@/components/ui/select';
import { cn } from '@/lib/utils';
import { Plus, X } from 'lucide-react';
import type { Category } from '@/types/category';

interface CategorySelectorProps {
  categories: Category[];
  selectedCategoryId?: string;
  onCategorySelect: (categoryId: string | undefined) => void;
  onCreateCategory: (name: string, color: string) => Promise<void>;
  isCreatingCategory?: boolean;
}

const DEFAULT_COLORS = [
  '#3b82f6', // blue
  '#10b981', // green
  '#f59e0b', // amber
  '#ef4444', // red
  '#8b5cf6', // violet
  '#ec4899', // pink
  '#06b6d4', // cyan
  '#f97316', // orange
];

export function CategorySelector({
  categories,
  selectedCategoryId,
  onCategorySelect,
  onCreateCategory,
  isCreatingCategory = false
}: CategorySelectorProps) {
  const [isCreating, setIsCreating] = useState(false);
  const [newCategoryName, setNewCategoryName] = useState('');
  const [newCategoryColor, setNewCategoryColor] = useState(DEFAULT_COLORS[0]);

  const handleCreate = async () => {
    if (!newCategoryName.trim()) return;

    try {
      await onCreateCategory(newCategoryName, newCategoryColor);
      setNewCategoryName('');
      setNewCategoryColor(DEFAULT_COLORS[0]);
      setIsCreating(false);
    } catch (error) {
      console.error('Failed to create category:', error);
    }
  };

  const canCreateMore = categories.length < 20;

  return (
    <div className="space-y-2">
      <Label className="text-sm font-medium text-zinc-300">
        Category
        {categories.length >= 20 && (
          <span className="ml-2 text-xs text-yellow-400">(Max 20 reached)</span>
        )}
      </Label>

      {!isCreating ? (
        <div className="space-y-2">
          <Select
            value={selectedCategoryId}
            onValueChange={onCategorySelect}
          >
            <SelectTrigger className="bg-zinc-900/50 border-zinc-700 text-zinc-100">
              <SelectValue placeholder="Select category" />
            </SelectTrigger>
            <SelectContent className="bg-zinc-900 border-zinc-700">
              {categories.map((category) => (
                <SelectItem
                  key={category.id}
                  value={category.id}
                  className="text-zinc-100 focus:bg-zinc-800 focus:text-zinc-100"
                >
                  <div className="flex items-center gap-2">
                    <div
                      className="w-3 h-3 rounded-full"
                      style={{ backgroundColor: category.color }}
                    />
                    {category.name}
                  </div>
                </SelectItem>
              ))}
            </SelectContent>
          </Select>

          {canCreateMore && (
            <Button
              type="button"
              variant="outline"
              size="sm"
              onClick={() => setIsCreating(true)}
              className="w-full bg-zinc-800/50 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100"
            >
              <Plus className="w-4 h-4 mr-2" />
              Create New Category
            </Button>
          )}
        </div>
      ) : (
        <div className="space-y-3 p-4 bg-zinc-900/50 border border-zinc-700 rounded-md">
          <div className="flex items-center justify-between">
            <span className="text-sm font-medium text-zinc-300">New Category</span>
            <Button
              type="button"
              variant="ghost"
              size="sm"
              onClick={() => setIsCreating(false)}
              className="h-6 w-6 p-0 text-zinc-400 hover:text-zinc-100"
              aria-label="Cancel"
            >
              <X className="w-4 h-4" />
            </Button>
          </div>

          <Input
            placeholder="Category name"
            value={newCategoryName}
            onChange={(e) => setNewCategoryName(e.target.value)}
            maxLength={50}
            className="bg-zinc-900 border-zinc-700 text-zinc-100 focus:border-blue-500/50"
          />

          <div className="space-y-2">
            <Label className="text-xs text-zinc-400">Color</Label>
            <div className="flex gap-2">
              {DEFAULT_COLORS.map((color) => (
                <button
                  key={color}
                  type="button"
                  onClick={() => setNewCategoryColor(color)}
                  className={cn(
                    'w-8 h-8 rounded-md transition-all',
                    newCategoryColor === color
                      ? 'ring-2 ring-offset-2 ring-offset-zinc-900 ring-zinc-400 scale-110'
                      : 'hover:scale-105'
                  )}
                  style={{ backgroundColor: color }}
                  aria-label={`Select color ${color}`}
                />
              ))}
            </div>
          </div>

          <Button
            type="button"
            onClick={handleCreate}
            disabled={!newCategoryName.trim() || isCreatingCategory}
            className="w-full bg-blue-500 hover:bg-blue-600 text-white"
          >
            {isCreatingCategory ? 'Creating...' : 'Create Category'}
          </Button>
        </div>
      )}
    </div>
  );
}
