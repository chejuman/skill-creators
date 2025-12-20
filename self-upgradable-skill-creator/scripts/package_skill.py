#!/usr/bin/env python3
"""
Skill Packager - Creates a distributable zip file.

Usage:
    python3 package_skill.py <skill-folder> [output-directory]
"""

import sys
import zipfile
from pathlib import Path
from quick_validate import validate_skill


def package_skill(skill_path: Path, output_dir: Path = None) -> Path:
    """Package a skill into a zip file."""
    skill_path = Path(skill_path).resolve()

    if not skill_path.exists():
        print(f"❌ Skill folder not found: {skill_path}")
        return None

    if not skill_path.is_dir():
        print(f"❌ Not a directory: {skill_path}")
        return None

    # Validate first
    print("🔍 Validating skill...")
    valid, message = validate_skill(skill_path)
    if not valid:
        print(f"❌ Validation failed: {message}")
        return None
    print(f"✅ {message}\n")

    # Determine output
    skill_name = skill_path.name
    if output_dir:
        output_path = Path(output_dir).resolve()
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = Path.cwd()

    zip_file = output_path / f"{skill_name}.zip"

    # Create zip
    try:
        with zipfile.ZipFile(zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            for file_path in skill_path.rglob('*'):
                if file_path.is_file():
                    # Skip hidden files and __pycache__
                    if '__pycache__' in str(file_path):
                        continue
                    if file_path.name.startswith('.'):
                        continue

                    arcname = file_path.relative_to(skill_path.parent)
                    zf.write(file_path, arcname)
                    print(f"  Added: {arcname}")

        print(f"\n✅ Packaged to: {zip_file}")
        return zip_file

    except Exception as e:
        print(f"❌ Error: {e}")
        return None


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 package_skill.py <skill-folder> [output-dir]")
        sys.exit(1)

    skill_path = sys.argv[1]
    output_dir = sys.argv[2] if len(sys.argv) > 2 else None

    print(f"📦 Packaging: {skill_path}\n")

    result = package_skill(skill_path, output_dir)
    sys.exit(0 if result else 1)


if __name__ == "__main__":
    main()
