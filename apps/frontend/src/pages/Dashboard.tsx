import { BarChart3, Briefcase, FileText, TrendingUp } from "lucide-react";

export default function Dashboard() {
  // Mock stats - replace with real API call
  const stats = {
    totalApplications: 0,
    inReview: 0,
    interviews: 0,
    successRate: 0,
  };

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Dashboard</h1>
        <p className="text-gray-600 mt-2">
          Welcome back! Here's your job application overview.
        </p>
      </div>

      {/* Stats Grid */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        <StatCard
          icon={<Briefcase className="text-primary-600" />}
          label="Total Applications"
          value={stats.totalApplications}
          trend="+0 this week"
        />
        <StatCard
          icon={<FileText className="text-blue-600" />}
          label="In Review"
          value={stats.inReview}
          trend="Pending responses"
        />
        <StatCard
          icon={<TrendingUp className="text-green-600" />}
          label="Interviews"
          value={stats.interviews}
          trend="Scheduled"
        />
        <StatCard
          icon={<BarChart3 className="text-purple-600" />}
          label="Success Rate"
          value={`${stats.successRate}%`}
          trend="All time"
        />
      </div>

      {/* Recent Activity */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Recent Activity</h2>
        <div className="text-center py-12 text-gray-500">
          No recent activity. Start by searching for jobs!
        </div>
      </div>

      {/* Quick Actions */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Quick Actions</h2>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <QuickAction
            title="Search Jobs"
            description="Find relevant opportunities"
            href="/jobs"
            color="primary"
          />
          <QuickAction
            title="Generate Resume"
            description="Create tailored resume"
            href="/documents"
            color="blue"
          />
          <QuickAction
            title="Update Profile"
            description="Keep your profile current"
            href="/profile"
            color="green"
          />
        </div>
      </div>
    </div>
  );
}

function StatCard({ icon, label, value, trend }: any) {
  return (
    <div className="card">
      <div className="flex items-start justify-between">
        <div className="flex-1">
          <p className="text-sm text-gray-600 mb-1">{label}</p>
          <p className="text-2xl font-bold text-gray-900">{value}</p>
          <p className="text-xs text-gray-500 mt-2">{trend}</p>
        </div>
        <div className="bg-gray-50 p-3 rounded-lg">{icon}</div>
      </div>
    </div>
  );
}

function QuickAction({ title, description, href, color }: any) {
  return (
    <a
      href={href}
      className={`block p-4 border-2 border-${color}-200 rounded-lg hover:border-${color}-400 hover:bg-${color}-50 transition-all`}
    >
      <h3 className="font-semibold text-gray-900 mb-1">{title}</h3>
      <p className="text-sm text-gray-600">{description}</p>
    </a>
  );
}
