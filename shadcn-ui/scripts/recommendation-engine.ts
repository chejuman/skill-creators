import { ShadcnClient, ComponentItem } from './shadcn-client.js';
import { RegistryManager } from './registry-manager.js';
import { extractKeywords } from './utils.js';

export interface RecommendationScore {
  component: ComponentItem;
  score: number;
  reasons: string[];
}

// Category keyword mappings
const CATEGORY_KEYWORDS: Record<string, string[]> = {
  form: ['form', 'input', 'field', 'validation', 'submit', 'checkbox', 'radio', 'select', 'textarea'],
  layout: ['layout', 'grid', 'flex', 'container', 'section', 'column', 'row'],
  navigation: ['nav', 'menu', 'breadcrumb', 'tab', 'link', 'sidebar', 'header'],
  data: ['table', 'list', 'card', 'display', 'show', 'data', 'grid'],
  feedback: ['alert', 'toast', 'notification', 'message', 'error', 'success', 'warning'],
  overlay: ['dialog', 'modal', 'popup', 'dropdown', 'tooltip', 'popover', 'sheet'],
  interactive: ['button', 'click', 'action', 'toggle', 'switch', 'slider'],
};

export class RecommendationEngine {
  private registryManager: RegistryManager;
  private client: ShadcnClient;

  constructor(client: ShadcnClient, registryManager: RegistryManager) {
    this.client = client;
    this.registryManager = registryManager;
  }

  /**
   * Recommend components based on task description
   */
  async recommend(taskDescription: string, limit: number = 10): Promise<RecommendationScore[]> {
    // Extract keywords from task description
    const keywords = extractKeywords(taskDescription);

    // Infer categories
    const categories = this.inferCategories(keywords);

    // Fetch all components
    const components = await this.client.listComponents();

    // Score each component
    const scored: RecommendationScore[] = [];

    for (const component of components) {
      const score = this.scoreComponent(component, keywords, categories);

      if (score > 0) {
        const reasons = this.explainScore(component, keywords, categories);
        scored.push({
          component: this.registryManager.enrichComponentItem(component),
          score,
          reasons,
        });
      }
    }

    // Sort by score (descending) and return top N
    scored.sort((a, b) => b.score - a.score);
    return scored.slice(0, limit);
  }

  /**
   * Score a component based on relevance to keywords and categories
   */
  private scoreComponent(component: ComponentItem, keywords: string[], categories: string[]): number {
    let score = 0;

    const componentName = component.name.toLowerCase();
    const componentDesc = (component.description || '').toLowerCase();
    const componentKeywords = this.registryManager.extractKeywords(component);
    const componentCategory = this.registryManager.categorizeComponent(component.name, component.type);

    // Exact name match (weight: 20)
    if (keywords.some(kw => componentName === kw)) {
      score += 20;
    }

    // Name contains keyword (weight: 10)
    for (const keyword of keywords) {
      if (componentName.includes(keyword)) {
        score += 10;
      }
    }

    // Description contains keyword (weight: 5)
    for (const keyword of keywords) {
      if (componentDesc.includes(keyword)) {
        score += 5;
      }
    }

    // Category match (weight: 8)
    if (categories.includes(componentCategory)) {
      score += 8;
    }

    // Keyword overlap (weight: 3 per keyword)
    for (const keyword of keywords) {
      if (componentKeywords.some(ck => ck.includes(keyword) || keyword.includes(ck))) {
        score += 3;
      }
    }

    // Type preference: ui > block > hook (weight: 2)
    if (component.type) {
      if (component.type.includes('ui')) score += 2;
      else if (component.type.includes('block')) score += 1;
    }

    return score;
  }

  /**
   * Infer categories from keywords
   */
  private inferCategories(keywords: string[]): string[] {
    const categories = new Set<string>();

    for (const [category, categoryKeywords] of Object.entries(CATEGORY_KEYWORDS)) {
      for (const keyword of keywords) {
        if (categoryKeywords.some(ck => ck.includes(keyword) || keyword.includes(ck))) {
          categories.add(category);
        }
      }
    }

    return Array.from(categories);
  }

  /**
   * Explain why a component was scored
   */
  private explainScore(component: ComponentItem, keywords: string[], categories: string[]): string[] {
    const reasons: string[] = [];

    const componentName = component.name.toLowerCase();
    const componentDesc = (component.description || '').toLowerCase();
    const componentCategory = this.registryManager.categorizeComponent(component.name, component.type);

    // Name matches
    const matchedNameKeywords = keywords.filter(kw => componentName.includes(kw));
    if (matchedNameKeywords.length > 0) {
      reasons.push(`Name matches: ${matchedNameKeywords.join(', ')}`);
    }

    // Description matches
    const matchedDescKeywords = keywords.filter(kw => componentDesc.includes(kw));
    if (matchedDescKeywords.length > 0) {
      reasons.push(`Description matches: ${matchedDescKeywords.join(', ')}`);
    }

    // Category match
    if (categories.includes(componentCategory)) {
      reasons.push(`Category: ${componentCategory}`);
    }

    // Type
    if (component.type) {
      reasons.push(`Type: ${component.type.replace('registry:', '')}`);
    }

    // Metadata use cases
    const metadata = this.registryManager.getMetadata(component.name);
    if (metadata && metadata.useCases && metadata.useCases.length > 0) {
      reasons.push(`Use cases: ${metadata.useCases.join(', ')}`);
    }

    return reasons.length > 0 ? reasons : ['General match'];
  }
}
