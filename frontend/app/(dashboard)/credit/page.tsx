'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { creditApi } from '@/lib/api'
import { Loader2, AlertTriangle, DollarSign } from 'lucide-react'

export default function CreditAnalysisPage() {
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState<any>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [filePath, setFilePath] = useState<string>('')

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setUploadedFile(file)
      try {
        const response = await creditApi.uploadAgreement(file)
        setFilePath(response.data.file_path)
      } catch (error) {
        console.error('Error uploading agreement:', error)
      }
    }
  }

  const handleAnalyze = async () => {
    if (!filePath) {
      alert('Please upload a credit agreement first')
      return
    }

    setLoading(true)
    try {
      const response = await creditApi.analyze({
        document_path: filePath,
      })
      setAnalysis(response.data)
    } catch (error) {
      console.error('Error analyzing credit facility:', error)
      alert('Error analyzing credit facility. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Credit Facility Analysis</h1>
        <p className="mt-2 text-gray-600">
          Comprehensive credit agreement analysis with hidden cost identification
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Upload Credit Agreement</CardTitle>
          <CardDescription>
            Upload a credit facility agreement PDF for comprehensive analysis
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Credit Agreement (PDF)</label>
            <div className="flex items-center space-x-2">
              <input
                type="file"
                accept=".pdf"
                onChange={handleFileUpload}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm file:border-0 file:bg-transparent file:text-sm file:font-medium cursor-pointer"
              />
              {uploadedFile && (
                <span className="text-sm text-green-600">✓ Uploaded</span>
              )}
            </div>
          </div>

          <Button onClick={handleAnalyze} disabled={loading || !uploadedFile} className="w-full">
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Analyzing...
              </>
            ) : (
              <>Analyze Credit Facility</>
            )}
          </Button>
        </CardContent>
      </Card>

      {analysis && (
        <Card>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
            <CardDescription>Credit facility comprehensive assessment</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Summary */}
            <div>
              <h3 className="font-semibold mb-2">Executive Summary</h3>
              <p className="text-gray-700">{analysis.summary}</p>
            </div>

            {/* Loan Details */}
            <div className="grid grid-cols-2 gap-4">
              <div className="border rounded-lg p-4">
                <div className="flex items-center space-x-2 mb-1">
                  <DollarSign className="h-4 w-4 text-gray-500" />
                  <span className="text-sm text-gray-600">Loan Amount</span>
                </div>
                <p className="text-xl font-bold">{analysis.loan_amount || 'Not specified'}</p>
              </div>
              <div className="border rounded-lg p-4">
                <span className="text-sm text-gray-600">Interest Rate</span>
                <p className="text-xl font-bold">{analysis.interest_rate || 'Not specified'}</p>
              </div>
              <div className="border rounded-lg p-4">
                <span className="text-sm text-gray-600">Margin</span>
                <p className="text-xl font-bold">{analysis.margin || 'Not specified'}</p>
              </div>
              <div className="border rounded-lg p-4">
                <span className="text-sm text-gray-600">Maturity Date</span>
                <p className="text-xl font-bold">{analysis.maturity_date || 'Not specified'}</p>
              </div>
            </div>

            {/* Overall Risk */}
            <div>
              <h3 className="font-semibold mb-2">Overall Risk Level</h3>
              <span className={`inline-block px-3 py-1 rounded-full text-sm font-medium ${
                analysis.risk_level === 'Low' ? 'bg-green-100 text-green-800' :
                analysis.risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                'bg-red-100 text-red-800'
              }`}>
                {analysis.risk_level}
              </span>
            </div>

            {/* Lawyer Required */}
            {analysis.lawyer_required && (
              <div className="bg-yellow-50 border border-yellow-200 rounded-md p-4">
                <div className="flex">
                  <AlertTriangle className="h-5 w-5 text-yellow-600 mr-2 flex-shrink-0" />
                  <div>
                    <p className="font-semibold text-yellow-800">Lawyer Review Recommended</p>
                    <p className="text-sm text-yellow-700 mt-1">{analysis.lawyer_required_reason}</p>
                  </div>
                </div>
              </div>
            )}

            {/* Covenants */}
            <div>
              <h3 className="font-semibold mb-3">Covenants ({analysis.covenants.length})</h3>
              <div className="space-y-3">
                {analysis.covenants.map((covenant: any, i: number) => (
                  <div key={i} className="border rounded-lg p-3">
                    <div className="flex justify-between items-start">
                      <div>
                        <h4 className="font-medium">{covenant.name}</h4>
                        <p className="text-sm text-gray-600 mt-1">{covenant.description}</p>
                        <span className="text-xs text-gray-500 mt-1 inline-block">
                          {covenant.type}
                        </span>
                      </div>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        covenant.risk_level === 'Low' ? 'bg-green-100 text-green-800' :
                        covenant.risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {covenant.risk_level}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Risk Heatmap */}
            <div>
              <h3 className="font-semibold mb-3">Risk Heatmap</h3>
              <div className="grid grid-cols-2 gap-3">
                {Object.entries(analysis.risk_heatmap).map(([key, level]: [string, any]) => (
                  <div key={key} className="border rounded-lg p-3">
                    <div className="flex justify-between items-center">
                      <span className="text-sm capitalize">{key.replace('_', ' ')}</span>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        level === 'Low' ? 'bg-green-100 text-green-800' :
                        level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {level}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Hidden Costs */}
            {analysis.hidden_costs.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Hidden Costs</h3>
                <ul className="list-disc list-inside space-y-1">
                  {analysis.hidden_costs.map((cost: string, i: number) => (
                    <li key={i} className="text-gray-700">{cost}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Negotiation Points */}
            {analysis.negotiation_points.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Negotiation Leverage Points</h3>
                <ul className="list-disc list-inside space-y-1">
                  {analysis.negotiation_points.map((point: string, i: number) => (
                    <li key={i} className="text-gray-700">{point}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Cost Saving Opportunities */}
            {analysis.cost_saving_opportunities.length > 0 && (
              <div className="bg-green-50 border border-green-200 rounded-md p-4">
                <h3 className="font-semibold text-green-800 mb-2">Cost-Saving Opportunities</h3>
                <ul className="list-disc list-inside space-y-1">
                  {analysis.cost_saving_opportunities.map((opp: string, i: number) => (
                    <li key={i} className="text-green-700 text-sm">{opp}</li>
                  ))}
                </ul>
              </div>
            )}

            {/* Worst Case Scenario */}
            <div className="bg-red-50 border border-red-200 rounded-md p-4">
              <h3 className="font-semibold text-red-800 mb-2">Worst-Case Scenario</h3>
              <p className="text-sm text-red-700">{analysis.worst_case_scenario}</p>
            </div>

            {/* Flags */}
            {(analysis.aggressive_terms.length > 0 || analysis.unusual_covenants.length > 0) && (
              <div>
                <h3 className="font-semibold mb-3">⚠️ Alerts & Flags</h3>
                <div className="space-y-3">
                  {analysis.aggressive_terms.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium text-red-700 mb-1">Aggressive Terms</h4>
                      <ul className="list-disc list-inside text-sm">
                        {analysis.aggressive_terms.map((term: string, i: number) => (
                          <li key={i} className="text-gray-700">{term}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                  {analysis.unusual_covenants.length > 0 && (
                    <div>
                      <h4 className="text-sm font-medium text-yellow-700 mb-1">Unusual Covenants</h4>
                      <ul className="list-disc list-inside text-sm">
                        {analysis.unusual_covenants.map((covenant: string, i: number) => (
                          <li key={i} className="text-gray-700">{covenant}</li>
                        ))}
                      </ul>
                    </div>
                  )}
                </div>
              </div>
            )}

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
