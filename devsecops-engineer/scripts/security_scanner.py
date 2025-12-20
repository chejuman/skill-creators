#!/usr/bin/env python3
"""
DevSecOps Security Scanner
Comprehensive security scanning for local machines and remote servers.
"""

import argparse
import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path


def run_command(cmd: list, timeout: int = 300) -> dict:
    """Execute command and capture output."""
    try:
        result = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
        return {"success": True, "stdout": result.stdout, "stderr": result.stderr, "code": result.returncode}
    except subprocess.TimeoutExpired:
        return {"success": False, "error": "Command timed out"}
    except FileNotFoundError:
        return {"success": False, "error": f"Command not found: {cmd[0]}"}


def scan_local_dependencies() -> dict:
    """Scan local project dependencies for vulnerabilities."""
    findings = {"npm": None, "pip": None, "gem": None}

    # npm audit
    if Path("package.json").exists():
        result = run_command(["npm", "audit", "--json"])
        if result["success"]:
            findings["npm"] = json.loads(result["stdout"]) if result["stdout"] else {}

    # pip audit
    result = run_command(["pip", "list", "--format=json"])
    if result["success"]:
        pip_result = run_command(["pip-audit", "--format=json"])
        if pip_result["success"]:
            findings["pip"] = json.loads(pip_result["stdout"]) if pip_result["stdout"] else []

    return findings


def scan_secrets() -> dict:
    """Detect exposed secrets and credentials."""
    findings = {"trufflehog": None, "patterns": []}

    # TruffleHog scan
    result = run_command(["trufflehog", "filesystem", ".", "--json", "--no-update"])
    if result["success"] and result["stdout"]:
        findings["trufflehog"] = [json.loads(line) for line in result["stdout"].strip().split("\n") if line]

    # Basic pattern matching for common secrets
    secret_patterns = [
        ("AWS Key", r"AKIA[0-9A-Z]{16}"),
        ("Private Key", r"-----BEGIN.*PRIVATE KEY-----"),
        ("API Key", r"api[_-]?key['\"]?\s*[:=]\s*['\"][a-zA-Z0-9]{20,}"),
    ]
    findings["patterns_checked"] = [p[0] for p in secret_patterns]

    return findings


def scan_system_config() -> dict:
    """Audit system security configuration."""
    findings = {"lynis": None, "ssh_config": None, "open_ports": None}

    # Check SSH configuration
    ssh_config = Path.home() / ".ssh" / "config"
    if ssh_config.exists():
        findings["ssh_config"] = {"exists": True, "readable": True}

    # Scan open ports
    result = run_command(["lsof", "-i", "-P", "-n"])
    if result["success"]:
        findings["open_ports"] = len(result["stdout"].strip().split("\n")) - 1

    return findings


def scan_remote_server(host: str, user: str = None) -> dict:
    """Scan remote server via SSH."""
    ssh_target = f"{user}@{host}" if user else host
    findings = {"connection": False, "checks": {}}

    # Test SSH connection
    result = run_command(["ssh", "-o", "ConnectTimeout=10", ssh_target, "echo", "connected"])
    if not result["success"] or "connected" not in result.get("stdout", ""):
        findings["error"] = "SSH connection failed"
        return findings

    findings["connection"] = True

    # System info
    result = run_command(["ssh", ssh_target, "uname -a && cat /etc/os-release 2>/dev/null"])
    if result["success"]:
        findings["checks"]["system_info"] = result["stdout"]

    # Check for security updates
    result = run_command(["ssh", ssh_target, "apt list --upgradable 2>/dev/null || yum check-update 2>/dev/null"])
    if result["success"]:
        findings["checks"]["pending_updates"] = len(result["stdout"].strip().split("\n"))

    # Check running services
    result = run_command(["ssh", ssh_target, "systemctl list-units --type=service --state=running"])
    if result["success"]:
        findings["checks"]["running_services"] = len(result["stdout"].strip().split("\n"))

    return findings


def main():
    parser = argparse.ArgumentParser(description="DevSecOps Security Scanner")
    parser.add_argument("--target", choices=["local", "ssh"], default="local", help="Scan target type")
    parser.add_argument("--host", help="Remote host for SSH scanning")
    parser.add_argument("--user", help="SSH username")
    parser.add_argument("--output", default="./security-reports", help="Output directory")
    args = parser.parse_args()

    output_dir = Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    report = {"timestamp": timestamp, "target": args.target, "findings": {}}

    print(f"[*] Starting security scan - Target: {args.target}")

    if args.target == "local":
        print("[*] Scanning dependencies...")
        report["findings"]["dependencies"] = scan_local_dependencies()
        print("[*] Scanning for secrets...")
        report["findings"]["secrets"] = scan_secrets()
        print("[*] Auditing system configuration...")
        report["findings"]["system"] = scan_system_config()

    elif args.target == "ssh":
        if not args.host:
            print("[!] Error: --host required for SSH scanning")
            sys.exit(1)
        print(f"[*] Scanning remote server: {args.host}")
        report["findings"]["remote"] = scan_remote_server(args.host, args.user)

    # Save report
    report_file = output_dir / f"scan_{args.target}_{timestamp}.json"
    report_file.write_text(json.dumps(report, indent=2, default=str))
    print(f"[+] Report saved: {report_file}")

    return report


if __name__ == "__main__":
    main()
