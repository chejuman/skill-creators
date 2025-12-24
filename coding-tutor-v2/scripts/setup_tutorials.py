#!/usr/bin/env python3
"""
Set up the central tutorials repository for coding-tutor-v2.

Usage:
    python setup_tutorials.py
    python setup_tutorials.py --create-github-repo
"""

import argparse
import subprocess
import sys
from pathlib import Path


def get_tutorials_repo_path():
    """Get the path for the tutorials repo (~/coding-tutor-tutorials/)."""
    return Path.home() / "coding-tutor-tutorials"


README_CONTENT = """# Coding Tutor V2 - My Learning Journey

Personal coding tutorials powered by multi-agent AI analysis.

## What's Here

- **learner_profile.md** - My background, goals, and learning preferences
- **codebase_analysis.md** - Analysis of current project's tech stack
- **curriculum.md** - Personalized learning path
- **YYYY-MM-DD-topic.md** - Individual tutorials with Q&A and quiz history

## How It Works

1. **Codebase Analysis**: 4-5 parallel agents analyze your project
2. **Web Research**: Latest docs and best practices fetched
3. **Curriculum Design**: Personalized learning path created
4. **Tutorial Generation**: Tutorials using YOUR code as examples
5. **Spaced Repetition**: Quiz system to reinforce learning

## Commands

- `/teach-me` - Start learning
- `/quiz-me` - Spaced repetition quiz
- `/analyze-codebase` - Analyze current project
- `/my-curriculum` - View learning path
"""


def setup_tutorials_repo(create_github=False):
    """Set up the central tutorials repository."""
    repo_path = get_tutorials_repo_path()

    if repo_path.exists():
        return True, f"Tutorials repo already exists at {repo_path.resolve()}"

    try:
        repo_path.mkdir(parents=True)
        subprocess.run(['git', 'init'], cwd=repo_path, check=True, capture_output=True)

        readme_path = repo_path / "README.md"
        readme_path.write_text(README_CONTENT)

        gitignore_path = repo_path / ".gitignore"
        gitignore_path.write_text(".DS_Store\n*.swp\n*.swo\nresearch_notes.md\n")

        subprocess.run(['git', 'add', '-A'], cwd=repo_path, check=True, capture_output=True)
        subprocess.run(
            ['git', 'commit', '-m', 'Initial commit: coding-tutor-v2 learning journey'],
            cwd=repo_path, check=True, capture_output=True
        )

        message = f"Created tutorials repo at {repo_path.resolve()}"

        if create_github:
            result = subprocess.run(
                ['gh', 'repo', 'create', 'coding-tutor-tutorials', '--private', '--source=.', '--push'],
                cwd=repo_path, capture_output=True, text=True
            )
            if result.returncode == 0:
                message += "\nCreated private GitHub repo and pushed"
            else:
                message += f"\nNote: Could not create GitHub repo: {result.stderr}"

        return True, message

    except Exception as e:
        return False, f"Error setting up tutorials repo: {e}"


def main():
    parser = argparse.ArgumentParser(description="Set up tutorials repository")
    parser.add_argument("--create-github-repo", action="store_true")
    args = parser.parse_args()

    success, message = setup_tutorials_repo(create_github=args.create_github_repo)
    print(message)
    return 0 if success else 1


if __name__ == "__main__":
    sys.exit(main())
