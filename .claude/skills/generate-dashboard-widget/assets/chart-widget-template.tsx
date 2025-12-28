import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { BarChart3 } from 'lucide-react'

interface ChartWidgetProps {
  title: string
  data: { labels: string[]; values: number[] }
  type?: 'line' | 'bar' | 'pie'
}

export function ChartWidget({ title, data, type = 'line' }: ChartWidgetProps) {
  return (
    <Card className="bg-zinc-900/50 border-white/10 backdrop-blur-md">
      <CardHeader>
        <CardTitle className="text-lg font-semibold">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {data.values.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-12 text-center">
            <BarChart3 className="h-12 w-12 text-zinc-600 mb-3" />
            <p className="text-sm text-muted-foreground">No data to display</p>
          </div>
        ) : (
          <div className="w-full h-64">
            {/* Integrate charting library here (Recharts recommended) */}
            <p className="text-xs text-muted-foreground">Chart implementation with {type} visualization</p>
          </div>
        )}
      </CardContent>
    </Card>
  )
}
