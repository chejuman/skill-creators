import { ComponentItem, SearchResult } from './shadcn-client.js';

export interface RegistryConfig {
  [registryName: string]: string; // registry name -> URL template
}

export interface RegistryItemResponse {
  $schema?: string;
  name: string;
  type: string;
  author?: { name?: string; url?: string };
  description?: string;
  dependencies?: string[];
  devDependencies?: string[];
  registryDependencies?: string[];
  files?: Array<{
    path: string;
    content: string;
    type: string;
    target?: string;
  }>;
}

/**
 * HTTP-based registry client for direct registry API access
 */
export class RegistryHttpClient {
  private registryConfig: RegistryConfig;

  constructor(registryConfig: RegistryConfig = {}) {
    this.registryConfig = registryConfig;
  }

  /**
   * Update registry configuration
   */
  setRegistryConfig(config: RegistryConfig): void {
    this.registryConfig = config;
  }

  /**
   * Get registry URL for a specific item
   */
  private getRegistryUrl(registry: string, itemName: string): string {
    const urlTemplate = this.registryConfig[registry];
    if (!urlTemplate) {
      throw new Error(`Registry ${registry} not found in configuration`);
    }

    return urlTemplate.replace('{name}', itemName);
  }

  /**
   * Fetch JSON from URL with error handling
   */
  private async fetchJson<T>(url: string): Promise<T | null> {
    try {
      const response = await fetch(url);

      if (!response.ok) {
        if (response.status === 404) {
          return null;
        }
        throw new Error(`HTTP ${response.status}: ${response.statusText}`);
      }

      return await response.json();
    } catch (error: any) {
      if (error.message.includes('fetch')) {
        throw new Error(`Failed to fetch ${url}: ${error.message}`);
      }
      throw error;
    }
  }

  /**
   * Get a specific registry item
   */
  async getRegistryItem(registry: string, itemName: string): Promise<ComponentItem | null> {
    const url = this.getRegistryUrl(registry, itemName);
    const data = await this.fetchJson<RegistryItemResponse>(url);

    if (!data) {
      return null;
    }

    return this.convertToComponentItem(data, registry);
  }

  /**
   * Search registry by fetching index/registry.json
   */
  async searchRegistry(
    registry: string,
    query?: string,
    limit: number = 100,
    offset: number = 0
  ): Promise<SearchResult> {
    // Try to fetch registry index
    const indexUrl = this.getRegistryUrl(registry, 'index');
    const registryUrl = this.getRegistryUrl(registry, 'registry');

    let items: ComponentItem[] = [];

    // Try index.json first, then registry.json
    let indexData = await this.fetchJson<{ items?: string[] }>(indexUrl);
    if (!indexData) {
      indexData = await this.fetchJson<{ items?: string[] }>(registryUrl);
    }

    if (indexData?.items) {
      // Fetch each item
      const itemPromises = indexData.items.map(itemName =>
        this.getRegistryItem(registry, itemName)
      );

      const results = await Promise.all(itemPromises);
      items = results.filter((item): item is ComponentItem => item !== null);
    }

    // Apply query filter if provided
    if (query) {
      const lowerQuery = query.toLowerCase();
      items = items.filter(
        item =>
          item.name.toLowerCase().includes(lowerQuery) ||
          item.description?.toLowerCase().includes(lowerQuery)
      );
    }

    // Apply pagination
    const total = items.length;
    const paginatedItems = items.slice(offset, offset + limit);

    return {
      items: paginatedItems,
      pagination: {
        total,
        offset,
        limit,
        hasMore: offset + limit < total,
      },
    };
  }

  /**
   * List all items from registry
   */
  async listRegistry(
    registry: string,
    limit: number = 100,
    offset: number = 0
  ): Promise<ComponentItem[]> {
    const result = await this.searchRegistry(registry, undefined, limit, offset);
    return result.items;
  }

  /**
   * Get multiple registry items
   */
  async getRegistryItems(itemNames: string[]): Promise<ComponentItem[]> {
    const items: ComponentItem[] = [];

    for (const itemName of itemNames) {
      // Parse registry from item name (e.g., @shadcn/button)
      const match = itemName.match(/^(@[^/]+)\/(.+)$/);
      if (!match) {
        continue;
      }

      const [, registry, name] = match;
      const item = await this.getRegistryItem(registry, name);
      if (item) {
        items.push(item);
      }
    }

    return items;
  }

  /**
   * Convert registry response to ComponentItem
   */
  private convertToComponentItem(data: RegistryItemResponse, registry: string): ComponentItem {
    return {
      name: data.name,
      type: data.type,
      description: data.description,
      dependencies: data.dependencies,
      devDependencies: data.devDependencies,
      registryDependencies: data.registryDependencies,
      files: data.files?.map(f => ({
        path: f.path,
        content: f.content,
        type: f.type,
      })),
      registry,
    };
  }

  /**
   * Check if registry is accessible
   */
  async testRegistry(registry: string): Promise<boolean> {
    try {
      // Try to fetch index or a common component like button
      const indexUrl = this.getRegistryUrl(registry, 'index');
      const response = await fetch(indexUrl);
      return response.ok;
    } catch {
      return false;
    }
  }
}
