import { useState } from 'react'
import { useQuery } from '@tanstack/react-query'
import { Briefcase, Calendar, FileText, Trash2 } from 'lucide-react'
import api from '@/lib/api'
import type { Application, ApplicationStatus } from '@/types'

const statusColors: Record<ApplicationStatus, string> = {
  draft: 'bg-gray-100 text-gray-800',
  submitted: 'bg-blue-100 text-blue-800',
  in_review: 'bg-yellow-100 text-yellow-800',
  interview: 'bg-purple-100 text-purple-800',
  rejected: 'bg-red-100 text-red-800',
  accepted: 'bg-green-100 text-green-800',
}

export default function Applications() {
  const [selectedStatus, setSelectedStatus] = useState<string | null>(null)

  // Mock data - replace with real API call
  const applications: Application[] = []

  const filterApplications = applications.filter(
    (app) => !selectedStatus || app.status === selectedStatus
  )

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold text-gray-900">Applications</h1>
          <p className="text-gray-600 mt-2">
            Track and manage your job applications.
          </p>
        </div>
        <button className="btn-primary">New Application</button>
      </div>

      {/* Status Filter */}
      <div className="card">
        <div className="flex gap-2 flex-wrap">
          <FilterButton
            label="All"
            count={applications.length}
            active={!selectedStatus}
            onClick={() => setSelectedStatus(null)}
          />
          {Object.keys(statusColors).map((status) => (
            <FilterButton
              key={status}
              label={status.replace('_', ' ')}
              count={applications.filter((a) => a.status === status).length}
              active={selectedStatus === status}
              onClick={() => setSelectedStatus(status)}
            />
          ))}
        </div>
      </div>

      {/* Applications List */}
      <div className="space-y-4">
        {filterApplications.length > 0 ? (
          filterApplications.map((app) => (
            <ApplicationCard key={app.id} application={app} />
          ))
        ) : (
          <div className="card text-center py-12">
            <Briefcase className="mx-auto text-gray-400 mb-4" size={48} />
            <p className="text-gray-600">
              {applications.length === 0
                ? 'No applications yet. Start applying to jobs!'
                : 'No applications with this status.'}
            </p>
          </div>
        )}
      </div>
    </div>
  )
}

function FilterButton({
  label,
  count,
  active,
  onClick,
}: {
  label: string
  count: number
  active: boolean
  onClick: () => void
}) {
  return (
    <button
      onClick={onClick}
      className={`px-4 py-2 rounded-lg font-medium transition-colors capitalize ${
        active
          ? 'bg-primary-600 text-white'
          : 'bg-gray-100 text-gray-700 hover:bg-gray-200'
      }`}
    >
      {label} ({count})
    </button>
  )
}

function ApplicationCard({ application }: { application: Application }) {
  return (
    <div className="card hover:shadow-md transition-shadow">
      <div className="flex items-start justify-between gap-4">
        <div className="flex-1">
          <div className="flex items-center gap-3 mb-2">
            <h3 className="font-semibold text-lg text-gray-900">
              {application.job_title}
            </h3>
            <span
              className={`px-3 py-1 rounded-full text-xs font-medium capitalize ${
                statusColors[application.status]
              }`}
            >
              {application.status.replace('_', ' ')}
            </span>
          </div>

          <p className="text-gray-700 font-medium mb-3">{application.company}</p>

          <div className="flex items-center gap-4 text-sm text-gray-600">
            <span className="flex items-center gap-1">
              <Calendar size={16} />
              Applied: {new Date(application.applied_date).toLocaleDateString()}
            </span>
            {application.resume_path && (
              <span className="flex items-center gap-1">
                <FileText size={16} />
                Resume attached
              </span>
            )}
          </div>

          {application.notes && (
            <p className="mt-3 text-sm text-gray-600">{application.notes}</p>
          )}
        </div>

        <div className="flex flex-col gap-2">
          <button className="btn-secondary text-sm">View Details</button>
          <button className="text-red-600 hover:text-red-700 p-2">
            <Trash2 size={18} />
          </button>
        </div>
      </div>
    </div>
  )
}
