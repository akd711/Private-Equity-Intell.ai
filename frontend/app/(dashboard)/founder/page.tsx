'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { Input } from '@/components/ui/input'
import { founderApi } from '@/lib/api'
import { Upload, Loader2 } from 'lucide-react'

export default function FounderResearchPage() {
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState<any>(null)
  const [formData, setFormData] = useState({
    founderName: '',
    linkedinUrl: '',
    twitterUrl: '',
    userNotes: '',
  })
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setUploadedFile(file)
      try {
        await founderApi.uploadPitchDeck(file)
      } catch (error) {
        console.error('Error uploading pitch deck:', error)
      }
    }
  }

  const handleAnalyze = async () => {
    if (!formData.founderName) {
      alert('Please enter a founder name')
      return
    }

    setLoading(true)
    try {
      // First ingest data
      await founderApi.ingest({
        founder_name: formData.founderName,
        linkedin_url: formData.linkedinUrl || null,
        twitter_url: formData.twitterUrl || null,
        user_notes: formData.userNotes || null,
        consent_obtained: true,
      })

      // Then analyze
      const response = await founderApi.analyze(formData.founderName)
      setAnalysis(response.data)
    } catch (error) {
      console.error('Error analyzing founder:', error)
      alert('Error analyzing founder. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Founder Research</h1>
        <p className="mt-2 text-gray-600">
          Automated founder due diligence with comprehensive analysis
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Founder Information</CardTitle>
          <CardDescription>
            Enter founder details for automated research and analysis
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Founder Name *</label>
            <Input
              placeholder="John Doe"
              value={formData.founderName}
              onChange={(e) => setFormData({ ...formData, founderName: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">LinkedIn URL</label>
            <Input
              placeholder="https://linkedin.com/in/johndoe"
              value={formData.linkedinUrl}
              onChange={(e) => setFormData({ ...formData, linkedinUrl: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Twitter/X URL</label>
            <Input
              placeholder="https://twitter.com/johndoe"
              value={formData.twitterUrl}
              onChange={(e) => setFormData({ ...formData, twitterUrl: e.target.value })}
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Pitch Deck (PDF)</label>
            <div className="flex items-center space-x-2">
              <Input
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                className="cursor-pointer"
              />
              {uploadedFile && (
                <span className="text-sm text-green-600">✓ Uploaded</span>
              )}
            </div>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Your Notes (Optional)</label>
            <textarea
              className="w-full min-h-[100px] rounded-md border border-input bg-background px-3 py-2 text-sm"
              placeholder="Add any additional context or observations..."
              value={formData.userNotes}
              onChange={(e) => setFormData({ ...formData, userNotes: e.target.value })}
            />
          </div>

          <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
            <p className="text-sm text-yellow-800">
              ⚠️ <strong>Data Collection Consent:</strong> By proceeding, you confirm that you have
              obtained proper consent to collect and analyze this data in accordance with privacy
              regulations.
            </p>
          </div>

          <Button onClick={handleAnalyze} disabled={loading} className="w-full">
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>Analyze Founder</>
            )}
          </Button>
        </CardContent>
      </Card>

      {analysis && (
        <Card>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
            <CardDescription>Founder assessment for {formData.founderName}</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Summary */}
            <div>
              <h3 className="font-semibold mb-2">Executive Summary</h3>
              <p className="text-gray-700">{analysis.summary}</p>
            </div>

            {/* Scorecard */}
            <div>
              <h3 className="font-semibold mb-3">Scorecard</h3>
              <div className="grid grid-cols-2 gap-4">
                {Object.entries(analysis.scorecard).map(([key, value]) => (
                  <div key={key} className="border rounded-lg p-3">
                    <div className="text-sm text-gray-600 capitalize">{key.replace('_', ' ')}</div>
                    <div className="text-2xl font-bold text-blue-600">{Number(value).toFixed(1)}/10</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Risk Level */}
            <div>
              <h3 className="font-semibold mb-2">Risk Level</h3>
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                analysis.risk_level === 'Low' ? 'bg-green-100 text-green-800' :
                analysis.risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {analysis.risk_level}
              </span>
            </div>

            {/* Key Points */}
            <div>
              <h3 className="font-semibold mb-2">Key Points</h3>
              <ul className="list-disc list-inside space-y-1">
                {analysis.key_points.map((point: string, i: number) => (
                  <li key={i} className="text-gray-700">{point}</li>
                ))}
              </ul>
            </div>

            {/* Strengths & Risks */}
            <div className="grid grid-cols-2 gap-4">
              <div>
                <h3 className="font-semibold mb-2 text-green-700">Key Strengths</h3>
                <ul className="list-disc list-inside space-y-1">
                  {analysis.key_strengths.map((strength: string, i: number) => (
                    <li key={i} className="text-gray-700">{strength}</li>
                  ))}
                </ul>
              </div>
              <div>
                <h3 className="font-semibold mb-2 text-red-700">Key Risks</h3>
                <ul className="list-disc list-inside space-y-1">
                  {analysis.key_risks.map((risk: string, i: number) => (
                    <li key={i} className="text-gray-700">{risk}</li>
                  ))}
                </ul>
              </div>
            </div>

            {/* Suggested Questions */}
            <div>
              <h3 className="font-semibold mb-2">Suggested Due Diligence Questions</h3>
              <ol className="list-decimal list-inside space-y-1">
                {analysis.suggested_questions.map((question: string, i: number) => (
                  <li key={i} className="text-gray-700">{question}</li>
                ))}
              </ol>
            </div>

            {/* Confidence Score */}
            <div className="border-t pt-4">
              <div className="flex justify-between items-center">
                <span className="text-sm text-gray-600">Confidence Score</span>
                <span className="font-semibold">{(analysis.confidence_score * 100).toFixed(0)}%</span>
              </div>
              <div className="mt-2 w-full bg-gray-200 rounded-full h-2">
                <div
                  className="bg-blue-600 h-2 rounded-full"
                  style={{ width: `${analysis.confidence_score * 100}%` }}
                />
              </div>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
