#!/usr/bin/env python3
"""Self-Upgrade Mechanism - Learns from security assessments to improve future scans."""
import argparse
import json
from datetime import datetime
from pathlib import Path

KNOWLEDGE_BASE_PATH = Path.home() / ".claude" / "security" / "knowledge_base.json"


def load_knowledge_base() -> dict:
    """Load existing knowledge base."""
    if KNOWLEDGE_BASE_PATH.exists():
        return json.loads(KNOWLEDGE_BASE_PATH.read_text())
    return {"version": "1.0.0", "last_updated": None, "learned_patterns": [],
            "custom_rules": [], "statistics": {"scans_processed": 0, "patterns_learned": 0}}


def save_knowledge_base(kb: dict):
    """Save updated knowledge base."""
    KNOWLEDGE_BASE_PATH.parent.mkdir(parents=True, exist_ok=True)
    kb["last_updated"] = datetime.now().isoformat()
    KNOWLEDGE_BASE_PATH.write_text(json.dumps(kb, indent=2))


def extract_patterns_from_findings(findings: dict) -> list:
    """Extract new threat patterns from scan findings."""
    patterns = []
    now = datetime.now().isoformat()
    deps = findings.get("dependencies", {})
    for pkg_manager, data in deps.items():
        if not data:
            continue
        if pkg_manager == "npm" and isinstance(data, dict):
            for pkg, info in data.get("vulnerabilities", {}).items():
                if isinstance(info, dict) and info.get("severity") in ["critical", "high"]:
                    patterns.append({"type": "dependency_vulnerability", "package_manager": "npm",
                                   "package": pkg, "severity": info.get("severity"), "learned_date": now})
        if pkg_manager == "pip" and isinstance(data, list):
            for vuln in data:
                if isinstance(vuln, dict):
                    sev = vuln.get("vulns", [{}])[0].get("severity", "unknown") if vuln.get("vulns") else "unknown"
                    patterns.append({"type": "dependency_vulnerability", "package_manager": "pip",
                                   "package": vuln.get("name", "unknown"), "severity": sev, "learned_date": now})
    secrets = findings.get("secrets", {})
    for secret in (secrets.get("trufflehog") or []):
        if isinstance(secret, dict):
            patterns.append({"type": "exposed_secret", "detector": secret.get("DetectorName", "unknown"),
                           "file_pattern": secret.get("SourceMetadata", {}).get("filename", "").split("/")[-1],
                           "learned_date": now})
    return patterns


def generate_recommendations(kb: dict, new_patterns: list) -> list:
    """Generate recommendations for workflow improvements."""
    recommendations = []
    pattern_types = {}
    for pattern in kb.get("learned_patterns", []) + new_patterns:
        ptype = pattern.get("type", "unknown")
        pattern_types[ptype] = pattern_types.get(ptype, 0) + 1
    if pattern_types.get("dependency_vulnerability", 0) > 5:
        recommendations.append({"priority": "high", "action": "enable_automated_dependency_updates",
            "description": "High frequency of dependency vulnerabilities. Consider Dependabot/Renovate."})
    if pattern_types.get("exposed_secret", 0) > 2:
        recommendations.append({"priority": "critical", "action": "implement_pre_commit_hooks",
            "description": "Multiple exposed secrets detected. Implement pre-commit secret scanning."})
    return recommendations


def update_scan_rules(kb: dict, new_patterns: list) -> list:
    """Update scanning rules based on learned patterns."""
    updated_rules = kb.get("custom_rules", [])
    existing_patterns = [r.get("pattern") for r in updated_rules]
    for pattern in new_patterns:
        if pattern["type"] == "exposed_secret":
            file_pattern = pattern.get("file_pattern", "")
            if file_pattern and file_pattern not in existing_patterns:
                updated_rules.append({"type": "file_watch", "pattern": file_pattern,
                    "reason": "Previously found secrets in similar files", "added_date": datetime.now().isoformat()})
    return updated_rules


def process_findings(findings_path: Path) -> dict:
    """Process scan findings and update knowledge base."""
    scan_files = list(findings_path.glob("scan_*.json"))
    if not scan_files:
        return {"status": "no_findings", "message": "No scan results found"}
    kb = load_knowledge_base()
    all_new_patterns = []
    for scan_file in scan_files:
        scan_data = json.loads(scan_file.read_text())
        all_new_patterns.extend(extract_patterns_from_findings(scan_data.get("findings", {})))
        kb["statistics"]["scans_processed"] += 1
    existing_keys = {json.dumps(p, sort_keys=True) for p in kb["learned_patterns"]}
    unique_new = [p for p in all_new_patterns if json.dumps(p, sort_keys=True) not in existing_keys]
    kb["learned_patterns"].extend(unique_new)
    kb["statistics"]["patterns_learned"] += len(unique_new)
    kb["custom_rules"] = update_scan_rules(kb, unique_new)
    recommendations = generate_recommendations(kb, unique_new)
    save_knowledge_base(kb)
    return {"status": "upgraded", "new_patterns_learned": len(unique_new), "total_patterns": len(kb["learned_patterns"]),
            "custom_rules": len(kb["custom_rules"]), "recommendations": recommendations,
            "knowledge_base_path": str(KNOWLEDGE_BASE_PATH)}


def main():
    parser = argparse.ArgumentParser(description="Self-Upgrade Mechanism")
    parser.add_argument("--findings", required=True, help="Directory with scan findings")
    parser.add_argument("--show-kb", action="store_true", help="Display current knowledge base")
    args = parser.parse_args()
    if args.show_kb:
        print(json.dumps(load_knowledge_base(), indent=2))
        return
    print("[*] Self-Upgrade: Processing findings...")
    findings_path = Path(args.findings)
    if not findings_path.exists():
        print(f"[!] Findings directory not found: {findings_path}")
        return
    result = process_findings(findings_path)
    print(f"\n[+] Self-Upgrade Complete")
    print(f"    New patterns learned: {result.get('new_patterns_learned', 0)}")
    print(f"    Total patterns: {result.get('total_patterns', 0)}")
    print(f"    Custom rules: {result.get('custom_rules', 0)}")
    if result.get("recommendations"):
        print("\n[!] Recommendations:")
        for rec in result["recommendations"]:
            print(f"    [{rec['priority'].upper()}] {rec['description']}")
    print(f"\n[+] Knowledge base saved: {result.get('knowledge_base_path')}")


if __name__ == "__main__":
    main()
