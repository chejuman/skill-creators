import type { QueryResults, APIDesign } from './state-manager.js';
import { toPascalCase, toSnakeCase, toCamelCase } from './utils.js';

export class BackendDesigner {
  designAPI(queryResults: QueryResults, resourceName: string): APIDesign {
    const resource = toSnakeCase(resourceName);
    const modelName = toPascalCase(resourceName);

    const endpoints = [
      {
        method: 'GET',
        path: `/api/${resource}`,
        functionName: `list_${resource}`,
        responseModel: `List[${modelName}]`,
        queryParams: [
          { name: 'page', type: 'int', default: 1 },
          { name: 'limit', type: 'int', default: 50 }
        ]
      },
      {
        method: 'GET',
        path: `/api/${resource}/{id}`,
        functionName: `get_${resource}`,
        responseModel: modelName
      },
      {
        method: 'POST',
        path: `/api/${resource}`,
        functionName: `create_${resource}`,
        requestModel: `${modelName}Create`,
        responseModel: modelName
      },
      {
        method: 'PUT',
        path: `/api/${resource}/{id}`,
        functionName: `update_${resource}`,
        requestModel: `${modelName}Update`,
        responseModel: modelName
      },
      {
        method: 'DELETE',
        path: `/api/${resource}/{id}`,
        functionName: `delete_${resource}`,
        responseModel: 'dict'
      }
    ];

    const models = [
      modelName,
      `${modelName}Create`,
      `${modelName}Update`,
      `${modelName}InDB`
    ];

    return { endpoints, models };
  }

  getPydanticFields(queryResults: QueryResults): Array<{ name: string; type: string; optional: boolean }> {
    return queryResults.columns.map(col => ({
      name: col,
      type: this.getPythonType(queryResults.columnTypes[col]),
      optional: col.toLowerCase().includes('id') || col.toLowerCase().includes('created')
    }));
  }

  private getPythonType(columnType: string): string {
    const map: Record<string, string> = {
      'number': 'int',
      'string': 'str',
      'boolean': 'bool',
      'date': 'datetime'
    };
    return map[columnType] || 'str';
  }
}
