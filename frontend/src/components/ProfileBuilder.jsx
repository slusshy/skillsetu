import { useState } from 'react'
import api from '../api'
import { motion } from 'framer-motion'
import { Loader2, User, MapPin, Calendar, FileText, Sparkles } from 'lucide-react'

function ProfileBuilder({ onProfileCreated, language = 'en' }) {
  const [formData, setFormData] = useState({
    name: '',
    age: '',
    location: '',
    work_experience: ''
  })
  const [loading, setLoading] = useState(false)
  const [error, setError] = useState('')

  const handleChange = (e) => {
    setFormData(prev => ({
      ...prev,
      [e.target.name]: e.target.value
    }))
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    setLoading(true)
    setError('')

    try {
      const response = await api.post('/api/profile', {
        name: formData.name,
        age: formData.age ? parseInt(formData.age) : null,
        location: formData.location || null,
        work_experience: formData.work_experience,
        language
      })

      onProfileCreated(response.data)
      setFormData({ name: '', age: '', location: '', work_experience: '' })
    } catch (err) {
      setError(err.response?.data?.detail || 'Failed to create profile. Please try again.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="max-w-3xl mx-auto">
      <motion.div
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.4 }}
        className="bg-white rounded-xl shadow-lg border border-neutral-200 p-8"
      >
        <div className="flex items-center space-x-3 mb-6">
          <motion.div
            whileHover={{ scale: 1.05 }}
            className="w-12 h-12 bg-neutral-900 rounded-lg flex items-center justify-center shadow-md"
          >
            <Sparkles className="w-6 h-6 text-white" />
          </motion.div>
          <div>
            <h2 className="text-2xl font-bold tracking-tight text-neutral-900">
              {language === 'hi' ? 'अपना पेशेवर प्रोफ़ाइल बनाएं' : 'Build Your Professional Profile'}
            </h2>
            <p className="text-neutral-500">
              {language === 'hi' ? 'अपना विवरण दर्ज करें और AI से अपना पेशेवर पहचान बनवाएं' : 'Enter your details and let AI create your professional identity'}
            </p>
          </div>
        </div>

        <form onSubmit={handleSubmit} className="space-y-6">
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            <div>
               <label htmlFor="name" className="block text-sm font-medium text-neutral-700 mb-2">
                {language === 'hi' ? 'पूरा नाम *' : 'Full Name *'}
              </label>
              <div className="relative">
                <User className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-neutral-400" />
                <input
                  type="text"
                  id="name"
                  name="name"
                  value={formData.name}
                  onChange={handleChange}
                  required
                  className="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-neutral-900 focus:border-transparent transition-all"
                  placeholder={language === 'hi' ? 'अपना नाम दर्ज करें' : 'Enter your name'}
                />
              </div>
            </div>

            <div>
              <label htmlFor="age" className="block text-sm font-medium text-neutral-700 mb-2">
                {language === 'hi' ? 'आयु' : 'Age'}
              </label>
              <div className="relative">
                <Calendar className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-neutral-400" />
                <input
                  type="number"
                  id="age"
                  name="age"
                  value={formData.age}
                  onChange={handleChange}
                  min="16"
                  max="100"
                  className="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-neutral-900 focus:border-transparent transition-all"
                  placeholder={language === 'hi' ? 'अपनी आयु दर्ज करें' : 'Enter your age'}
                />
              </div>
            </div>

            <div className="md:col-span-2">
              <label htmlFor="location" className="block text-sm font-medium text-neutral-700 mb-2">
                {language === 'hi' ? 'स्थान' : 'Location'}
              </label>
              <div className="relative">
                <MapPin className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-neutral-400" />
                <input
                  type="text"
                  id="location"
                  name="location"
                  value={formData.location}
                  onChange={handleChange}
                  className="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-neutral-900 focus:border-transparent transition-all"
                  placeholder={language === 'hi' ? 'शहर, राज्य या क्षेत्र' : 'City, State or Region'}
                />
              </div>
            </div>

            <div className="md:col-span-2">
              <label htmlFor="work_experience" className="block text-sm font-medium text-neutral-700 mb-2">
                {language === 'hi' ? 'कार्य अनुभव और कौशल विवरण *' : 'Work Experience & Skills Description *'}
              </label>
              <div className="relative">
                <FileText className="absolute left-3 top-3 w-5 h-5 text-neutral-400" />
                <textarea
                  id="work_experience"
                  name="work_experience"
                  value={formData.work_experience}
                  onChange={handleChange}
                  required
                  rows={8}
                  className="w-full pl-10 pr-4 py-3 border border-neutral-300 rounded-lg focus:ring-2 focus:ring-neutral-900 focus:border-transparent transition-all resize-none"
                  placeholder={language === 'hi' ? 'अपना कार्य अनुभव, कौशल और आप क्या करते हैं describe करें। उदाहरण: \'मैं 5 वर्षों से निर्माण कार्यकर्ता के रूप में काम कर रहा हूं। मैं ब्लूप्रिंट पढ़ना, पावर टूल चलाना, सुरक्षा प्रोटोकॉल follows करना और टीम में अच्छा काम करना जानता हूं। मैं शारीरिक श्रम में अच्छा हूं और भारी सामान संभाल सकता हूं।\'' : "Describe your work experience, skills, and what you do. For example: 'I have been working as a construction worker for 5 years. I know how to read blueprints, operate power tools, follow safety protocols, and work well in teams. I'm good at physical labor and can handle heavy materials.'"}
                />
              </div>
              <p className="mt-2 text-sm text-neutral-500">
                {language === 'hi' ? 'जितना संभव हो उतना विस्तृत रहें। AI आपके कौशल को निकालकर एक पेशेवर प्रोफ़ाइल बनाएगा।' : 'Be as detailed as possible. The AI will extract your skills and create a professional profile.'}
              </p>
            </div>
          </div>

          {error && (
            <div className="bg-neutral-50 border border-neutral-200 text-neutral-900 px-4 py-3 rounded-lg">
              {error}
            </div>
          )}

          <button
            type="submit"
            disabled={loading}
            className="w-full bg-neutral-900 text-white font-semibold py-4 px-6 rounded-lg hover:shadow-lg transform hover:scale-[1.02] transition-all disabled:opacity-50 disabled:cursor-not-allowed disabled:transform-none flex items-center justify-center space-x-2"
          >
            {loading ? (
              <>
                <Loader2 className="w-5 h-5 animate-spin" />
                <span>{language === 'hi' ? 'अपना प्रोफ़ाइल विश्लेषण कर रहा हूं...' : 'Analyzing Your Profile...'}</span>
              </>
            ) : (
              <>
                <Sparkles className="w-5 h-5" />
                <span>{language === 'hi' ? 'पेशेवर प्रोफ़ाइल बनाएं' : 'Generate Professional Profile'}</span>
              </>
            )}
          </button>
        </form>
      </motion.div>

      <div className="mt-8 bg-neutral-50 border border-neutral-200 rounded-xl p-6">
        <h3 className="text-lg font-semibold text-neutral-900 mb-2">
          {language === 'hi' ? '💡 सबसे अच्छे परिणामों के लिए सुझाव' : '💡 Tips for Best Results'}
        </h3>
        <ul className="list-disc list-inside space-y-2 text-neutral-700">
          <li>{language === 'hi' ? 'नौकरी पर सीखे गए विशिष्ट कौशल शामिल करें' : 'Include specific skills you\'ve learned on the job'}</li>
          <li>{language === 'hi' ? 'उपकरण, उपकरण या सॉफ्टवेयर का उल्लेख करें' : 'Mention tools, equipment, or software you use'}</li>
          <li>{language === 'hi' ? 'अपना कार्य वातावरण और जिम्मेदारियों का वर्णन करें' : 'Describe your work environment and responsibilities'}</li>
          <li>{language === 'hi' ? 'टीमवर्क, संचार या नेतृत्व जैसे सॉफ्ट स्किल्स शामिल करें' : 'Include soft skills like teamwork, communication, or leadership'}</li>
        </ul>
      </div>
    </div>
  )
}

export default ProfileBuilder