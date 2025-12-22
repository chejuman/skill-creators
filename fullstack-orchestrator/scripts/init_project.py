#!/usr/bin/env python3
"""
Project Initializer for Fullstack Orchestrator

Creates the initial project structure for a new fullstack application.
"""

import argparse
import os
from pathlib import Path


def create_backend_structure(project_path: Path):
    """Create FastAPI backend structure."""
    backend = project_path / "backend"

    dirs = [
        "app",
        "app/api",
        "app/api/routes",
        "app/core",
        "app/models",
        "app/schemas",
        "app/crud",
        "app/services",
        "alembic/versions",
        "tests",
    ]

    for d in dirs:
        (backend / d).mkdir(parents=True, exist_ok=True)
        (backend / d / "__init__.py").touch()

    # Create main.py
    main_py = '''"""FastAPI Application Entry Point."""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.core.config import settings
from app.api.routes import router

app = FastAPI(
    title=settings.PROJECT_NAME,
    version="1.0.0",
    openapi_url=f"{settings.API_PREFIX}/openapi.json"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(router, prefix=settings.API_PREFIX)

@app.get("/health")
async def health_check():
    return {"status": "healthy"}
'''
    (backend / "app" / "main.py").write_text(main_py)

    # Create config.py
    config_py = '''"""Application Configuration."""
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    PROJECT_NAME: str = "Fullstack App"
    API_PREFIX: str = "/api"
    DATABASE_URL: str = "sqlite+aiosqlite:///./app.db"
    SECRET_KEY: str = "change-me-in-production"
    CORS_ORIGINS: list[str] = ["http://localhost:3000", "http://localhost:5173"]

    class Config:
        env_file = ".env"

settings = Settings()
'''
    (backend / "app" / "core" / "config.py").write_text(config_py)

    # Create requirements.txt
    requirements = '''fastapi>=0.109.0
uvicorn[standard]>=0.27.0
sqlalchemy[asyncio]>=2.0.0
aiosqlite
alembic>=1.13.0
pydantic>=2.5.0
pydantic-settings>=2.1.0
python-jose[cryptography]>=3.3.0
passlib[bcrypt]>=1.7.4
python-multipart>=0.0.6
httpx>=0.26.0
pytest>=7.4.0
pytest-asyncio>=0.23.0
'''
    (backend / "requirements.txt").write_text(requirements)

    print(f"Created backend structure at {backend}")


def create_frontend_structure(project_path: Path):
    """Create React + shadcn/ui frontend structure."""
    frontend = project_path / "frontend"

    dirs = [
        "src/components/ui",
        "src/components/layout",
        "src/components/features",
        "src/hooks",
        "src/lib",
        "src/stores",
        "src/types",
        "src/pages",
    ]

    for d in dirs:
        (frontend / d).mkdir(parents=True, exist_ok=True)

    # Create package.json
    package_json = '''{
  "name": "frontend",
  "private": true,
  "version": "0.0.0",
  "type": "module",
  "scripts": {
    "dev": "vite",
    "build": "tsc && vite build",
    "lint": "eslint . --ext ts,tsx",
    "preview": "vite preview",
    "test": "vitest"
  },
  "dependencies": {
    "react": "^18.2.0",
    "react-dom": "^18.2.0",
    "react-router-dom": "^6.21.0",
    "@tanstack/react-query": "^5.17.0",
    "zustand": "^4.4.7",
    "react-hook-form": "^7.49.0",
    "@hookform/resolvers": "^3.3.0",
    "zod": "^3.22.0",
    "class-variance-authority": "^0.7.0",
    "clsx": "^2.1.0",
    "tailwind-merge": "^2.2.0",
    "lucide-react": "^0.303.0"
  },
  "devDependencies": {
    "@types/react": "^18.2.0",
    "@types/react-dom": "^18.2.0",
    "@vitejs/plugin-react": "^4.2.0",
    "typescript": "^5.3.0",
    "vite": "^5.0.0",
    "vitest": "^1.1.0",
    "@testing-library/react": "^14.1.0",
    "tailwindcss": "^3.4.0",
    "postcss": "^8.4.0",
    "autoprefixer": "^10.4.0"
  }
}
'''
    (frontend / "package.json").write_text(package_json)

    # Create vite.config.ts
    vite_config = '''import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
})
'''
    (frontend / "vite.config.ts").write_text(vite_config)

    # Create main.tsx
    main_tsx = '''import React from 'react'
import ReactDOM from 'react-dom/client'
import { QueryClient, QueryClientProvider } from '@tanstack/react-query'
import { BrowserRouter } from 'react-router-dom'
import App from './App'
import './index.css'

const queryClient = new QueryClient()

ReactDOM.createRoot(document.getElementById('root')!).render(
  <React.StrictMode>
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <App />
      </BrowserRouter>
    </QueryClientProvider>
  </React.StrictMode>,
)
'''
    (frontend / "src" / "main.tsx").write_text(main_tsx)

    # Create App.tsx
    app_tsx = '''function App() {
  return (
    <div className="min-h-screen bg-background">
      <main className="container mx-auto py-6">
        <h1 className="text-3xl font-bold">Welcome to Your App</h1>
        <p className="text-muted-foreground mt-2">
          Start building your fullstack application!
        </p>
      </main>
    </div>
  )
}

export default App
'''
    (frontend / "src" / "App.tsx").write_text(app_tsx)

    print(f"Created frontend structure at {frontend}")


def create_shared_files(project_path: Path):
    """Create shared configuration files."""
    # docker-compose.yml
    docker_compose = '''version: '3.8'

services:
  backend:
    build: ./backend
    ports:
      - "8000:8000"
    environment:
      - DATABASE_URL=sqlite+aiosqlite:///./app.db
    volumes:
      - ./backend:/app

  frontend:
    build: ./frontend
    ports:
      - "3000:80"
    depends_on:
      - backend
'''
    (project_path / "docker-compose.yml").write_text(docker_compose)

    # .gitignore
    gitignore = '''# Dependencies
node_modules/
__pycache__/
*.pyc
.venv/
venv/

# Build
dist/
build/
*.egg-info/

# Environment
.env
.env.local
.env.production

# IDE
.vscode/
.idea/

# Testing
.coverage
htmlcov/
.pytest_cache/

# Misc
*.log
*.db
.DS_Store
'''
    (project_path / ".gitignore").write_text(gitignore)

    # README.md
    readme = '''# Fullstack Application

Generated by Fullstack Orchestrator.

## Quick Start

### Backend
```bash
cd backend
python -m venv venv
source venv/bin/activate  # or `venv\\Scripts\\activate` on Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Tech Stack
- Backend: FastAPI + SQLAlchemy
- Frontend: React + shadcn/ui + Tailwind
- Database: SQLite (dev) / PostgreSQL (prod)

## Documentation
- API Docs: http://localhost:8000/docs
- Frontend: http://localhost:5173
'''
    (project_path / "README.md").write_text(readme)

    print(f"Created shared files at {project_path}")


def main():
    parser = argparse.ArgumentParser(description="Initialize fullstack project")
    parser.add_argument("name", help="Project name")
    parser.add_argument("--path", default=".", help="Parent directory")
    args = parser.parse_args()

    project_path = Path(args.path) / args.name
    project_path.mkdir(parents=True, exist_ok=True)

    print(f"Initializing project: {args.name}")
    print("=" * 50)

    create_backend_structure(project_path)
    create_frontend_structure(project_path)
    create_shared_files(project_path)

    print("=" * 50)
    print(f"Project initialized successfully at {project_path}")
    print("\nNext steps:")
    print(f"  cd {project_path}")
    print("  # Start backend: cd backend && uvicorn app.main:app --reload")
    print("  # Start frontend: cd frontend && npm install && npm run dev")


if __name__ == "__main__":
    main()
