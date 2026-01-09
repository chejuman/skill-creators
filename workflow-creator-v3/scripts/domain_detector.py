#!/usr/bin/env python3
"""
Domain Detection Module for Workflow Creator V3

Classifies user requests into domain categories for specialized processing.
"""

import re
from typing import Dict, List, Tuple
from dataclasses import dataclass


@dataclass
class DomainResult:
    """Result of domain detection"""
    domain: str
    confidence: float
    complexity: int
    keywords_matched: List[str]
    suggested_tools: List[str]


class DomainDetector:
    """Detect domain and complexity from user workflow requests"""

    DOMAINS = {
        'DevOps': {
            'keywords': [
                'deploy', 'deployment', 'ci/cd', 'ci-cd', 'pipeline',
                'kubernetes', 'k8s', 'docker', 'container', 'terraform',
                'ansible', 'jenkins', 'gitlab-ci', 'github-actions',
                'aws', 'gcp', 'azure', 'cloud', 'infrastructure'
            ],
            'tools': ['docker', 'kubernetes', 'terraform', 'github-actions']
        },
        'Security': {
            'keywords': [
                'security', 'scan', 'audit', 'vulnerability', 'vuln',
                'compliance', 'owasp', 'penetration', 'pentest',
                'sast', 'dast', 'sca', 'cve', 'threat', 'firewall',
                'authentication', 'authorization', 'encryption'
            ],
            'tools': ['trivy', 'semgrep', 'snyk', 'owasp-zap']
        },
        'WebDev': {
            'keywords': [
                'frontend', 'backend', 'react', 'vue', 'angular', 'svelte',
                'api', 'rest', 'graphql', 'component', 'ui', 'ux',
                'styling', 'css', 'tailwind', 'nextjs', 'node',
                'express', 'fastapi', 'django', 'web', 'html'
            ],
            'tools': ['react', 'tailwind', 'vite', 'typescript']
        },
        'DataOps': {
            'keywords': [
                'data', 'etl', 'pipeline', 'analytics', 'database',
                'sql', 'postgres', 'mysql', 'mongodb', 'redis',
                'bigquery', 'snowflake', 'spark', 'airflow',
                'dbt', 'transform', 'warehouse', 'lake'
            ],
            'tools': ['dbt', 'airflow', 'postgres', 'bigquery']
        },
        'Documentation': {
            'keywords': [
                'docs', 'documentation', 'readme', 'api-docs',
                'changelog', 'guide', 'tutorial', 'reference',
                'markdown', 'swagger', 'openapi', 'technical-writing'
            ],
            'tools': ['markdown', 'mkdocs', 'docusaurus']
        },
        'Testing': {
            'keywords': [
                'test', 'testing', 'e2e', 'unit', 'integration',
                'coverage', 'pytest', 'jest', 'vitest', 'playwright',
                'cypress', 'qa', 'quality', 'regression'
            ],
            'tools': ['pytest', 'jest', 'playwright', 'vitest']
        }
    }

    COMPLEXITY_INDICATORS = {
        'simple': ['simple', 'basic', 'quick', 'minimal', 'small'],
        'standard': ['standard', 'normal', 'typical', 'regular'],
        'complex': ['complex', 'advanced', 'comprehensive', 'full', 'complete', 'enterprise']
    }

    def detect(self, request: str) -> DomainResult:
        """
        Detect domain and complexity from user request

        Args:
            request: User's workflow creation request

        Returns:
            DomainResult with detected domain, confidence, and metadata
        """

        request_lower = request.lower()

        # Detect domain
        domain_scores = {}
        domain_keywords = {}

        for domain, config in self.DOMAINS.items():
            matches = [kw for kw in config['keywords'] if kw in request_lower]
            score = len(matches) / len(config['keywords'])  # Normalized score
            domain_scores[domain] = score
            domain_keywords[domain] = matches

        # Get best match
        if domain_scores and max(domain_scores.values()) > 0:
            detected_domain = max(domain_scores, key=domain_scores.get)
            confidence = domain_scores[detected_domain]
            keywords = domain_keywords[detected_domain]
            tools = self.DOMAINS[detected_domain]['tools']
        else:
            detected_domain = 'General'
            confidence = 1.0
            keywords = []
            tools = []

        # Detect complexity
        complexity = 3  # Default standard

        for level, indicators in self.COMPLEXITY_INDICATORS.items():
            if any(ind in request_lower for ind in indicators):
                if level == 'simple':
                    complexity = 2
                elif level == 'complex':
                    complexity = 5
                break

        # Adjust complexity based on request length
        if len(request.split()) > 50:
            complexity = min(complexity + 1, 5)

        return DomainResult(
            domain=detected_domain,
            confidence=confidence,
            complexity=complexity,
            keywords_matched=keywords,
            suggested_tools=tools
        )

    def suggest_mcp_servers(self, domain: str) -> List[Dict[str, str]]:
        """Suggest relevant MCP servers for domain"""

        mcp_suggestions = {
            'DevOps': [
                {'name': 'github', 'package': '@modelcontextprotocol/server-github'},
                {'name': 'gitlab', 'package': '@modelcontextprotocol/server-gitlab'}
            ],
            'Security': [
                {'name': 'github', 'package': '@modelcontextprotocol/server-github'},  # For vuln scanning
            ],
            'DataOps': [
                {'name': 'postgres', 'package': '@modelcontextprotocol/server-postgres'},
                {'name': 'sqlite', 'package': '@modelcontextprotocol/server-sqlite'}
            ],
            'Documentation': [
                {'name': 'filesystem', 'package': '@modelcontextprotocol/server-filesystem'}
            ],
            'Testing': [
                {'name': 'playwright', 'package': '@modelcontextprotocol/server-playwright'}
            ]
        }

        return mcp_suggestions.get(domain, [])

    def get_domain_templates(self, domain: str) -> Dict[str, str]:
        """Get template file paths for domain"""

        return {
            'skill_template': f'templates/{domain.lower()}_skill.md',
            'script_template': f'templates/{domain.lower()}_script.py',
            'hooks_template': f'templates/{domain.lower()}_hooks.json'
        }


if __name__ == '__main__':
    # Example usage
    detector = DomainDetector()

    test_requests = [
        "Create a CI/CD pipeline for deploying to Kubernetes",
        "Build a security scanner for OWASP vulnerabilities",
        "Create a React component library with Tailwind CSS",
        "Set up an ETL pipeline for BigQuery data warehouse",
        "Generate API documentation with OpenAPI specs",
        "Create e2e testing workflow with Playwright"
    ]

    print("=" * 70)
    print("DOMAIN DETECTION RESULTS")
    print("=" * 70)

    for request in test_requests:
        result = detector.detect(request)

        print(f"\nRequest: {request}")
        print(f"Domain: {result.domain} (confidence: {result.confidence:.2f})")
        print(f"Complexity: {result.complexity}/5")
        print(f"Keywords: {', '.join(result.keywords_matched[:5])}")
        print(f"Suggested Tools: {', '.join(result.suggested_tools)}")

        mcp = detector.suggest_mcp_servers(result.domain)
        if mcp:
            print(f"MCP Servers: {', '.join(s['name'] for s in mcp)}")
