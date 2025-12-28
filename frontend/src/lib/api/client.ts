/**
 * Base API Client with JWT Header Injection
 *
 * Provides a configured fetch wrapper that automatically:
 * - Adds JWT Authorization header
 * - Handles JSON serialization
 * - Provides typed error responses
 */

const API_BASE_URL = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

export class APIError extends Error {
  constructor(
    message: string,
    public status: number,
    public details?: unknown
  ) {
    super(message);
    this.name = "APIError";
  }
}

export interface APIClientOptions {
  headers?: Record<string, string>;
  body?: unknown;
  method?: string;
}

/**
 * Make an authenticated API request
 */
export async function apiClient<T>(
  endpoint: string,
  options: APIClientOptions = {}
): Promise<T> {
  const { headers = {}, body, method = "GET" } = options;

  // Get JWT token from Better Auth
  const token = await getAuthToken();

  // Prepare headers
  const requestHeaders: Record<string, string> = {
    "Content-Type": "application/json",
    ...headers,
  };

  // Add Authorization header if token exists
  if (token) {
    requestHeaders["Authorization"] = `Bearer ${token}`;
  }

  // Prepare request config
  const config: RequestInit = {
    method,
    headers: requestHeaders,
  };

  // Add body if provided
  if (body !== undefined) {
    config.body = JSON.stringify(body);
  }

  // Make request
  const response = await fetch(`${API_BASE_URL}${endpoint}`, config);

  // Handle non-OK responses
  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}));
    throw new APIError(
      errorData.message || "An error occurred",
      response.status,
      errorData.details
    );
  }

  // Parse and return JSON response
  const data = await response.json();
  return data as T;
}

/**
 * Get authentication token from Better Auth
 */
async function getAuthToken(): Promise<string | null> {
  // TODO: Implement actual token retrieval from Better Auth session
  // For now, return null - will be implemented when auth is fully integrated
  if (typeof window === "undefined") {
    return null;
  }

  // Get token from cookie or session storage
  const token = document.cookie
    .split("; ")
    .find((row) => row.startsWith("taskflow.session="))
    ?.split("=")[1];

  return token || null;
}

/**
 * Helper methods for common HTTP methods
 */
export const api = {
  get: <T>(endpoint: string, headers?: Record<string, string>) =>
    apiClient<T>(endpoint, { method: "GET", headers }),

  post: <T>(endpoint: string, body: unknown, headers?: Record<string, string>) =>
    apiClient<T>(endpoint, { method: "POST", body, headers }),

  patch: <T>(endpoint: string, body: unknown, headers?: Record<string, string>) =>
    apiClient<T>(endpoint, { method: "PATCH", body, headers }),

  put: <T>(endpoint: string, body: unknown, headers?: Record<string, string>) =>
    apiClient<T>(endpoint, { method: "PUT", body, headers }),

  delete: <T>(endpoint: string, headers?: Record<string, string>) =>
    apiClient<T>(endpoint, { method: "DELETE", headers }),
};
