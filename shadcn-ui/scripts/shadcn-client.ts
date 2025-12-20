import { execShadcnCommand, parseShadcnOutput, normalizeComponentName } from './utils.js';
import { RegistryHttpClient } from './registry-http-client.js';
import { existsSync, readFileSync } from 'fs';
import { join } from 'path';

export interface ComponentItem {
  name: string;
  type?: string;
  description?: string;
  dependencies?: string[];
  devDependencies?: string[];
  registryDependencies?: string[];
  files?: ComponentFile[];
  registry?: string;
}

export interface ComponentFile {
  path: string;
  content: string;
  type?: string;
}

export interface SearchResult {
  items: ComponentItem[];
  pagination: {
    total: number;
    offset: number;
    limit: number;
    hasMore: boolean;
  };
}

export interface ProjectInfo {
  hasConfig: boolean;
  registries?: string[];
  registryUrls?: { [name: string]: string };
  style?: string;
  typescript?: boolean;
  tailwind?: { cssVariables?: boolean };
}

export interface ListOptions {
  limit?: number;
  offset?: number;
}

export interface SearchOptions extends ListOptions {
  query?: string;
}

export interface AddOptions {
  yes?: boolean;
  overwrite?: boolean;
  path?: string;
}

export class ShadcnClient {
  private cwd: string;
  private httpClient: RegistryHttpClient;
  private useHttp: boolean = false;

  constructor(cwd?: string) {
    this.cwd = cwd || process.cwd();
    this.httpClient = new RegistryHttpClient();
    this.initializeHttpClient();
  }

  /**
   * Initialize HTTP client with registry config from components.json
   */
  private async initializeHttpClient(): Promise<void> {
    try {
      const projectInfo = await this.getProjectInfo();
      if (projectInfo.registryUrls) {
        this.httpClient.setRegistryConfig(projectInfo.registryUrls);
        this.useHttp = true;
      }
    } catch {
      // Fallback to CLI mode
      this.useHttp = false;
    }
  }

  /**
   * List all components from registry
   */
  async listComponents(registry?: string, options: ListOptions = {}): Promise<ComponentItem[]> {
    const { limit = 100, offset = 0 } = options;
    const registryArg = registry || '@shadcn';

    // Ensure HTTP client is initialized
    await this.initializeHttpClient();

    // Try HTTP first if registry is configured
    if (this.useHttp && registry) {
      try {
        return await this.httpClient.listRegistry(registry, limit, offset);
      } catch (error: any) {
        console.warn(`⚠️  HTTP failed, falling back to CLI: ${error.message}`);
        // Fall through to CLI
      }
    }

    // Fallback to CLI
    const command = `search ${registryArg} -l ${limit} -o ${offset}`;
    const output = await execShadcnCommand(command, this.cwd);
    const parsed = parseShadcnOutput(output, 'json');

    // Handle different output formats
    if (Array.isArray(parsed)) {
      return parsed;
    }

    if (parsed.items) {
      return parsed.items;
    }

    // Parse table format
    return this.parseTableOutput(output);
  }

  /**
   * Search components by query
   */
  async searchComponents(query: string, registry?: string, options: SearchOptions = {}): Promise<SearchResult> {
    const { limit = 100, offset = 0 } = options;
    const registryArg = registry || '@shadcn';

    // Ensure HTTP client is initialized
    await this.initializeHttpClient();

    // Try HTTP first if registry is configured
    if (this.useHttp && registry) {
      try {
        return await this.httpClient.searchRegistry(registry, query, limit, offset);
      } catch (error: any) {
        console.warn(`⚠️  HTTP failed, falling back to CLI: ${error.message}`);
        // Fall through to CLI
      }
    }

    // Fallback to CLI
    const command = `search ${registryArg} -q "${query}" -l ${limit} -o ${offset}`;
    const output = await execShadcnCommand(command, this.cwd);
    const parsed = parseShadcnOutput(output, 'json');

    // Handle different output formats
    if (Array.isArray(parsed)) {
      return {
        items: parsed,
        pagination: {
          total: parsed.length,
          offset,
          limit,
          hasMore: false,
        },
      };
    }

    if (parsed.items && parsed.pagination) {
      return parsed as SearchResult;
    }

    // Parse table format
    const items = this.parseTableOutput(output);
    return {
      items,
      pagination: {
        total: items.length,
        offset,
        limit,
        hasMore: false,
      },
    };
  }

  /**
   * View component details
   */
  async viewComponent(componentName: string): Promise<ComponentItem> {
    // Ensure HTTP client is initialized
    await this.initializeHttpClient();

    // Check if component name has registry prefix (@registry/component)
    const registryMatch = componentName.match(/^(@[^/]+)\/(.+)$/);

    if (this.useHttp && registryMatch) {
      const [, registry, name] = registryMatch;
      try {
        const item = await this.httpClient.getRegistryItem(registry, name);
        if (item) {
          return item;
        }
      } catch (error: any) {
        console.warn(`⚠️  HTTP failed, falling back to CLI: ${error.message}`);
        // Fall through to CLI
      }
    }

    // Fallback to CLI
    const command = `view ${componentName}`;
    const output = await execShadcnCommand(command, this.cwd);
    const parsed = parseShadcnOutput(output, 'json');

    // shadcn view always returns JSON
    if (Array.isArray(parsed) && parsed.length > 0) {
      return parsed[0];
    }

    return parsed as ComponentItem;
  }

  /**
   * Get project info
   */
  async getProjectInfo(): Promise<ProjectInfo> {
    const configPath = join(this.cwd, 'components.json');
    const hasConfig = existsSync(configPath);

    if (!hasConfig) {
      return { hasConfig: false };
    }

    try {
      const configContent = readFileSync(configPath, 'utf-8');
      const config = JSON.parse(configContent);

      return {
        hasConfig: true,
        registries: config.registries ? Object.keys(config.registries) : undefined,
        registryUrls: config.registries || undefined,
        style: config.style,
        typescript: config.typescript,
        tailwind: config.tailwind,
      };
    } catch (error) {
      return { hasConfig: true };
    }
  }

  /**
   * Check if components.json exists
   */
  async hasComponentsConfig(): Promise<boolean> {
    const configPath = join(this.cwd, 'components.json');
    return existsSync(configPath);
  }

  /**
   * Generate add command (does not execute)
   */
  generateAddCommand(componentNames: string[], options: AddOptions = {}): string {
    const components = componentNames.join(' ');
    const flags: string[] = [];

    if (options.yes) flags.push('--yes');
    if (options.overwrite) flags.push('--overwrite');
    if (options.path) flags.push(`--path ${options.path}`);

    const flagsStr = flags.length > 0 ? ' ' + flags.join(' ') : '';

    return `npx shadcn@latest add ${components}${flagsStr}`;
  }

  /**
   * Parse table-formatted output
   */
  private parseTableOutput(output: string): ComponentItem[] {
    const lines = output.split('\n').filter(line => line.trim());
    const items: ComponentItem[] = [];

    for (const line of lines) {
      // Skip header and separator lines
      if (line.includes('─') || line.includes('Name') || line.includes('Type')) {
        continue;
      }

      // Try to extract component name
      const match = line.match(/│\s*([a-z0-9-]+)\s*│/i);
      if (match) {
        items.push({
          name: match[1].trim(),
        });
      }
    }

    return items;
  }
}
