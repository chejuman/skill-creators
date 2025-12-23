#!/usr/bin/env python3
"""
새로운 Track 생성 스크립트
spec.md와 plan.md 템플릿으로 Track 디렉토리 생성
"""

import os
import sys
import json
import re
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


def slugify(text: str) -> str:
    """텍스트를 URL-safe slug로 변환"""
    text = text.lower().strip()
    text = re.sub(r'[^\w\s-]', '', text)
    text = re.sub(r'[\s_]+', '-', text)
    text = re.sub(r'-+', '-', text)
    return text[:50]


def get_next_track_id(tracks_dir: Path) -> str:
    """다음 Track ID 생성"""
    existing = list(tracks_dir.glob("*"))
    max_num = 0
    for track in existing:
        if track.is_dir():
            match = re.match(r'track-(\d+)', track.name)
            if match:
                max_num = max(max_num, int(match.group(1)))
    return f"track-{max_num + 1:03d}"


def create_track(description: str, project_path: str = ".") -> dict:
    """새 Track 생성"""
    project = Path(project_path).resolve()
    conductor_dir = project / ".claude" / "conductor"
    tracks_dir = conductor_dir / "tracks"

    if not conductor_dir.exists():
        return {
            "success": False,
            "error": "Conductor not initialized. Run /conductor:setup first."
        }

    # Track ID 및 디렉토리 생성
    track_id = get_next_track_id(tracks_dir)
    slug = slugify(description) if description else "untitled"
    track_name = f"{track_id}-{slug}"
    track_dir = tracks_dir / track_name
    track_dir.mkdir(parents=True, exist_ok=True)

    # 템플릿으로 파일 생성
    spec_content = get_template("spec.md").replace("{{DESCRIPTION}}", description or "새 기능")
    plan_content = get_template("plan.md").replace("{{DESCRIPTION}}", description or "새 기능")

    (track_dir / "spec.md").write_text(spec_content, encoding="utf-8")
    (track_dir / "plan.md").write_text(plan_content, encoding="utf-8")

    # 메타데이터
    metadata = {
        "id": track_id,
        "name": track_name,
        "description": description,
        "status": "planning",
        "created": datetime.now().isoformat(),
        "branch": f"feature/{track_name}"
    }
    (track_dir / "metadata.json").write_text(
        json.dumps(metadata, indent=2, ensure_ascii=False), encoding="utf-8"
    )

    # tracks.md 업데이트
    tracks_index = conductor_dir / "tracks.md"
    if tracks_index.exists():
        content = tracks_index.read_text(encoding="utf-8")
        new_entry = f"- [{track_name}](tracks/{track_name}/) - {description} (planning)\n"
        content = content.replace("## Active Tracks\n\n(none)", f"## Active Tracks\n\n{new_entry}")
        content = content.replace("## Active Tracks\n\n", f"## Active Tracks\n\n{new_entry}")
        tracks_index.write_text(content, encoding="utf-8")

    return {
        "success": True,
        "track_id": track_id,
        "track_name": track_name,
        "path": str(track_dir.relative_to(project)),
        "files": ["spec.md", "plan.md", "metadata.json"],
        "branch": f"feature/{track_name}"
    }


if __name__ == "__main__":
    description = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else ""
    result = create_track(description)
    print(json.dumps(result, indent=2, ensure_ascii=False))
