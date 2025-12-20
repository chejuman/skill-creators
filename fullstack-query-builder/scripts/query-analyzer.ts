import type { QueryResult } from './db-connector.js';
import type { QueryResults } from './state-manager.js';

export interface UIRecommendation {
  type: 'table' | 'cards' | 'detail' | 'form' | 'dashboard';
  confidence: number;
  rationale: string;
  suggestedComponents: string[];
}

export class QueryAnalyzer {
  analyzeResults(queryResult: QueryResult, query: string): QueryResults {
    const { rows, rowCount, fields } = queryResult;

    const columns = fields.map(f => f.name);
    const columnTypes: Record<string, string> = {};

    fields.forEach(field => {
      columnTypes[field.name] = this.detectColumnType(
        field.name,
        field.dataTypeID,
        rows.slice(0, 5).map(r => r[field.name])
      );
    });

    const sampleData = rows.slice(0, 10);
    const uiRecommendation = this.recommendUIType(rowCount, columns.length, query, columnTypes);

    return {
      rowCount,
      columns,
      columnTypes,
      sampleData,
      uiRecommendation
    };
  }

  private recommendUIType(
    rowCount: number,
    columnCount: number,
    query: string,
    columnTypes: Record<string, string>
  ): UIRecommendation {
    const upperQuery = query.toUpperCase();

    // Single row → Detail view
    if (rowCount === 1) {
      return {
        type: 'detail',
        confidence: 0.95,
        rationale: 'Single row is best displayed as a detail view',
        suggestedComponents: ['Card', 'Badge', 'Separator']
      };
    }

    // Aggregated data → Dashboard
    if (this.hasAggregations(upperQuery)) {
      return {
        type: 'dashboard',
        confidence: 0.88,
        rationale: 'Aggregated data is best shown in a dashboard',
        suggestedComponents: ['Card', 'Progress', 'Badge']
      };
    }

    // Few rows + rich columns → Cards
    if (rowCount <= 10 && columnCount >= 4) {
      return {
        type: 'cards',
        confidence: 0.85,
        rationale: 'Small dataset with rich information suits card grid layout',
        suggestedComponents: ['Card', 'Badge', 'Button']
      };
    }

    // Many rows → Table (default for most cases)
    if (rowCount > 10 && columnCount <= 10) {
      return {
        type: 'table',
        confidence: 0.90,
        rationale: 'Large structured data is best displayed in a table',
        suggestedComponents: ['Table', 'Pagination', 'DropdownMenu', 'Button']
      };
    }

    // Default fallback
    return {
      type: 'table',
      confidence: 0.70,
      rationale: 'Default table view for structured data',
      suggestedComponents: ['Table', 'Pagination']
    };
  }

  private hasAggregations(query: string): boolean {
    const aggregateFunctions = ['COUNT', 'SUM', 'AVG', 'MIN', 'MAX', 'GROUP BY'];
    return aggregateFunctions.some(func => query.includes(func));
  }

  private detectColumnType(
    columnName: string,
    dataTypeID: number,
    samples: any[]
  ): string {
    // PostgreSQL type ID mapping
    const typeMap: Record<number, string> = {
      20: 'number',    // bigint
      21: 'number',    // smallint
      23: 'number',    // integer
      700: 'number',   // real
      701: 'number',   // double precision
      1082: 'date',    // date
      1114: 'date',    // timestamp
      1184: 'date',    // timestamptz
      16: 'boolean',   // boolean
      25: 'string',    // text
      1043: 'string',  // varchar
      2950: 'string'   // uuid
    };

    if (typeMap[dataTypeID]) {
      return typeMap[dataTypeID];
    }

    // Fallback: infer from samples
    const nonNullSamples = samples.filter(v => v != null);
    if (nonNullSamples.length === 0) return 'string';

    if (nonNullSamples.every(v => typeof v === 'number')) return 'number';
    if (nonNullSamples.every(v => typeof v === 'boolean')) return 'boolean';
    if (nonNullSamples.every(v => this.isValidDate(v))) return 'date';

    return 'string';
  }

  private isValidDate(value: any): boolean {
    if (value instanceof Date) return !isNaN(value.getTime());
    if (typeof value === 'string') {
      const date = new Date(value);
      return !isNaN(date.getTime());
    }
    return false;
  }

  getTSType(columnType: string): string {
    const map: Record<string, string> = {
      'number': 'number',
      'string': 'string',
      'boolean': 'boolean',
      'date': 'Date'
    };
    return map[columnType] || 'string';
  }

  getPythonType(columnType: string): string {
    const map: Record<string, string> = {
      'number': 'int',
      'string': 'str',
      'boolean': 'bool',
      'date': 'datetime'
    };
    return map[columnType] || 'str';
  }
}
