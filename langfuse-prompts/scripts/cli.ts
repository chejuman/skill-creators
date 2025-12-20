#!/usr/bin/env node
/**
 * Langfuse Prompts CLI
 *
 * Command-line interface for managing Langfuse prompts
 * Supports list, search, recommend, get, execute, and cache operations
 */

import dotenv from 'dotenv';
import { resolve } from 'path';
import { readFile } from 'fs/promises';
import { LangfuseClient } from './langfuse-client.js';
import { CacheManager } from './cache-manager.js';

// Load environment variables following skill-creator spec hierarchy
const skillEnv = resolve(process.cwd(), '.env');
const skillsEnv = resolve(process.cwd(), '../.env');
const claudeEnv = resolve(process.cwd(), '../../.env');

dotenv.config({ path: claudeEnv });
dotenv.config({ path: skillsEnv });
dotenv.config({ path: skillEnv });

/**
 * Display usage information
 */
function printUsage() {
  console.log(`
Langfuse Prompts CLI

Usage:
  npx tsx cli.ts <command> [arguments]

Commands:
  list                           List all production prompts and cache them
  search <query>                 Search cached prompts by name/description
  recommend "<task-description>" Display prompts for Claude to analyze
  get <prompt-name>              Get specific prompt details
  execute <prompt-name> <vars>   Execute prompt with variables (vars as JSON string or file path)
  cache-refresh                  Force refresh the local cache
  cache-info                     Show cache information

Examples:
  npx tsx cli.ts list
  npx tsx cli.ts search "email"
  npx tsx cli.ts recommend "user onboarding email"
  npx tsx cli.ts get user-welcome-email
  npx tsx cli.ts execute user-welcome-email '{"user_name":"John","company":"Acme"}'
  npx tsx cli.ts execute user-welcome-email vars.json
  npx tsx cli.ts cache-refresh
  npx tsx cli.ts cache-info
  `);
}

/**
 * List all prompts and cache them
 */
async function handleList() {
  try {
    console.log('📋 Fetching production prompts from Langfuse...\n');

    const cache = await CacheManager.refresh();

    console.log(`✅ Found ${cache.prompts.length} prompts\n`);
    console.log('Prompts by Type:');

    const chatPrompts = cache.prompts.filter((p) => p.type === 'chat');
    const textPrompts = cache.prompts.filter((p) => p.type === 'text');

    console.log(`  Chat: ${chatPrompts.length}`);
    console.log(`  Text: ${textPrompts.length}\n`);

    console.log('All Prompts:');
    cache.prompts.forEach((prompt, idx) => {
      console.log(`  ${idx + 1}. ${prompt.name} (${prompt.type})`);
      console.log(`     Variables: ${prompt.variables.length > 0 ? prompt.variables.join(', ') : 'None'}`);
      if (prompt.tags && prompt.tags.length > 0) {
        console.log(`     Tags: ${prompt.tags.join(', ')}`);
      }
    });

    console.log(`\n💾 Cached ${cache.prompts.length} prompts to assets/prompts.json`);
  } catch (error: any) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Search prompts by query
 */
async function handleSearch(query: string) {
  try {
    const cache = await CacheManager.loadWithRefresh();
    const lowerQuery = query.toLowerCase();

    const matches = cache.prompts.filter(
      (p) =>
        p.name.toLowerCase().includes(lowerQuery) ||
        (p.description && p.description.toLowerCase().includes(lowerQuery)) ||
        (p.tags && p.tags.some((tag) => tag.toLowerCase().includes(lowerQuery)))
    );

    if (matches.length === 0) {
      console.log(`No prompts found matching: "${query}"`);
      return;
    }

    console.log(`Found ${matches.length} prompt(s) matching "${query}":\n`);

    matches.forEach((prompt, idx) => {
      console.log(`${idx + 1}. ${prompt.name}`);
      console.log(`   Type: ${prompt.type}`);
      console.log(`   Variables: ${prompt.variables.length > 0 ? prompt.variables.join(', ') : 'None'}`);
      if (prompt.tags && prompt.tags.length > 0) {
        console.log(`   Tags: ${prompt.tags.join(', ')}`);
      }
      console.log('');
    });
  } catch (error: any) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Display all prompts for Claude to recommend
 */
async function handleRecommend(taskDescription: string) {
  try {
    const cache = await CacheManager.loadWithRefresh();

    if (cache.prompts.length === 0) {
      console.log('No prompts available. Run "npx tsx cli.ts list" first.');
      return;
    }

    console.log(`Task: ${taskDescription}\n`);
    console.log(`Available Prompts (${cache.prompts.length} total):\n`);

    cache.prompts.forEach((prompt, idx) => {
      console.log(`${idx + 1}. ${prompt.name}`);
      console.log(`   Description: ${prompt.description || 'No description'}`);
      console.log(`   Type: ${prompt.type}`);
      console.log(`   Variables: ${prompt.variables.length > 0 ? prompt.variables.join(', ') : 'None'}`);
      if (prompt.tags && prompt.tags.length > 0) {
        console.log(`   Tags: ${prompt.tags.join(', ')}`);
      }
      console.log('');
    });

    console.log('📊 Claude: Please analyze the task and recommend the most suitable prompt(s).\n');
  } catch (error: any) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Get specific prompt details
 */
async function handleGet(promptName: string) {
  try {
    console.log(`🔍 Fetching prompt: ${promptName}...\n`);

    const client = new LangfuseClient();
    const prompt = await client.getPrompt(promptName);

    console.log(`Name: ${prompt.name}`);
    console.log(`Type: ${prompt.type}`);
    console.log(`Version: ${prompt.version}`);
    console.log(`Variables: ${prompt.variables.length > 0 ? prompt.variables.join(', ') : 'None'}`);
    console.log(`Labels: ${prompt.labels.join(', ')}`);
    if (prompt.tags && prompt.tags.length > 0) {
      console.log(`Tags: ${prompt.tags.join(', ')}`);
    }

    console.log('\nTemplate:');
    console.log('---');
    if (prompt.type === 'chat') {
      const messages = prompt.template as any[];
      messages.forEach((msg: any) => {
        console.log(`[${msg.role}]: ${msg.content}`);
      });
    } else {
      console.log(prompt.template);
    }
    console.log('---\n');
  } catch (error: any) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Execute prompt with variables
 */
async function handleExecute(promptName: string, varsInput: string) {
  try {
    // Parse variables (either JSON string or file path)
    let variables: Record<string, string>;

    if (varsInput.endsWith('.json')) {
      // Load from file
      const fileContent = await readFile(varsInput, 'utf-8');
      variables = JSON.parse(fileContent);
    } else {
      // Parse as JSON string
      variables = JSON.parse(varsInput);
    }

    console.log(`⚙️  Compiling prompt: ${promptName}...\n`);

    const client = new LangfuseClient();
    const compiled = await client.compilePrompt(promptName, variables);

    console.log(`Type: ${compiled.type}\n`);
    console.log('Compiled Prompt:');
    console.log('---');

    if (compiled.type === 'chat') {
      const messages = compiled.content as any[];
      messages.forEach((msg: any) => {
        console.log(`[${msg.role}]: ${msg.content}`);
      });
    } else {
      console.log(compiled.content);
    }

    console.log('---\n');
  } catch (error: any) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Refresh cache
 */
async function handleCacheRefresh() {
  try {
    console.log('🔄 Refreshing cache...\n');

    const cache = await CacheManager.refresh();

    console.log(`✅ Cache refreshed successfully`);
    console.log(`   Prompts: ${cache.prompts.length}`);
    console.log(`   Last Updated: ${new Date(cache.lastUpdated).toLocaleString()}`);
    console.log(`   TTL: ${cache.ttl} seconds (${Math.floor(cache.ttl / 60)} minutes)\n`);
  } catch (error: any) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Show cache info
 */
async function handleCacheInfo() {
  try {
    const info = await CacheManager.info();

    console.log('📊 Cache Information:\n');

    if (!info.exists) {
      console.log('   Status: No cache exists');
      console.log('   Run "npx tsx cli.ts list" to create cache\n');
      return;
    }

    console.log(`   Status: ${info.isValid ? '✅ Valid' : '⚠️  Stale/Empty'}`);
    console.log(`   Prompts: ${info.count}`);
    console.log(`   Last Updated: ${new Date(info.lastUpdated!).toLocaleString()}`);
    console.log(`   Age: ${Math.floor(info.age!)} seconds (${Math.floor(info.age! / 60)} minutes)`);

    const ttl = parseInt(process.env.PROMPT_CACHE_TTL_SECONDS || '3600');
    const remaining = Math.max(0, ttl - info.age!);
    console.log(`   TTL: ${ttl} seconds`);
    console.log(`   Remaining: ${Math.floor(remaining)} seconds (${Math.floor(remaining / 60)} minutes)\n`);

    if (!info.isValid) {
      console.log('   💡 Run "npx tsx cli.ts cache-refresh" to update\n');
    }
  } catch (error: any) {
    console.error(`❌ Error: ${error.message}`);
    process.exit(1);
  }
}

/**
 * Main CLI entry point
 */
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === 'help' || command === '--help' || command === '-h') {
    printUsage();
    return;
  }

  switch (command) {
    case 'list':
      await handleList();
      break;

    case 'search':
      if (!args[1]) {
        console.error('❌ Error: Search query required');
        console.log('Usage: npx tsx cli.ts search <query>');
        process.exit(1);
      }
      await handleSearch(args[1]);
      break;

    case 'recommend':
      if (!args[1]) {
        console.error('❌ Error: Task description required');
        console.log('Usage: npx tsx cli.ts recommend "<task-description>"');
        process.exit(1);
      }
      await handleRecommend(args[1]);
      break;

    case 'get':
      if (!args[1]) {
        console.error('❌ Error: Prompt name required');
        console.log('Usage: npx tsx cli.ts get <prompt-name>');
        process.exit(1);
      }
      await handleGet(args[1]);
      break;

    case 'execute':
      if (!args[1] || !args[2]) {
        console.error('❌ Error: Prompt name and variables required');
        console.log('Usage: npx tsx cli.ts execute <prompt-name> <vars>');
        console.log('       vars can be JSON string or file path (.json)');
        process.exit(1);
      }
      await handleExecute(args[1], args[2]);
      break;

    case 'cache-refresh':
      await handleCacheRefresh();
      break;

    case 'cache-info':
      await handleCacheInfo();
      break;

    default:
      console.error(`❌ Unknown command: ${command}`);
      printUsage();
      process.exit(1);
  }
}

// Run CLI
main().catch((error) => {
  console.error('Fatal error:', error);
  process.exit(1);
});
