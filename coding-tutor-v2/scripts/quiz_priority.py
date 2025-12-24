#!/usr/bin/env python3
"""
Prioritize tutorials for quizzing based on spaced repetition (FSRS-inspired).

Usage:
    python quiz_priority.py
    python quiz_priority.py --tutorials-dir /path/to/tutorials
"""

import argparse
import re
from datetime import datetime
from pathlib import Path


def get_tutorials_directory():
    """Get the tutorials directory."""
    return Path.home() / "coding-tutor-tutorials"


# FSRS-inspired intervals (Fibonacci-ish progression)
INTERVALS = {
    0: 1,    # Never assessed
    1: 2,    # Very poor retention
    2: 3,
    3: 5,
    4: 8,
    5: 13,
    6: 21,
    7: 34,
    8: 55,
    9: 89,
    10: 144  # Mastered
}


def parse_frontmatter(filepath: Path) -> dict:
    """Extract YAML frontmatter from tutorial."""
    content = filepath.read_text()
    match = re.match(r'^---\s*\n(.*?)\n---\s*\n', content, re.DOTALL)
    if not match:
        return None

    frontmatter_text = match.group(1)
    metadata = {'filepath': str(filepath), 'filename': filepath.name}

    for line in frontmatter_text.split('\n'):
        line = line.strip()
        if ':' in line:
            key, value = line.split(':', 1)
            key = key.strip()
            value = value.strip()

            if value == 'null' or value == '':
                value = None
            elif key == 'understanding_score' and value:
                try:
                    value = int(value)
                except ValueError:
                    pass
            elif key == 'concepts' and value.startswith('['):
                value = [v.strip() for v in value.strip('[]').split(',') if v.strip()]

            metadata[key] = value

    return metadata


def parse_date(date_value: str) -> datetime.date:
    """Parse date from DD-MM-YYYY format."""
    if isinstance(date_value, str):
        return datetime.strptime(date_value, '%d-%m-%Y').date()
    return date_value


def calculate_priority(tutorial: dict, today: datetime.date) -> float:
    """Calculate quiz priority. Higher = more urgent."""
    score = tutorial.get('understanding_score') or 0
    ideal_interval = INTERVALS.get(score, INTERVALS[5])
    last_quizzed = tutorial.get('last_quizzed')

    if not last_quizzed:
        # Never quizzed - need baseline
        created = tutorial.get('created')
        if created:
            try:
                created = parse_date(created)
                days_since = (today - created).days
                return days_since / ideal_interval + 10  # Bonus for never-quizzed
            except Exception:
                pass
        return 100  # Max urgency

    try:
        last_quizzed = parse_date(last_quizzed)
        days_since = (today - last_quizzed).days
        days_overdue = days_since - ideal_interval
        return days_overdue / ideal_interval
    except Exception:
        return 50


def main():
    parser = argparse.ArgumentParser(description="Quiz priority based on spaced repetition")
    parser.add_argument("--tutorials-dir", help="Path to tutorials directory")
    parser.add_argument("--format", choices=["human", "json"], default="human")
    args = parser.parse_args()

    today = datetime.now().date()
    tutorials = []

    tutorials_path = Path(args.tutorials_dir) if args.tutorials_dir else get_tutorials_directory()

    if not tutorials_path.exists():
        print("No tutorials found. Run `/teach-me` to create your first tutorial.")
        return 0

    for filepath in tutorials_path.glob("*.md"):
        if filepath.name in ["learner_profile.md", "codebase_analysis.md",
                             "curriculum.md", "README.md", "research_notes.md"]:
            continue

        metadata = parse_frontmatter(filepath)
        if metadata:
            metadata['priority'] = calculate_priority(metadata, today)
            tutorials.append(metadata)

    if not tutorials:
        print("No tutorials found. Run `/teach-me` to start learning.")
        return 0

    tutorials.sort(key=lambda t: t['priority'], reverse=True)

    print("=" * 60)
    print("QUIZ PRIORITY (most urgent first)")
    print("=" * 60)
    print()

    for i, t in enumerate(tutorials, 1):
        score = t.get('understanding_score') or 0
        last_q = t.get('last_quizzed')
        concepts = t.get('concepts', [])

        if isinstance(concepts, list):
            concepts_str = ', '.join(concepts[:2])
        else:
            concepts_str = str(concepts)

        if last_q:
            try:
                last_q_date = parse_date(last_q)
                days_ago = (today - last_q_date).days
                last_quizzed_str = f"{days_ago} days ago"
            except Exception:
                last_quizzed_str = last_q
        else:
            last_quizzed_str = "never"

        status = ""
        if score == 0:
            status = " [NEEDS BASELINE]"
        elif t['priority'] > 1:
            status = " [OVERDUE]"
        elif t['priority'] > 0:
            status = " [DUE SOON]"

        print(f"{i}. {concepts_str}{status}")
        print(f"   Score: {score}/10 | Last quiz: {last_quizzed_str}")
        print(f"   File: {t['filename']}")
        print()


if __name__ == "__main__":
    main()
