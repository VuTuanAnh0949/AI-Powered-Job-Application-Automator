import { useState } from 'react'
import { Save, Plus, X } from 'lucide-react'

export default function Profile() {
  const [skills, setSkills] = useState<string[]>([])
  const [newSkill, setNewSkill] = useState('')

  const addSkill = () => {
    if (newSkill.trim()) {
      setSkills([...skills, newSkill.trim()])
      setNewSkill('')
    }
  }

  const removeSkill = (index: number) => {
    setSkills(skills.filter((_, i) => i !== index))
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Profile</h1>
          <p className="text-gray-600 mt-2">
            Manage your professional profile and preferences.
          </p>
        </div>
        <button className="btn-primary flex items-center gap-2">
          <Save size={18} />
          Save Changes
        </button>
      </div>

      {/* Personal Information */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Personal Information</h2>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Full Name
            </label>
            <input type="text" className="input" placeholder="John Doe" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Email
            </label>
            <input
              type="email"
              className="input"
              placeholder="john@example.com"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Phone
            </label>
            <input type="tel" className="input" placeholder="+1 (555) 000-0000" />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Location
            </label>
            <input type="text" className="input" placeholder="San Francisco, CA" />
          </div>
        </div>
      </div>

      {/* Professional Links */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Professional Links</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              LinkedIn URL
            </label>
            <input
              type="url"
              className="input"
              placeholder="https://linkedin.com/in/yourprofile"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              GitHub URL
            </label>
            <input
              type="url"
              className="input"
              placeholder="https://github.com/yourusername"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Portfolio URL
            </label>
            <input
              type="url"
              className="input"
              placeholder="https://yourportfolio.com"
            />
          </div>
        </div>
      </div>

      {/* Professional Summary */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Professional Summary</h2>
        <textarea
          className="input min-h-[120px]"
          placeholder="Write a brief summary about your professional experience and career goals..."
        />
      </div>

      {/* Skills */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Skills</h2>
        <div className="flex gap-2 mb-4">
          <input
            type="text"
            className="input flex-1"
            placeholder="Add a skill..."
            value={newSkill}
            onChange={(e) => setNewSkill(e.target.value)}
            onKeyPress={(e) => e.key === 'Enter' && addSkill()}
          />
          <button onClick={addSkill} className="btn-primary">
            <Plus size={20} />
          </button>
        </div>
        <div className="flex flex-wrap gap-2">
          {skills.map((skill, index) => (
            <span
              key={index}
              className="bg-primary-100 text-primary-800 px-3 py-1 rounded-full text-sm font-medium flex items-center gap-2"
            >
              {skill}
              <button
                onClick={() => removeSkill(index)}
                className="hover:text-primary-900"
              >
                <X size={14} />
              </button>
            </span>
          ))}
          {skills.length === 0 && (
            <p className="text-gray-500 text-sm">No skills added yet.</p>
          )}
        </div>
      </div>

      {/* Job Preferences */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Job Preferences</h2>
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Desired Job Titles
            </label>
            <input
              type="text"
              className="input"
              placeholder="e.g., Software Engineer, Full Stack Developer"
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Preferred Locations
            </label>
            <input
              type="text"
              className="input"
              placeholder="e.g., Remote, San Francisco, New York"
            />
          </div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Min Salary
              </label>
              <input type="number" className="input" placeholder="80000" />
            </div>
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Salary
              </label>
              <input type="number" className="input" placeholder="150000" />
            </div>
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Work Arrangement
            </label>
            <select className="input">
              <option value="any">Any</option>
              <option value="remote">Remote</option>
              <option value="hybrid">Hybrid</option>
              <option value="onsite">On-site</option>
            </select>
          </div>
        </div>
      </div>
    </div>
  )
}
