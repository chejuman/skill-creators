#!/usr/bin/env python3
"""Expert-Level Security Report Generator with CVSS scoring and visualizations."""
import argparse
import json
from datetime import datetime
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent.parent
TEMPLATE_DIR = SCRIPT_DIR / "assets" / "templates"

CVSS_WEIGHTS = {"critical": 10, "high": 7, "medium": 4, "low": 1}
RISK_THRESHOLDS = [(80, "Critical", "Immediate action required. Critical vulnerabilities present."),
                   (50, "High", "Significant risks identified requiring prompt attention."),
                   (25, "Medium", "Moderate risks found. Plan remediation within 30 days."),
                   (0, "Low", "Minor issues identified. Address in regular maintenance.")]


def calculate_cvss_risk(findings: dict) -> dict:
    """Calculate risk score using CVSS-weighted methodology."""
    counts = {"critical": 0, "high": 0, "medium": 0, "low": 0}
    for category, data in findings.items():
        if isinstance(data, dict):
            for key, value in data.items():
                if isinstance(value, list):
                    for item in value:
                        sev = (item.get("severity", "") or "").lower() if isinstance(item, dict) else ""
                        if sev in counts:
                            counts[sev] += 1
        if category == "threat_intelligence" and isinstance(data, dict):
            for cve in data.get("relevant_cves", []):
                sev = (cve.get("severity", "") or "").lower()
                if sev in counts:
                    counts[sev] += 1
    score = sum(counts[k] * CVSS_WEIGHTS[k] for k in counts)
    score = min(score, 100)
    for threshold, level, summary in RISK_THRESHOLDS:
        if score >= threshold:
            return {"score": score, "level": level, "summary": summary, "counts": counts}
    return {"score": 0, "level": "Low", "summary": "No significant issues found.", "counts": counts}


def build_executive_summary(findings: dict, risk: dict) -> str:
    """Generate executive summary paragraph."""
    total = sum(risk["counts"].values())
    summary = f"This security assessment identified {total} potential security issues across the target environment. "
    if risk["counts"]["critical"] > 0:
        summary += f"{risk['counts']['critical']} critical vulnerabilities require immediate attention. "
    if findings.get("system", {}).get("critical_ports"):
        exposed = len(findings["system"]["critical_ports"])
        summary += f"{exposed} network services were found exposed to potential attacks. "
    if findings.get("threat_intelligence", {}).get("relevant_cves"):
        intel_count = len(findings["threat_intelligence"]["relevant_cves"])
        summary += f"Real-time threat intelligence identified {intel_count} relevant CVEs affecting detected technologies. "
    summary += f"Overall risk level: {risk['level']}. {risk['summary']}"
    return summary


def build_key_findings(findings: dict) -> str:
    """Generate key findings list."""
    items = []
    if findings.get("system", {}).get("open_ports"):
        items.append(f"<li>{findings['system']['open_ports']} open network ports detected</li>")
    for port in findings.get("system", {}).get("critical_ports", [])[:3]:
        items.append(f"<li><strong>{port['service']}</strong> exposed on port {port['port']} (Risk: {port.get('risk', 'unknown')})</li>")
    if findings.get("threat_intelligence", {}).get("relevant_cves"):
        for cve in findings["threat_intelligence"]["relevant_cves"][:2]:
            items.append(f"<li><strong>{cve['cve_id']}</strong>: {cve.get('description', 'N/A')[:80]}...</li>")
    return "\n".join(items) if items else "<li>No critical findings</li>"


def build_threat_intel(findings: dict) -> str:
    """Generate threat intelligence section."""
    intel = findings.get("threat_intelligence", {})
    if not intel.get("relevant_cves"):
        return '<div class="intel-item"><span>No relevant CVEs collected</span></div>'
    items = []
    for cve in intel.get("relevant_cves", []):
        items.append(f'''<div class="intel-item">
            <span class="intel-cve">{cve.get('cve_id', 'N/A')}</span>
            <span><strong>{cve.get('severity', 'N/A').upper()}</strong> (CVSS: {cve.get('cvss', 'N/A')}) - {cve.get('affected', 'N/A')}<br>{cve.get('description', 'N/A')}</span>
        </div>''')
    return "\n".join(items)


def build_detailed_findings(findings: dict) -> str:
    """Generate detailed findings section."""
    sections = []
    for port in findings.get("system", {}).get("critical_ports", []):
        risk = port.get("risk", "medium")
        sections.append(f'''<div class="finding {risk}">
            <div class="finding-header">
                <span class="finding-title">Exposed Service: {port['service']}</span>
                <span class="severity-badge {risk}">{risk.upper()}</span>
            </div>
            <p><strong>Port:</strong> {port['port']} | <strong>Exposure:</strong> {port.get('exposure', 'N/A')}</p>
            <p><strong>Recommendation:</strong> Restrict access to localhost or implement firewall rules.</p>
        </div>''')
    for cve in findings.get("threat_intelligence", {}).get("relevant_cves", []):
        sev = cve.get("severity", "medium").lower()
        sections.append(f'''<div class="finding {sev}">
            <div class="finding-header">
                <span class="finding-title">{cve.get('cve_id', 'N/A')}: {cve.get('affected', 'Unknown')}</span>
                <span class="cvss-score">CVSS {cve.get('cvss', 'N/A')}</span>
            </div>
            <p>{cve.get('description', 'No description available.')}</p>
            <p><strong>Recommendation:</strong> Apply vendor patches or implement compensating controls.</p>
        </div>''')
    return "\n".join(sections) if sections else '<p>No significant findings to report.</p>'


def build_remediation_timeline(risk: dict) -> str:
    """Generate remediation timeline."""
    items = []
    if risk["counts"]["critical"] > 0:
        items.append(f'<div class="timeline-item critical"><strong>Immediate (24h):</strong> Address {risk["counts"]["critical"]} critical vulnerabilities</div>')
    if risk["counts"]["high"] > 0:
        items.append(f'<div class="timeline-item high"><strong>1 Week:</strong> Remediate {risk["counts"]["high"]} high-severity issues</div>')
    if risk["counts"]["medium"] > 0:
        items.append(f'<div class="timeline-item"><strong>30 Days:</strong> Fix {risk["counts"]["medium"]} medium-severity findings</div>')
    if risk["counts"]["low"] > 0:
        items.append(f'<div class="timeline-item"><strong>Ongoing:</strong> Address {risk["counts"]["low"]} low-severity items in maintenance</div>')
    return "\n".join(items) if items else '<div class="timeline-item">No remediation items</div>'


def generate_expert_report(scan_data: dict, output_path: Path) -> Path:
    """Generate expert-level HTML security report."""
    template_path = TEMPLATE_DIR / "expert_report.html"
    if not template_path.exists():
        raise FileNotFoundError(f"Template not found: {template_path}")

    findings = scan_data.get("findings", {})
    risk = calculate_cvss_risk(findings)
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    total = sum(risk["counts"].values())

    replacements = {
        "{{TARGET}}": scan_data.get("target", "Local System"),
        "{{REPORT_DATE}}": timestamp,
        "{{CLASSIFICATION}}": "CONFIDENTIAL",
        "{{RISK_SCORE}}": str(risk["score"]),
        "{{RISK_LEVEL}}": risk["level"],
        "{{RISK_LEVEL_LOWER}}": risk["level"].lower(),
        "{{RISK_SUMMARY}}": risk["summary"],
        "{{CRITICAL}}": str(risk["counts"]["critical"]),
        "{{HIGH}}": str(risk["counts"]["high"]),
        "{{MEDIUM}}": str(risk["counts"]["medium"]),
        "{{LOW}}": str(risk["counts"]["low"]),
        "{{CRITICAL_PCT}}": str(min(risk["counts"]["critical"] * 25, 100)),
        "{{HIGH_PCT}}": str(min(risk["counts"]["high"] * 20, 100)),
        "{{MEDIUM_PCT}}": str(min(risk["counts"]["medium"] * 15, 100)),
        "{{LOW_PCT}}": str(min(risk["counts"]["low"] * 10, 100)),
        "{{EXECUTIVE_SUMMARY}}": build_executive_summary(findings, risk),
        "{{KEY_FINDINGS}}": build_key_findings(findings),
        "{{IMMEDIATE_ACTIONS}}": "<li>Review and restrict exposed network services</li><li>Apply critical security patches</li><li>Rotate any potentially compromised credentials</li>",
        "{{THREAT_INTEL_ITEMS}}": build_threat_intel(findings),
        "{{DETAILED_FINDINGS}}": build_detailed_findings(findings),
        "{{OWASP_ICON}}": "⚠️" if risk["counts"]["critical"] > 0 else "✅",
        "{{OWASP_STATUS}}": "Review Required" if risk["counts"]["critical"] > 0 else "Compliant",
        "{{CIS_ICON}}": "⚠️" if risk["score"] > 25 else "✅",
        "{{CIS_STATUS}}": f"{max(0, 100 - risk['score'])}% Compliant",
        "{{NIST_ICON}}": "⚠️" if risk["score"] > 50 else "✅",
        "{{NIST_STATUS}}": "Partial" if risk["score"] > 25 else "Aligned",
        "{{REMEDIATION_TIMELINE}}": build_remediation_timeline(risk),
        "{{EVIDENCE_TABLE}}": f"<tr><td>Scan Results</td><td>Automated security scan output</td><td>scan_{scan_data.get('timestamp', 'N/A')}.json</td></tr>",
    }

    html = template_path.read_text()
    for key, value in replacements.items():
        html = html.replace(key, value)

    report_file = output_path / f"expert_report_{datetime.now().strftime('%Y%m%d_%H%M%S')}.html"
    report_file.write_text(html)
    return report_file


def main():
    parser = argparse.ArgumentParser(description="Expert Security Report Generator")
    parser.add_argument("--input", required=True, help="Directory with scan results")
    parser.add_argument("--output", default="./final-reports", help="Output directory")
    args = parser.parse_args()

    input_dir, output_dir = Path(args.input), Path(args.output)
    output_dir.mkdir(parents=True, exist_ok=True)

    scan_files = list(input_dir.glob("scan_*.json"))
    if not scan_files:
        print("[!] No scan results found")
        return

    latest = max(scan_files, key=lambda p: p.stat().st_mtime)
    print(f"[*] Processing: {latest.name}")
    scan_data = json.loads(latest.read_text())

    report = generate_expert_report(scan_data, output_dir)
    print(f"[+] Expert report generated: {report}")


if __name__ == "__main__":
    main()
