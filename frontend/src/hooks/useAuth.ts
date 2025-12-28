/**
 * useAuth Hook
 *
 * Provides authentication state and methods throughout the application.
 * Must be used within AuthProvider context.
 */

"use client";

import { useContext, createContext } from "react";
import type { UserResponse } from "@/../../shared/types";

export interface AuthContextValue {
  user: UserResponse | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  signUp: (email: string, password: string, name: string) => Promise<void>;
  signIn: (email: string, password: string) => Promise<void>;
  signOut: () => Promise<void>;
}

export const AuthContext = createContext<AuthContextValue | undefined>(
  undefined
);

/**
 * Hook to access authentication context
 *
 * @throws Error if used outside AuthProvider
 *
 * @example
 * ```tsx
 * function MyComponent() {
 *   const { user, isAuthenticated, signIn } = useAuth();
 *
 *   if (!isAuthenticated) {
 *     return <button onClick={() => signIn(email, password)}>Login</button>;
 *   }
 *
 *   return <div>Welcome, {user?.name}</div>;
 * }
 * ```
 */
export function useAuth(): AuthContextValue {
  const context = useContext(AuthContext);

  if (context === undefined) {
    throw new Error("useAuth must be used within an AuthProvider");
  }

  return context;
}
