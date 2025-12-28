/**
 * Authentication API Client
 *
 * Handles signup, login, and logout requests to backend auth endpoints.
 */

import type {
  SignupRequest,
  LoginRequest,
  TokenResponse,
  UserResponse,
} from "@/../../shared/types";

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export interface AuthResponse {
  user: UserResponse;
  tokens: TokenResponse;
}

export class AuthError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: unknown
  ) {
    super(message);
    this.name = "AuthError";
  }
}

/**
 * Sign up a new user account
 */
export async function signUp(data: SignupRequest): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/signup`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new AuthError(
      errorData.message || errorData.detail || "Signup failed",
      response.status,
      errorData.details
    );
  }

  return await response.json();
}

/**
 * Sign in an existing user
 */
export async function signIn(data: LoginRequest): Promise<AuthResponse> {
  const response = await fetch(`${API_BASE_URL}/auth/login`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify(data),
  });

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new AuthError(
      errorData.message || errorData.detail || "Login failed",
      response.status,
      errorData.details
    );
  }

  return await response.json();
}

/**
 * Sign out the current user
 */
export async function signOut(token: string): Promise<void> {
  const response = await fetch(`${API_BASE_URL}/auth/logout`, {
    method: "POST",
    headers: {
      Authorization: `Bearer ${token}`,
    },
  });

  if (!response.ok && response.status !== 204) {
    const errorData = await response.json().catch(() => ({}));
    throw new AuthError(
      errorData.message || errorData.detail || "Logout failed",
      response.status,
      errorData.details
    );
  }
}

/**
 * Store tokens in localStorage
 */
export function storeTokens(tokens: TokenResponse): void {
  localStorage.setItem("access_token", tokens.access_token);
  localStorage.setItem("refresh_token", tokens.refresh_token);
}

/**
 * Retrieve access token from localStorage
 */
export function getAccessToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("access_token");
}

/**
 * Retrieve refresh token from localStorage
 */
export function getRefreshToken(): string | null {
  if (typeof window === "undefined") return null;
  return localStorage.getItem("refresh_token");
}

/**
 * Clear all auth tokens from localStorage
 */
export function clearTokens(): void {
  localStorage.removeItem("access_token");
  localStorage.removeItem("refresh_token");
}
