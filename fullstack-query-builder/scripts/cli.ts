#!/usr/bin/env node

import { createInterface } from 'readline';
import path from 'path';
import { DatabaseConnector } from './db-connector.js';
import { QueryAnalyzer } from './query-analyzer.js';
import { UIDesigner } from './ui-designer.js';
import { FrontendScaffold } from './frontend-scaffold.js';
import { ComponentGenerator } from './component-generator.js';
import { BackendDesigner } from './backend-designer.js';
import { BackendScaffold } from './backend-scaffold.js';
import { APIGenerator } from './api-generator.js';
import { IntegrationManager } from './integration-manager.js';
import { loadState, saveState, updatePhase, resetState, createInitialState } from './state-manager.js';

const readline = createInterface({
  input: process.stdin,
  output: process.stdout
});

function prompt(question: string): Promise<string> {
  return new Promise(resolve => readline.question(question, resolve));
}

async function phase1(): Promise<void> {
  console.log('\n=== Phase 1: Database Query & Analysis ===\n');

  const connStr = await prompt('PostgreSQL connection string: ');
  const query = await prompt('SQL query: ');

  const db = new DatabaseConnector();
  await db.connect(connStr);

  const result = await db.executeQuery(query);
  const analyzer = new QueryAnalyzer();
  const analysis = analyzer.analyzeResults(result, query);

  console.log(`\n✅ Query executed: ${analysis.rowCount} rows, ${analysis.columns.length} columns`);
  console.log(`✅ Recommended UI: ${analysis.uiRecommendation?.type} (confidence: ${analysis.uiRecommendation?.confidence})`);
  console.log(`   Rationale: ${analysis.uiRecommendation?.rationale}`);

  await db.close();

  const approve = await prompt('\n→ Continue with this data? [y/N]: ');
  if (approve.toLowerCase() !== 'y') {
    console.log('Aborting. Run again to try different query.');
    process.exit(0);
  }

  await updatePhase(1, { dbConnection: db.getMaskedConnection(), query, results: analysis }, true);
  console.log('\n✅ Phase 1 complete. Run: npx tsx cli.ts continue 2');
}

async function phase2(): Promise<void> {
  console.log('\n=== Phase 2: UI Design Expert Analysis ===\n');

  const state = await loadState();
  if (!state || !state.phases[1]) {
    console.error('❌ Phase 1 not completed. Run: npx tsx cli.ts start');
    process.exit(1);
  }

  const resourceName = await prompt('Resource name (e.g., users, products): ');
  const designer = new UIDesigner();
  const design = designer.generateDesign(state.phases[1].results, resourceName);

  console.log('\nUI Design Generated:');
  console.log(`  - Main View: ${design.mainView}`);
  console.log(`  - Components: ${design.components.join(', ')}`);
  console.log(`  - shadcn/ui: ${design.shadcnComponents.join(', ')}`);
  console.log(`  - Layout: ${design.layout}`);

  const approve = await prompt('\n→ Approve design? [y/N]: ');
  if (approve.toLowerCase() !== 'y') {
    console.log('Run again to modify design.');
    process.exit(0);
  }

  await updatePhase(2, { resourceName, designSpec: design }, true);
  console.log('\n✅ Phase 2 complete. Run: npx tsx cli.ts continue 3');
}

async function phase3(): Promise<void> {
  console.log('\n=== Phase 3: Frontend Implementation ===\n');

  const state = await loadState();
  if (!state || !state.phases[2]) {
    console.error('❌ Phase 2 not completed.');
    process.exit(1);
  }

  const projectPath = await prompt('Project path (e.g., ./my-app): ');
  const projectName = path.basename(projectPath);

  const scaffold = new FrontendScaffold();
  await scaffold.createProject(projectPath, projectName);

  const assetPath = path.join(process.cwd(), '../assets');
  const generator = new ComponentGenerator(assetPath);
  await generator.generateComponents(
    path.join(projectPath, 'frontend'),
    state.phases[2].designSpec,
    state.phases[1].results,
    state.phases[2].resourceName
  );

  state.projectPath = projectPath;
  await saveState(state);

  console.log('\n✅ Frontend scaffold complete');
  console.log(`→ Run: cd ${projectPath}/frontend && npm run dev`);

  const approve = await prompt('\n→ Frontend looks correct? [y/N]: ');
  if (approve.toLowerCase() !== 'y') {
    console.log('Review and modify generated code as needed.');
    process.exit(0);
  }

  await updatePhase(3, { frontendPath: path.join(projectPath, 'frontend') }, true);
  console.log('\n✅ Phase 3 complete. Run: npx tsx cli.ts continue 4');
}

async function phase4(): Promise<void> {
  console.log('\n=== Phase 4: Backend API Design ===\n');

  const state = await loadState();
  if (!state || !state.phases[3]) {
    console.error('❌ Phase 3 not completed.');
    process.exit(1);
  }

  const designer = new BackendDesigner();
  const apiDesign = designer.designAPI(state.phases[1].results, state.phases[2].resourceName);

  console.log('\nAPI Design:');
  apiDesign.endpoints.forEach(ep => {
    console.log(`  - ${ep.method} ${ep.path} → ${ep.responseModel}`);
  });

  const approve = await prompt('\n→ Approve API design? [y/N]: ');
  if (approve.toLowerCase() !== 'y') {
    console.log('Run again to modify design.');
    process.exit(0);
  }

  await updatePhase(4, { apiDesign }, true);
  console.log('\n✅ Phase 4 complete. Run: npx tsx cli.ts continue 5');
}

async function phase5(): Promise<void> {
  console.log('\n=== Phase 5: Backend Implementation ===\n');

  const state = await loadState();
  if (!state || !state.phases[4]) {
    console.error('❌ Phase 4 not completed.');
    process.exit(1);
  }

  const scaffold = new BackendScaffold();
  await scaffold.createProject(state.projectPath!, state.phases[1].dbConnection);

  const assetPath = path.join(process.cwd(), '../assets');
  const generator = new APIGenerator(assetPath);
  await generator.generateAPI(
    path.join(state.projectPath!, 'backend'),
    state.phases[4].apiDesign,
    state.phases[1].results,
    state.phases[2].resourceName
  );

  console.log('\n✅ Backend scaffold complete');
  console.log(`→ Run: cd ${state.projectPath}/backend && uvicorn app.main:app --reload`);

  const approve = await prompt('\n→ Backend works? [y/N]: ');
  if (approve.toLowerCase() !== 'y') {
    console.log('Review and test backend as needed.');
    process.exit(0);
  }

  await updatePhase(5, { backendPath: path.join(state.projectPath!, 'backend') }, true);
  console.log('\n✅ Phase 5 complete. Run: npx tsx cli.ts continue 6');
}

async function phase6(): Promise<void> {
  console.log('\n=== Phase 6: Full Integration ===\n');

  const state = await loadState();
  if (!state || !state.phases[5]) {
    console.error('❌ Phase 5 not completed.');
    process.exit(1);
  }

  const integration = new IntegrationManager();
  await integration.integrate(
    state.projectPath!,
    state.phases[2].resourceName,
    state.phases[1].results,
    state.phases[1].dbConnection
  );

  console.log('\n✅ Integration complete!');
  console.log('\nTo run the application:');
  console.log(`  Terminal 1: cd ${state.projectPath}/backend && uvicorn app.main:app --reload`);
  console.log(`  Terminal 2: cd ${state.projectPath}/frontend && npm run dev`);
  console.log(`  Open: http://localhost:5173`);

  await updatePhase(6, {}, true);
}

async function showStatus(): Promise<void> {
  const state = await loadState();
  if (!state) {
    console.log('No workflow in progress. Run: npx tsx cli.ts start');
    return;
  }

  console.log('\n=== Workflow Status ===\n');
  console.log(`Current Phase: ${state.currentPhase}`);
  console.log(`Project Path: ${state.projectPath || 'Not set'}`);

  for (let i = 1; i <= 6; i++) {
    const status = state.phases[i]?.completed ? '✅' : '⏳';
    console.log(`  ${status} Phase ${i}`);
  }
}

async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  try {
    if (command === 'start') {
      await phase1();
    } else if (command === 'continue') {
      const phase = parseInt(args[1]);
      if (phase === 2) await phase2();
      else if (phase === 3) await phase3();
      else if (phase === 4) await phase4();
      else if (phase === 5) await phase5();
      else if (phase === 6) await phase6();
      else console.error('Invalid phase. Use 2-6.');
    } else if (command === 'status') {
      await showStatus();
    } else if (command === 'reset') {
      await resetState();
      console.log('✅ State reset');
    } else {
      console.log('Full-Stack Query Builder CLI\n');
      console.log('Commands:');
      console.log('  npx tsx cli.ts start           - Begin Phase 1');
      console.log('  npx tsx cli.ts continue <2-6>  - Continue from phase');
      console.log('  npx tsx cli.ts status          - Show workflow status');
      console.log('  npx tsx cli.ts reset           - Reset state');
    }
  } catch (error: any) {
    console.error(`\n❌ Error: ${error.message}`);
    process.exit(1);
  } finally {
    readline.close();
  }
}

main();
