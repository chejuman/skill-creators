import { promises as fs } from 'fs';
import path from 'path';
import { fileExists } from './utils.js';

export interface QueryResults {
  rowCount: number;
  columns: string[];
  columnTypes: Record<string, string>;
  sampleData: any[];
  uiRecommendation?: {
    type: 'table' | 'cards' | 'detail' | 'form' | 'dashboard';
    confidence: number;
    rationale: string;
    suggestedComponents: string[];
  };
}

export interface DesignSpec {
  mainView: string;
  components: string[];
  shadcnComponents: string[];
  layout: string;
  props: Record<string, any>;
}

export interface APIDesign {
  endpoints: Array<{
    method: string;
    path: string;
    functionName: string;
    requestModel?: string;
    responseModel: string;
    queryParams?: Array<{ name: string; type: string; default?: any }>;
  }>;
  models: string[];
}

export interface WorkflowState {
  version: string;
  currentPhase: number;
  projectPath?: string;
  phases: {
    [key: number]: {
      completed: boolean;
      [key: string]: any;
    };
  };
}

const STATE_FILE = '.fullstack-state.json';

export async function loadState(): Promise<WorkflowState | null> {
  if (!(await fileExists(STATE_FILE))) {
    return null;
  }
  const content = await fs.readFile(STATE_FILE, 'utf-8');
  return JSON.parse(content);
}

export async function saveState(state: WorkflowState): Promise<void> {
  await fs.writeFile(STATE_FILE, JSON.stringify(state, null, 2));
}

export async function updatePhase(
  phase: number,
  data: any,
  completed: boolean = false
): Promise<void> {
  const state = await loadState() || createInitialState();
  state.phases[phase] = { ...state.phases[phase], ...data, completed };
  state.currentPhase = completed ? phase + 1 : phase;
  await saveState(state);
}

export async function resetState(): Promise<void> {
  if (await fileExists(STATE_FILE)) {
    await fs.unlink(STATE_FILE);
  }
}

export function createInitialState(): WorkflowState {
  return {
    version: '1.0',
    currentPhase: 1,
    phases: {}
  };
}
