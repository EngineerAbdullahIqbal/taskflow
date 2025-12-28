/**
 * Better Auth Configuration with JWT Plugin
 *
 * This configures Better Auth for JWT-based authentication with:
 * - 15-minute access tokens
 * - 7-day refresh tokens
 * - Email/password authentication
 */

import { betterAuth } from "better-auth";
import { jwt } from "better-auth/plugins";

export const auth = betterAuth({
  // Base URL for authentication endpoints
  baseURL: process.env.BETTER_AUTH_URL || "http://localhost:3000",

  // Secret for JWT signing (must match backend)
  secret: process.env.BETTER_AUTH_SECRET!,

  // Database configuration (using backend API as proxy)
  database: {
    provider: "postgres",
    url: process.env.DATABASE_URL || "",
  },

  // Email/password authentication
  emailAndPassword: {
    enabled: true,
    requireEmailVerification: false, // TODO: Enable in production
  },

  // JWT Plugin for token-based auth
  plugins: [
    jwt({
      // JWT configuration
      jwks: {
        // Key pair algorithm
        keyPairConfig: {
          alg: "EdDSA",
          crv: "Ed25519",
        },
      },
    }),
  ],

  // Session configuration
  session: {
    expiresIn: 60 * 15, // 15 minutes (access token)
    updateAge: 60 * 60 * 24, // 24 hours (update threshold)
    cookieCache: {
      enabled: true,
      maxAge: 60 * 5, // 5 minutes cache
    },
  },

  // Advanced security options
  advanced: {
    cookiePrefix: "taskflow",
    crossSubDomainCookies: {
      enabled: false,
    },
    useSecureCookies: process.env.NODE_ENV === "production",
    generateId: () => crypto.randomUUID(),
  },
});

export type Session = typeof auth.$Infer.Session;
