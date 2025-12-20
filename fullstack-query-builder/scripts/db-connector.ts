import pg from 'pg';
import { maskPassword } from './utils.js';

const { Pool } = pg;

export interface DBConfig {
  connectionString: string;
}

export interface QueryResult {
  rows: any[];
  rowCount: number;
  fields: Array<{ name: string; dataTypeID: number }>;
}

export class DatabaseConnector {
  private pool: pg.Pool | null = null;
  private connectionString: string = '';

  async connect(connectionString: string): Promise<void> {
    this.connectionString = connectionString;

    if (!this.validateConnectionString(connectionString)) {
      throw new Error('Invalid PostgreSQL connection string format');
    }

    this.pool = new Pool({ connectionString, max: 1 });

    try {
      const client = await this.pool.connect();
      client.release();
      console.log('✅ Connected to PostgreSQL');
    } catch (error: any) {
      throw new Error(`Connection failed: ${error.message}`);
    }
  }

  async executeQuery(query: string): Promise<QueryResult> {
    if (!this.pool) {
      throw new Error('Not connected to database');
    }

    const validation = this.validateQuery(query);
    if (!validation.safe) {
      throw new Error(`Query validation failed: ${validation.reason}`);
    }

    try {
      const result = await this.pool.query(query);
      return {
        rows: result.rows,
        rowCount: result.rowCount || 0,
        fields: result.fields.map(f => ({
          name: f.name,
          dataTypeID: f.dataTypeID
        }))
      };
    } catch (error: any) {
      throw new Error(`Query execution failed: ${error.message}`);
    }
  }

  async close(): Promise<void> {
    if (this.pool) {
      await this.pool.end();
      this.pool = null;
      console.log('✅ Database connection closed');
    }
  }

  private validateConnectionString(connStr: string): boolean {
    return connStr.startsWith('postgres://') || connStr.startsWith('postgresql://');
  }

  private validateQuery(query: string): { safe: boolean; reason?: string } {
    const trimmed = query.trim().toUpperCase();

    if (!trimmed.startsWith('SELECT')) {
      return { safe: false, reason: 'Only SELECT queries are allowed' };
    }

    const dangerous = ['DROP', 'DELETE', 'TRUNCATE', 'ALTER', 'INSERT', 'UPDATE'];
    for (const keyword of dangerous) {
      if (trimmed.includes(keyword)) {
        return { safe: false, reason: `Dangerous keyword detected: ${keyword}` };
      }
    }

    return { safe: true };
  }

  getMaskedConnection(): string {
    return maskPassword(this.connectionString);
  }

  getPostgresTypeMapping(dataTypeID: number): string {
    const typeMap: Record<number, string> = {
      20: 'number',    // bigint
      21: 'number',    // smallint
      23: 'number',    // integer
      700: 'number',   // real
      701: 'number',   // double precision
      1082: 'Date',    // date
      1114: 'Date',    // timestamp
      1184: 'Date',    // timestamptz
      16: 'boolean',   // boolean
      25: 'string',    // text
      1043: 'string',  // varchar
      2950: 'string'   // uuid
    };
    return typeMap[dataTypeID] || 'string';
  }
}
