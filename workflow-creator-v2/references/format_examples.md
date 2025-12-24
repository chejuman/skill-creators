# Workflow Format Examples

Complete examples for each output format.

## Skill Example

**Location:** `~/.claude/skills/code-formatter/SKILL.md`

```yaml
---
name: code-formatter
description: Format code files using project-specific formatters. Use when user asks to format code, clean up files, or apply code style. Supports Prettier, ESLint, Black, and rustfmt.
---

# Code Formatter

Format code files using detected project formatters.

## Workflow

1. Detect project type and available formatters
2. Identify files to format (from user request or git status)
3. Run appropriate formatter
4. Report results

## Formatter Detection

Check for configuration files:
- `package.json` with prettier/eslint → npm run format
- `pyproject.toml` with black → black .
- `Cargo.toml` → cargo fmt
- `.prettierrc` → npx prettier --write
```

## Slash Command Example

**Location:** `~/.claude/commands/deploy.md`

```yaml
---
allowed-tools: Bash(kubectl:*), Bash(docker:*), Read
argument-hint: [environment] [version]
description: Deploy application to Kubernetes
---

Deploy to $1 environment with version $2.

## Context
- Current cluster: !`kubectl config current-context`
- Available namespaces: !`kubectl get namespaces -o name`

## Deployment Steps

1. Build Docker image with tag $2
2. Push to registry
3. Update Kubernetes manifests
4. Apply to $1 namespace
5. Monitor rollout status
6. Rollback on failure

## Verification
After deployment, verify:
- Pods are running: `kubectl get pods -n $1`
- Service is accessible: `kubectl get svc -n $1`
```

## Subagent Example

**Location:** `~/.claude/agents/security-auditor.md`

```yaml
---
name: security-auditor
description: Expert security auditor for code and infrastructure. Use when reviewing security, scanning for vulnerabilities, or checking compliance.
tools: Read, Grep, Glob, Bash
model: sonnet
---

You are an expert security auditor with deep knowledge of:
- OWASP Top 10 vulnerabilities
- CWE common weaknesses
- Security best practices
- Compliance frameworks (SOC2, PCI-DSS, HIPAA)

## Audit Approach

1. **Threat Modeling**: Identify attack surfaces
2. **Code Review**: Look for security anti-patterns
3. **Dependency Scan**: Check for vulnerable packages
4. **Configuration Audit**: Review security settings
5. **Compliance Check**: Verify against framework requirements

## Common Vulnerabilities to Check

- SQL Injection
- XSS (Cross-Site Scripting)
- CSRF (Cross-Site Request Forgery)
- Authentication bypasses
- Authorization flaws
- Sensitive data exposure
- Insecure dependencies

## Reporting

Provide findings with:
- Severity: Critical/High/Medium/Low
- Location: File and line number
- Description: What the vulnerability is
- Impact: What an attacker could do
- Remediation: How to fix it
```

## Hook Example

**Location:** `.claude/settings.json`

```json
{
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Write|Edit",
        "hooks": [
          {
            "type": "command",
            "command": "npx prettier --write \"$TOOL_INPUT_FILE_PATH\"",
            "timeout": 30
          }
        ]
      }
    ],
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 ~/.claude/hooks/validate_command.py"
          }
        ]
      }
    ],
    "UserPromptSubmit": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/add_context.sh"
          }
        ]
      }
    ],
    "SessionStart": [
      {
        "hooks": [
          {
            "type": "command",
            "command": "bash ~/.claude/hooks/session_setup.sh"
          }
        ]
      }
    ]
  }
}
```

## Composite Workflow Example

A complete automation system combining multiple formats.

### Directory Structure

```
deployment-automation/
├── skills/
│   └── deploy-manager/
│       ├── SKILL.md
│       ├── scripts/
│       │   ├── deploy.py
│       │   ├── rollback.py
│       │   └── validate.py
│       └── references/
│           └── environments.md
├── commands/
│   ├── deploy.md
│   ├── rollback.md
│   └── status.md
├── agents/
│   └── deploy-reviewer.md
└── hooks/
    └── hooks.json
```

### 1. Main Skill (deploy-manager/SKILL.md)

```yaml
---
name: deploy-manager
description: Orchestrate deployments with validation and rollback. Use when deploying applications, managing releases, or troubleshooting deployments.
---

# Deployment Manager

Orchestrate deployments across environments.

## Workflow

1. Validate deployment request
2. Run pre-flight checks
3. Execute deployment
4. Monitor rollout
5. Rollback on failure

## Commands

- `/deploy [env] [version]` - Deploy to environment
- `/rollback [env]` - Rollback last deployment
- `/status [env]` - Check deployment status

## Scripts

- [deploy.py](scripts/deploy.py) - Deployment orchestration
- [rollback.py](scripts/rollback.py) - Automated rollback
- [validate.py](scripts/validate.py) - Pre-flight validation
```

### 2. Quick Command (commands/deploy.md)

```yaml
---
allowed-tools: Bash(kubectl:*), Bash(docker:*)
argument-hint: [environment] [version]
description: Quick deploy to environment
---

Quick deploy version $2 to $1.

## Pre-checks
!`kubectl cluster-info`

## Deploy
Use the deploy-manager skill to orchestrate deployment.
```

### 3. Review Agent (agents/deploy-reviewer.md)

```yaml
---
name: deploy-reviewer
description: Review deployment plans before execution
tools: Read, Grep
model: haiku
---

Review deployment plan for:
- Configuration correctness
- Resource requirements
- Potential risks
- Rollback strategy

Provide approval or concerns.
```

### 4. Automation Hooks (hooks/hooks.json)

```json
{
  "PostToolUse": [
    {
      "matcher": "Bash.*kubectl apply",
      "hooks": [
        {
          "type": "command",
          "command": "python3 ~/.claude/skills/deploy-manager/scripts/log_deployment.py"
        }
      ]
    }
  ]
}
```

## Installation Commands

### Skill Installation

```bash
# Package and install skill
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py ./deploy-manager .
unzip -o deploy-manager.zip -d ~/.claude/skills/
chmod +x ~/.claude/skills/deploy-manager/scripts/*.py
```

### Command Installation

```bash
# Install commands
cp ./commands/*.md ~/.claude/commands/
```

### Agent Installation

```bash
# Install agents
cp ./agents/*.md ~/.claude/agents/
```

### Hook Integration

```bash
# Merge hooks into existing settings
# Manual merge required for hooks.json
jq -s '.[0] * .[1]' ~/.claude/settings.json ./hooks/hooks.json > /tmp/merged.json
mv /tmp/merged.json ~/.claude/settings.json
```
