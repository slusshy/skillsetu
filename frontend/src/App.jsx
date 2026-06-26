import { useState, useEffect } from 'react'
import { api } from './api'
import ProfileBuilder from './components/ProfileBuilder'
import ResumeGenerator from './components/ResumeGenerator'
import JobMatcher from './components/JobMatcher'

function App() {
  const [activeTab, setActiveTab] = useState('profile')
  const [profiles, setProfiles] = useState([])
  const [loading, setLoading] = useState(true)
  const [language, setLanguage] = useState('en')

  useEffect(() => {
    fetchProfiles()
  }, [])

  const fetchProfiles = async () => {
    try {
      const response = await api.get('/api/profiles')
      setProfiles(Array.isArray(response.data) ? response.data : [])
    } catch (err) {
      console.error('Failed to fetch profiles')
      setProfiles([])
    } finally {
      setLoading(false)
    }
  }

  const handleProfileCreated = (newProfile) => {
    setProfiles(prev => [newProfile, ...prev])
  }

  const tabs = [
    { id: 'profile', label: 'Profile Builder', icon: '👤' },
    { id: 'resume', label: 'Resume Generator', icon: '📄' },
    { id: 'jobs', label: 'Job Matching', icon: '💼' },
  ]

  return (
    <div className="min-h-screen bg-white text-neutral-900">
      {/* Header */}
      <header className="bg-white border-b border-neutral-200 sticky top-0 z-40">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-4">
          <div className="flex items-center justify-between">
            <div className="flex items-center space-x-3">
              <div className="w-10 h-10 bg-neutral-900 rounded-lg flex items-center justify-center text-white font-bold text-xl shadow-md">
                S
              </div>
              <div>
                <h1 className="text-2xl font-bold tracking-tight text-neutral-900">SkillSetu AI</h1>
                <p className="text-sm text-neutral-500">Professional Identity Builder</p>
              </div>
            </div>
            <div className="flex items-center space-x-4">
              <div className="text-sm text-neutral-500 hidden sm:block">
                {profiles.length > 0 && `${profiles.length} profile${profiles.length > 1 ? 's' : ''} created`}
              </div>
              <select
                value={language}
                onChange={(e) => setLanguage(e.target.value)}
                className="px-3 py-2 border border-neutral-300 rounded-lg text-sm focus:ring-2 focus:ring-neutral-900 focus:border-transparent bg-white"
              >
                <option value="en">English</option>
                <option value="hi">हिन्दी</option>
              </select>
            </div>
          </div>
        </div>
      </header>

      {/* Navigation Tabs */}
      <nav className="bg-white border-b border-neutral-200 sticky top-[73px] z-30">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="flex space-x-8">
            {tabs.map((tab) => (
              <button
                key={tab.id}
                onClick={() => setActiveTab(tab.id)}
                className={`py-4 px-1 border-b-2 font-medium text-sm transition-colors ${
                  activeTab === tab.id
                    ? 'border-neutral-900 text-neutral-900'
                    : 'border-transparent text-neutral-400 hover:text-neutral-600 hover:border-neutral-300'
                }`}
              >
                <span className="mr-2">{tab.icon}</span>
                {tab.label}
              </button>
            ))}
          </div>
        </div>
      </nav>

      {/* Content */}
      <main className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {loading ? (
          <div className="flex items-center justify-center py-20">
            <div className="w-8 h-8 border-4 border-neutral-900 border-t-transparent rounded-full animate-spin" />
          </div>
        ) : (
          <div className="page-enter">
            {activeTab === 'profile' && (
              <ProfileBuilder onProfileCreated={handleProfileCreated} language={language} />
            )}
            {activeTab === 'resume' && (
              <ResumeGenerator profiles={profiles} language={language} />
            )}
            {activeTab === 'jobs' && (
              <JobMatcher profiles={profiles} language={language} />
            )}
          </div>
        )}
      </main>

      {/* Footer */}
      <footer className="bg-neutral-50 border-t border-neutral-200 mt-12">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-6">
          <p className="text-center text-neutral-500 text-sm">
            SkillSetu AI - Built with React, FastAPI, Ollama & SQLite
          </p>
          <p className="text-center text-neutral-400 text-xs mt-2">
            Designed for informal workers. No paid APIs. Fully local.
          </p>
        </div>
      </footer>

    </div>
  )
}

export default App
