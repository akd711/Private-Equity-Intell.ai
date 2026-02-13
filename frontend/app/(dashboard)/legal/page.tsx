'use client'

import { useState } from 'react'
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from '@/components/ui/card'
import { Button } from '@/components/ui/button'
import { legalApi } from '@/lib/api'
import { Loader2, AlertTriangle } from 'lucide-react'

export default function LegalTranslatorPage() {
  const [loading, setLoading] = useState(false)
  const [analysis, setAnalysis] = useState<any>(null)
  const [uploadedFile, setUploadedFile] = useState<File | null>(null)
  const [filePath, setFilePath] = useState<string>('')

  const handleFileUpload = async (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0]
    if (file) {
      setUploadedFile(file)
      try {
        const response = await legalApi.uploadDocument(file)
        setFilePath(response.data.file_path)
      } catch (error) {
        console.error('Error uploading document:', error)
      }
    }
  }

  const handleTranslate = async () => {
    if (!filePath) {
      alert('Please upload a document first')
      return
    }

    setLoading(true)
    try {
      const response = await legalApi.translate({
        document_path: filePath,
        document_type: 'contract',
      })
      setAnalysis(response.data)
    } catch (error) {
      console.error('Error translating document:', error)
      alert('Error translating document. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold">Legal Document Translator</h1>
        <p className="mt-2 text-gray-600">
          Plain-English translation of legal documents with risk assessment
        </p>
      </div>

      <Card>
        <CardHeader>
          <CardTitle>Upload Legal Document</CardTitle>
          <CardDescription>
            Upload a PDF, DOCX, or TXT legal document for analysis
          </CardDescription>
        </CardHeader>
        <CardContent className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Legal Document</label>
            <div className="flex items-center space-x-2">
              <input
                type="file"
                accept=".pdf,.docx,.txt"
                onChange={handleFileUpload}
                className="flex h-10 w-full rounded-md border border-input bg-background px-3 py-2 text-sm file:border-0 file:bg-transparent file:text-sm file:font-medium cursor-pointer"
              />
              {uploadedFile && (
                <span className="text-sm text-green-600">✓ Uploaded</span>
              )}
            </div>
          </div>

          <div className="bg-red-50 border border-red-200 rounded-md p-4">
            <div className="flex">
              <AlertTriangle className="h-5 w-5 text-red-600 mr-2 flex-shrink-0" />
              <div className="text-sm text-red-800">
                <p className="font-semibold mb-1">⚠️ LEGAL DISCLAIMER</p>
                <p>
                  This analysis is provided for informational purposes only and does not constitute
                  legal advice. Always consult with a qualified attorney before making any legal
                  decisions. This tool uses AI and may contain errors or misinterpretations.
                </p>
              </div>
            </div>
          </div>

          <Button onClick={handleTranslate} disabled={loading || !uploadedFile} className="w-full">
            {loading ? (
              <>
                <Loader2 className="mr-2 h-4 w-4 animate-spin" />
                Translating...
              </>
            ) : (
              <>Translate to Plain English</>
            )}
          </Button>
        </CardContent>
      </Card>

      {analysis && (
        <Card>
          <CardHeader>
            <CardTitle>Analysis Results</CardTitle>
            <CardDescription>Plain-English translation and risk assessment</CardDescription>
          </CardHeader>
          <CardContent className="space-y-6">
            {/* Summary */}
            <div>
              <h3 className="font-semibold mb-2">Executive Summary</h3>
              <p className="text-gray-700">{analysis.summary}</p>
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

            {/* Key Points */}
            <div>
              <h3 className="font-semibold mb-2">Key Points</h3>
              <ul className="list-disc list-inside space-y-1">
                {analysis.key_points.map((point: string, i: number) => (
                  <li key={i} className="text-gray-700">{point}</li>
                ))}
              </ul>
            </div>

            {/* Clauses */}
            <div>
              <h3 className="font-semibold mb-3">Clause Analysis</h3>
              <div className="space-y-4">
                {analysis.clauses.slice(0, 5).map((clause: any, i: number) => (
                  <div key={i} className="border rounded-lg p-4">
                    <div className="flex justify-between items-start mb-2">
                      <h4 className="font-medium">Clause {clause.clause_id}</h4>
                      <span className={`px-2 py-1 rounded text-xs font-medium ${
                        clause.risk_level === 'Low' ? 'bg-green-100 text-green-800' :
                        clause.risk_level === 'Medium' ? 'bg-yellow-100 text-yellow-800' :
                        'bg-red-100 text-red-800'
                      }`}>
                        {clause.risk_level}
                      </span>
                    </div>
                    
                    <div className="space-y-2">
                      <div>
                        <p className="text-sm font-semibold text-gray-600">TL;DR</p>
                        <p className="text-sm text-gray-700">{clause.tldr}</p>
                      </div>
                      
                      <div>
                        <p className="text-sm font-semibold text-gray-600">Plain English</p>
                        <p className="text-sm text-gray-700">{clause.explanation}</p>
                      </div>
                      
                      {clause.business_impact.length > 0 && (
                        <div>
                          <p className="text-sm font-semibold text-gray-600">Business Impact</p>
                          <ul className="text-sm text-gray-700 list-disc list-inside">
                            {clause.business_impact.map((impact: string, j: number) => (
                              <li key={j}>{impact}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Suggested Redlines */}
            {analysis.redlines.length > 0 && (
              <div>
                <h3 className="font-semibold mb-2">Suggested Redlines</h3>
                <ul className="list-disc list-inside space-y-1">
                  {analysis.redlines.map((redline: string, i: number) => (
                    <li key={i} className="text-gray-700">{redline}</li>
                  ))}
                </ul>
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

            {/* Legal Disclaimer */}
            <div className="bg-gray-50 border border-gray-200 rounded-md p-4">
              <pre className="text-xs text-gray-600 whitespace-pre-wrap font-sans">
                {analysis.legal_disclaimer}
              </pre>
            </div>
          </CardContent>
        </Card>
      )}
    </div>
  )
}
