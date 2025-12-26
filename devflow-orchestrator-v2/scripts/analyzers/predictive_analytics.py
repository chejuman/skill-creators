#!/usr/bin/env python3
"""Predictive Analytics Engine - Velocity, burndown, and predictions."""

import json
import sys
from datetime import datetime, timedelta
from pathlib import Path
from typing import Dict, List, Optional

DEVFLOW_DIR = ".devflow"

class PredictiveAnalytics:
    def __init__(self):
        self.devflow = Path.cwd() / DEVFLOW_DIR
        self.project = self._load_project()
        self.analytics = self._load_analytics()

    def _load_project(self) -> Dict:
        if not self.devflow.exists():
            print("No DevFlow project found.")
            sys.exit(1)
        with open(self.devflow / "project.json") as f:
            return json.load(f)

    def _load_analytics(self) -> Dict:
        analytics_file = self.devflow / "analytics" / "velocity.json"
        if analytics_file.exists():
            with open(analytics_file) as f:
                return json.load(f)
        return {"velocity": {"history": [], "current": 0}, "predictions": {}, "burndown": {}}

    def _save_analytics(self):
        with open(self.devflow / "analytics" / "velocity.json", "w") as f:
            json.dump(self.analytics, f, indent=2)

    def record_velocity(self, features_completed: int, days_elapsed: int):
        """Record velocity data point."""
        velocity = features_completed / max(days_elapsed, 1)

        self.analytics["velocity"]["history"].append({
            "date": datetime.now().isoformat(),
            "features": features_completed,
            "days": days_elapsed,
            "velocity": round(velocity, 2)
        })

        # Calculate rolling average
        history = self.analytics["velocity"]["history"][-10:]  # Last 10 data points
        avg_velocity = sum(h["velocity"] for h in history) / len(history)
        self.analytics["velocity"]["current"] = round(avg_velocity, 2)

        self._save_analytics()
        print(f"Recorded velocity: {velocity:.2f} features/day")
        print(f"Rolling average: {avg_velocity:.2f} features/day")

    def calculate_predictions(self) -> Dict:
        """Calculate predictive analytics."""
        current_version = float(self.project.get("current_version", "0.0"))
        target_version = float(self.project.get("target_version", "10.0"))
        velocity = self.analytics["velocity"].get("current", 0.1)

        # Load feature backlog
        backlog_file = self.devflow / "features" / "backlog.json"
        pending_features = 0
        if backlog_file.exists():
            with open(backlog_file) as f:
                backlog = json.load(f)
                pending_features = len([f for f in backlog.get("features", [])
                                       if f.get("status") != "completed"])

        # Estimate features per version (based on complexity)
        complexity = self.project.get("complexity", 3)
        features_per_version = 3 + complexity

        # Remaining versions
        remaining_versions = target_version - current_version

        # Total remaining features estimate
        total_remaining = remaining_versions * features_per_version

        # Time predictions
        if velocity > 0:
            days_to_next = features_per_version / velocity
            days_to_target = total_remaining / velocity
        else:
            days_to_next = float('inf')
            days_to_target = float('inf')

        # Confidence based on velocity history
        history_len = len(self.analytics["velocity"].get("history", []))
        confidence = min(95, 50 + history_len * 5)

        predictions = {
            "next_version": {
                "version": f"{current_version + 1:.1f}",
                "estimated_days": round(days_to_next, 1),
                "estimated_date": (datetime.now() + timedelta(days=days_to_next)).strftime("%Y-%m-%d"),
                "features_needed": features_per_version
            },
            "target_version": {
                "version": str(target_version),
                "estimated_days": round(days_to_target, 1),
                "estimated_date": (datetime.now() + timedelta(days=days_to_target)).strftime("%Y-%m-%d"),
                "remaining_versions": remaining_versions
            },
            "velocity": {
                "current": velocity,
                "trend": self._calculate_trend(),
                "confidence": confidence
            },
            "risks": self._identify_velocity_risks(velocity, days_to_target)
        }

        self.analytics["predictions"] = predictions
        self._save_analytics()

        return predictions

    def _calculate_trend(self) -> str:
        """Calculate velocity trend."""
        history = self.analytics["velocity"].get("history", [])
        if len(history) < 3:
            return "insufficient_data"

        recent = history[-3:]
        older = history[-6:-3] if len(history) >= 6 else history[:3]

        recent_avg = sum(h["velocity"] for h in recent) / len(recent)
        older_avg = sum(h["velocity"] for h in older) / len(older)

        if recent_avg > older_avg * 1.1:
            return "improving"
        elif recent_avg < older_avg * 0.9:
            return "declining"
        return "stable"

    def _identify_velocity_risks(self, velocity: float, days_to_target: float) -> List[Dict]:
        """Identify risks based on velocity."""
        risks = []

        if velocity < 0.1:
            risks.append({
                "risk": "Very low velocity",
                "severity": "high",
                "suggestion": "Review blockers and resource allocation"
            })

        if days_to_target > 365:
            risks.append({
                "risk": "Extended timeline",
                "severity": "medium",
                "suggestion": "Consider scope reduction or phased approach"
            })

        trend = self._calculate_trend()
        if trend == "declining":
            risks.append({
                "risk": "Declining velocity",
                "severity": "medium",
                "suggestion": "Investigate causes of slowdown"
            })

        return risks

    def update_burndown(self, total: int, completed: int):
        """Update burndown chart data."""
        self.analytics["burndown"] = {
            "total_features": total,
            "completed": completed,
            "remaining": total - completed,
            "percentage": round(completed / max(total, 1) * 100, 1)
        }

        # Add to history
        if "history" not in self.analytics["burndown"]:
            self.analytics["burndown"]["history"] = []

        self.analytics["burndown"]["history"].append({
            "date": datetime.now().isoformat(),
            "remaining": total - completed
        })

        self._save_analytics()

    def get_dashboard(self) -> Dict:
        """Get analytics dashboard data."""
        predictions = self.calculate_predictions()

        return {
            "project": {
                "name": self.project.get("idea", "")[:50],
                "domain": self.project.get("domain", "general"),
                "version": self.project.get("current_version", "0.0"),
                "target": self.project.get("target_version", "10.0")
            },
            "velocity": {
                "current": self.analytics["velocity"].get("current", 0),
                "trend": self._calculate_trend(),
                "history_points": len(self.analytics["velocity"].get("history", []))
            },
            "predictions": predictions,
            "burndown": self.analytics.get("burndown", {}),
            "generated_at": datetime.now().isoformat()
        }

def main():
    if len(sys.argv) < 2:
        print("Usage: predictive_analytics.py <command>")
        print("Commands: velocity, predict, burndown, dashboard")
        sys.exit(1)

    analytics = PredictiveAnalytics()
    cmd = sys.argv[1]

    if cmd == "velocity":
        if len(sys.argv) < 4:
            print("Usage: predictive_analytics.py velocity <features> <days>")
            sys.exit(1)
        analytics.record_velocity(int(sys.argv[2]), int(sys.argv[3]))
    elif cmd == "predict":
        predictions = analytics.calculate_predictions()
        print(json.dumps(predictions, indent=2))
    elif cmd == "burndown":
        if len(sys.argv) < 4:
            print("Usage: predictive_analytics.py burndown <total> <completed>")
            sys.exit(1)
        analytics.update_burndown(int(sys.argv[2]), int(sys.argv[3]))
        print("Burndown updated")
    elif cmd == "dashboard":
        dashboard = analytics.get_dashboard()
        print(json.dumps(dashboard, indent=2))
    else:
        print(f"Unknown command: {cmd}")
        sys.exit(1)

if __name__ == "__main__":
    main()
