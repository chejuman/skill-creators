import { existsSync, readFileSync, writeFileSync, mkdirSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export interface RegistryInfo {
  name: string;
  url: string;
  addedAt: string;
  lastAccessed: string;
  description?: string;
  verified: boolean;
}

export interface RegistriesCache {
  registries: { [name: string]: RegistryInfo };
  lastUpdated: string;
}

export class RegistryCache {
  private cachePath: string;
  private cache: RegistriesCache;

  constructor() {
    this.cachePath = join(__dirname, '..', 'assets', 'registries-cache.json');
    this.cache = this.loadCache();
  }

  /**
   * Load cache from file
   */
  private loadCache(): RegistriesCache {
    try {
      if (existsSync(this.cachePath)) {
        const content = readFileSync(this.cachePath, 'utf-8');
        return JSON.parse(content);
      }
    } catch (error) {
      console.warn('⚠️  Failed to load registry cache, creating new one');
    }

    return {
      registries: {},
      lastUpdated: new Date().toISOString(),
    };
  }

  /**
   * Save cache to file
   */
  private saveCache(): void {
    try {
      const dir = dirname(this.cachePath);
      if (!existsSync(dir)) {
        mkdirSync(dir, { recursive: true });
      }

      this.cache.lastUpdated = new Date().toISOString();
      writeFileSync(this.cachePath, JSON.stringify(this.cache, null, 2), 'utf-8');
    } catch (error) {
      console.error('❌ Failed to save registry cache:', error);
    }
  }

  /**
   * Add or update a registry
   */
  addRegistry(name: string, url: string, description?: string, verified: boolean = false): void {
    const now = new Date().toISOString();

    if (this.cache.registries[name]) {
      // Update existing
      this.cache.registries[name].lastAccessed = now;
      this.cache.registries[name].verified = verified;
      if (description) {
        this.cache.registries[name].description = description;
      }
    } else {
      // Add new
      this.cache.registries[name] = {
        name,
        url,
        addedAt: now,
        lastAccessed: now,
        description,
        verified,
      };
    }

    this.saveCache();
  }

  /**
   * Remove a registry
   */
  removeRegistry(name: string): boolean {
    if (this.cache.registries[name]) {
      delete this.cache.registries[name];
      this.saveCache();
      return true;
    }
    return false;
  }

  /**
   * Get a registry by name
   */
  getRegistry(name: string): RegistryInfo | null {
    return this.cache.registries[name] || null;
  }

  /**
   * Get all registries
   */
  getAllRegistries(): RegistryInfo[] {
    return Object.values(this.cache.registries).sort((a, b) =>
      b.lastAccessed.localeCompare(a.lastAccessed)
    );
  }

  /**
   * Check if registry exists in cache
   */
  hasRegistry(name: string): boolean {
    return !!this.cache.registries[name];
  }

  /**
   * Update last accessed time
   */
  updateLastAccessed(name: string): void {
    if (this.cache.registries[name]) {
      this.cache.registries[name].lastAccessed = new Date().toISOString();
      this.saveCache();
    }
  }

  /**
   * Mark registry as verified (successfully accessed)
   */
  markAsVerified(name: string): void {
    if (this.cache.registries[name]) {
      this.cache.registries[name].verified = true;
      this.cache.registries[name].lastAccessed = new Date().toISOString();
      this.saveCache();
    }
  }

  /**
   * Get cache statistics
   */
  getStats(): { total: number; verified: number; lastUpdated: string } {
    const all = this.getAllRegistries();
    return {
      total: all.length,
      verified: all.filter(r => r.verified).length,
      lastUpdated: this.cache.lastUpdated,
    };
  }

  /**
   * Clear all cached registries
   */
  clear(): void {
    this.cache = {
      registries: {},
      lastUpdated: new Date().toISOString(),
    };
    this.saveCache();
  }

  /**
   * Import registries from project components.json format
   */
  importFromConfig(registries: { [name: string]: string }): void {
    for (const [name, url] of Object.entries(registries)) {
      this.addRegistry(name, url, `Imported from project config`, false);
    }
  }

  /**
   * Export to components.json format
   */
  exportToConfig(): { [name: string]: string } {
    const result: { [name: string]: string } = {};
    for (const [name, info] of Object.entries(this.cache.registries)) {
      result[name] = info.url;
    }
    return result;
  }
}
