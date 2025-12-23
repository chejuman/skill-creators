#!/usr/bin/env python3
"""
Track의 plan.md와 TodoWrite 동기화 스크립트
plan.md의 태스크 목록을 파싱하여 JSON으로 출력
"""

import os
import sys
import json
import re
from pathlib import Path
from typing import List, Dict, Optional


def parse_plan(plan_path: Path) -> Dict:
    """plan.md를 파싱하여 태스크 구조 추출"""
    if not plan_path.exists():
        return {"success": False, "error": f"Plan not found: {plan_path}"}

    content = plan_path.read_text(encoding="utf-8")
    lines = content.split("\n")

    phases = []
    current_phase = None

    for line in lines:
        # Phase 헤더 감지
        phase_match = re.match(r'^##\s+Phase\s+(\d+):\s*(.+)$', line)
        if phase_match:
            if current_phase:
                phases.append(current_phase)
            current_phase = {
                "number": int(phase_match.group(1)),
                "title": phase_match.group(2).strip(),
                "tasks": []
            }
            continue

        # 태스크 감지
        if current_phase:
            task_match = re.match(r'^-\s*\[([ xX])\]\s*(.+)$', line)
            if task_match:
                status = "completed" if task_match.group(1).lower() == 'x' else "pending"
                task_text = task_match.group(2).strip()

                # Task ID 추출 시도
                id_match = re.match(r'^Task\s+(\d+\.\d+):\s*(.+)$', task_text)
                if id_match:
                    task_id = id_match.group(1)
                    task_content = id_match.group(2)
                else:
                    task_id = f"{current_phase['number']}.{len(current_phase['tasks']) + 1}"
                    task_content = task_text

                current_phase["tasks"].append({
                    "id": task_id,
                    "content": task_content,
                    "status": status
                })

    if current_phase:
        phases.append(current_phase)

    # 통계 계산
    total_tasks = sum(len(p["tasks"]) for p in phases)
    completed_tasks = sum(
        sum(1 for t in p["tasks"] if t["status"] == "completed")
        for p in phases
    )

    return {
        "success": True,
        "phases": phases,
        "stats": {
            "total_phases": len(phases),
            "total_tasks": total_tasks,
            "completed_tasks": completed_tasks,
            "progress_percent": round(completed_tasks / total_tasks * 100, 1) if total_tasks > 0 else 0
        }
    }


def get_next_task(plan_data: Dict) -> Optional[Dict]:
    """다음 실행할 태스크 반환"""
    if not plan_data.get("success"):
        return None

    for phase in plan_data["phases"]:
        for task in phase["tasks"]:
            if task["status"] == "pending":
                return {
                    "phase": phase["number"],
                    "phase_title": phase["title"],
                    "task": task
                }
    return None


def to_todowrite_format(plan_data: Dict) -> List[Dict]:
    """plan 데이터를 TodoWrite 형식으로 변환"""
    todos = []
    if not plan_data.get("success"):
        return todos

    for phase in plan_data["phases"]:
        for task in phase["tasks"]:
            content = f"[Phase {phase['number']}] {task['content']}"
            active_form = f"Working on Phase {phase['number']}: {task['content']}"
            todos.append({
                "content": content,
                "status": task["status"],
                "activeForm": active_form
            })

    return todos


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(json.dumps({"error": "Usage: sync_todos.py <plan.md path>"}))
        sys.exit(1)

    plan_path = Path(sys.argv[1])
    result = parse_plan(plan_path)

    if "--next" in sys.argv:
        next_task = get_next_task(result)
        print(json.dumps(next_task, indent=2, ensure_ascii=False))
    elif "--todowrite" in sys.argv:
        todos = to_todowrite_format(result)
        print(json.dumps(todos, indent=2, ensure_ascii=False))
    else:
        print(json.dumps(result, indent=2, ensure_ascii=False))
