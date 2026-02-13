import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Users, FileText, CreditCard, TrendingUp } from 'lucide-react'
import Link from 'next/link'

export default function DashboardPage() {
  const stats = [
    { name: 'Total Analyses', value: '12', icon: TrendingUp, change: '+4.75%' },
    { name: 'Founder Reports', value: '5', icon: Users, change: '+2' },
    { name: 'Legal Documents', value: '4', icon: FileText, change: '+1' },
    { name: 'Credit Analyses', value: '3', icon: CreditCard, change: '+1' },
  ]

  const modules = [
    {
      title: 'Founder Research',
      description: 'Automated founder due diligence with LinkedIn, Twitter, and pitch deck analysis',
      href: '/dashboard/founder',
      icon: Users,
    },
    {
      title: 'Legal Document Translator',
      description: 'Plain-English translation of legal documents with risk assessment',
      href: '/dashboard/legal',
      icon: FileText,
    },
    {
      title: 'Credit Facility Analysis',
      description: 'Comprehensive credit agreement analysis with hidden cost identification',
      href: '/dashboard/credit',
      icon: CreditCard,
    },
  ]

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Welcome to PE Intelligence AI</h1>
        <p className="mt-2 text-gray-600">
          AI-powered intelligence platform for private equity professionals
        </p>
      </div>

      {/* Stats */}
      <div className="grid grid-cols-1 gap-6 sm:grid-cols-2 lg:grid-cols-4">
        {stats.map((stat) => (
          <Card key={stat.name}>
            <CardHeader className="flex flex-row items-center justify-between pb-2">
              <CardTitle className="text-sm font-medium text-gray-600">{stat.name}</CardTitle>
              <stat.icon className="h-4 w-4 text-gray-400" />
            </CardHeader>
            <CardContent>
              <div className="text-2xl font-bold">{stat.value}</div>
              <p className="text-xs text-green-600">{stat.change} from last month</p>
            </CardContent>
          </Card>
        ))}
      </div>

      {/* Modules */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Analysis Modules</h2>
        <div className="grid grid-cols-1 gap-6 lg:grid-cols-3">
          {modules.map((module) => (
            <Link key={module.title} href={module.href}>
              <Card className="h-full hover:shadow-lg transition-shadow cursor-pointer">
                <CardHeader>
                  <div className="flex items-center space-x-3">
                    <module.icon className="h-8 w-8 text-blue-600" />
                    <CardTitle>{module.title}</CardTitle>
                  </div>
                  <CardDescription className="mt-3">{module.description}</CardDescription>
                </CardHeader>
              </Card>
            </Link>
          ))}
        </div>
      </div>

      {/* Recent Activity */}
      <div>
        <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
        <Card>
          <CardContent className="pt-6">
            <div className="space-y-4">
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <Users className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="font-medium">Founder Analysis: John Doe</p>
                    <p className="text-sm text-gray-500">2 hours ago</p>
                  </div>
                </div>
                <span className="text-sm text-green-600">Completed</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <FileText className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="font-medium">Legal Document Translation</p>
                    <p className="text-sm text-gray-500">5 hours ago</p>
                  </div>
                </div>
                <span className="text-sm text-green-600">Completed</span>
              </div>
              <div className="flex items-center justify-between">
                <div className="flex items-center space-x-3">
                  <CreditCard className="h-5 w-5 text-gray-400" />
                  <div>
                    <p className="font-medium">Credit Facility Analysis</p>
                    <p className="text-sm text-gray-500">1 day ago</p>
                  </div>
                </div>
                <span className="text-sm text-green-600">Completed</span>
              </div>
            </div>
          </CardContent>
        </Card>
      </div>
    </div>
  )
}
