#!/usr/bin/env python3
"""
Automated Security Patch Application System
Interactive patching with user approval and rollback support.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path
from typing import Optional


def run_command(cmd: list, timeout: int = 300, check: bool = False) -> dict:
    """Execute command and capture output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {
            "success": result.returncode == 0 or not check,
            "stdout": result.stdout,
            "stderr": result.stderr,
            "code": result.returncode
        }
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except FileNotFoundError:
        return {"success": False, "error": f"Command not found: {cmd[0]}"}


def create_backup(backup_dir: Path) -> dict:
    """Create backup before applying patches."""
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_path = backup_dir / f"pre_patch_backup_{timestamp}"
    backup_path.mkdir(parents=True, exist_ok=True)

    backups = {"timestamp": timestamp, "path": str(backup_path), "items": []}

    # Backup package lock files
    for lock_file in ["package-lock.json", "yarn.lock", "pnpm-lock.yaml"]:
        if Path(lock_file).exists():
            result = run_command(["cp", lock_file, str(backup_path / lock_file)])
            if result["success"]:
                backups["items"].append(lock_file)

    # Backup requirements files
    for req_file in Path(".").glob("*requirements*.txt"):
        result = run_command(["cp", str(req_file), str(backup_path / req_file.name)])
        if result["success"]:
            backups["items"].append(str(req_file))

    # Backup Gemfile.lock
    if Path("Gemfile.lock").exists():
        result = run_command(["cp", "Gemfile.lock", str(backup_path / "Gemfile.lock")])
        if result["success"]:
            backups["items"].append("Gemfile.lock")

    return backups


def analyze_vulnerabilities(scan_report: Path) -> list:
    """Parse scan report and extract actionable vulnerabilities."""
    if not scan_report.exists():
        return []

    report = json.loads(scan_report.read_text())
    vulnerabilities = []

    # Parse npm audit results
    npm_findings = report.get("findings", {}).get("dependencies", {}).get("npm", {})
    if npm_findings and isinstance(npm_findings, dict):
        for vuln_id, vuln_data in npm_findings.get("vulnerabilities", {}).items():
            vulnerabilities.append({
                "id": vuln_id,
                "type": "npm",
                "package": vuln_data.get("name", vuln_id),
                "severity": vuln_data.get("severity", "unknown"),
                "fix_available": vuln_data.get("fixAvailable", False),
                "recommendation": vuln_data.get("via", [{}])[0] if isinstance(vuln_data.get("via"), list) else {}
            })

    # Parse pip audit results
    pip_findings = report.get("findings", {}).get("dependencies", {}).get("pip", [])
    if pip_findings and isinstance(pip_findings, list):
        for vuln in pip_findings:
            vulnerabilities.append({
                "id": vuln.get("id", "unknown"),
                "type": "pip",
                "package": vuln.get("name", "unknown"),
                "severity": vuln.get("severity", "unknown"),
                "fix_available": bool(vuln.get("fix_versions")),
                "fix_version": vuln.get("fix_versions", [None])[0] if vuln.get("fix_versions") else None
            })

    return vulnerabilities


def generate_patch_plan(vulnerabilities: list) -> list:
    """Generate patch plan sorted by severity."""
    severity_order = {"critical": 0, "high": 1, "medium": 2, "low": 3, "unknown": 4}

    # Filter fixable vulnerabilities and sort by severity
    fixable = [v for v in vulnerabilities if v.get("fix_available")]
    fixable.sort(key=lambda x: severity_order.get(x.get("severity", "unknown").lower(), 5))

    return fixable


def apply_npm_patch(package: str, dry_run: bool = False) -> dict:
    """Apply npm security fix."""
    if dry_run:
        return {"success": True, "action": "dry_run", "package": package}

    # Try npm audit fix first
    result = run_command(["npm", "audit", "fix", "--package-lock-only"])
    if result["success"]:
        return {"success": True, "action": "audit_fix", "output": result["stdout"]}

    # If audit fix fails, try updating specific package
    result = run_command(["npm", "update", package])
    return {"success": result["success"], "action": "update", "output": result.get("stdout", result.get("error"))}


def apply_pip_patch(package: str, version: Optional[str], dry_run: bool = False) -> dict:
    """Apply pip security fix."""
    if dry_run:
        return {"success": True, "action": "dry_run", "package": package, "version": version}

    if version:
        cmd = ["pip", "install", f"{package}>={version}"]
    else:
        cmd = ["pip", "install", "--upgrade", package]

    result = run_command(cmd)
    return {"success": result["success"], "action": "upgrade", "output": result.get("stdout", result.get("error"))}


def rollback_patches(backup: dict) -> dict:
    """Rollback to pre-patch state."""
    results = {"restored": [], "failed": []}
    backup_path = Path(backup["path"])

    if not backup_path.exists():
        return {"success": False, "error": "Backup not found"}

    for item in backup["items"]:
        backup_file = backup_path / Path(item).name
        if backup_file.exists():
            result = run_command(["cp", str(backup_file), item])
            if result["success"]:
                results["restored"].append(item)
            else:
                results["failed"].append(item)

    # Reinstall dependencies
    if Path("package.json").exists():
        run_command(["npm", "ci"])
    if Path("requirements.txt").exists():
        run_command(["pip", "install", "-r", "requirements.txt"])

    return {"success": len(results["failed"]) == 0, **results}


def print_patch_summary(vulnerabilities: list, patch_plan: list):
    """Print summary of vulnerabilities and patch plan."""
    print("\n" + "=" * 60)
    print("SECURITY PATCH ANALYSIS")
    print("=" * 60)

    print(f"\nTotal Vulnerabilities Found: {len(vulnerabilities)}")
    print(f"Fixable Vulnerabilities: {len(patch_plan)}")

    severity_counts = {}
    for v in vulnerabilities:
        sev = v.get("severity", "unknown").upper()
        severity_counts[sev] = severity_counts.get(sev, 0) + 1

    print("\nBy Severity:")
    for sev in ["CRITICAL", "HIGH", "MEDIUM", "LOW"]:
        if sev in severity_counts:
            print(f"  {sev}: {severity_counts[sev]}")

    if patch_plan:
        print("\n" + "-" * 60)
        print("PROPOSED PATCHES")
        print("-" * 60)
        for i, patch in enumerate(patch_plan, 1):
            fix_ver = f" -> {patch.get('fix_version')}" if patch.get('fix_version') else ""
            print(f"{i}. [{patch['severity'].upper()}] {patch['type']}: {patch['package']}{fix_ver}")


def interactive_patch(patch_plan: list, backup_dir: Path, dry_run: bool = False) -> dict:
    """Interactive patching with user confirmation."""
    results = {"applied": [], "skipped": [], "failed": []}

    # Create backup first
    print("\n[*] Creating backup before patching...")
    backup = create_backup(backup_dir)
    print(f"[+] Backup created: {backup['path']}")

    for patch in patch_plan:
        print(f"\n{'=' * 40}")
        print(f"Package: {patch['package']}")
        print(f"Type: {patch['type']}")
        print(f"Severity: {patch['severity'].upper()}")
        if patch.get('fix_version'):
            print(f"Fix Version: {patch['fix_version']}")
        print("=" * 40)

        # For non-interactive mode, apply critical and high severity automatically
        if dry_run:
            response = 'y' if patch['severity'].lower() in ['critical', 'high'] else 'n'
        else:
            response = input("\nApply this patch? [y/N/q(quit)]: ").strip().lower()

        if response == 'q':
            print("[*] Patching cancelled by user")
            break
        elif response == 'y':
            print(f"[*] Applying patch for {patch['package']}...")

            if patch['type'] == 'npm':
                result = apply_npm_patch(patch['package'], dry_run)
            elif patch['type'] == 'pip':
                result = apply_pip_patch(patch['package'], patch.get('fix_version'), dry_run)
            else:
                result = {"success": False, "error": f"Unknown package type: {patch['type']}"}

            if result["success"]:
                print(f"[+] Successfully patched: {patch['package']}")
                results["applied"].append(patch)
            else:
                print(f"[-] Failed to patch: {patch['package']}")
                print(f"    Error: {result.get('error', result.get('output', 'Unknown error'))}")
                results["failed"].append({**patch, "error": result.get('error')})

                # Ask about rollback on failure
                if not dry_run:
                    rollback = input("Rollback all changes? [y/N]: ").strip().lower()
                    if rollback == 'y':
                        print("[*] Rolling back changes...")
                        rollback_result = rollback_patches(backup)
                        if rollback_result["success"]:
                            print("[+] Rollback completed successfully")
                        else:
                            print("[-] Rollback encountered issues")
                        break
        else:
            print(f"[*] Skipping: {patch['package']}")
            results["skipped"].append(patch)

    results["backup"] = backup
    return results


def main():
    parser = argparse.ArgumentParser(description="Automated Security Patch Application")
    parser.add_argument("--scan-report", type=Path, help="Path to security scan report JSON")
    parser.add_argument("--backup-dir", type=Path, default=Path("./patch-backups"), help="Backup directory")
    parser.add_argument("--dry-run", action="store_true", help="Analyze without applying patches")
    parser.add_argument("--auto-apply", choices=["critical", "high", "all"], help="Auto-apply patches by severity")
    parser.add_argument("--rollback", type=Path, help="Rollback using backup directory")
    args = parser.parse_args()

    # Handle rollback
    if args.rollback:
        backup_info_file = args.rollback / "backup_info.json"
        if backup_info_file.exists():
            backup = json.loads(backup_info_file.read_text())
            result = rollback_patches(backup)
            print(f"Rollback result: {'Success' if result['success'] else 'Failed'}")
            sys.exit(0 if result["success"] else 1)
        else:
            print("Error: backup_info.json not found in rollback directory")
            sys.exit(1)

    # Find latest scan report if not specified
    if not args.scan_report:
        reports = sorted(Path("./security-reports").glob("scan_*.json"), reverse=True)
        if reports:
            args.scan_report = reports[0]
            print(f"[*] Using latest scan report: {args.scan_report}")
        else:
            print("Error: No scan report found. Run security_scanner.py first.")
            sys.exit(1)

    # Analyze vulnerabilities
    print("[*] Analyzing security scan results...")
    vulnerabilities = analyze_vulnerabilities(args.scan_report)
    patch_plan = generate_patch_plan(vulnerabilities)

    # Print summary
    print_patch_summary(vulnerabilities, patch_plan)

    if not patch_plan:
        print("\n[+] No actionable patches available.")
        sys.exit(0)

    # Apply patches
    if args.dry_run:
        print("\n[*] Dry run mode - no changes will be made")
        results = {"plan": patch_plan, "mode": "dry_run"}
    else:
        results = interactive_patch(patch_plan, args.backup_dir, dry_run=args.dry_run)

    # Save results
    args.backup_dir.mkdir(parents=True, exist_ok=True)
    results_file = args.backup_dir / f"patch_results_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json"
    results_file.write_text(json.dumps(results, indent=2, default=str))
    print(f"\n[+] Patch results saved: {results_file}")

    # Summary
    if not args.dry_run and "applied" in results:
        print(f"\n{'=' * 60}")
        print("PATCH SUMMARY")
        print("=" * 60)
        print(f"Applied: {len(results['applied'])}")
        print(f"Skipped: {len(results['skipped'])}")
        print(f"Failed: {len(results['failed'])}")


if __name__ == "__main__":
    main()
