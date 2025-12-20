import { promises as fs } from 'fs';
import path from 'path';
import { exec } from 'child_process';
import { promisify } from 'util';
import { ensureDir } from './utils.js';

const execAsync = promisify(exec);

export class FrontendScaffold {
  async createProject(projectPath: string, projectName: string): Promise<void> {
    const frontendPath = path.join(projectPath, 'frontend');
    await ensureDir(frontendPath);

    console.log('📦 Creating Vite + React + TypeScript project...');
    await this.initViteProject(frontendPath, projectName);

    console.log('📦 Installing dependencies...');
    await this.installDependencies(frontendPath);

    console.log('🎨 Setting up shadcn/ui...');
    await this.setupShadcn(frontendPath);

    console.log('📁 Creating directory structure...');
    await this.createDirectories(frontendPath);

    console.log('✅ Frontend scaffold complete');
  }

  private async initViteProject(frontendPath: string, projectName: string): Promise<void> {
    const cwd = path.dirname(frontendPath);
    const folderName = path.basename(frontendPath);

    try {
      await execAsync(
        `npm create vite@latest ${folderName} -- --template react-ts`,
        { cwd }
      );
    } catch (error: any) {
      throw new Error(`Failed to create Vite project: ${error.message}`);
    }
  }

  private async installDependencies(frontendPath: string): Promise<void> {
    const packageJson = await fs.readFile(
      path.join(frontendPath, 'package.json'),
      'utf-8'
    );
    const pkg = JSON.parse(packageJson);

    pkg.dependencies = {
      ...pkg.dependencies,
      'react-router-dom': '^6.22.0',
      'zustand': '^4.5.0',
      '@radix-ui/react-table': 'latest',
      'class-variance-authority': '^0.7.0',
      'clsx': '^2.1.0',
      'tailwind-merge': '^2.2.0'
    };

    pkg.devDependencies = {
      ...pkg.devDependencies,
      'tailwindcss': '^3.4.1',
      'autoprefixer': '^10.4.17',
      'postcss': '^8.4.35'
    };

    await fs.writeFile(
      path.join(frontendPath, 'package.json'),
      JSON.stringify(pkg, null, 2)
    );

    try {
      await execAsync('npm install', { cwd: frontendPath });
    } catch (error: any) {
      throw new Error(`Failed to install dependencies: ${error.message}`);
    }
  }

  private async setupShadcn(frontendPath: string): Promise<void> {
    // Create tailwind.config.js
    const tailwindConfig = `/** @type {import('tailwindcss').Config} */
export default {
  darkMode: ["class"],
  content: [
    './pages/**/*.{ts,tsx}',
    './components/**/*.{ts,tsx}',
    './app/**/*.{ts,tsx}',
    './src/**/*.{ts,tsx}',
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}`;

    await fs.writeFile(
      path.join(frontendPath, 'tailwind.config.js'),
      tailwindConfig
    );

    // Create postcss.config.js
    const postcssConfig = `export default {
  plugins: {
    tailwindcss: {},
    autoprefixer: {},
  },
}`;

    await fs.writeFile(
      path.join(frontendPath, 'postcss.config.js'),
      postcssConfig
    );

    // Update src/index.css with Tailwind directives
    const indexCss = `@tailwind base;
@tailwind components;
@tailwind utilities;`;

    await fs.writeFile(
      path.join(frontendPath, 'src/index.css'),
      indexCss
    );
  }

  private async createDirectories(frontendPath: string): Promise<void> {
    const dirs = [
      'src/components',
      'src/components/ui',
      'src/lib',
      'src/pages',
      'src/store',
      'src/types'
    ];

    for (const dir of dirs) {
      await ensureDir(path.join(frontendPath, dir));
    }

    // Create lib/utils.ts
    const utilsContent = `import { type ClassValue, clsx } from "clsx"
import { twMerge } from "tailwind-merge"

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs))
}`;

    await fs.writeFile(
      path.join(frontendPath, 'src/lib/utils.ts'),
      utilsContent
    );
  }
}
