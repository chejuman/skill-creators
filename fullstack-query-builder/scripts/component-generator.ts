import { promises as fs } from 'fs';
import path from 'path';
import Mustache from 'mustache';
import type { DesignSpec, QueryResults } from './state-manager.js';
import { toPascalCase, toTitleCase, toCamelCase } from './utils.js';

export class ComponentGenerator {
  private assetPath: string;

  constructor(assetPath: string) {
    this.assetPath = assetPath;
  }

  async generateComponents(
    frontendPath: string,
    designSpec: DesignSpec,
    queryResults: QueryResults,
    resourceName: string
  ): Promise<void> {
    const uiType = queryResults.uiRecommendation?.type || 'table';
    const componentName = toPascalCase(resourceName);

    switch (uiType) {
      case 'table':
        await this.generateTableComponent(frontendPath, componentName, queryResults);
        break;
      case 'cards':
        await this.generateCardComponent(frontendPath, componentName, queryResults);
        break;
      case 'detail':
        await this.generateDetailComponent(frontendPath, componentName, queryResults);
        break;
      case 'dashboard':
        await this.generateDashboardComponent(frontendPath, componentName, queryResults);
        break;
    }

    await this.generateTypes(frontendPath, componentName, queryResults);
    await this.generateStore(frontendPath, componentName);
    await this.generateMainPage(frontendPath, componentName, uiType);
  }

  private async generateTableComponent(
    frontendPath: string,
    componentName: string,
    queryResults: QueryResults
  ): Promise<void> {
    const templatePath = path.join(this.assetPath, 'components/table-view.tsx.template');
    const template = await fs.readFile(templatePath, 'utf-8');

    const data = {
      ComponentName: `${componentName}Table`,
      DataType: componentName,
      columns: queryResults.columns.map(col => ({
        name: col,
        label: toTitleCase(col),
        type: queryResults.columnTypes[col]
      }))
    };

    const output = Mustache.render(template, data);
    const outputPath = path.join(
      frontendPath,
      'src/components',
      `${componentName}Table.tsx`
    );

    await fs.writeFile(outputPath, output);
    console.log(`✅ Generated ${componentName}Table component`);
  }

  private async generateCardComponent(
    frontendPath: string,
    componentName: string,
    queryResults: QueryResults
  ): Promise<void> {
    const templatePath = path.join(this.assetPath, 'components/card-grid.tsx.template');
    const template = await fs.readFile(templatePath, 'utf-8');

    const data = {
      ComponentName: `${componentName}Card`,
      GridComponentName: `${componentName}Grid`,
      DataType: componentName,
      columns: queryResults.columns.map(col => ({
        name: col,
        label: toTitleCase(col),
        type: queryResults.columnTypes[col]
      }))
    };

    const output = Mustache.render(template, data);
    const outputPath = path.join(
      frontendPath,
      'src/components',
      `${componentName}Card.tsx`
    );

    await fs.writeFile(outputPath, output);
    console.log(`✅ Generated ${componentName}Card component`);
  }

  private async generateDetailComponent(
    frontendPath: string,
    componentName: string,
    queryResults: QueryResults
  ): Promise<void> {
    const templatePath = path.join(this.assetPath, 'components/detail-view.tsx.template');
    const template = await fs.readFile(templatePath, 'utf-8');

    const data = {
      ComponentName: `${componentName}Detail`,
      DataType: componentName,
      columns: queryResults.columns.map(col => ({
        name: col,
        label: toTitleCase(col),
        type: queryResults.columnTypes[col]
      }))
    };

    const output = Mustache.render(template, data);
    const outputPath = path.join(
      frontendPath,
      'src/components',
      `${componentName}Detail.tsx`
    );

    await fs.writeFile(outputPath, output);
    console.log(`✅ Generated ${componentName}Detail component`);
  }

  private async generateDashboardComponent(
    frontendPath: string,
    componentName: string,
    queryResults: QueryResults
  ): Promise<void> {
    const templatePath = path.join(this.assetPath, 'components/dashboard.tsx.template');
    const template = await fs.readFile(templatePath, 'utf-8');

    const data = {
      ComponentName: `${componentName}Dashboard`,
      DataType: componentName,
      metrics: queryResults.columns
        .filter(col => queryResults.columnTypes[col] === 'number')
        .map(col => ({
          name: col,
          label: toTitleCase(col)
        }))
    };

    const output = Mustache.render(template, data);
    const outputPath = path.join(
      frontendPath,
      'src/components',
      `${componentName}Dashboard.tsx`
    );

    await fs.writeFile(outputPath, output);
    console.log(`✅ Generated ${componentName}Dashboard component`);
  }

  private async generateTypes(
    frontendPath: string,
    componentName: string,
    queryResults: QueryResults
  ): Promise<void> {
    const fields = queryResults.columns.map(col => {
      const tsType = this.getTSType(queryResults.columnTypes[col]);
      return `  ${col}: ${tsType};`;
    }).join('\n');

    const typeContent = `export interface ${componentName} {\n${fields}\n}\n`;

    const outputPath = path.join(frontendPath, 'src/types', `${componentName}.ts`);
    await fs.writeFile(outputPath, typeContent);
    console.log(`✅ Generated ${componentName} type definitions`);
  }

  private async generateStore(frontendPath: string, componentName: string): Promise<void> {
    const storeName = toCamelCase(componentName);
    const storeContent = `import { create } from 'zustand';
import type { ${componentName} } from '../types/${componentName}';

interface ${componentName}Store {
  items: ${componentName}[];
  setItems: (items: ${componentName}[]) => void;
  loading: boolean;
  setLoading: (loading: boolean) => void;
  error: string | null;
  setError: (error: string | null) => void;
}

export const use${componentName}Store = create<${componentName}Store>((set) => ({
  items: [],
  setItems: (items) => set({ items }),
  loading: false,
  setLoading: (loading) => set({ loading }),
  error: null,
  setError: (error) => set({ error }),
}));
`;

    const outputPath = path.join(frontendPath, 'src/store', `${storeName}Store.ts`);
    await fs.writeFile(outputPath, storeContent);
    console.log(`✅ Generated ${componentName} store`);
  }

  private async generateMainPage(
    frontendPath: string,
    componentName: string,
    uiType: string
  ): Promise<void> {
    const componentImport = this.getComponentImport(componentName, uiType);
    const pageContent = `import { ${componentImport} } from '../components/${componentImport}';

export function ${componentName}Page() {
  return (
    <div className="container mx-auto py-8">
      <h1 className="text-3xl font-bold mb-6">${toTitleCase(componentName)}</h1>
      <${componentImport} />
    </div>
  );
}
`;

    const outputPath = path.join(frontendPath, 'src/pages', `${componentName}Page.tsx`);
    await fs.writeFile(outputPath, pageContent);
    console.log(`✅ Generated ${componentName}Page`);
  }

  private getComponentImport(componentName: string, uiType: string): string {
    switch (uiType) {
      case 'table': return `${componentName}Table`;
      case 'cards': return `${componentName}Card`;
      case 'detail': return `${componentName}Detail`;
      case 'dashboard': return `${componentName}Dashboard`;
      default: return `${componentName}Table`;
    }
  }

  private getTSType(columnType: string): string {
    const map: Record<string, string> = {
      'number': 'number',
      'string': 'string',
      'boolean': 'boolean',
      'date': 'Date'
    };
    return map[columnType] || 'string';
  }
}
