import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { TrendingUp, TrendingDown } from 'lucide-react'

interface StatCardProps {
  title: string
  value: string | number
  change?: number
  trend?: 'up' | 'down' | 'neutral'
  period?: string
  icon?: React.ReactNode
}

export function StatCard({ title, value, change, trend, period, icon }: StatCardProps) {
  return (
    <Card className="bg-zinc-900/50 border-white/10 backdrop-blur-md">
      <CardHeader className="flex flex-row items-center justify-between pb-2">
        <CardTitle className="text-sm font-medium text-muted-foreground">{title}</CardTitle>
        {icon}
      </CardHeader>
      <CardContent>
        <div className="text-3xl font-bold text-foreground">{value}</div>
        {change !== undefined && (
          <div className="flex items-center gap-1 mt-1">
            {trend === 'up' && <TrendingUp className="h-4 w-4 text-green-500" />}
            {trend === 'down' && <TrendingDown className="h-4 w-4 text-red-500" />}
            <span className={trend === 'up' ? 'text-green-500' : trend === 'down' ? 'text-red-500' : 'text-zinc-400'}>
              {change > 0 ? '+' : ''}{change}%
            </span>
            {period && <span className="text-xs text-muted-foreground ml-1">{period}</span>}
          </div>
        )}
      </CardContent>
    </Card>
  )
}

export function StatCardSkeleton() {
  return (
    <Card className="bg-zinc-900/50 border-white/10 backdrop-blur-md">
      <CardHeader className="pb-2">
        <div className="h-4 w-24 bg-zinc-800 animate-pulse rounded" />
      </CardHeader>
      <CardContent>
        <div className="h-8 w-32 bg-zinc-800 animate-pulse rounded" />
        <div className="h-4 w-20 bg-zinc-800 animate-pulse rounded mt-2" />
      </CardContent>
    </Card>
  )
}
