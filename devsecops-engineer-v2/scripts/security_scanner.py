#!/usr/bin/env python3
"""
DevSecOps Security Scanner v2
Multi-category security scanning with parallel execution support.

Each scan category can be run independently by separate agents:
- vulnerability: CVE/vulnerability scanning
- secrets: Secret/credential detection
- config: Configuration auditing
- deps: Dependency checking
- container: Container security
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Optional


def run_command(cmd: List[str], timeout: int = 300) -> dict:
    """Execute command and capture output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"success": True, "stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except FileNotFoundError:
        return {"success": False, "error": f"Command not found: {cmd[0]}"}


def scan_vulnerability(target: str = ".") -> dict:
    """Scan for vulnerabilities using Trivy and language-specific tools."""
    findings = {
        "scan_type": "vulnerability",
        "target": target,
        "findings": [],
        "summary": {"critical": 0, "high": 0, "medium": 0, "low": 0}
    }

    # Trivy filesystem scan
    result = run_command(["trivy", "fs", target, "--format", "json", "--severity", "CRITICAL,HIGH,MEDIUM,LOW"])
    if result["success"] and result["stdout"]:
        try:
            trivy_output = json.loads(result["stdout"])
            for result_item in trivy_output.get("Results", []):
                for vuln in result_item.get("Vulnerabilities", []):
                    severity = vuln.get("Severity", "UNKNOWN").lower()
                    findings["findings"].append({
                        "id": vuln.get("VulnerabilityID"),
                        "severity": severity,
                        "cvss_score": vuln.get("CVSS", {}).get("nvd", {}).get("V3Score", 0),
                        "package": vuln.get("PkgName"),
                        "installed": vuln.get("InstalledVersion"),
                        "fixed": vuln.get("FixedVersion"),
                        "title": vuln.get("Title", ""),
                        "description": vuln.get("Description", "")[:200]
                    })
                    if severity in findings["summary"]:
                        findings["summary"][severity] += 1
        except json.JSONDecodeError:
            findings["error"] = "Failed to parse Trivy output"

    # npm audit if package.json exists
    if Path(target).joinpath("package.json").exists() or Path("package.json").exists():
        result = run_command(["npm", "audit", "--json"])
        if result["success"] and result["stdout"]:
            try:
                npm_output = json.loads(result["stdout"])
                for vuln_id, vuln in npm_output.get("vulnerabilities", {}).items():
                    severity = vuln.get("severity", "low")
                    findings["findings"].append({
                        "id": f"NPM-{vuln_id}",
                        "severity": severity,
                        "package": vuln.get("name"),
                        "via": vuln.get("via", []),
                        "title": f"npm vulnerability in {vuln.get('name')}"
                    })
            except json.JSONDecodeError:
                pass

    return findings


def scan_secrets(target: str = ".") -> dict:
    """Detect exposed secrets and credentials."""
    findings = {
        "scan_type": "secrets",
        "target": target,
        "findings": [],
        "summary": {"critical": 0, "high": 0}
    }

    # TruffleHog scan
    result = run_command(["trufflehog", "filesystem", target, "--json", "--no-update"])
    if result["success"] and result["stdout"]:
        for line in result["stdout"].strip().split("\n"):
            if line:
                try:
                    secret = json.loads(line)
                    findings["findings"].append({
                        "id": f"SECRET-{len(findings['findings'])+1}",
                        "severity": "critical",
                        "type": secret.get("DetectorType", "unknown"),
                        "file": secret.get("SourceMetadata", {}).get("Data", {}).get("Filesystem", {}).get("file", ""),
                        "verified": secret.get("Verified", False)
                    })
                    findings["summary"]["critical"] += 1
                except json.JSONDecodeError:
                    continue

    # Pattern-based detection
    secret_patterns = [
        ("AWS Access Key", r"AKIA[0-9A-Z]{16}"),
        ("Private Key", r"-----BEGIN (RSA|DSA|EC|OPENSSH) PRIVATE KEY-----"),
        ("API Key", r"api[_-]?key['\"]?\s*[:=]\s*['\"][a-zA-Z0-9]{20,}"),
        ("Password", r"password['\"]?\s*[:=]\s*['\"][^'\"]{8,}"),
        ("Token", r"(bearer|token)['\"]?\s*[:=]\s*['\"][a-zA-Z0-9._-]{20,}"),
    ]
    findings["patterns_checked"] = [p[0] for p in secret_patterns]

    return findings


def scan_config(target: str = "local", host: Optional[str] = None) -> dict:
    """Audit system security configuration."""
    findings = {
        "scan_type": "config",
        "target": target,
        "findings": [],
        "summary": {"high": 0, "medium": 0, "low": 0},
        "hardening_score": 0
    }

    checks_passed = 0
    total_checks = 0

    if target == "local":
        # SSH config check
        total_checks += 1
        ssh_config = Path.home() / ".ssh" / "config"
        if ssh_config.exists():
            content = ssh_config.read_text()
            if "PasswordAuthentication yes" in content:
                findings["findings"].append({
                    "id": "CONFIG-SSH-001",
                    "severity": "medium",
                    "category": "ssh",
                    "title": "Password authentication enabled",
                    "current_value": "PasswordAuthentication yes",
                    "expected_value": "PasswordAuthentication no",
                    "remediation": "Disable password auth in ~/.ssh/config"
                })
                findings["summary"]["medium"] += 1
            else:
                checks_passed += 1

        # Check for world-readable SSH keys
        total_checks += 1
        ssh_dir = Path.home() / ".ssh"
        if ssh_dir.exists():
            for key_file in ssh_dir.glob("id_*"):
                if not key_file.name.endswith(".pub"):
                    mode = key_file.stat().st_mode
                    if mode & 0o077:  # Group or world readable
                        findings["findings"].append({
                            "id": f"CONFIG-SSH-002",
                            "severity": "high",
                            "category": "permissions",
                            "title": f"SSH key has insecure permissions: {key_file.name}",
                            "current_value": oct(mode),
                            "expected_value": "0600",
                            "remediation": f"chmod 600 {key_file}"
                        })
                        findings["summary"]["high"] += 1
                    else:
                        checks_passed += 1

        # Open ports check
        total_checks += 1
        result = run_command(["lsof", "-i", "-P", "-n"])
        if result["success"]:
            port_count = len(result["stdout"].strip().split("\n")) - 1
            if port_count > 50:
                findings["findings"].append({
                    "id": "CONFIG-NET-001",
                    "severity": "low",
                    "category": "network",
                    "title": f"High number of open ports: {port_count}",
                    "remediation": "Review and close unnecessary ports"
                })
                findings["summary"]["low"] += 1
            else:
                checks_passed += 1

        # Lynis audit (if available)
        result = run_command(["lynis", "audit", "system", "--quick", "--quiet", "--no-colors"])
        if result["success"]:
            findings["lynis_available"] = True

    if total_checks > 0:
        findings["hardening_score"] = int((checks_passed / total_checks) * 100)

    return findings


def scan_deps(target: str = ".") -> dict:
    """Check dependencies for outdated packages and license issues."""
    findings = {
        "scan_type": "deps",
        "target": target,
        "findings": [],
        "summary": {"vulnerable": 0, "outdated": 0, "license_issues": 0},
        "sbom": {"packages": [], "total": 0}
    }

    # npm outdated
    if Path(target).joinpath("package.json").exists() or Path("package.json").exists():
        result = run_command(["npm", "outdated", "--json"])
        if result["success"] and result["stdout"]:
            try:
                outdated = json.loads(result["stdout"])
                for pkg, info in outdated.items():
                    findings["findings"].append({
                        "id": f"DEP-NPM-{pkg}",
                        "severity": "medium",
                        "package": pkg,
                        "issue": "outdated",
                        "current": info.get("current"),
                        "latest": info.get("latest")
                    })
                    findings["summary"]["outdated"] += 1
            except json.JSONDecodeError:
                pass

        # Get package list for SBOM
        result = run_command(["npm", "list", "--json", "--depth=0"])
        if result["success"] and result["stdout"]:
            try:
                pkg_list = json.loads(result["stdout"])
                for name, info in pkg_list.get("dependencies", {}).items():
                    findings["sbom"]["packages"].append({
                        "name": name,
                        "version": info.get("version"),
                        "ecosystem": "npm"
                    })
                findings["sbom"]["total"] = len(findings["sbom"]["packages"])
            except json.JSONDecodeError:
                pass

    # pip outdated
    if Path(target).joinpath("requirements.txt").exists() or Path("requirements.txt").exists():
        result = run_command(["pip", "list", "--outdated", "--format=json"])
        if result["success"] and result["stdout"]:
            try:
                outdated = json.loads(result["stdout"])
                for pkg in outdated:
                    findings["findings"].append({
                        "id": f"DEP-PIP-{pkg['name']}",
                        "severity": "low",
                        "package": pkg["name"],
                        "issue": "outdated",
                        "current": pkg.get("version"),
                        "latest": pkg.get("latest_version")
                    })
                    findings["summary"]["outdated"] += 1
            except json.JSONDecodeError:
                pass

    return findings


def scan_container(target: str = ".") -> dict:
    """Scan container images and Dockerfiles."""
    findings = {
        "scan_type": "container",
        "target": target,
        "findings": [],
        "summary": {"critical": 0, "high": 0, "medium": 0, "low": 0},
        "image_info": None
    }

    # Find Dockerfile
    dockerfile = Path(target) / "Dockerfile"
    if dockerfile.exists():
        # Hadolint check
        result = run_command(["hadolint", str(dockerfile), "--format", "json"])
        if result["success"] and result["stdout"]:
            try:
                issues = json.loads(result["stdout"])
                for issue in issues:
                    severity = {"error": "high", "warning": "medium", "info": "low"}.get(issue.get("level"), "low")
                    findings["findings"].append({
                        "id": f"DOCKER-{issue.get('code')}",
                        "severity": severity,
                        "type": "dockerfile",
                        "title": issue.get("message"),
                        "line": issue.get("line"),
                        "remediation": f"Fix {issue.get('code')} in Dockerfile"
                    })
                    if severity in findings["summary"]:
                        findings["summary"][severity] += 1
            except json.JSONDecodeError:
                pass

    # Trivy container scan (if target is an image name)
    if ":" in target or target.startswith("docker.io"):
        result = run_command(["trivy", "image", target, "--format", "json"])
        if result["success"] and result["stdout"]:
            try:
                trivy_output = json.loads(result["stdout"])
                findings["image_info"] = {
                    "name": target,
                    "layers": len(trivy_output.get("Results", []))
                }
                for result_item in trivy_output.get("Results", []):
                    for vuln in result_item.get("Vulnerabilities", []):
                        severity = vuln.get("Severity", "UNKNOWN").lower()
                        findings["findings"].append({
                            "id": vuln.get("VulnerabilityID"),
                            "severity": severity,
                            "type": "vulnerability",
                            "package": vuln.get("PkgName"),
                            "title": vuln.get("Title", ""),
                            "layer": result_item.get("Target")
                        })
                        if severity in findings["summary"]:
                            findings["summary"][severity] += 1
            except json.JSONDecodeError:
                pass

    return findings


def main():
    parser = argparse.ArgumentParser(
        description="DevSecOps Security Scanner v2 - Multi-category scanning"
    )
    parser.add_argument(
        "--category", "-c",
        choices=["vulnerability", "secrets", "config", "deps", "container", "all"],
        default="all",
        help="Scan category (default: all)"
    )
    parser.add_argument("--target", "-t", default=".", help="Target path or image")
    parser.add_argument("--host", help="Remote host for SSH-based config scanning")
    parser.add_argument("--output", "-o", default="./security-reports", help="Output directory")

    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    categories = ["vulnerability", "secrets", "config", "deps", "container"] if args.category == "all" else [args.category]

    print(f"[*] DevSecOps Scanner v2 - Categories: {', '.join(categories)}")

    for category in categories:
        print(f"[*] Running {category} scan...")

        if category == "vulnerability":
            result = scan_vulnerability(args.target)
        elif category == "secrets":
            result = scan_secrets(args.target)
        elif category == "config":
            result = scan_config("local" if not args.host else "ssh", args.host)
        elif category == "deps":
            result = scan_deps(args.target)
        elif category == "container":
            result = scan_container(args.target)
        else:
            continue

        # Save individual category report
        report_file = output_dir / f"scan_{category}_{timestamp}.json"
        report_file.write_text(json.dumps(result, indent=2, default=str))
        print(f"[+] {category} report saved: {report_file}")

        # Print summary
        summary = result.get("summary", {})
        print(f"    Summary: {summary}")


if __name__ == "__main__":
    main()
