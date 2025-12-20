import { promises as fs } from 'fs';
import path from 'path';
import Mustache from 'mustache';
import type { APIDesign, QueryResults } from './state-manager.js';
import { toPascalCase, toSnakeCase } from './utils.js';

export class APIGenerator {
  private assetPath: string;

  constructor(assetPath: string) {
    this.assetPath = assetPath;
  }

  async generateAPI(
    backendPath: string,
    apiDesign: APIDesign,
    queryResults: QueryResults,
    resourceName: string
  ): Promise<void> {
    const modelName = toPascalCase(resourceName);
    const tableName = toSnakeCase(resourceName);

    await this.generateModels(backendPath, modelName, queryResults);
    await this.generateSchemas(backendPath, modelName, queryResults);
    await this.generateRouter(backendPath, apiDesign, modelName, tableName);
    await this.updateMainFile(backendPath, resourceName);

    console.log('✅ API generation complete');
  }

  private async generateModels(
    backendPath: string,
    modelName: string,
    queryResults: QueryResults
  ): Promise<void> {
    const fields = queryResults.columns.map(col => {
      const pyType = this.getPythonType(queryResults.columnTypes[col]);
      const isId = col.toLowerCase() === 'id';
      return `    ${col} = Column(${this.getSQLType(pyType)}, ${isId ? 'primary_key=True, index=True' : ''})`;
    }).join('\n');

    const modelContent = `from sqlalchemy import Column, Integer, String, Boolean, DateTime
from app.database import Base

class ${modelName}(Base):
    __tablename__ = "${toSnakeCase(modelName)}"

${fields}
`;

    await fs.writeFile(
      path.join(backendPath, 'app/models', `${toSnakeCase(modelName)}.py`),
      modelContent
    );
    console.log(`✅ Generated ${modelName} model`);
  }

  private async generateSchemas(
    backendPath: string,
    modelName: string,
    queryResults: QueryResults
  ): Promise<void> {
    const fields = queryResults.columns.map(col => {
      const pyType = this.getPythonType(queryResults.columnTypes[col]);
      return `    ${col}: ${pyType}`;
    }).join('\n');

    const schemaContent = `from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class ${modelName}Base(BaseModel):
${fields}

class ${modelName}Create(${modelName}Base):
    pass

class ${modelName}Update(${modelName}Base):
    pass

class ${modelName}InDB(${modelName}Base):
    class Config:
        from_attributes = True
`;

    await fs.writeFile(
      path.join(backendPath, 'app/schemas', `${toSnakeCase(modelName)}.py`),
      schemaContent
    );
    console.log(`✅ Generated ${modelName} schemas`);
  }

  private async generateRouter(
    backendPath: string,
    apiDesign: APIDesign,
    modelName: string,
    tableName: string
  ): Promise<void> {
    const routerContent = `from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from app.database import get_db
from app.models.${tableName} import ${modelName}
from app.schemas.${tableName} import ${modelName}Create, ${modelName}Update, ${modelName}InDB

router = APIRouter(prefix="/api/${tableName}", tags=["${tableName}"])

@router.get("/", response_model=List[${modelName}InDB])
def list_${tableName}(
    page: int = 1,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    skip = (page - 1) * limit
    items = db.query(${modelName}).offset(skip).limit(limit).all()
    return items

@router.get("/{id}", response_model=${modelName}InDB)
def get_${tableName}(id: int, db: Session = Depends(get_db)):
    item = db.query(${modelName}).filter(${modelName}.id == id).first()
    if not item:
        raise HTTPException(status_code=404, detail="${modelName} not found")
    return item

@router.post("/", response_model=${modelName}InDB)
def create_${tableName}(
    item: ${modelName}Create,
    db: Session = Depends(get_db)
):
    db_item = ${modelName}(**item.dict())
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@router.put("/{id}", response_model=${modelName}InDB)
def update_${tableName}(
    id: int,
    item: ${modelName}Update,
    db: Session = Depends(get_db)
):
    db_item = db.query(${modelName}).filter(${modelName}.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="${modelName} not found")

    for key, value in item.dict().items():
        setattr(db_item, key, value)

    db.commit()
    db.refresh(db_item)
    return db_item

@router.delete("/{id}")
def delete_${tableName}(id: int, db: Session = Depends(get_db)):
    db_item = db.query(${modelName}).filter(${modelName}.id == id).first()
    if not db_item:
        raise HTTPException(status_code=404, detail="${modelName} not found")

    db.delete(db_item)
    db.commit()
    return {"message": "${modelName} deleted successfully"}
`;

    await fs.writeFile(
      path.join(backendPath, 'app/routers', `${tableName}.py`),
      routerContent
    );
    console.log(`✅ Generated ${tableName} router`);
  }

  private async updateMainFile(backendPath: string, resourceName: string): Promise<void> {
    const mainPath = path.join(backendPath, 'app/main.py');
    const content = await fs.readFile(mainPath, 'utf-8');

    const tableName = toSnakeCase(resourceName);
    const importLine = `from app.routers import ${tableName}`;
    const includeLine = `app.include_router(${tableName}.router)`;

    const lines = content.split('\n');
    const importIdx = lines.findIndex(line => line.includes('from fastapi import'));
    lines.splice(importIdx + 1, 0, importLine);

    const healthIdx = lines.findIndex(line => line.includes('def health_check'));
    lines.splice(healthIdx + 4, 0, '', includeLine);

    await fs.writeFile(mainPath, lines.join('\n'));
    console.log('✅ Updated main.py with router');
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

  private getSQLType(pyType: string): string {
    const map: Record<string, string> = {
      'int': 'Integer',
      'str': 'String',
      'bool': 'Boolean',
      'datetime': 'DateTime'
    };
    return map[pyType] || 'String';
  }
}
