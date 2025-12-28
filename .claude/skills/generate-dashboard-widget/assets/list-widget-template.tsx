import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'
import { Inbox } from 'lucide-react'

interface ListWidgetProps<T> {
  title: string
  data: T[]
  renderItem: (item: T) => React.ReactNode
  emptyMessage?: string
}

export function ListWidget<T extends { id: string | number }>({ 
  title, data, renderItem, emptyMessage = 'No items yet' 
}: ListWidgetProps<T>) {
  return (
    <Card className="bg-zinc-900/50 border-white/10 backdrop-blur-md">
      <CardHeader>
        <CardTitle className="text-lg font-semibold">{title}</CardTitle>
      </CardHeader>
      <CardContent>
        {data.length === 0 ? (
          <div className="flex flex-col items-center justify-center py-8 text-center">
            <Inbox className="h-12 w-12 text-zinc-600 mb-3" />
            <p className="text-sm text-muted-foreground">{emptyMessage}</p>
          </div>
        ) : (
          <div className="space-y-2 max-h-[400px] overflow-y-auto">
            {data.map(item => renderItem(item))}
          </div>
        )}
      </CardContent>
    </Card>
  )
}
