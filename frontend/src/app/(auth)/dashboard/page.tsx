/**
 * Dashboard Page (T067)
 *
 * Protected route - main dashboard for authenticated users.
 * Displays task list with create button and glassmorphism design.
 */

"use client";

import { useState } from "react";
import { useAuth } from "@/hooks/useAuth";
import { ProtectedRoute } from "@/components/features/auth/ProtectedRoute";
import { TaskList } from "@/components/features/tasks/TaskList";
import { CreateTaskModal } from "@/components/features/tasks/CreateTaskModal";
import { Button } from "@/components/ui/button";
import { useRouter } from "next/navigation";
import { Plus, LogOut } from "lucide-react";
import { motion } from "framer-motion";

function DashboardContent() {
  const { user, signOut } = useAuth();
  const router = useRouter();
  const [isCreateModalOpen, setIsCreateModalOpen] = useState(false);

  const handleSignOut = async () => {
    await signOut();
    router.push("/login");
  };

  return (
    <div className="min-h-screen bg-zinc-950">
      {/* Navigation Bar */}
      <nav className="sticky top-0 z-50 bg-zinc-900/80 backdrop-blur-md border-b border-zinc-800">
        <div className="mx-auto max-w-7xl px-4 sm:px-6 lg:px-8">
          <div className="flex h-16 items-center justify-between">
            <motion.div
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
              className="flex items-center"
            >
              <h1 className="text-2xl font-bold bg-gradient-to-r from-blue-400 to-violet-400 bg-clip-text text-transparent">
                TaskFlow
              </h1>
            </motion.div>

            <motion.div
              initial={{ opacity: 0, x: 20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ duration: 0.3 }}
              className="flex items-center gap-4"
            >
              <span className="text-sm text-zinc-300 hidden sm:inline">
                {user?.name || user?.email}
              </span>
              <Button
                variant="outline"
                size="sm"
                onClick={handleSignOut}
                className="bg-zinc-800/50 border-zinc-700 text-zinc-300 hover:bg-zinc-800 hover:text-zinc-100"
              >
                <LogOut className="w-4 h-4 mr-2" />
                Sign Out
              </Button>
            </motion.div>
          </div>
        </div>
      </nav>

      {/* Main Content */}
      <main className="mx-auto max-w-7xl px-4 py-8 sm:px-6 lg:px-8">
        {/* Header Section */}
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.4 }}
          className="mb-8 flex items-center justify-between"
        >
          <div>
            <h2 className="text-3xl font-bold text-zinc-100">Tasks & Habits</h2>
            <p className="mt-2 text-zinc-400">
              Manage your one-time tasks and recurring habits in one place.
            </p>
          </div>

          <Button
            onClick={() => setIsCreateModalOpen(true)}
            className="bg-blue-500 hover:bg-blue-600 text-white"
          >
            <Plus className="w-4 h-4 mr-2" />
            Create Task
          </Button>
        </motion.div>

        {/* Task List */}
        <TaskList onCreateTask={() => setIsCreateModalOpen(true)} />
      </main>

      {/* Create Task Modal */}
      <CreateTaskModal
        open={isCreateModalOpen}
        onOpenChange={setIsCreateModalOpen}
      />
    </div>
  );
}

export default function DashboardPage() {
  return (
    <ProtectedRoute>
      <DashboardContent />
    </ProtectedRoute>
  );
}
