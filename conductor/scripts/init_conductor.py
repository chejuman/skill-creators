#!/usr/bin/env python3
"""
Conductor 프로젝트 초기화 스크립트
.claude/conductor/ 디렉토리와 기본 컨텍스트 파일 생성
"""

import os
import sys
import json
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
ASSETS_DIR = SCRIPT_DIR.parent / "assets"


def get_template(name: str) -> str:
    """템플릿 파일 로드"""
    template_path = ASSETS_DIR / f"{name}.template"
    if template_path.exists():
        return template_path.read_text(encoding="utf-8")
    return f"# {name}\n\nTODO: 내용을 작성하세요.\n"


def init_conductor(project_path: str = ".") -> dict:
    """Conductor 디렉토리 구조 초기화"""
    project = Path(project_path).resolve()
    conductor_dir = project / ".claude" / "conductor"

    # 이미 존재하는지 확인
    if conductor_dir.exists():
        return {
            "success": False,
            "error": "Conductor already initialized",
            "path": str(conductor_dir)
        }

    # 디렉토리 생성
    dirs = [
        conductor_dir,
        conductor_dir / "tracks",
        conductor_dir / "code-styleguides"
    ]
    for d in dirs:
        d.mkdir(parents=True, exist_ok=True)

    # 기본 파일 생성
    files = {
        "product.md": get_template("product.md"),
        "tech-stack.md": get_template("tech-stack.md"),
        "workflow.md": get_template("workflow.md"),
        "product-guidelines.md": "# Product Guidelines\n\n## Brand\n\n## Style\n\n## Voice & Tone\n",
        "tracks.md": f"# Tracks\n\nCreated: {datetime.now().strftime('%Y-%m-%d')}\n\n## Active Tracks\n\n(none)\n\n## Completed Tracks\n\n(none)\n"
    }

    created_files = []
    for filename, content in files.items():
        filepath = conductor_dir / filename
        filepath.write_text(content, encoding="utf-8")
        created_files.append(str(filepath.relative_to(project)))

    # 메타데이터 생성
    metadata = {
        "version": "1.0.0",
        "created": datetime.now().isoformat(),
        "project_name": project.name
    }
    meta_path = conductor_dir / "metadata.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8")
    created_files.append(str(meta_path.relative_to(project)))

    return {
        "success": True,
        "path": str(conductor_dir.relative_to(project)),
        "files": created_files
    }


if __name__ == "__main__":
    project_path = sys.argv[1] if len(sys.argv) > 1 else "."
    result = init_conductor(project_path)
    print(json.dumps(result, indent=2, ensure_ascii=False))
