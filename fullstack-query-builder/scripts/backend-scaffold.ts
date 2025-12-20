import { promises as fs } from 'fs';
import path from 'path';
import { ensureDir } from './utils.js';

export class BackendScaffold {
  async createProject(projectPath: string, dbConnection: string): Promise<void> {
    const backendPath = path.join(projectPath, 'backend');
    await ensureDir(backendPath);

    console.log('📦 Creating FastAPI project structure...');
    await this.createDirectories(backendPath);
    await this.createRequirements(backendPath);
    await this.createMainFile(backendPath);
    await this.createDatabase(backendPath, dbConnection);
    await this.createInitFiles(backendPath);

    console.log('✅ Backend scaffold complete');
  }

  private async createDirectories(backendPath: string): Promise<void> {
    const dirs = [
      'app',
      'app/routers',
      'app/models',
      'app/schemas'
    ];

    for (const dir of dirs) {
      await ensureDir(path.join(backendPath, dir));
    }
  }

  private async createRequirements(backendPath: string): Promise<void> {
    const requirements = `fastapi==0.110.0
uvicorn[standard]==0.27.1
pydantic==2.6.3
pydantic-settings==2.2.1
sqlalchemy==2.0.27
psycopg2-binary==2.9.9
python-dotenv==1.0.1
`;

    await fs.writeFile(path.join(backendPath, 'requirements.txt'), requirements);
    console.log('✅ Created requirements.txt');
  }

  private async createMainFile(backendPath: string): Promise<void> {
    const mainContent = `from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

app = FastAPI(title="Full-Stack Query Builder API")

# CORS configuration
origins = os.getenv("CORS_ORIGINS", "http://localhost:5173").split(",")

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Full-Stack Query Builder API"}

@app.get("/health")
def health_check():
    return {"status": "healthy"}
`;

    await fs.writeFile(path.join(backendPath, 'app/main.py'), mainContent);
    console.log('✅ Created app/main.py');
  }

  private async createDatabase(backendPath: string, dbConnection: string): Promise<void> {
    const dbContent = `from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

DATABASE_URL = os.getenv("DATABASE_URL", "${dbConnection}")

engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
`;

    await fs.writeFile(path.join(backendPath, 'app/database.py'), dbContent);
    console.log('✅ Created app/database.py');
  }

  private async createInitFiles(backendPath: string): Promise<void> {
    const dirs = ['app', 'app/routers', 'app/models', 'app/schemas'];

    for (const dir of dirs) {
      const initPath = path.join(backendPath, dir, '__init__.py');
      await fs.writeFile(initPath, '');
    }
  }
}
