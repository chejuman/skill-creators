/**
 * Langfuse API Client Wrapper
 *
 * Provides a clean interface for interacting with Langfuse API
 * Handles pagination, variable extraction, and prompt compilation
 */

import { Langfuse, ChatPromptClient } from 'langfuse';
import { extractVariables } from './utils.js';

export interface PromptMetadata {
  name: string;
  description: string;
  type: 'chat' | 'text';
  variables: string[];
  version: number;
  labels: string[];
  tags?: string[];
}

export interface PromptDetail extends PromptMetadata {
  template: string | ChatMessage[];
  createdAt: string;
  updatedAt: string;
}

export interface ChatMessage {
  role: string;
  content: string;
}

export interface CompiledPrompt {
  type: 'chat' | 'text';
  content: string | ChatMessage[];
}

export class LangfuseClient {
  private langfuse: Langfuse;

  constructor() {
    // Load credentials from environment
    const secretKey = process.env.LANGFUSE_SECRET_KEY;
    const publicKey = process.env.LANGFUSE_PUBLIC_KEY;
    const baseUrl = process.env.LANGFUSE_BASE_URL || 'https://cloud.langfuse.com';

    if (!secretKey || !publicKey) {
      throw new Error(
        'Missing Langfuse credentials. Please set LANGFUSE_SECRET_KEY and LANGFUSE_PUBLIC_KEY environment variables.'
      );
    }

    this.langfuse = new Langfuse({
      secretKey,
      publicKey,
      baseUrl,
    });
  }

  /**
   * List production prompts with pagination
   */
  async listPrompts(options?: { limit?: number; page?: number }): Promise<PromptMetadata[]> {
    const limit = options?.limit || 100;
    const page = options?.page || 1;

    try {
      const response = await this.langfuse.api.promptsList({
        limit,
        page,
        label: 'production',
      });

      const prompts: PromptMetadata[] = await Promise.all(
        response.data.map(async (item) => {
          // Get full prompt to extract variables
          const prompt = await this.langfuse.getPrompt(item.name, undefined, {
            cacheTtlSeconds: 0,
          });

          const variables = extractVariables(JSON.stringify(prompt.prompt));

          return {
            name: item.name,
            description: item.name, // Langfuse API doesn't return description in list
            type: item.type === 'chat' ? 'chat' : 'text',
            variables,
            version: item.version,
            labels: item.labels || [],
            tags: item.tags || [],
          };
        })
      );

      return prompts;
    } catch (error: any) {
      throw new Error(`Failed to list prompts: ${error.message}`);
    }
  }

  /**
   * Get all prompts (handles pagination automatically)
   */
  async getAllPrompts(): Promise<PromptMetadata[]> {
    const allPrompts: PromptMetadata[] = [];
    let page = 1;
    let hasMore = true;

    while (hasMore) {
      try {
        const response = await this.langfuse.api.promptsList({
          limit: 100,
          page,
          label: 'production',
        });

        const prompts = await Promise.all(
          response.data.map(async (item) => {
            const prompt = await this.langfuse.getPrompt(item.name, undefined, {
              cacheTtlSeconds: 0,
            });

            const variables = extractVariables(JSON.stringify(prompt.prompt));

            return {
              name: item.name,
              description: item.name,
              type: item.type === 'chat' ? 'chat' : 'text',
              variables,
              version: item.version,
              labels: item.labels || [],
              tags: item.tags || [],
            } as PromptMetadata;
          })
        );

        allPrompts.push(...prompts);

        // Check if there are more pages
        hasMore = response.meta.totalPages > page;
        page++;
      } catch (error: any) {
        throw new Error(`Failed to fetch page ${page}: ${error.message}`);
      }
    }

    return allPrompts;
  }

  /**
   * Get specific prompt details
   */
  async getPrompt(name: string, version?: number): Promise<PromptDetail> {
    try {
      const prompt = await this.langfuse.getPrompt(name, version, {
        cacheTtlSeconds: 0,
      });

      const variables = extractVariables(JSON.stringify(prompt.prompt));

      return {
        name: prompt.name,
        description: prompt.name,
        type: prompt.type === 'chat' ? 'chat' : 'text',
        variables,
        version: prompt.version,
        labels: prompt.labels || [],
        tags: prompt.tags || [],
        template: prompt.prompt,
        createdAt: new Date().toISOString(), // Langfuse doesn't expose these
        updatedAt: new Date().toISOString(),
      };
    } catch (error: any) {
      throw new Error(`Failed to get prompt '${name}': ${error.message}`);
    }
  }

  /**
   * Compile prompt with variables
   * Handles both chat and text prompt types with fallback
   */
  async compilePrompt(
    name: string,
    variables: Record<string, string>
  ): Promise<CompiledPrompt> {
    try {
      // Try chat prompt type first
      try {
        const prompt = await this.langfuse.getPrompt(name, undefined, {
          type: 'chat',
        });

        if (prompt.type !== 'chat') {
          throw new Error('Not a chat prompt');
        }

        const compiled = prompt.compile(variables) as ChatPromptClient['prompt'];

        // Transform role mappings: "ai"/"assistant" → "assistant", others → "user"
        const messages: ChatMessage[] = compiled.map((msg: any) => ({
          role: ['ai', 'assistant'].includes(msg.role) ? 'assistant' : 'user',
          content: msg.content,
        }));

        return {
          type: 'chat',
          content: messages,
        };
      } catch (chatError) {
        // Fallback to text prompt type
        const prompt = await this.langfuse.getPrompt(name, undefined, {
          type: 'text',
        });

        const compiled = prompt.compile(variables) as string;

        return {
          type: 'text',
          content: compiled,
        };
      }
    } catch (error: any) {
      throw new Error(`Failed to compile prompt '${name}': ${error.message}`);
    }
  }
}
