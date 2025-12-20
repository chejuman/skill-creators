#!/usr/bin/env node
import { config } from 'dotenv';
import { existsSync, readFileSync } from 'fs';
import { join, dirname } from 'path';
import { fileURLToPath } from 'url';
import { ShadcnClient } from './shadcn-client.js';
import { RegistryManager } from './registry-manager.js';
import { RecommendationEngine } from './recommendation-engine.js';
import { RegistryCache } from './registry-cache.js';
import { formatComponentList, formatComponentDetails, formatExamples } from './utils.js';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);

// Load environment (skill-creator hierarchy)
function loadEnvironment(): void {
  const envPaths = [
    join(__dirname, '..', '.env'),
    join(__dirname, '..', '..', '.env'),
    join(__dirname, '..', '..', '..', '.env'),
  ];

  for (const envPath of envPaths) {
    if (existsSync(envPath)) {
      config({ path: envPath });
      break;
    }
  }
}

// Print usage
function printUsage(): void {
  console.log(`
shadcn-ui CLI - Manage shadcn/ui components

Usage: npx tsx cli.ts <command> [options]

Commands:
  list [registry]                    List all available components
  search <query> [registry]          Search components by keyword
  view <component>                   View component details
  examples <component>               Get usage examples for component
  recommend "<task>"                 Get component recommendations for a task
  add-command <components...>        Generate add command for components
  registries [list|add|remove]       Manage known registries
  audit                              Show project audit checklist

Registry Management:
  registries list                    Show all known registries
  registries add <name> <url>        Add a new registry
  registries remove <name>           Remove a registry
  registries import                  Import from project components.json

Examples:
  npx tsx cli.ts list
  npx tsx cli.ts search "button"
  npx tsx cli.ts view button
  npx tsx cli.ts examples button
  npx tsx cli.ts recommend "user registration form"
  npx tsx cli.ts add-command button card input
  npx tsx cli.ts registries
  npx tsx cli.ts audit
`);
}

// Main function
async function main() {
  loadEnvironment();

  const args = process.argv.slice(2);
  const command = args[0];

  if (!command || command === 'help' || command === '--help' || command === '-h') {
    printUsage();
    process.exit(0);
  }

  const client = new ShadcnClient();
  const registryManager = new RegistryManager();
  const registryCache = new RegistryCache();
  await registryManager.loadCategories();

  try {
    switch (command) {
      case 'list': {
        const registry = args[1];
        console.log('📦 Listing components...\n');
        const components = await client.listComponents(registry);
        console.log(formatComponentList(components));
        console.log(`\n✅ Found ${components.length} components`);

        // Save registry to cache if successfully accessed
        if (components.length > 0 && registry) {
          // Get actual URL from components.json
          const projectInfo = await client.getProjectInfo();
          const registryUrl = projectInfo.registryUrls?.[registry] || `https://ui.shadcn.com/r/{name}.json`;
          registryCache.addRegistry(registry, registryUrl, `Auto-discovered from list command`, true);
        }
        break;
      }

      case 'search': {
        const query = args[1];
        const registry = args[2];

        if (!query) {
          console.error('❌ Error: Search query required');
          console.log('Usage: npx tsx cli.ts search <query> [registry]');
          process.exit(1);
        }

        console.log(`🔍 Searching for "${query}"...\n`);
        const result = await client.searchComponents(query, registry);
        console.log(formatComponentList(result.items));
        console.log(`\n✅ Found ${result.items.length} components`);

        if (result.pagination.hasMore) {
          console.log(`\n💡 More results available. Use offset: ${result.pagination.offset + result.pagination.limit}`);
        }
        break;
      }

      case 'view': {
        const componentName = args[1];

        if (!componentName) {
          console.error('❌ Error: Component name required');
          console.log('Usage: npx tsx cli.ts view <component>');
          process.exit(1);
        }

        console.log(`📖 Viewing ${componentName}...\n`);
        const component = await client.viewComponent(componentName);
        console.log(formatComponentDetails(component));

        // Extract and save registry from component name like @8bitcn/button
        const registryMatch = componentName.match(/^(@[^/]+)\//);
        if (registryMatch) {
          const registryName = registryMatch[1];
          // Get actual URL from components.json
          const projectInfo = await client.getProjectInfo();
          const registryUrl = projectInfo.registryUrls?.[registryName] || `https://ui.shadcn.com/r/{name}.json`;
          registryCache.addRegistry(registryName, registryUrl, `Auto-discovered from view command`, true);
        }
        break;
      }

      case 'examples': {
        const componentName = args[1];

        if (!componentName) {
          console.error('❌ Error: Component name required');
          console.log('Usage: npx tsx cli.ts examples <component>');
          process.exit(1);
        }

        console.log(`📝 Getting examples for ${componentName}...\n`);
        const component = await client.viewComponent(componentName);
        console.log(formatExamples(component));
        break;
      }

      case 'recommend': {
        const taskDescription = args.slice(1).join(' ');

        if (!taskDescription) {
          console.error('❌ Error: Task description required');
          console.log('Usage: npx tsx cli.ts recommend "<task description>"');
          process.exit(1);
        }

        console.log(`🤖 Analyzing task: "${taskDescription}"\n`);
        const engine = new RecommendationEngine(client, registryManager);
        const recommendations = await engine.recommend(taskDescription, 10);

        if (recommendations.length === 0) {
          console.log('❌ No recommendations found. Try a different task description.');
          process.exit(0);
        }

        console.log(`## Top ${recommendations.length} Component Recommendations\n`);

        recommendations.forEach((rec, index) => {
          console.log(`${index + 1}. **${rec.component.name}** (score: ${rec.score})`);

          if (rec.component.type) {
            console.log(`   Type: ${rec.component.type}`);
          }

          if (rec.component.description) {
            console.log(`   ${rec.component.description}`);
          }

          if (rec.reasons.length > 0) {
            console.log(`   Reasons: ${rec.reasons.join(', ')}`);
          }

          if (rec.component.metadata) {
            console.log(`   Use cases: ${rec.component.metadata.useCases.join(', ')}`);
          }

          console.log('');
        });

        console.log('\n💡 Use "view" command to see details or "add-command" to install components.');
        break;
      }

      case 'add-command': {
        const components = args.slice(1);

        if (components.length === 0) {
          console.error('❌ Error: At least one component name required');
          console.log('Usage: npx tsx cli.ts add-command <component1> [component2] ...');
          process.exit(1);
        }

        console.log('📦 Generating add command...\n');
        const addCommand = client.generateAddCommand(components);
        console.log('Run this command to install:');
        console.log(`\n  ${addCommand}\n`);
        break;
      }

      case 'registries': {
        const subcommand = args[1];

        if (subcommand === 'add') {
          const name = args[2];
          const url = args[3];
          const description = args.slice(4).join(' ') || undefined;

          if (!name || !url) {
            console.error('❌ Error: Name and URL required');
            console.log('Usage: npx tsx cli.ts registries add <name> <url> [description]');
            process.exit(1);
          }

          registryCache.addRegistry(name, url, description, false);
          console.log(`✅ Added registry: ${name}`);
          console.log(`   URL: ${url}`);
          if (description) console.log(`   Description: ${description}`);
          break;
        }

        if (subcommand === 'remove') {
          const name = args[2];

          if (!name) {
            console.error('❌ Error: Registry name required');
            console.log('Usage: npx tsx cli.ts registries remove <name>');
            process.exit(1);
          }

          const removed = registryCache.removeRegistry(name);
          if (removed) {
            console.log(`✅ Removed registry: ${name}`);
          } else {
            console.log(`❌ Registry not found: ${name}`);
          }
          break;
        }

        if (subcommand === 'import') {
          console.log('📥 Importing registries from project components.json...\n');
          const projectInfo = await client.getProjectInfo();

          if (!projectInfo.hasConfig) {
            console.log('❌ No components.json found in current directory.');
            process.exit(1);
          }

          // Read the full config to get registry URLs
          const configPath = join(process.cwd(), 'components.json');
          if (existsSync(configPath)) {
            const configContent = readFileSync(configPath, 'utf-8');
            const projectConfig = JSON.parse(configContent);
            if (projectConfig.registries) {
              registryCache.importFromConfig(projectConfig.registries);
              console.log(`✅ Imported ${Object.keys(projectConfig.registries).length} registries`);
            }
          }
          break;
        }

        // Default: list all registries
        console.log('📋 Known Registries\n');

        const allRegistries = registryCache.getAllRegistries();
        const stats = registryCache.getStats();

        if (allRegistries.length === 0) {
          console.log('❌ No registries in cache.');
          console.log('\n💡 Registries are auto-discovered when you use view/list/search commands.');
          console.log('💡 Or manually add with: npx tsx cli.ts registries add <name> <url>\n');
          break;
        }

        console.log(`Total: ${stats.total} | Verified: ${stats.verified} | Last updated: ${new Date(stats.lastUpdated).toLocaleString()}\n`);

        allRegistries.forEach((reg, index) => {
          console.log(`${index + 1}. ${reg.name}`);
          console.log(`   URL: ${reg.url}`);
          if (reg.description) {
            console.log(`   Description: ${reg.description}`);
          }
          console.log(`   Status: ${reg.verified ? '✅ Verified' : '⚠️  Unverified'}`);
          console.log(`   Added: ${new Date(reg.addedAt).toLocaleString()}`);
          console.log(`   Last accessed: ${new Date(reg.lastAccessed).toLocaleString()}`);
          console.log('');
        });

        console.log('💡 Commands:');
        console.log('   registries add <name> <url>    - Add a new registry');
        console.log('   registries remove <name>       - Remove a registry');
        console.log('   registries import              - Import from components.json\n');

        // Also show project config if available
        const projectInfo = await client.getProjectInfo();
        if (projectInfo.hasConfig && projectInfo.registries && projectInfo.registries.length > 0) {
          console.log('📂 Project Configuration (components.json):\n');
          projectInfo.registries.forEach(reg => {
            const url = projectInfo.registryUrls?.[reg];
            if (url) {
              console.log(`  ${reg}`);
              console.log(`    URL: ${url}`);
            } else {
              console.log(`  - ${reg}`);
            }
          });
          console.log('\n💡 Tip: Run "registries import" to add these to your cache');
          console.log('');
        }

        break;
      }

      case 'audit': {
        console.log('🔍 Project Audit Checklist\n');
        console.log('## After Adding Components\n');
        console.log('Run through this checklist to ensure everything works:\n');
        console.log('- [ ] Ensure all imports are correct (named vs default)');
        console.log('- [ ] If using next/image, configure images.remotePatterns in next.config.js');
        console.log('- [ ] Verify all dependencies are installed (npm install)');
        console.log('- [ ] Check for linting errors (npm run lint)');
        console.log('- [ ] Check for TypeScript errors (npm run type-check or tsc)');
        console.log('- [ ] Test components in browser');
        console.log('- [ ] Verify responsive design on different screen sizes');
        console.log('- [ ] Check accessibility (ARIA labels, keyboard navigation)');
        console.log('\n💡 Common Issues:\n');
        console.log('  • Missing dependencies: Run npm install again');
        console.log('  • Import errors: Check component path matches your project structure');
        console.log('  • Style issues: Verify Tailwind CSS is configured correctly');
        console.log('  • Type errors: Ensure TypeScript is configured (tsconfig.json)\n');
        break;
      }

      default:
        console.error(`❌ Unknown command: ${command}`);
        printUsage();
        process.exit(1);
    }
  } catch (error: any) {
    console.error(`\n❌ Error: ${error.message}\n`);

    // Provide helpful suggestions
    if (error.message.includes('components.json')) {
      console.log('💡 To initialize shadcn/ui, run: npx shadcn@latest init\n');
    } else if (error.message.includes('not found')) {
      console.log('💡 Try searching with: npx tsx cli.ts search <query>\n');
    }

    process.exit(1);
  }
}

main();
