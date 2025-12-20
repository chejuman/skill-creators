import { readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { ComponentItem } from './shadcn-client.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

export interface ComponentMetadata {
  category: string;
  keywords: string[];
  useCases: string[];
  relatedComponents?: string[];
}

export interface ComponentCategories {
  [componentName: string]: ComponentMetadata;
}

export class RegistryManager {
  private categories: Map<string, ComponentMetadata>;
  private loaded: boolean = false;

  constructor() {
    this.categories = new Map();
  }

  /**
   * Load component categories from assets/component-categories.json
   */
  async loadCategories(): Promise<void> {
    if (this.loaded) {
      return;
    }

    try {
      const categoriesPath = join(__dirname, '..', 'assets', 'component-categories.json');
      const content = readFileSync(categoriesPath, 'utf-8');
      const data: ComponentCategories = JSON.parse(content);

      // Populate map
      for (const [name, metadata] of Object.entries(data)) {
        this.categories.set(name.toLowerCase(), metadata);
      }

      this.loaded = true;
    } catch (error) {
      // If categories file doesn't exist, use defaults
      console.warn('⚠️  Component categories file not found, using defaults');
      this.loaded = true;
    }
  }

  /**
   * Get metadata for a component
   */
  getMetadata(componentName: string): ComponentMetadata | null {
    const normalized = componentName.toLowerCase().replace(/^@[^/]+\//, '');
    return this.categories.get(normalized) || null;
  }

  /**
   * Get all components in a category
   */
  getComponentsByCategory(category: string): string[] {
    const components: string[] = [];

    for (const [name, metadata] of this.categories.entries()) {
      if (metadata.category === category) {
        components.push(name);
      }
    }

    return components;
  }

  /**
   * Get all available categories
   */
  getAllCategories(): string[] {
    const categories = new Set<string>();

    for (const metadata of this.categories.values()) {
      categories.add(metadata.category);
    }

    return Array.from(categories).sort();
  }

  /**
   * Enrich component item with metadata
   */
  enrichComponentItem(item: ComponentItem): ComponentItem & { metadata?: ComponentMetadata } {
    const metadata = this.getMetadata(item.name);

    return {
      ...item,
      metadata: metadata || undefined,
    };
  }

  /**
   * Infer category from component name and type
   */
  categorizeComponent(name: string, type?: string): string {
    // Check if we have metadata
    const metadata = this.getMetadata(name);
    if (metadata) {
      return metadata.category;
    }

    // Infer from name
    const lowerName = name.toLowerCase();

    if (lowerName.includes('form') || lowerName.includes('input') || lowerName.includes('select')) {
      return 'form';
    }

    if (lowerName.includes('button') || lowerName.includes('link')) {
      return 'interactive';
    }

    if (lowerName.includes('dialog') || lowerName.includes('modal') || lowerName.includes('popup')) {
      return 'overlay';
    }

    if (lowerName.includes('table') || lowerName.includes('list') || lowerName.includes('card')) {
      return 'data';
    }

    if (lowerName.includes('nav') || lowerName.includes('menu') || lowerName.includes('tabs')) {
      return 'navigation';
    }

    if (lowerName.includes('alert') || lowerName.includes('toast') || lowerName.includes('notification')) {
      return 'feedback';
    }

    // Infer from type
    if (type) {
      if (type.includes('hook')) return 'hook';
      if (type.includes('block')) return 'block';
      if (type.includes('ui')) return 'ui';
    }

    return 'other';
  }

  /**
   * Extract keywords from component item
   */
  extractKeywords(component: ComponentItem): string[] {
    const keywords: string[] = [];

    // Add name
    keywords.push(component.name);

    // Add from metadata
    const metadata = this.getMetadata(component.name);
    if (metadata) {
      keywords.push(...metadata.keywords);
    }

    // Add from description
    if (component.description) {
      const words = component.description
        .toLowerCase()
        .replace(/[^a-z0-9\s]/g, ' ')
        .split(/\s+/)
        .filter(word => word.length > 3);

      keywords.push(...words);
    }

    // Add from dependencies
    if (component.dependencies) {
      keywords.push(...component.dependencies);
    }

    // Remove duplicates
    return Array.from(new Set(keywords));
  }
}
