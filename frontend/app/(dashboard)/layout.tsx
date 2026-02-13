'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { cn } from '@/lib/utils'
import { FileText, Users, CreditCard, Archive, Settings, BarChart3 } from 'lucide-react'

const navigation = [
  { name: 'Dashboard', href: '/dashboard', icon: BarChart3 },
  { name: 'Founder Research', href: '/dashboard/founder', icon: Users },
  { name: 'Legal Translator', href: '/dashboard/legal', icon: FileText },
  { name: 'Credit Analysis', href: '/dashboard/credit', icon: CreditCard },
  { name: 'Reports', href: '/dashboard/reports', icon: Archive },
  { name: 'Settings', href: '/dashboard/settings', icon: Settings },
]

export default function DashboardLayout({
  children,
}: {
  children: React.ReactNode
}) {
  const pathname = usePathname()

  return (
    <div className="flex min-h-screen">
      {/* Sidebar */}
      <div className="w-64 bg-gray-900 text-white">
        <div className="p-6">
          <h1 className="text-2xl font-bold">PE Intelligence AI</h1>
        </div>
        <nav className="mt-6">
          {navigation.map((item) => {
            const isActive = pathname === item.href || pathname?.startsWith(item.href + '/')
            return (
              <Link
                key={item.name}
                href={item.href}
                className={cn(
                  'flex items-center px-6 py-3 text-sm font-medium transition-colors',
                  isActive
                    ? 'bg-gray-800 text-white border-l-4 border-blue-500'
                    : 'text-gray-300 hover:bg-gray-800 hover:text-white'
                )}
              >
                <item.icon className="mr-3 h-5 w-5" />
                {item.name}
              </Link>
            )
          })}
        </nav>
      </div>

      {/* Main content */}
      <div className="flex-1 bg-gray-50">
        <header className="bg-white shadow-sm">
          <div className="px-8 py-4">
            <div className="flex items-center justify-between">
              <h2 className="text-2xl font-semibold text-gray-800">
                {navigation.find((item) => item.href === pathname)?.name || 'Dashboard'}
              </h2>
              <div className="flex items-center space-x-4">
                <button className="text-sm text-gray-600 hover:text-gray-900">
                  Sign Out
                </button>
              </div>
            </div>
          </div>
        </header>
        <main className="p-8">{children}</main>
      </div>
    </div>
  )
}
