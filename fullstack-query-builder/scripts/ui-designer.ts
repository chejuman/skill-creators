import type { QueryResults, DesignSpec } from './state-manager.js';
import { toPascalCase } from './utils.js';

export class UIDesigner {
  generateDesign(queryResults: QueryResults, resourceName: string): DesignSpec {
    const uiType = queryResults.uiRecommendation?.type || 'table';
    const componentName = toPascalCase(resourceName);

    switch (uiType) {
      case 'table':
        return this.designTableView(componentName, queryResults);
      case 'cards':
        return this.designCardGrid(componentName, queryResults);
      case 'detail':
        return this.designDetailView(componentName, queryResults);
      case 'dashboard':
        return this.designDashboard(componentName, queryResults);
      default:
        return this.designTableView(componentName, queryResults);
    }
  }

  private designTableView(componentName: string, queryResults: QueryResults): DesignSpec {
    return {
      mainView: `${componentName}Table`,
      components: [
        `${componentName}Table`,
        'TableFilters',
        'PaginationControls'
      ],
      shadcnComponents: [
        'Table',
        'TableHeader',
        'TableBody',
        'TableRow',
        'TableHead',
        'TableCell',
        'Button',
        'DropdownMenu',
        'Input'
      ],
      layout: 'single-page-with-filters',
      props: {
        columns: queryResults.columns,
        columnTypes: queryResults.columnTypes,
        enableSorting: queryResults.rowCount > 10,
        enableFiltering: queryResults.rowCount > 20,
        enablePagination: queryResults.rowCount > 50,
        pageSize: 50
      }
    };
  }

  private designCardGrid(componentName: string, queryResults: QueryResults): DesignSpec {
    const primaryFields = this.selectPrimaryFields(queryResults);

    return {
      mainView: `${componentName}Grid`,
      components: [
        `${componentName}Card`,
        `${componentName}Grid`
      ],
      shadcnComponents: [
        'Card',
        'CardHeader',
        'CardTitle',
        'CardContent',
        'Badge',
        'Button'
      ],
      layout: 'grid-layout',
      props: {
        columns: queryResults.columns,
        columnTypes: queryResults.columnTypes,
        primaryFields,
        gridColumns: queryResults.rowCount <= 4 ? 2 : 3
      }
    };
  }

  private designDetailView(componentName: string, queryResults: QueryResults): DesignSpec {
    return {
      mainView: `${componentName}Detail`,
      components: [`${componentName}Detail`],
      shadcnComponents: [
        'Card',
        'CardHeader',
        'CardTitle',
        'CardContent',
        'Separator',
        'Badge',
        'Label'
      ],
      layout: 'single-card',
      props: {
        columns: queryResults.columns,
        columnTypes: queryResults.columnTypes,
        sections: this.groupIntoSections(queryResults.columns)
      }
    };
  }

  private designDashboard(componentName: string, queryResults: QueryResults): DesignSpec {
    return {
      mainView: `${componentName}Dashboard`,
      components: [
        'MetricCard',
        'ChartCard',
        `${componentName}Dashboard`
      ],
      shadcnComponents: [
        'Card',
        'CardHeader',
        'CardTitle',
        'CardContent',
        'Progress',
        'Badge'
      ],
      layout: 'dashboard-grid',
      props: {
        columns: queryResults.columns,
        columnTypes: queryResults.columnTypes,
        metrics: this.identifyMetrics(queryResults)
      }
    };
  }

  private selectPrimaryFields(queryResults: QueryResults): string[] {
    const columns = queryResults.columns;
    const priorityFields: string[] = [];

    // Common name patterns
    const namePatterns = ['name', 'title', 'label', 'description'];
    for (const pattern of namePatterns) {
      const match = columns.find(col => col.toLowerCase().includes(pattern));
      if (match) priorityFields.push(match);
    }

    // Add first 3-4 non-ID columns
    const nonIdColumns = columns.filter(col =>
      !col.toLowerCase().includes('id') &&
      !priorityFields.includes(col)
    );
    priorityFields.push(...nonIdColumns.slice(0, Math.min(3, nonIdColumns.length)));

    return priorityFields.length > 0 ? priorityFields : columns.slice(0, 3);
  }

  private groupIntoSections(columns: string[]): Array<{ title: string; fields: string[] }> {
    // Simple grouping: split into sections of 5 fields
    const sections: Array<{ title: string; fields: string[] }> = [];
    for (let i = 0; i < columns.length; i += 5) {
      sections.push({
        title: i === 0 ? 'Basic Information' : `Additional Details ${Math.floor(i / 5)}`,
        fields: columns.slice(i, i + 5)
      });
    }
    return sections;
  }

  private identifyMetrics(queryResults: QueryResults): Array<{ name: string; type: string }> {
    return queryResults.columns
      .filter(col => queryResults.columnTypes[col] === 'number')
      .map(col => ({ name: col, type: 'number' }));
  }
}
