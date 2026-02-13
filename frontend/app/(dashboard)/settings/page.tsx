import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Input } from '@/components/ui/input'
import { Button } from '@/components/ui/button'

export default function SettingsPage() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Settings</h1>
        <p className="mt-2 text-gray-600">
          Manage your account and application preferences
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>API Configuration</CardTitle>
          <CardDescription>Configure your API keys and endpoints</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">OpenAI API Key</label>
            <Input type="password" placeholder="sk-..." />
          </div>
          <div>
            <label className="block text-sm font-medium mb-2">Backend API URL</label>
            <Input placeholder="http://localhost:8000" />
          </div>
          <Button>Save Settings</Button>
        </CardContent>
      </Card>

      <Card>
        <CardHeader>
          <CardTitle>Privacy & Compliance</CardTitle>
          <CardDescription>Data retention and privacy settings</CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium">LinkedIn Scraping</h4>
              <p className="text-sm text-gray-600">Enable LinkedIn profile scraping</p>
            </div>
            <input type="checkbox" className="h-4 w-4" />
          </div>
          <div className="flex items-center justify-between">
            <div>
              <h4 className="font-medium">Twitter Scraping</h4>
              <p className="text-sm text-gray-600">Enable Twitter profile scraping</p>
            </div>
            <input type="checkbox" className="h-4 w-4" />
          </div>
          <div className="border-t pt-4">
            <p className="text-sm text-gray-600">
              Data retention period: 90 days
            </p>
          </div>
        </CardContent>
      </Card>
    </div>
  )
}
