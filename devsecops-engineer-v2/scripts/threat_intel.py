#!/usr/bin/env python3
"""
Threat Intelligence Collector v2
Multi-agent intelligence gathering with parallel query support.

Supports three intel types for parallel execution:
- cve: CVE and zero-day monitoring
- tech: Technology-specific threats and attack patterns
- compliance: Compliance updates and regulatory changes
"""

import argparse
import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional


# Known CVE databases and security feeds
INTEL_SOURCES = {
    "cve": {
        "nvd": "https://nvd.nist.gov/vuln/search",
        "cisa_kev": "https://www.cisa.gov/known-exploited-vulnerabilities-catalog",
        "github_advisories": "https://github.com/advisories",
    },
    "tech": {
        "exploit_db": "https://www.exploit-db.com",
        "mitre_attack": "https://attack.mitre.org",
        "vendor_advisories": "Various vendor security pages",
    },
    "compliance": {
        "owasp": "https://owasp.org",
        "cis": "https://www.cisecurity.org/cis-benchmarks",
        "nist": "https://www.nist.gov/cybersecurity",
    }
}

# Technologies to monitor
MONITORED_TECHNOLOGIES = [
    "nodejs", "python", "docker", "kubernetes", "nginx",
    "apache", "openssh", "linux-kernel", "postgresql", "redis"
]


def generate_cve_queries(technologies: List[str] = None) -> dict:
    """Generate CVE monitoring queries for Intel Agent."""
    techs = technologies or MONITORED_TECHNOLOGIES
    current_year = datetime.now().year

    queries = []
    for tech in techs[:5]:  # Limit to top 5 for efficiency
        queries.extend([
            f"{tech} CVE {current_year} critical vulnerability",
            f"{tech} security advisory patch {current_year}",
            f"CISA KEV {tech} {current_year}",
        ])

    return {
        "intel_type": "cve",
        "focus": "CVE and zero-day monitoring",
        "technologies": techs[:5],
        "search_queries": queries[:10],
        "sources": INTEL_SOURCES["cve"],
        "priority_keywords": [
            "critical", "remote code execution", "RCE",
            "privilege escalation", "zero-day", "actively exploited",
            "CVSS 9", "CVSS 10"
        ],
        "output_schema": {
            "cve_id": "CVE-XXXX-XXXXX",
            "severity": "critical|high",
            "cvss_score": 9.8,
            "affected_packages": ["package@version"],
            "description": "brief description",
            "exploited_in_wild": True,
            "patch_available": True,
            "source_url": "https://..."
        }
    }


def generate_tech_queries(technologies: List[str] = None) -> dict:
    """Generate technology-specific threat queries for Intel Agent."""
    techs = technologies or MONITORED_TECHNOLOGIES
    current_year = datetime.now().year

    queries = []
    for tech in techs[:5]:
        queries.extend([
            f"{tech} attack pattern technique {current_year}",
            f"{tech} security misconfiguration common",
            f"{tech} best practices security hardening",
        ])

    return {
        "intel_type": "tech",
        "focus": "Technology-specific threats and attack patterns",
        "technologies": techs[:5],
        "search_queries": queries[:10],
        "sources": INTEL_SOURCES["tech"],
        "priority_keywords": [
            "attack pattern", "MITRE ATT&CK", "misconfiguration",
            "security hardening", "best practice", "vulnerability"
        ],
        "output_schema": {
            "attack_patterns": [{
                "name": "pattern name",
                "mitre_id": "T1XXX",
                "affected_tech": ["..."],
                "description": "...",
                "mitigations": ["..."]
            }],
            "misconfigurations": [{
                "issue": "description",
                "risk": "high|medium|low",
                "detection": "how to detect",
                "remediation": "how to fix"
            }]
        }
    }


def generate_compliance_queries() -> dict:
    """Generate compliance update queries for Intel Agent."""
    current_year = datetime.now().year

    queries = [
        f"OWASP Top 10 {current_year} changes updates",
        f"CIS Benchmark updates {current_year}",
        f"NIST Cybersecurity Framework {current_year} updates",
        f"security compliance requirements {current_year}",
        f"PCI DSS SOC2 HIPAA updates {current_year}",
    ]

    return {
        "intel_type": "compliance",
        "focus": "Compliance and regulatory updates",
        "search_queries": queries,
        "sources": INTEL_SOURCES["compliance"],
        "frameworks": ["OWASP 2025", "CIS Benchmarks", "NIST CSF"],
        "priority_keywords": [
            "OWASP Top 10", "CIS Benchmark", "NIST CSF",
            "compliance requirement", "regulation", "audit"
        ],
        "output_schema": {
            "owasp_2025": {
                "version": "2025",
                "key_changes": ["..."],
                "new_controls": ["..."]
            },
            "cis": {
                "benchmarks": ["..."],
                "updates": ["..."]
            },
            "nist_csf": {
                "version": "2.0",
                "changes": ["..."]
            }
        }
    }


def get_intel_instructions(intel_type: str = "all", technologies: List[str] = None) -> dict:
    """
    Return instructions for Claude to gather specific threat intelligence.
    Used by Intel Agents in parallel execution.
    """
    if intel_type == "cve":
        return generate_cve_queries(technologies)
    elif intel_type == "tech":
        return generate_tech_queries(technologies)
    elif intel_type == "compliance":
        return generate_compliance_queries()
    elif intel_type == "all":
        return {
            "cve": generate_cve_queries(technologies),
            "tech": generate_tech_queries(technologies),
            "compliance": generate_compliance_queries()
        }
    else:
        raise ValueError(f"Unknown intel type: {intel_type}")


def analyze_project_dependencies(project_path: str = ".") -> dict:
    """Analyze project to identify technologies for targeted intelligence."""
    path = Path(project_path)
    detected_tech = []

    file_tech_map = {
        "package.json": "nodejs",
        "requirements.txt": "python",
        "Pipfile": "python",
        "pyproject.toml": "python",
        "Dockerfile": "docker",
        "docker-compose.yml": "docker",
        "docker-compose.yaml": "docker",
        "kubernetes.yaml": "kubernetes",
        "k8s.yaml": "kubernetes",
        "nginx.conf": "nginx",
        "Gemfile": "ruby",
        "go.mod": "golang",
        "Cargo.toml": "rust",
        "pom.xml": "java",
        "build.gradle": "java",
    }

    for file, tech in file_tech_map.items():
        if (path / file).exists() or list(path.rglob(file)):
            detected_tech.append(tech)

    return {
        "detected_technologies": list(set(detected_tech)),
        "project_path": str(path.absolute())
    }


def load_cached_intel(intel_type: str = "all", cache_dir: Path = None) -> dict:
    """Load cached threat intelligence if available and recent."""
    cache_dir = cache_dir or Path.home() / ".claude" / "security"

    if intel_type == "all":
        cache_file = cache_dir / "threat_intel_cache.json"
    else:
        cache_file = cache_dir / f"threat_intel_{intel_type}_cache.json"

    if not cache_file.exists():
        return {"cached": False, "data": None}

    try:
        data = json.loads(cache_file.read_text())
        cached_time = datetime.fromisoformat(data.get("timestamp", "2000-01-01"))

        # Cache valid for 24 hours
        if datetime.now() - cached_time < timedelta(hours=24):
            age_hours = (datetime.now() - cached_time).seconds // 3600
            return {"cached": True, "data": data, "age_hours": age_hours}
    except (json.JSONDecodeError, ValueError):
        pass

    return {"cached": False, "data": None, "reason": "Cache expired or invalid"}


def save_intel_cache(intel_data: dict, intel_type: str = "all", cache_dir: Path = None):
    """Save collected intelligence to cache."""
    cache_dir = cache_dir or Path.home() / ".claude" / "security"
    cache_dir.mkdir(parents=True, exist_ok=True)

    if intel_type == "all":
        cache_file = cache_dir / "threat_intel_cache.json"
    else:
        cache_file = cache_dir / f"threat_intel_{intel_type}_cache.json"

    intel_data["timestamp"] = datetime.now().isoformat()
    intel_data["intel_type"] = intel_type
    cache_file.write_text(json.dumps(intel_data, indent=2))
    print(f"[+] Threat intelligence cached: {cache_file}")


def main():
    parser = argparse.ArgumentParser(
        description="Threat Intelligence Collector v2 - Multi-agent support"
    )
    parser.add_argument(
        "--type", "-t",
        choices=["cve", "tech", "compliance", "all"],
        default="all",
        help="Intelligence type to gather (default: all)"
    )
    parser.add_argument(
        "--project", "-p",
        default=".",
        help="Project path for technology detection"
    )
    parser.add_argument(
        "--no-cache",
        action="store_true",
        help="Ignore cached intelligence"
    )
    parser.add_argument(
        "--output", "-o",
        help="Output file for instructions JSON"
    )

    args = parser.parse_args()

    print(f"[*] Threat Intelligence Collector v2 - Type: {args.type}")
    print("=" * 50)

    # Check for cached intelligence
    if not args.no_cache:
        cached = load_cached_intel(args.type)
        if cached["cached"]:
            print(f"[*] Using cached intelligence (age: {cached['age_hours']}h)")
            if args.output:
                Path(args.output).write_text(json.dumps(cached["data"], indent=2))
            else:
                print(json.dumps(cached["data"], indent=2))
            return cached["data"]

    # Analyze current project
    print("[*] Analyzing project dependencies...")
    project_analysis = analyze_project_dependencies(args.project)
    detected_tech = project_analysis["detected_technologies"]
    print(f"[*] Detected technologies: {detected_tech}")

    # Generate intelligence gathering instructions
    print(f"\n[*] Intelligence Instructions for {args.type.upper()} Agent:")
    print("-" * 50)

    instructions = get_intel_instructions(args.type, detected_tech)

    if args.output:
        Path(args.output).write_text(json.dumps(instructions, indent=2))
        print(f"[+] Instructions saved to: {args.output}")
    else:
        print(json.dumps(instructions, indent=2))

    return instructions


if __name__ == "__main__":
    main()
