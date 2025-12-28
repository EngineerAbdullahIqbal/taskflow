/**
 * SaaS Landing Page Template
 *
 * This template provides a high-conversion landing page structure with:
 * - Sticky glassmorphism navbar
 * - Hero section with dual CTAs
 * - Bento grid feature showcase
 * - Mobile-first responsive design
 *
 * Variables to replace:
 * {{PRODUCT_NAME}} - Name of the SaaS product
 * {{VALUE_PROPOSITION}} - Main headline/value proposition
 * {{SUBTEXT}} - Supporting hero subtext
 * {{FEATURES}} - JSON array of features [{title, description, icon, gridArea}]
 */

import Link from 'next/link'
import { Button } from '@/components/ui/button'
import {
  ArrowRight,
  {{FEATURE_ICONS}}
} from 'lucide-react'

export default function LandingPage() {
  return (
    <div className="min-h-screen bg-zinc-950">
      {/* Sticky Navbar with Glassmorphism */}
      <nav className="sticky top-0 z-50 border-b border-white/10 bg-zinc-950/80 backdrop-blur-md">
        <div className="container mx-auto flex h-16 items-center justify-between px-4 md:px-6 lg:px-8">
          <Link href="/" className="text-xl font-bold text-zinc-100">
            {{PRODUCT_NAME}}
          </Link>

          <div className="flex items-center gap-4">
            <Link
              href="/login"
              className="text-sm text-zinc-400 transition-colors hover:text-zinc-100"
            >
              Sign In
            </Link>
            <Button size="sm" className="bg-blue-600 hover:bg-blue-700">
              Get Started
            </Button>
          </div>
        </div>
      </nav>

      {/* Hero Section */}
      <section className="container mx-auto px-4 py-20 md:px-6 md:py-32 lg:px-8 lg:py-40">
        <div className="mx-auto max-w-4xl text-center">
          <h1 className="bg-gradient-to-r from-zinc-100 to-zinc-400 bg-clip-text text-5xl font-bold text-transparent md:text-6xl lg:text-7xl">
            {{VALUE_PROPOSITION}}
          </h1>

          <p className="mt-6 text-lg text-zinc-400 md:text-xl lg:mt-8">
            {{SUBTEXT}}
          </p>

          {/* Dual CTAs */}
          <div className="mt-10 flex flex-col gap-4 sm:flex-row sm:justify-center lg:mt-12">
            <Button size="lg" className="group bg-blue-600 hover:bg-blue-700">
              Start Free Trial
              <ArrowRight className="ml-2 h-4 w-4 transition-transform group-hover:translate-x-1" />
            </Button>
            <Button
              size="lg"
              variant="outline"
              className="border-zinc-700 bg-transparent hover:bg-zinc-900"
            >
              Watch Demo
            </Button>
          </div>
        </div>
      </section>

      {/* Bento Grid Features */}
      <section className="container mx-auto px-4 py-20 md:px-6 lg:px-8">
        <div className="mx-auto max-w-7xl">
          <h2 className="mb-12 text-center text-3xl font-bold text-zinc-100 md:text-4xl">
            Everything you need
          </h2>

          {/* Asymmetric Bento Grid */}
          <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3 lg:gap-6">
            {{#each FEATURES}}
            <div
              className="group rounded-lg border border-white/10 bg-zinc-900/50 p-6 backdrop-blur-md transition-all hover:border-white/20 hover:bg-zinc-900/70 {{gridArea}}"
            >
              <div className="mb-4 inline-flex h-12 w-12 items-center justify-center rounded-lg bg-blue-600/10">
                <{{icon}} className="h-6 w-6 text-blue-500" />
              </div>

              <h3 className="mb-2 text-xl font-semibold text-zinc-100">
                {{title}}
              </h3>

              <p className="text-sm text-zinc-400">
                {{description}}
              </p>
            </div>
            {{/each}}
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="container mx-auto px-4 py-20 md:px-6 lg:px-8">
        <div className="mx-auto max-w-4xl rounded-2xl border border-white/10 bg-gradient-to-r from-blue-600/10 to-purple-600/10 p-12 text-center backdrop-blur-md">
          <h2 className="mb-4 text-3xl font-bold text-zinc-100 md:text-4xl">
            Ready to get started?
          </h2>
          <p className="mb-8 text-lg text-zinc-400">
            Join thousands of teams already using {{PRODUCT_NAME}}
          </p>
          <Button size="lg" className="bg-blue-600 hover:bg-blue-700">
            Start Your Free Trial
          </Button>
        </div>
      </section>

      {/* Footer */}
      <footer className="border-t border-white/10 py-12">
        <div className="container mx-auto px-4 text-center text-sm text-zinc-500 md:px-6 lg:px-8">
          © 2025 {{PRODUCT_NAME}}. All rights reserved.
        </div>
      </footer>
    </div>
  )
}
