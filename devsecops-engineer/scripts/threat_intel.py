#!/usr/bin/env python3
"""
Threat Intelligence Collector
Gathers real-time security information from multiple sources.
"""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path


# Known CVE databases and security feeds
INTEL_SOURCES = {
    "nvd": "https://nvd.nist.gov/vuln/search",
    "github_advisories": "https://github.com/advisories",
    "cisa_kev": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
    "exploit_db": "https://www.exploit-db.com",
}

# Technologies to monitor
MONITORED_TECHNOLOGIES = [
    "nodejs", "python", "docker", "kubernetes", "nginx",
    "apache", "openssh", "linux-kernel", "postgresql", "redis"
]


def generate_search_queries(technologies: list = None) -> list:
    """Generate search queries for threat intelligence gathering."""
    techs = technologies or MONITORED_TECHNOLOGIES
    current_year = datetime.now().year

    queries = []
    for tech in techs:
        queries.extend([
            f"{tech} CVE vulnerability {current_year}",
            f"{tech} security advisory {current_year}",
            f"{tech} zero-day exploit",
            f"{tech} critical patch update"
        ])

    return queries


def get_intelligence_instructions() -> dict:
    """
    Return instructions for Claude to gather threat intelligence.
    Claude will use WebSearch and WebFetch based on these instructions.
    """
    return {
        "action": "gather_threat_intelligence",
        "description": "Collect latest security advisories and CVE information",
        "search_queries": generate_search_queries()[:10],  # Limit to top 10 for efficiency
        "sources_to_check": INTEL_SOURCES,
        "priority_keywords": [
            "critical", "remote code execution", "RCE",
            "privilege escalation", "zero-day", "actively exploited"
        ],
        "output_format": {
            "cve_id": "CVE-XXXX-XXXXX",
            "severity": "critical|high|medium|low",
            "affected_software": "software name and versions",
            "description": "brief description",
            "remediation": "patch or workaround",
            "references": ["urls"]
        }
    }


def analyze_project_dependencies(project_path: str = ".") -> dict:
    """Analyze project to identify technologies for targeted intelligence."""
    path = Path(project_path)
    detected_tech = []

    # Detect based on config files
    file_tech_map = {
        "package.json": "nodejs",
        "requirements.txt": "python",
        "Pipfile": "python",
        "Dockerfile": "docker",
        "docker-compose.yml": "docker",
        "kubernetes.yaml": "kubernetes",
        "k8s.yaml": "kubernetes",
        "nginx.conf": "nginx",
        "Gemfile": "ruby",
        "go.mod": "golang",
        "Cargo.toml": "rust",
    }

    for file, tech in file_tech_map.items():
        if (path / file).exists() or list(path.rglob(file)):
            detected_tech.append(tech)

    return {
        "detected_technologies": list(set(detected_tech)),
        "targeted_queries": generate_search_queries(detected_tech) if detected_tech else None
    }


def load_cached_intel(cache_file: Path = None) -> dict:
    """Load cached threat intelligence if available and recent."""
    cache = cache_file or Path.home() / ".claude" / "security" / "threat_intel_cache.json"

    if not cache.exists():
        return {"cached": False, "data": None}

    try:
        data = json.loads(cache.read_text())
        cached_time = datetime.fromisoformat(data.get("timestamp", "2000-01-01"))

        # Cache valid for 24 hours
        if datetime.now() - cached_time < timedelta(hours=24):
            return {"cached": True, "data": data, "age_hours": (datetime.now() - cached_time).seconds // 3600}
    except (json.JSONDecodeError, ValueError):
        pass

    return {"cached": False, "data": None, "reason": "Cache expired or invalid"}


def save_intel_cache(intel_data: dict, cache_file: Path = None):
    """Save collected intelligence to cache."""
    cache = cache_file or Path.home() / ".claude" / "security" / "threat_intel_cache.json"
    cache.parent.mkdir(parents=True, exist_ok=True)

    intel_data["timestamp"] = datetime.now().isoformat()
    cache.write_text(json.dumps(intel_data, indent=2))
    print(f"[+] Threat intelligence cached: {cache}")


def main():
    print("[*] Threat Intelligence Collector")
    print("=" * 50)

    # Check for cached intelligence
    cached = load_cached_intel()
    if cached["cached"]:
        print(f"[*] Using cached intelligence (age: {cached['age_hours']}h)")
        print(json.dumps(cached["data"], indent=2))
        return cached["data"]

    # Analyze current project
    print("[*] Analyzing project dependencies...")
    project_analysis = analyze_project_dependencies()
    print(f"[*] Detected technologies: {project_analysis['detected_technologies']}")

    # Generate intelligence gathering instructions
    print("\n[*] Intelligence Gathering Instructions for Claude:")
    print("-" * 50)
    instructions = get_intelligence_instructions()

    if project_analysis["targeted_queries"]:
        instructions["search_queries"] = project_analysis["targeted_queries"][:10]
        instructions["detected_technologies"] = project_analysis["detected_technologies"]

    print(json.dumps(instructions, indent=2))

    return instructions


if __name__ == "__main__":
    main()
