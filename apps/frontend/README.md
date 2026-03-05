# AutoApply AI Frontend

Modern React + TypeScript frontend for AutoApply AI job application automation platform.

## 🚀 Quick Start

### Prerequisites

- Node.js 18+ or Bun
- npm, yarn, pnpm, or bun

### Installation

```bash
# Using npm
npm install

# Using yarn
yarn install

# Using pnpm
pnpm install

# Using bun
bun install
```

### Configuration

```bash
# Copy environment file
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Run Development Server

```bash
# Using npm
npm run dev

# Using yarn
yarn dev

# Using pnpm
pnpm dev

# Using bun
bun dev
```

The app will be available at: http://localhost:3000

### Build for Production

```bash
npm run build
npm run preview
```

## 📁 Project Structure

```
apps/frontend/
├── public/              # Static assets
├── src/
│   ├── components/      # Reusable UI components
│   │   └── Layout.tsx   # Main layout component
│   ├── pages/           # Page components
│   │   ├── Dashboard.tsx
│   │   ├── JobSearch.tsx
│   │   ├── Applications.tsx
│   │   ├── Documents.tsx
│   │   └── Profile.tsx
│   ├── lib/             # Utilities and API client
│   │   ├── api.ts       # Axios API client
│   │   └── utils.ts     # Helper functions
│   ├── types/           # TypeScript type definitions
│   │   └── index.ts
│   ├── App.tsx          # Main app component
│   ├── main.tsx         # App entry point
│   └── index.css        # Global styles
├── index.html
├── package.json
├── tsconfig.json
├── vite.config.ts
└── tailwind.config.js
```

## 🎨 Tech Stack

- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **TailwindCSS** - Utility-first CSS
- **React Router** - Routing
- **TanStack Query** - Data fetching & caching
- **Zustand** - State management
- **React Hook Form** - Form handling
- **Zod** - Schema validation
- **Axios** - HTTP client
- **Lucide React** - Icons
- **Sonner** - Toast notifications

## 🧩 Features

### Pages

- **Dashboard** - Overview of applications and statistics
- **Job Search** - Multi-platform job search with AI matching
- **Applications** - Track and manage job applications
- **Documents** - Generate and manage resumes/cover letters
- **Profile** - Manage professional profile and preferences

### Key Features

- 🎨 Modern, responsive UI with TailwindCSS
- 🚀 Fast development with Vite HMR
- 📱 Mobile-friendly design
- 🔄 Real-time API integration
- 🎯 Type-safe development with TypeScript
- 🔐 JWT authentication ready
- 📊 Application statistics and insights
- 🤖 AI-powered document generation

## 🔌 API Integration

The frontend communicates with the backend API at `http://localhost:8000` (configurable via `.env`).

API client is configured in `src/lib/api.ts` with:
- Automatic auth token injection
- Request/response interceptors
- Error handling
- Auto-redirect on 401

## 🧪 Testing

```bash
# Run tests (when configured)
npm run test

# Type checking
npm run type-check
```

## 🎨 Styling

This project uses TailwindCSS for styling with:
- Custom color palette (primary blue theme)
- Reusable component classes (`.btn-primary`, `.card`, `.input`)
- Responsive design utilities
- Dark mode ready (to be implemented)

## 🔧 Development Tips

### Adding New Pages

1. Create component in `src/pages/`
2. Add route in `src/App.tsx`
3. Add navigation item in `src/components/Layout.tsx`

### Custom Components

Reusable components go in `src/components/` with:
- TypeScript interfaces for props
- TailwindCSS for styling
- Lucide React for icons

### API Calls

Use TanStack Query for data fetching:

```tsx
import { useQuery } from '@tanstack/react-query'
import api from '@/lib/api'

const { data, isLoading } = useQuery({
  queryKey: ['jobs'],
  queryFn: async () => {
    const res = await api.get('/api/v1/jobs/search')
    return res.data
  }
})
```

## 🐳 Docker

```bash
# Build image
docker build -t autoapply-frontend .

# Run container
docker run -p 3000:80 autoapply-frontend
```

## 📝 Code Style

- ESLint for code linting
- Prettier for formatting (TBD)
- TypeScript strict mode enabled
- Functional components with hooks

## 🤝 Contributing

1. Create feature branch
2. Make changes
3. Test thoroughly
4. Submit pull request

## 📄 License

MIT License - See LICENSE file for details
