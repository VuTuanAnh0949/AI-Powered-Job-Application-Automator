import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Search, MapPin, Briefcase, ExternalLink } from 'lucide-react'
import api from '@/lib/api'
import type { Job, JobSearchParams } from '@/types'

export default function JobSearch() {
  const [searchParams, setSearchParams] = useState<JobSearchParams>({
    keywords: [''],
    location: 'Remote',
    job_site: 'linkedin',
    max_results: 50,
  })

  const [searching, setSearching] = useState(false)
  const [jobs, setJobs] = useState<Job[]>([])

  const handleSearch = async () => {
    setSearching(true)
    try {
      const response = await api.post('/api/v1/jobs/search', searchParams)
      setJobs(response.data.jobs || [])
    } catch (error) {
      console.error('Search failed:', error)
    } finally {
      setSearching(false)
    }
  }

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Job Search</h1>
        <p className="text-gray-600 mt-2">
          Search for jobs across multiple platforms with AI-powered filtering.
        </p>
      </div>

      {/* Search Form */}
      <div className="card">
        <div className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-700 mb-2">
              Keywords
            </label>
            <input
              type="text"
              className="input"
              placeholder="e.g., Python Developer, Data Scientist"
              value={searchParams.keywords[0]}
              onChange={(e) =>
                setSearchParams({ ...searchParams, keywords: [e.target.value] })
              }
            />
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Location
              </label>
              <input
                type="text"
                className="input"
                placeholder="Remote, City, etc."
                value={searchParams.location}
                onChange={(e) =>
                  setSearchParams({ ...searchParams, location: e.target.value })
                }
              />
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Job Site
              </label>
              <select
                className="input"
                value={searchParams.job_site}
                onChange={(e) =>
                  setSearchParams({ ...searchParams, job_site: e.target.value })
                }
              >
                <option value="linkedin">LinkedIn</option>
                <option value="indeed">Indeed</option>
                <option value="glassdoor">Glassdoor</option>
              </select>
            </div>

            <div>
              <label className="block text-sm font-medium text-gray-700 mb-2">
                Max Results
              </label>
              <input
                type="number"
                className="input"
                min="1"
                max="200"
                value={searchParams.max_results}
                onChange={(e) =>
                  setSearchParams({
                    ...searchParams,
                    max_results: parseInt(e.target.value),
                  })
                }
              />
            </div>
          </div>

          <button
            onClick={handleSearch}
            disabled={searching}
            className="btn-primary w-full flex items-center justify-center gap-2"
          >
            <Search size={18} />
            {searching ? 'Searching...' : 'Search Jobs'}
          </button>
        </div>
      </div>

      {/* Results */}
      <div className="space-y-4">
        {jobs.length > 0 ? (
          <>
            <div className="flex items-center justify-between">
              <h2 className="text-xl font-semibold">
                Found {jobs.length} jobs
              </h2>
            </div>
            {jobs.map((job) => (
              <JobCard key={job.id} job={job} />
            ))}
          </>
        ) : (
          <div className="card text-center py-12">
            <Search className="mx-auto text-gray-400 mb-4" size={48} />
            <p className="text-gray-600">
              {searching
                ? 'Searching for jobs...'
                : 'Start searching to find relevant job opportunities'}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

function JobCard({ job }: { job: Job }) {
  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-start gap-3">
            <Briefcase className="text-primary-600 mt-1 flex-shrink-0" size={20} />
            <div>
              <h3 className="font-semibold text-lg text-gray-900">{job.title}</h3>
              <p className="text-gray-700 font-medium">{job.company}</p>
            </div>
          </div>

          <div className="flex items-center gap-4 mt-3 text-sm text-gray-600">
            <span className="flex items-center gap-1">
              <MapPin size={16} />
              {job.location}
            </span>
            {job.job_type && <span>• {job.job_type}</span>}
            {job.salary_range && <span>• {job.salary_range}</span>}
          </div>

          {job.match_score && (
            <div className="mt-3">
              <div className="flex items-center gap-2">
                <span className="text-sm font-medium text-gray-700">Match Score:</span>
                <div className="flex-1 bg-gray-200 rounded-full h-2 max-w-xs">
                  <div
                    className="bg-primary-600 h-2 rounded-full"
                    style={{ width: `${job.match_score * 100}%` }}
                  />
                </div>
                <span className="text-sm font-semibold text-primary-600">
                  {Math.round(job.match_score * 100)}%
                </span>
              </div>
            </div>
          )}

          <p className="mt-3 text-sm text-gray-600 line-clamp-2">
            {job.description}
          </p>
        </div>

        <div className="flex flex-col gap-2">
          <a
            href={job.url}
            target="_blank"
            rel="noopener noreferrer"
            className="btn-secondary text-sm flex items-center gap-2"
          >
            View Job <ExternalLink size={14} />
          </a>
          <button className="btn-primary text-sm">Quick Apply</button>
        </div>
      </div>
    </div>
  )
}
