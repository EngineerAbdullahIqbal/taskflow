"use client";

/**
 * Authentication Context Provider
 *
 * Provides authentication state and methods to the entire application.
 * Wraps the app in layout.tsx to make auth available everywhere.
 */

import { useEffect, useState } from "react";
import type { UserResponse } from "@/../../shared/types";
import { AuthContext, type AuthContextValue } from "@/hooks/useAuth";
import * as authApi from "./api/auth";

export function AuthProvider({ children }: { children: React.ReactNode }) {
  const [user, setUser] = useState<UserResponse | null>(null);
  const [isLoading, setIsLoading] = useState(true);

  // Load user from token on mount
  useEffect(() => {
    loadUser();
  }, []);

  async function loadUser() {
    try {
      setIsLoading(true);
      const token = authApi.getAccessToken();

      if (!token) {
        setUser(null);
        return;
      }

      // Decode JWT to get user info (basic implementation)
      // In production, fetch user profile from /api/user/me endpoint
      const payload = JSON.parse(atob(token.split(".")[1]));
      const userId = parseInt(payload.sub, 10);

      // For now, we'll set a placeholder user
      // This will be replaced with actual API call in next phase
      setUser({
        id: userId,
        email: "",
        name: "",
        created_at: "",
        updated_at: "",
      });
    } catch (error) {
      console.error("Failed to load user:", error);
      setUser(null);
      authApi.clearTokens();
    } finally {
      setIsLoading(false);
    }
  }

  async function signUp(email: string, password: string, name: string) {
    const response = await authApi.signUp({ email, password, name });
    authApi.storeTokens(response.tokens);
    setUser(response.user);
  }

  async function signIn(email: string, password: string) {
    const response = await authApi.signIn({ email, password });
    authApi.storeTokens(response.tokens);
    setUser(response.user);
  }

  async function signOut() {
    const token = authApi.getAccessToken();
    if (token) {
      try {
        await authApi.signOut(token);
      } catch (error) {
        console.error("Logout error:", error);
      }
    }
    authApi.clearTokens();
    setUser(null);
  }

  const value: AuthContextValue = {
    user,
    isLoading,
    isAuthenticated: !!user,
    signUp,
    signIn,
    signOut,
  };

  return <AuthContext.Provider value={value}>{children}</AuthContext.Provider>;
}
