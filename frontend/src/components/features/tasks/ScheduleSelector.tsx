/**
 * ScheduleSelector Component (T074)
 *
 * Allows user to choose between:
 * - Habit mode: Recurring days (Mon-Sun checkboxes)
 * - One-time mode: Due date picker
 *
 * Implements XOR logic (mutual exclusion).
 */

'use client';

import { useState } from 'react';
import { Label } from '@/components/ui/label';
import { Checkbox } from '@/components/ui/checkbox';
import { Input } from '@/components/ui/input';
import { cn } from '@/lib/utils';
import { Calendar, Repeat } from 'lucide-react';

interface ScheduleSelectorProps {
  schedule?: string[];
  dueDate?: string;
  onScheduleChange: (schedule: string[] | undefined) => void;
  onDueDateChange: (dueDate: string | undefined) => void;
}

const WEEKDAYS = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'];

export function ScheduleSelector({
  schedule,
  dueDate,
  onScheduleChange,
  onDueDateChange
}: ScheduleSelectorProps) {
  const [mode, setMode] = useState<'habit' | 'one-time'>(
    schedule && schedule.length > 0 ? 'habit' : dueDate ? 'one-time' : 'habit'
  );

  const handleModeToggle = (newMode: 'habit' | 'one-time') => {
    setMode(newMode);

    // Clear opposite mode
    if (newMode === 'habit') {
      onDueDateChange(undefined);
    } else {
      onScheduleChange(undefined);
    }
  };

  const handleDayToggle = (day: string) => {
    const currentSchedule = schedule || [];
    const newSchedule = currentSchedule.includes(day)
      ? currentSchedule.filter(d => d !== day)
      : [...currentSchedule, day];

    onScheduleChange(newSchedule.length > 0 ? newSchedule : undefined);
  };

  return (
    <div className="space-y-4">
      {/* Mode Toggle */}
      <div className="flex gap-2">
        <button
          type="button"
          onClick={() => handleModeToggle('habit')}
          className={cn(
            'flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all',
            mode === 'habit'
              ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
              : 'bg-zinc-800/50 text-zinc-400 border border-zinc-700 hover:bg-zinc-800'
          )}
          aria-label="Habit mode"
        >
          <Repeat className="w-4 h-4" />
          Habit (Recurring)
        </button>
        <button
          type="button"
          onClick={() => handleModeToggle('one-time')}
          className={cn(
            'flex-1 flex items-center justify-center gap-2 px-4 py-2 rounded-md text-sm font-medium transition-all',
            mode === 'one-time'
              ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
              : 'bg-zinc-800/50 text-zinc-400 border border-zinc-700 hover:bg-zinc-800'
          )}
          aria-label="One-time task mode"
        >
          <Calendar className="w-4 h-4" />
          One-time Task
        </button>
      </div>

      {/* Habit Mode: Weekday Checkboxes */}
      {mode === 'habit' && (
        <div className="space-y-2">
          <Label className="text-sm font-medium text-zinc-300">
            Repeat on Days
          </Label>
          <div className="flex flex-wrap gap-2">
            {WEEKDAYS.map(day => (
              <label
                key={day}
                className={cn(
                  'flex items-center gap-2 px-3 py-2 rounded-md text-sm font-medium cursor-pointer transition-all',
                  schedule?.includes(day)
                    ? 'bg-blue-500/20 text-blue-400 border border-blue-500/30'
                    : 'bg-zinc-800/50 text-zinc-400 border border-zinc-700 hover:bg-zinc-800'
                )}
              >
                <Checkbox
                  checked={schedule?.includes(day)}
                  onCheckedChange={() => handleDayToggle(day)}
                  className="sr-only"
                />
                {day}
              </label>
            ))}
          </div>
        </div>
      )}

      {/* One-time Mode: Date Picker */}
      {mode === 'one-time' && (
        <div className="space-y-2">
          <Label htmlFor="due-date" className="text-sm font-medium text-zinc-300">
            Due Date
          </Label>
          <Input
            id="due-date"
            type="date"
            value={dueDate || ''}
            onChange={(e) => onDueDateChange(e.target.value || undefined)}
            className="bg-zinc-900/50 border-zinc-700 text-zinc-100 focus:border-blue-500/50"
          />
        </div>
      )}
    </div>
  );
}
