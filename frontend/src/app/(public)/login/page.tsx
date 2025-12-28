/**
 * Login Page
 *
 * User authentication page with email and password fields.
 */

import Link from "next/link";
import { LoginForm } from "@/components/features/auth/LoginForm";

export default function LoginPage() {
  return (
    <div className="flex min-h-screen items-center justify-center bg-gray-50 px-4 py-12 sm:px-6 lg:px-8">
      <div className="w-full max-w-md space-y-8">
        <div>
          <h2 className="mt-6 text-center text-3xl font-bold tracking-tight text-gray-900">
            Sign in to your account
          </h2>
          <p className="mt-2 text-center text-sm text-gray-600">
            Don't have an account?{" "}
            <Link
              href="/signup"
              className="font-medium text-blue-600 hover:text-blue-500"
            >
              Create one
            </Link>
          </p>
        </div>

        <div className="mt-8 rounded-lg bg-white px-8 py-8 shadow">
          <LoginForm />
        </div>
      </div>
    </div>
  );
}
