import { promises as fs } from 'fs';
import path from 'path';
import { toPascalCase, toSnakeCase } from './utils.js';
import type { QueryResults } from './state-manager.js';

export class IntegrationManager {
  async integrate(
    projectPath: string,
    resourceName: string,
    queryResults: QueryResults,
    dbConnection: string
  ): Promise<void> {
    const frontendPath = path.join(projectPath, 'frontend');
    const backendPath = path.join(projectPath, 'backend');

    console.log('🔗 Generating API client...');
    await this.generateAPIClient(frontendPath, resourceName, queryResults);

    console.log('⚙️  Configuring Vite proxy...');
    await this.configureViteProxy(frontendPath);

    console.log('📝 Creating environment files...');
    await this.createEnvFiles(projectPath, dbConnection);

    console.log('📖 Generating README...');
    await this.generateREADME(projectPath, resourceName);

    console.log('✅ Integration complete');
  }

  private async generateAPIClient(
    frontendPath: string,
    resourceName: string,
    queryResults: QueryResults
  ): Promise<void> {
    const modelName = toPascalCase(resourceName);
    const endpoint = toSnakeCase(resourceName);

    const apiClientContent = `import type { ${modelName} } from '../types/${modelName}';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

export class APIClient {
  private baseURL: string;

  constructor(baseURL: string = API_BASE_URL) {
    this.baseURL = baseURL;
  }

  async list${modelName}(page: number = 1, limit: number = 50): Promise<${modelName}[]> {
    const response = await fetch(
      \`\${this.baseURL}/api/${endpoint}?page=\${page}&limit=\${limit}\`
    );
    if (!response.ok) throw new Error('Failed to fetch ${resourceName}');
    return response.json();
  }

  async get${modelName}(id: number): Promise<${modelName}> {
    const response = await fetch(\`\${this.baseURL}/api/${endpoint}/\${id}\`);
    if (!response.ok) throw new Error('Failed to fetch ${resourceName}');
    return response.json();
  }

  async create${modelName}(data: Omit<${modelName}, 'id'>): Promise<${modelName}> {
    const response = await fetch(\`\${this.baseURL}/api/${endpoint}\`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to create ${resourceName}');
    return response.json();
  }

  async update${modelName}(id: number, data: Partial<${modelName}>): Promise<${modelName}> {
    const response = await fetch(\`\${this.baseURL}/api/${endpoint}/\${id}\`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(data),
    });
    if (!response.ok) throw new Error('Failed to update ${resourceName}');
    return response.json();
  }

  async delete${modelName}(id: number): Promise<void> {
    const response = await fetch(\`\${this.baseURL}/api/${endpoint}/\${id}\`, {
      method: 'DELETE',
    });
    if (!response.ok) throw new Error('Failed to delete ${resourceName}');
  }
}

export const apiClient = new APIClient();
`;

    await fs.writeFile(
      path.join(frontendPath, 'src/lib/api-client.ts'),
      apiClientContent
    );
    console.log('✅ Generated API client');
  }

  private async configureViteProxy(frontendPath: string): Promise<void> {
    const viteConfig = `import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import path from 'path'

export default defineConfig({
  plugins: [react()],
  resolve: {
    alias: {
      '@': path.resolve(__dirname, './src'),
    },
  },
  server: {
    proxy: {
      '/api': {
        target: 'http://localhost:8000',
        changeOrigin: true,
      },
    },
  },
})
`;

    await fs.writeFile(
      path.join(frontendPath, 'vite.config.ts'),
      viteConfig
    );
    console.log('✅ Configured Vite proxy');
  }

  private async createEnvFiles(projectPath: string, dbConnection: string): Promise<void> {
    // Frontend .env
    const frontendEnv = `VITE_API_URL=http://localhost:8000
VITE_API_TIMEOUT=30000
VITE_ENABLE_DEBUG=false
`;

    await fs.writeFile(
      path.join(projectPath, 'frontend/.env'),
      frontendEnv
    );

    // Backend .env
    const backendEnv = `DATABASE_URL=${dbConnection}
DB_POOL_SIZE=10
API_HOST=0.0.0.0
API_PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
`;

    await fs.writeFile(
      path.join(projectPath, 'backend/.env'),
      backendEnv
    );

    console.log('✅ Created environment files');
  }

  private async generateREADME(projectPath: string, resourceName: string): Promise<void> {
    const readme = `# Full-Stack Query Builder - ${toPascalCase(resourceName)}

Generated full-stack application for managing ${resourceName}.

## Project Structure

\`\`\`
${path.basename(projectPath)}/
├── frontend/          # React + Vite + shadcn/ui
│   ├── src/
│   │   ├── components/
│   │   ├── lib/
│   │   ├── pages/
│   │   ├── store/
│   │   └── types/
│   └── .env
└── backend/           # FastAPI + PostgreSQL
    ├── app/
    │   ├── routers/
    │   ├── models/
    │   └── schemas/
    └── .env
\`\`\`

## Getting Started

### Prerequisites

- Node.js 18+
- Python 3.10+
- PostgreSQL database

### Running the Application

**Terminal 1 - Backend:**

\`\`\`bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
\`\`\`

Backend will run at http://localhost:8000

**Terminal 2 - Frontend:**

\`\`\`bash
cd frontend
npm install
npm run dev
\`\`\`

Frontend will run at http://localhost:5173

## API Endpoints

- \`GET /api/${toSnakeCase(resourceName)}\` - List all items
- \`GET /api/${toSnakeCase(resourceName)}/{id}\` - Get single item
- \`POST /api/${toSnakeCase(resourceName)}\` - Create item
- \`PUT /api/${toSnakeCase(resourceName)}/{id}\` - Update item
- \`DELETE /api/${toSnakeCase(resourceName)}/{id}\` - Delete item

## Development

- Frontend uses Zustand for state management
- Backend uses SQLAlchemy for ORM
- CORS is configured for local development

## Generated by

Full-Stack Query Builder Claude Code Skill
`;

    await fs.writeFile(
      path.join(projectPath, 'README.md'),
      readme
    );
    console.log('✅ Generated README');
  }
}
