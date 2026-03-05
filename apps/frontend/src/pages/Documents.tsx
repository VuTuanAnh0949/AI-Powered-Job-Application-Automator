import { FileText, Upload } from "lucide-react";

export default function Documents() {
  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold text-gray-900">Documents</h1>
        <p className="text-gray-600 mt-2">
          Generate and manage your resumes and cover letters.
        </p>
      </div>

      {/* Upload Section */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Base Resume</h2>
        <div className="border-2 border-dashed border-gray-300 rounded-lg p-8 text-center hover:border-primary-400 transition-colors cursor-pointer">
          <Upload className="mx-auto text-gray-400 mb-3" size={48} />
          <p className="text-gray-700 font-medium mb-2">
            Upload your base resume
          </p>
          <p className="text-sm text-gray-500 mb-4">
            PDF or DOCX format, max 5MB
          </p>
          <button className="btn-primary">Choose File</button>
        </div>
      </div>

      {/* Generate Section */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
        <div className="card">
          <FileText className="text-primary-600 mb-3" size={32} />
          <h3 className="text-lg font-semibold mb-2">Generate Resume</h3>
          <p className="text-sm text-gray-600 mb-4">
            Create a tailored resume for a specific job posting using AI.
          </p>
          <button className="btn-primary w-full">Generate Resume</button>
        </div>

        <div className="card">
          <FileText className="text-blue-600 mb-3" size={32} />
          <h3 className="text-lg font-semibold mb-2">Generate Cover Letter</h3>
          <p className="text-sm text-gray-600 mb-4">
            Create a personalized cover letter that highlights your strengths.
          </p>
          <button className="btn-primary w-full">Generate Cover Letter</button>
        </div>
      </div>

      {/* Document History */}
      <div className="card">
        <h2 className="text-xl font-semibold mb-4">Generated Documents</h2>
        <div className="text-center py-12 text-gray-500">
          <FileText className="mx-auto text-gray-400 mb-4" size={48} />
          <p>No documents generated yet.</p>
        </div>
      </div>
    </div>
  );
}
