import { motion } from 'framer-motion'
import { useState } from 'react'
import api from '../api'
import { Download, FileText, CheckCircle, User, Clock, MapPin } from 'lucide-react'

function ResumeGenerator({ profiles, language = 'en' }) {
  const [selectedProfileId, setSelectedProfileId] = useState('')
  const [downloadUrl, setDownloadUrl] = useState('')
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleGenerate = async () => {
    if (!selectedProfileId) return
    
    setLoading(true)
    setError('')

    try {
      const response = await api.post(`/api/resume/${selectedProfileId}`)
      const fullUrl = `${import.meta.env.VITE_API_URL}${response.data.download_url}`
      setDownloadUrl(fullUrl)
    } catch (err) {
      setError('Failed to generate resume. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const handleDownload = () => {
    if (downloadUrl) {
      window.open(downloadUrl, '_blank')
    }
  }

  if (profiles.length === 0) {
    return (
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <FileText className="w-16 h-16 text-neutral-300 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-neutral-900 mb-2">No Profiles Yet</h2>
          <p className="text-neutral-500 mb-6">Create a profile first to generate your resume.</p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-4xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-12 h-12 bg-neutral-900 rounded-lg flex items-center justify-center shadow-md">
            <FileText className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-neutral-900">
              {language === 'hi' ? 'रिज्यूमे जनरेट करें' : 'Generate Resume'}
            </h2>
            <p className="text-neutral-500">
              {language === 'hi' ? 'एक प्रोफ़ाइल चुनें और पेशेवर PDF रिज्यूमे डाउनलोड करें' : 'Select a profile and download a professional PDF resume'}
            </p>
          </div>
        </div>

        {error && (
          <div className="bg-neutral-50 border border-neutral-200 text-neutral-900 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <div className="space-y-4">
          <div>
            <label htmlFor="profile" className="block text-sm font-medium text-neutral-700 mb-2">
              {language === 'hi' ? 'प्रोफ़ाइल चुनें' : 'Select Profile'}
            </label>
            <select
              id="profile"
              value={selectedProfileId}
              onChange={(e) => setSelectedProfileId(parseInt(e.target.value))}
              className="w-full px-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-neutral-900 focus:border-transparent"
            >
              <option value="">-- {language === 'hi' ? 'प्रोफ़ाइल चुनें' : 'Choose a profile'} --</option>
              {(Array.isArray(profiles) ? profiles : []).map((profile) => (
                <option key={profile.id} value={profile.id}>
                  {profile.name} - {profile.recommended_job_category || 'General'}
                </option>
              ))}
            </select>
          </div>

          <button
            onClick={handleGenerate}
            disabled={!selectedProfileId || loading}
            className="w-full bg-neutral-900 text-white font-semibold py-4 px-6 rounded-lg hover:shadow-lg transform hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                <span>{language === 'hi' ? 'रिज्यूमे बना रहा हूं...' : 'Generating Resume...'}</span>
              </>
            ) : (
              <>
                <FileText className="w-5 h-5" />
                <span>{language === 'hi' ? 'PDF रिज्यूमे बनाएं' : 'Generate PDF Resume'}</span>
              </>
            )}
          </button>
        </div>
      </div>

          {downloadUrl && (
        <motion.div
          initial={{ opacity: 0, scale: 0.95 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.3 }}
          className="bg-white rounded-xl shadow-lg p-8 border-2 border-neutral-200"
        >
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-4">
              <div className="w-16 h-16 bg-neutral-100 rounded-full flex items-center justify-center">
                <CheckCircle className="w-8 h-8 text-neutral-900" />
              </div>
              <div>
                <h3 className="text-xl font-bold text-neutral-900">
                  {language === 'hi' ? 'रिज्यूमे तैयार है!' : 'Resume Ready!'}
                </h3>
                <p className="text-neutral-500">
                  {language === 'hi' ? 'आपका पेशेवर रिज्यूमे सफलतापूर्वक तैयार कर लिया गया है।' : 'Your professional resume has been generated successfully.'}
                </p>
              </div>
            </div>
            <motion.button
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              onClick={handleDownload}
              className="flex items-center space-x-2 bg-neutral-900 text-white px-6 py-3 rounded-lg hover:shadow-lg transition-all"
            >
              <Download className="w-5 h-5" />
              <span>{language === 'hi' ? 'PDF डाउनलोड करें' : 'Download PDF'}</span>
            </motion.button>
          </div>
        </motion.div>
      )}

      <div className="mt-8 grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-neutral-900 mb-4">
            {language === 'hi' ? 'रिज्यूमे प्रारूप के बारे में' : 'About Resume Format'}
          </h3>
          <ul className="space-y-3 text-neutral-600">
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-neutral-900 mt-0.5" />
              <span>{language === 'hi' ? 'ATS-फ्रेंडली फॉर्मेट' : 'ATS-friendly format'}</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-neutral-900 mt-0.5" />
              <span>{language === 'hi' ? 'पेशेवर लेआउट' : 'Professional layout'}</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-neutral-900 mt-0.5" />
              <span>{language === 'hi' ? 'सभी निकाले गए कौशल शामिल हैं' : 'Includes all extracted skills'}</span>
            </li>
            <li className="flex items-start space-x-2">
              <CheckCircle className="w-5 h-5 text-neutral-900 mt-0.5" />
              <span>{language === 'hi' ? 'नियोक्ताओं के साथ साझा करने के लिए तैयार' : 'Ready to share with employers'}</span>
            </li>
          </ul>
        </div>

        <div className="bg-white rounded-xl shadow p-6">
          <h3 className="text-lg font-semibold text-neutral-900 mb-4">
            {language === 'hi' ? 'हाल के प्रोफ़ाइल' : 'Recent Profiles'}
          </h3>
          <div className="space-y-3">
            {profiles.slice(0, 5).map((profile) => (
              <div key={profile.id} className="flex items-center justify-between p-3 bg-neutral-50 rounded-lg">
                <div className="flex items-center space-x-3">
                  <User className="w-5 h-5 text-neutral-400" />
                  <div>
                    <p className="font-medium text-neutral-900">{profile.name}</p>
                    <p className="text-sm text-neutral-500">{profile.recommended_job_category || 'General'}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  )
}

export default ResumeGenerator