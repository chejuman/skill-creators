import { exec } from 'child_process';
import { promisify } from 'util';

const execAsync = promisify(exec);

/**
 * Execute shadcn CLI command
 */
export async function execShadcnCommand(command: string, cwd?: string): Promise<string> {
  try {
    const fullCommand = `npx shadcn@latest ${command}`;
    const { stdout, stderr } = await execAsync(fullCommand, {
      cwd: cwd || process.cwd(),
      maxBuffer: 1024 * 1024 * 10, // 10MB buffer
    });

    if (stderr && !stdout) {
      throw new Error(stderr);
    }

    return stdout.trim();
  } catch (error: any) {
    // Extract useful error message
    const errorMessage = error.message || String(error);

    // Check for common errors
    if (errorMessage.includes('ENOENT') || errorMessage.includes('command not found')) {
      throw new Error('shadcn CLI not found. Ensure npm/npx is installed and in PATH.');
    }

    if (errorMessage.includes('components.json')) {
      throw new Error('No components.json found. Run: npx shadcn@latest init');
    }

    throw new Error(errorMessage);
  }
}

/**
 * Parse shadcn CLI output (JSON or table format)
 */
export function parseShadcnOutput(output: string, expectedFormat: 'json' | 'text' = 'json'): any {
  if (!output || output.trim() === '') {
    return expectedFormat === 'json' ? {} : '';
  }

  // Try to parse as JSON first
  try {
    const jsonMatch = output.match(/\{[\s\S]*\}|\[[\s\S]*\]/);
    if (jsonMatch) {
      return JSON.parse(jsonMatch[0]);
    }
  } catch {
    // Not JSON, continue
  }

  // Return as text
  return output.trim();
}

/**
 * Normalize component name (remove registry prefix, lowercase)
 */
export function normalizeComponentName(name: string): string {
  // Remove registry prefix like @shadcn/ or @acme/
  const withoutPrefix = name.replace(/^@[^/]+\//, '');

  // Lowercase
  return withoutPrefix.toLowerCase();
}

/**
 * Format component list for display
 */
export function formatComponentList(items: any[]): string {
  if (!items || items.length === 0) {
    return 'No components found.';
  }

  const lines: string[] = [];

  items.forEach((item, index) => {
    const name = item.name || item;
    const type = item.type ? ` (${item.type.replace('registry:', '')})` : '';
    const description = item.description ? `\n  ${item.description}` : '';
    const registry = item.registry ? ` [${item.registry}]` : '';

    lines.push(`${index + 1}. ${name}${type}${registry}${description}`);
  });

  return lines.join('\n\n');
}

/**
 * Format component details for display
 */
export function formatComponentDetails(item: any): string {
  const lines: string[] = [];

  lines.push(`## ${item.name}`);

  if (item.description) {
    lines.push(`\n${item.description}\n`);
  }

  if (item.type) {
    lines.push(`**Type:** ${item.type}`);
  }

  if (item.dependencies && item.dependencies.length > 0) {
    lines.push(`**Dependencies:** ${item.dependencies.join(', ')}`);
  }

  if (item.devDependencies && item.devDependencies.length > 0) {
    lines.push(`**Dev Dependencies:** ${item.devDependencies.join(', ')}`);
  }

  if (item.registryDependencies && item.registryDependencies.length > 0) {
    lines.push(`**Registry Dependencies:** ${item.registryDependencies.join(', ')}`);
  }

  if (item.files && item.files.length > 0) {
    lines.push(`\n**Files (${item.files.length}):**`);
    item.files.forEach((file: any) => {
      lines.push(`  - ${file.path || file.name}`);
    });
  }

  return lines.join('\n');
}

/**
 * Format examples/code for display
 */
export function formatExamples(item: any): string {
  const lines: string[] = [];

  lines.push(`# ${item.name} - Usage Examples`);

  if (item.description) {
    lines.push(`\n${item.description}\n`);
  }

  if (item.files && item.files.length > 0) {
    item.files.forEach((file: any) => {
      if (file.content) {
        lines.push(`\n## ${file.path || file.name}\n`);
        lines.push('```tsx');
        lines.push(file.content);
        lines.push('```\n');
      }
    });
  } else {
    lines.push('\nNo example code available for this component.');
  }

  return lines.join('\n');
}

/**
 * Check if a string looks like a component name
 */
export function isValidComponentName(name: string): boolean {
  // Must be alphanumeric with optional hyphens and @ prefix
  return /^(@[a-z0-9-]+\/)?[a-z0-9-]+$/i.test(name);
}

/**
 * Extract keywords from text (lowercase, tokenize, remove stopwords)
 */
export function extractKeywords(text: string): string[] {
  const stopwords = new Set(['the', 'a', 'an', 'to', 'for', 'with', 'using', 'create', 'make', 'build', 'add', 'new']);

  const words = text
    .toLowerCase()
    .replace(/[^a-z0-9\s-]/g, ' ')
    .split(/\s+/)
    .filter(word => word.length > 2 && !stopwords.has(word));

  // Remove duplicates
  return Array.from(new Set(words));
}
