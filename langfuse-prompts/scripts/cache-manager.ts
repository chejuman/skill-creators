/**
 * Cache Manager
 *
 * Manages local caching of prompt metadata for fast access
 * Implements TTL-based cache invalidation
 */

import { readFile, writeFile, stat, mkdir } from 'fs/promises';
import { resolve, dirname } from 'path';
import { existsSync } from 'fs';
import { PromptMetadata, LangfuseClient } from './langfuse-client.js';

export interface PromptCache {
  lastUpdated: string; // ISO 8601 timestamp
  ttl: number; // TTL in seconds
  prompts: PromptMetadata[];
}

export interface CacheInfo {
  exists: boolean;
  lastUpdated: string | null;
  age: number | null; // seconds
  count: number;
  isValid: boolean;
}

export class CacheManager {
  private static CACHE_PATH = resolve(dirname(new URL(import.meta.url).pathname), '../assets/prompts.json');

  /**
   * Load cache from file
   */
  static async load(): Promise<PromptCache> {
    try {
      if (!existsSync(this.CACHE_PATH)) {
        // Return empty cache if file doesn't exist
        return {
          lastUpdated: new Date(0).toISOString(),
          ttl: this.getTTL(),
          prompts: [],
        };
      }

      const data = await readFile(this.CACHE_PATH, 'utf-8');
      const cache: PromptCache = JSON.parse(data);

      return cache;
    } catch (error: any) {
      console.error(`Warning: Failed to load cache: ${error.message}`);
      return {
        lastUpdated: new Date(0).toISOString(),
        ttl: this.getTTL(),
        prompts: [],
      };
    }
  }

  /**
   * Save cache to file
   */
  static async save(cache: PromptCache): Promise<void> {
    try {
      // Ensure assets directory exists
      const assetsDir = dirname(this.CACHE_PATH);
      if (!existsSync(assetsDir)) {
        await mkdir(assetsDir, { recursive: true });
      }

      await writeFile(this.CACHE_PATH, JSON.stringify(cache, null, 2), 'utf-8');
    } catch (error: any) {
      throw new Error(`Failed to save cache: ${error.message}`);
    }
  }

  /**
   * Check if cache is valid (not expired)
   */
  static isValid(cache: PromptCache): boolean {
    const ttl = this.getTTL();
    const age = (Date.now() - new Date(cache.lastUpdated).getTime()) / 1000;
    return age < ttl && cache.prompts.length > 0;
  }

  /**
   * Refresh cache from Langfuse API
   */
  static async refresh(): Promise<PromptCache> {
    try {
      const client = new LangfuseClient();
      const prompts = await client.getAllPrompts();

      const cache: PromptCache = {
        lastUpdated: new Date().toISOString(),
        ttl: this.getTTL(),
        prompts,
      };

      await this.save(cache);
      return cache;
    } catch (error: any) {
      throw new Error(`Failed to refresh cache: ${error.message}`);
    }
  }

  /**
   * Get cache info
   */
  static async info(): Promise<CacheInfo> {
    try {
      const exists = existsSync(this.CACHE_PATH);

      if (!exists) {
        return {
          exists: false,
          lastUpdated: null,
          age: null,
          count: 0,
          isValid: false,
        };
      }

      const cache = await this.load();
      const age = (Date.now() - new Date(cache.lastUpdated).getTime()) / 1000;

      return {
        exists: true,
        lastUpdated: cache.lastUpdated,
        age,
        count: cache.prompts.length,
        isValid: this.isValid(cache),
      };
    } catch (error: any) {
      throw new Error(`Failed to get cache info: ${error.message}`);
    }
  }

  /**
   * Clear cache
   */
  static async clear(): Promise<void> {
    try {
      if (existsSync(this.CACHE_PATH)) {
        const emptyCache: PromptCache = {
          lastUpdated: new Date(0).toISOString(),
          ttl: this.getTTL(),
          prompts: [],
        };
        await this.save(emptyCache);
      }
    } catch (error: any) {
      throw new Error(`Failed to clear cache: ${error.message}`);
    }
  }

  /**
   * Load cache with auto-refresh if stale
   */
  static async loadWithRefresh(): Promise<PromptCache> {
    const cache = await this.load();

    if (!this.isValid(cache)) {
      console.log('Cache is stale or empty, refreshing...');
      return await this.refresh();
    }

    return cache;
  }

  /**
   * Get TTL from environment or default
   */
  private static getTTL(): number {
    return parseInt(process.env.PROMPT_CACHE_TTL_SECONDS || '3600');
  }
}
