import { promises as fs } from 'fs';
import path from 'path';

export function toPascalCase(str: string): string {
  return str
    .split(/[-_\s]+/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join('');
}

export function toTitleCase(str: string): string {
  return str
    .split(/[-_\s]+/)
    .map(word => word.charAt(0).toUpperCase() + word.slice(1).toLowerCase())
    .join(' ');
}

export function toKebabCase(str: string): string {
  return str
    .replace(/([a-z])([A-Z])/g, '$1-$2')
    .replace(/[\s_]+/g, '-')
    .toLowerCase();
}

export function toCamelCase(str: string): string {
  const pascal = toPascalCase(str);
  return pascal.charAt(0).toLowerCase() + pascal.slice(1);
}

export function toSnakeCase(str: string): string {
  return str
    .replace(/([a-z])([A-Z])/g, '$1_$2')
    .replace(/[\s-]+/g, '_')
    .toLowerCase();
}

export async function ensureDir(dirPath: string): Promise<void> {
  try {
    await fs.mkdir(dirPath, { recursive: true });
  } catch (error: any) {
    if (error.code !== 'EEXIST') {
      throw error;
    }
  }
}

export async function fileExists(filePath: string): Promise<boolean> {
  try {
    await fs.access(filePath);
    return true;
  } catch {
    return false;
  }
}

export async function copyTemplate(
  templatePath: string,
  targetPath: string
): Promise<void> {
  const content = await fs.readFile(templatePath, 'utf-8');
  await ensureDir(path.dirname(targetPath));
  await fs.writeFile(targetPath, content);
}

export function maskPassword(connectionString: string): string {
  return connectionString.replace(
    /:([^:@]+)@/,
    ':***@'
  );
}

export function validateSkillName(name: string): { valid: boolean; error?: string } {
  if (name.length > 40) {
    return { valid: false, error: 'Name must be 40 characters or less' };
  }
  if (!/^[a-z0-9]+(-[a-z0-9]+)*$/.test(name)) {
    return { valid: false, error: 'Name must be hyphen-case (lowercase, hyphens only)' };
  }
  return { valid: true };
}
