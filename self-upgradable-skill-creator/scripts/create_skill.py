#!/usr/bin/env python3
"""
One-Click Skill Creator
Combines all phases into single execution with interactive prompts.
"""

import subprocess
import sys
import json
import os
from pathlib import Path

SKILL_CREATOR_PATH = Path.home() / ".claude/skills/skill-creator/scripts"

def run_step(name: str, cmd: list) -> bool:
    print(f"\n{'='*50}")
    print(f"🔄 {name}")
    print(f"{'='*50}")
    result = subprocess.run(cmd, capture_output=False)
    if result.returncode == 0:
        print(f"✅ {name} completed")
        return True
    else:
        print(f"❌ {name} failed")
        return False

def create_skill(name: str, output_dir: str = "."):
    """Create skill with full workflow."""
    skill_path = Path(output_dir) / name
    
    print(f"\n🚀 Creating skill: {name}")
    print(f"📁 Output: {skill_path.absolute()}")
    
    # Phase 1: Initialize
    if not run_step("Initialize Skill", [
        "python3", str(SKILL_CREATOR_PATH / "init_skill.py"),
        name, "--path", output_dir
    ]):
        return False
    
    # Phase 2: Analyze (self-check)
    analyze_script = Path(__file__).parent / "analyze_skill.py"
    if analyze_script.exists():
        run_step("Analyze Structure", [
            "python3", str(analyze_script), str(skill_path)
        ])
    
    # Phase 3: Validate
    if not run_step("Validate Skill", [
        "python3", str(SKILL_CREATOR_PATH / "quick_validate.py"),
        str(skill_path)
    ]):
        print("\n⚠️ Validation failed - fix issues and re-run")
        return False
    
    # Phase 4: Package
    if not run_step("Package Skill", [
        "python3", str(SKILL_CREATOR_PATH / "package_skill.py"),
        str(skill_path), output_dir
    ]):
        return False
    
    # Phase 5: Install (optional)
    print(f"\n{'='*50}")
    print("📦 Install to ~/.claude/skills/?")
    print("Run: unzip -o {name}.zip -d ~/.claude/skills/")
    print(f"{'='*50}")
    
    return True

def main():
    if len(sys.argv) < 2:
        print("Usage: create_skill.py <skill-name> [output-dir]")
        print("\nExample:")
        print("  python3 create_skill.py my-awesome-skill")
        print("  python3 create_skill.py api-helper ./skills")
        sys.exit(1)
    
    name = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else "."
    
    success = create_skill(name, output_dir)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
