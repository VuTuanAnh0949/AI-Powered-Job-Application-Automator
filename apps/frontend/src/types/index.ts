export interface Job {
  id: string
  title: string
  company: string
  location: string
  description: string
  url: string
  posted_date?: string
  salary_range?: string
  job_type?: string
  match_score?: number
}

export interface Application {
  id: string
  job_id: string
  job_title: string
  company: string
  status: ApplicationStatus
  applied_date: string
  last_updated: string
  resume_path?: string
  cover_letter_path?: string
  notes?: string
}

export type ApplicationStatus = 
  | 'draft' 
  | 'submitted' 
  | 'in_review' 
  | 'interview' 
  | 'rejected' 
  | 'accepted'

export interface UserProfile {
  id?: string
  full_name: string
  email: string
  phone?: string
  location?: string
  linkedin_url?: string
  github_url?: string
  portfolio_url?: string
  summary?: string
  skills: string[]
  experience: Experience[]
  education: Education[]
  certifications: string[]
  languages: string[]
  job_preferences?: JobPreferences
}

export interface Experience {
  company: string
  title: string
  start_date: string
  end_date?: string
  description: string
  achievements: string[]
}

export interface Education {
  institution: string
  degree: string
  field_of_study: string
  start_date: string
  end_date: string
  gpa?: number
}

export interface JobPreferences {
  desired_titles: string[]
  locations: string[]
  salary_min?: number
  salary_max?: number
  work_arrangement: 'remote' | 'hybrid' | 'onsite' | 'any'
  company_size?: string[]
}

export interface JobSearchParams {
  keywords: string[]
  location: string
  job_site: string
  max_results: number
  experience_level?: string
}
