import axios from 'axios'

const API_URL = process.env.NEXT_PUBLIC_API_URL || 'http://localhost:8000'

export const api = axios.create({
  baseURL: API_URL,
  headers: {
    'Content-Type': 'application/json',
  },
})

// Founder Research APIs
export const founderApi = {
  ingest: (data: any) => api.post('/api/founder/ingest', data),
  analyze: (founderName: string, reportId?: string) => 
    api.post('/api/founder/analyze', null, { params: { founder_name: founderName, report_id: reportId } }),
  getReport: (reportId: string) => api.get(`/api/founder/report/${reportId}`),
  uploadPitchDeck: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/founder/upload-pitch-deck', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// Legal Assistant APIs
export const legalApi = {
  translate: (data: any) => api.post('/api/legal/translate', data),
  getReport: (reportId: string) => api.get(`/api/legal/report/${reportId}`),
  uploadDocument: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/legal/upload-document', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}

// Credit Analysis APIs
export const creditApi = {
  analyze: (data: any) => api.post('/api/credit/analyze', data),
  getReport: (reportId: string) => api.get(`/api/credit/report/${reportId}`),
  uploadAgreement: (file: File) => {
    const formData = new FormData()
    formData.append('file', file)
    return api.post('/api/credit/upload-agreement', formData, {
      headers: { 'Content-Type': 'multipart/form-data' },
    })
  },
}
