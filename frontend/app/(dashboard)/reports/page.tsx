import { Card, CardContent, CardHeader, CardTitle } from '@/components/ui/card'

export default function ReportsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Historical Reports</h1>
        <p className="mt-2 text-gray-600">
          View and search through your past analyses
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>All Reports</CardTitle>
        </CardHeader>
        <CardContent>
          <p className="text-gray-500">No reports found. Start by analyzing a founder, legal document, or credit facility.</p>
        </CardContent>
      </Card>
    </div>
  )
}
