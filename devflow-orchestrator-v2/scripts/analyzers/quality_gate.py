#!/usr/bin/env python3
"""Quality Gate System - Automated validation at each phase."""

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Tuple

DEVFLOW_DIR = ".devflow"

# Quality gate definitions
GATES = {
    "research_complete": {
        "name": "Research Complete",
        "phase": 2,
        "checks": [
            {"name": "tech_stack_research", "required": True},
            {"name": "market_trends_research", "required": True},
            {"name": "open_source_research", "required": True},
            {"name": "security_research", "required": True},
            {"name": "competitor_research", "required": True},
            {"name": "synthesis_exists", "required": False}
        ],
        "min_pass_rate": 80
    },
    "analysis_complete": {
        "name": "Analysis Complete",
        "phase": 3,
        "checks": [
            {"name": "user_perspective", "required": True},
            {"name": "technical_perspective", "required": True},
            {"name": "business_perspective", "required": True},
            {"name": "risk_perspective", "required": True},
            {"name": "feasibility_score", "required": True}
        ],
        "min_pass_rate": 100
    },
    "plan_validated": {
        "name": "Plan Validated",
        "phase": 6,
        "checks": [
            {"name": "features_selected", "required": True},
            {"name": "tasks_generated", "required": True},
            {"name": "dependencies_mapped", "required": True},
            {"name": "risks_identified", "required": False},
            {"name": "effort_estimated", "required": True}
        ],
        "min_pass_rate": 80
    },
    "version_ready": {
        "name": "Version Ready",
        "phase": 9,
        "checks": [
            {"name": "all_gates_passed", "required": True},
            {"name": "retrospective_done", "required": False},
            {"name": "knowledge_updated", "required": False}
        ],
        "min_pass_rate": 60
    }
}

class QualityGate:
    def __init__(self):
        self.devflow = Path.cwd() / DEVFLOW_DIR
        self.project = self._load_project()
        self.gates = self._load_gates()

    def _load_project(self) -> Dict:
        if not self.devflow.exists():
            print("No DevFlow project found.")
            sys.exit(1)
        with open(self.devflow / "project.json") as f:
            return json.load(f)

    def _load_gates(self) -> Dict:
        gates_file = self.devflow / "meta" / "quality_gates.json"
        if gates_file.exists():
            with open(gates_file) as f:
                return json.load(f)
        return {"gates": {}, "history": []}

    def _save_gates(self):
        with open(self.devflow / "meta" / "quality_gates.json", "w") as f:
            json.dump(self.gates, f, indent=2)

    def run_gate(self, gate_name: str) -> Tuple[bool, Dict]:
        """Run a specific quality gate."""
        if gate_name not in GATES:
            return False, {"error": f"Unknown gate: {gate_name}"}

        gate_def = GATES[gate_name]
        results = []

        for check in gate_def["checks"]:
            check_name = check["name"]
            passed = self._run_check(gate_name, check_name)
            results.append({
                "check": check_name,
                "passed": passed,
                "required": check["required"]
            })

        # Calculate pass rate
        total_checks = len(results)
        passed_checks = sum(1 for r in results if r["passed"])
        pass_rate = (passed_checks / total_checks) * 100 if total_checks > 0 else 0

        # Check required items
        required_passed = all(r["passed"] for r in results if r["required"])

        # Determine overall pass
        gate_passed = required_passed and pass_rate >= gate_def["min_pass_rate"]

        result = {
            "gate": gate_name,
            "name": gate_def["name"],
            "passed": gate_passed,
            "pass_rate": round(pass_rate, 1),
            "required_pass_rate": gate_def["min_pass_rate"],
            "checks": results,
            "timestamp": datetime.now().isoformat()
        }

        # Update gates state
        self.gates["gates"][gate_name] = {
            "passed": gate_passed,
            "timestamp": datetime.now().isoformat(),
            "pass_rate": pass_rate
        }
        self.gates["history"].append(result)
        self._save_gates()

        return gate_passed, result

    def _run_check(self, gate: str, check: str) -> bool:
        """Run individual check."""
        domain = self.project.get("domain", "general")

        # Research checks
        if check == "tech_stack_research":
            return (self.devflow / "research" / domain / "tech_stack.md").exists()
        elif check == "market_trends_research":
            return (self.devflow / "research" / domain / "market_trends.md").exists()
        elif check == "open_source_research":
            return (self.devflow / "research" / domain / "open_source.md").exists()
        elif check == "security_research":
            return (self.devflow / "research" / domain / "security.md").exists()
        elif check == "competitor_research":
            return (self.devflow / "research" / domain / "competitors.md").exists()
        elif check == "synthesis_exists":
            return (self.devflow / "research" / "synthesis.md").exists()

        # Analysis checks
        elif check == "user_perspective":
            return self._check_perspective_exists("user")
        elif check == "technical_perspective":
            return self._check_perspective_exists("technical")
        elif check == "business_perspective":
            return self._check_perspective_exists("business")
        elif check == "risk_perspective":
            return self._check_perspective_exists("risk")
        elif check == "feasibility_score":
            return (self.devflow / "analysis" / "feasibility.json").exists()

        # Plan checks
        elif check == "features_selected":
            return self._check_features_selected()
        elif check == "tasks_generated":
            return (self.devflow / "plans" / "current").exists() and \
                   any((self.devflow / "plans" / "current").iterdir())
        elif check == "dependencies_mapped":
            return self._check_dependencies_mapped()
        elif check == "risks_identified":
            return (self.devflow / "analysis" / "risk_matrix.json").exists()
        elif check == "effort_estimated":
            return self._check_effort_estimated()

        # Version checks
        elif check == "all_gates_passed":
            return all(g.get("passed", False) for g in self.gates["gates"].values()
                      if g != "version_ready")
        elif check == "retrospective_done":
            return (self.devflow / "knowledge" / "retrospectives").exists() and \
                   any((self.devflow / "knowledge" / "retrospectives").iterdir())
        elif check == "knowledge_updated":
            patterns_file = self.devflow / "knowledge" / "patterns.json"
            if patterns_file.exists():
                with open(patterns_file) as f:
                    data = json.load(f)
                    return len(data.get("patterns", [])) > 0
            return False

        return False

    def _check_perspective_exists(self, perspective: str) -> bool:
        perspectives_file = self.devflow / "analysis" / "perspectives.md"
        if perspectives_file.exists():
            with open(perspectives_file) as f:
                content = f.read().lower()
                return perspective in content
        return False

    def _check_features_selected(self) -> bool:
        backlog_file = self.devflow / "features" / "backlog.json"
        if backlog_file.exists():
            with open(backlog_file) as f:
                data = json.load(f)
                return any(f.get("status") == "selected" for f in data.get("features", []))
        return False

    def _check_dependencies_mapped(self) -> bool:
        # Check if any plan file mentions dependencies
        plans_dir = self.devflow / "plans" / "current"
        if plans_dir.exists():
            for plan_file in plans_dir.glob("*.md"):
                with open(plan_file) as f:
                    if "dependency" in f.read().lower():
                        return True
        return False

    def _check_effort_estimated(self) -> bool:
        backlog_file = self.devflow / "features" / "backlog.json"
        if backlog_file.exists():
            with open(backlog_file) as f:
                data = json.load(f)
                features = data.get("features", [])
                return any(f.get("effort", 0) > 0 for f in features)
        return False

    def get_all_gates_status(self) -> Dict:
        """Get status of all gates."""
        status = {}
        for gate_name, gate_def in GATES.items():
            gate_state = self.gates["gates"].get(gate_name, {})
            status[gate_name] = {
                "name": gate_def["name"],
                "phase": gate_def["phase"],
                "passed": gate_state.get("passed", False),
                "timestamp": gate_state.get("timestamp"),
                "pass_rate": gate_state.get("pass_rate", 0)
            }
        return status

    def generate_report(self) -> str:
        """Generate quality gate report."""
        status = self.get_all_gates_status()

        report = "# Quality Gate Report\n\n"
        report += f"Generated: {datetime.now().isoformat()}\n\n"
        report += "## Gate Status\n\n"
        report += "| Gate | Status | Pass Rate | Phase |\n"
        report += "|------|--------|-----------|-------|\n"

        for gate_name, gate_status in status.items():
            icon = "✅" if gate_status["passed"] else "❌"
            report += f"| {gate_status['name']} | {icon} | {gate_status['pass_rate']}% | {gate_status['phase']} |\n"

        return report

def main():
    if len(sys.argv) < 2:
        print("Usage: quality_gate.py <command> [gate_name]")
        print("Commands: run, status, report")
        print("Gates: research_complete, analysis_complete, plan_validated, version_ready")
        sys.exit(1)

    gate = QualityGate()
    cmd = sys.argv[1]

    if cmd == "run":
        if len(sys.argv) < 3:
            print("Usage: quality_gate.py run <gate_name>")
            sys.exit(1)
        passed, result = gate.run_gate(sys.argv[2])
        print(json.dumps(result, indent=2))
        sys.exit(0 if passed else 1)
    elif cmd == "status":
        status = gate.get_all_gates_status()
        print(json.dumps(status, indent=2))
    elif cmd == "report":
        report = gate.generate_report()
        print(report)
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
