import { useState, useEffect } from 'react'
import api from '../api'
import { Briefcase, TrendingUp, AlertCircle, CheckCircle, XCircle, Search } from 'lucide-react'

function JobMatcher({ profiles, language = 'en' }) {
  const [selectedProfileId, setSelectedProfileId] = useState('')
  const [matches, setMatches] = useState([])
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleFindMatches = async () => {
    if (!selectedProfileId) return

    setLoading(true)
    setError('')
    setMatches([])

    try {
      const response = await api.get(`/api/profile/${selectedProfileId}/matches`)
      setMatches(response.data)
    } catch (err) {
      setError('Failed to find job matches. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  const getMatchColor = (percentage) => {
    if (percentage >= 80) return 'text-neutral-900 bg-neutral-100'
    if (percentage >= 50) return 'text-neutral-700 bg-neutral-50'
    return 'text-neutral-600 bg-neutral-100'
  }

  const getMatchLabel = (percentage) => {
    if (percentage >= 80) return 'Excellent Match'
    if (percentage >= 50) return 'Good Match'
    return 'Partial Match'
  }

  if (!Array.isArray(profiles) || profiles.length === 0) {
    return (
      <div className="max-w-3xl mx-auto">
        <div className="bg-white rounded-xl shadow-lg p-12 text-center">
          <Briefcase className="w-16 h-16 text-neutral-300 mx-auto mb-4" />
          <h2 className="text-2xl font-bold text-neutral-900 mb-2">
            {language === 'hi' ? 'अभी कोई प्रोफ़ाइल नहीं है' : 'No Profiles Yet'}
          </h2>
          <p className="text-neutral-500 mb-6">
            {language === 'hi' ? 'मैचिंग नौकरियां खोजने के लिए पहले एक प्रोफ़ाइल बनाएं।' : 'Create a profile first to find matching jobs.'}
          </p>
        </div>
      </div>
    )
  }

  return (
    <div className="max-w-5xl mx-auto">
      <div className="bg-white rounded-xl shadow-lg p-8 mb-6">
        <div className="flex items-center space-x-3 mb-6">
          <div className="w-12 h-12 bg-neutral-900 rounded-lg flex items-center justify-center shadow-md">
            <Briefcase className="w-6 h-6 text-white" />
          </div>
          <div>
            <h2 className="text-2xl font-bold text-neutral-900">
              {language === 'hi' ? 'मैचिंग नौकरियां खोजें' : 'Find Matching Jobs'}
            </h2>
            <p className="text-neutral-500">
              {language === 'hi' ? 'अपने कौशल से मैच करने वाले रोजगार के अवसर खोजें' : 'Discover job opportunities that match your skills'}
            </p>
          </div>
        </div>

        {error && (
          <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-3 rounded-lg mb-6">
            {error}
          </div>
        )}

        <div className="flex flex-col md:flex-row gap-4">
          <div className="flex-1">
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
            {(Array.isArray(profiles) ? profiles : []).slice(0,5).map((profile) => (
                <option key={profile.id} value={profile.id}>
                  {profile.name} - {profile.recommended_job_category || 'General'}
                </option>
              ))}
            </select>
          </div>

          <div className="flex items-end">
            <button
              onClick={handleFindMatches}
              disabled={!selectedProfileId || loading}
              className="w-full md:w-auto bg-neutral-900 text-white font-semibold py-3 px-8 rounded-lg hover:shadow-lg transform hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
            >
              {loading ? (
                <>
                  <div className="w-5 h-5 border-2 border-white border-t-transparent rounded-full animate-spin" />
                  <span>{language === 'hi' ? 'मैच खोज रहे हैं...' : 'Finding Matches...'}</span>
                </>
              ) : (
                <>
                  <Search className="w-5 h-5" />
                  <span>{language === 'hi' ? 'नौकरियां खोजें' : 'Find Jobs'}</span>
                </>
              )}
            </button>
          </div>
        </div>
      </div>

      {matches.length > 0 && (
        <div className="space-y-4">
          <div className="bg-white rounded-xl shadow-lg p-6">
            <h3 className="text-lg font-semibold text-neutral-900 mb-4">
              {language === 'hi' ? 'नौकरी मैच मिला' : 'Job Matches Found'}
            </h3>
            <div className="grid grid-cols-1 gap-4">
              {matches.map((job, index) => (
                <div
                  key={index}
                  className="border border-neutral-200 rounded-lg p-6 hover:shadow-md transition-shadow bg-white"
                >
                  <div className="flex items-start justify-between mb-2">
                    <div className="flex items-start space-x-4">
                      <div className="w-12 h-12 bg-neutral-100 rounded-lg flex items-center justify-center flex-shrink-0">
                        <Briefcase className="w-6 h-6 text-neutral-700" />
                      </div>
                      <div>
                        <h4 className="text-lg font-semibold text-neutral-900">{job.title}</h4>
                        <p className="text-sm text-neutral-600">{job.company} • {job.location}</p>
                        {(job.salary_min || job.salary_max) && (
                          <p className="text-sm text-neutral-500 mt-1">
                            {job.salary_min && job.salary_max
                              ? `₹${job.salary_min} - ₹${job.salary_max}`
                              : job.salary_min
                                ? `From ₹${job.salary_min}`
                                : `Up to ₹${job.salary_max}`}
                          </p>
                        )}
                        <span
                          className={`inline-flex items-center px-3 py-1 rounded-full text-sm font-medium mt-2 ${getMatchColor(
                            job.match_percentage
                          )}`}
                        >
                          <TrendingUp className="w-4 h-4 mr-1" />
                          {job.match_percentage}% Match - {getMatchLabel(job.match_percentage)}
                        </span>
                      </div>
                    </div>
                    {job.redirect_url && (
                      <a
                        href={job.redirect_url}
                        target="_blank"
                        rel="noreferrer"
                        className="text-sm bg-white border border-neutral-300 text-neutral-700 px-3 py-2 rounded-lg hover:bg-neutral-50 transition-colors"
                      >
                        Apply
                      </a>
                    )}
                  </div>

                  {job.description && (
                    <p className="mt-3 text-sm text-neutral-700 line-clamp-3">{job.description}</p>
                  )}

                  {job.missing_skills.length > 0 && (
                    <div className="mt-4">
                      <div className="flex items-start space-x-2">
                        <AlertCircle className="w-5 h-5 text-neutral-500 mt-0.5 flex-shrink-0" />
                        <div className="flex-1">
                          <p className="text-sm font-medium text-neutral-700 mb-2">
                            {language === 'hi' ? 'विकसित करने के लिए कौशल:' : 'Skills to develop:'}
                          </p>
            <div className="flex flex-wrap gap-2">
                            {(Array.isArray(job.missing_skills) ? job.missing_skills : []).map((skill, i) => (
                              <span
                                key={i}
                                className="inline-flex items-center px-3 py-1 rounded-full text-sm bg-neutral-100 text-neutral-700 border border-neutral-200"
                              >
                                <XCircle className="w-3 h-3 mr-1" />
                                {skill}
                              </span>
                            ))}
                          </div>
                        </div>
                      </div>
                    </div>
                  )}

                  {job.missing_skills.length === 0 && (
                    <div className="mt-4 flex items-start space-x-2">
                      <CheckCircle className="w-5 h-5 text-neutral-900 mt-0.5" />
                      <p className="text-sm text-neutral-900 font-medium">
                        {language === 'hi' ? 'आपके पास इस रोल के लिए सभी आवश्यक कौशल हैं!' : 'You have all the required skills for this role!'}
                      </p>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </div>

          <div className="bg-neutral-50 border border-neutral-200 rounded-xl p-6">
            <h3 className="text-lg font-semibold text-neutral-900 mb-2">
              {language === 'hi' ? '💡 करियर सुझाव' : '💡 Career Tips'}
            </h3>
            <ul className="list-disc list-inside space-y-2 text-neutral-700">
              <li>{language === 'hi' ? 'अपने शीर्ष मैच के लिए गुम कौशल विकसित करने पर ध्यान दें' : 'Focus on developing the missing skills for your top matches'}</li>
              <li>{language === 'hi' ? 'ऑनलाइन कोर्स या प्रमाणपत्र लेने पर विचार करें' : 'Consider taking online courses or certifications'}</li>
              <li>{language === 'hi' ? 'स्वयंसेवक कार्य या इंटर्नशिप के माध्यम से व्यावहारिक अनुभव हासिल करें' : 'Gain practical experience through volunteer work or internships'}</li>
              <li>{language === 'hi' ? 'अपने लक्षित उद्योग में पेशेवरों के साथ नेटवर्क बनाएं' : 'Network with professionals in your target industry'}</li>
            </ul>
          </div>
        </div>
      )}
    </div>
  )
}

export default JobMatcher