# /devflow-roadmap

Show full roadmap from current version to v10.0+.

## Usage

```
/devflow-roadmap [--export <format>]
```

## Options

- `--export <format>`: Export roadmap (md, json, html)

## What This Does

### Step 1: Load Project History

Load all version files and feature backlog from `.devflow/`.

### Step 2: Analyze Completed Versions

Summarize features delivered in each completed version.

### Step 3: Project Future Versions

Based on:

- Backlog features
- RICE scores
- MoSCoW priorities
- Research insights

### Step 4: Generate Roadmap

```markdown
# Roadmap to v10.0

## Completed

### v0.0 - Idea Stage ✓

- Initial concept captured
- Domain identified

### v1.0 - MVP ✓

- Core authentication
- Basic dashboard
- Essential API

## In Progress

### v2.0 - Stability (Current)

- [ ] Enhanced error handling
- [ ] Performance optimization
- [ ] User feedback integration

## Planned

### v3.0 - Growth

- Advanced integrations
- Mobile support
- Analytics dashboard

### v4.0 - Expansion

- Multi-tenant support
- Enterprise features
- API marketplace

### v5.0 - Maturity

- Full feature parity
- Comprehensive docs
- Community edition

### v6.0 - Optimization

- Performance at scale
- Cost optimization
- Global deployment

### v7.0 - Enterprise

- SSO/SAML
- Audit logging
- Compliance (SOC2, GDPR)

### v8.0 - Intelligence

- AI-powered features
- Predictive analytics
- Smart automation

### v9.0 - Platform

- Plugin ecosystem
- Custom workflows
- White-label options

### v10.0 - Excellence

- Industry leadership
- Complete ecosystem
- Self-sustaining growth

## Feature Backlog by Priority

### Must Have (Next 2 versions)

| Feature   | Target | RICE |
| --------- | ------ | ---- |
| Feature A | v2.0   | 150  |
| Feature B | v3.0   | 140  |

### Should Have (v4-5)

| Feature   | Target | RICE |
| --------- | ------ | ---- |
| Feature C | v4.0   | 100  |

### Could Have (v6+)

| Feature   | Target | RICE |
| --------- | ------ | ---- |
| Feature D | v6.0   | 60   |

## Timeline Projection

Based on current velocity:

- v3.0: +2 months
- v5.0: +6 months
- v7.0: +12 months
- v10.0: +18-24 months

## Risk Factors

1. [Risk] - May impact [versions]
2. [Risk] - May impact [versions]
```

### Step 5: Save Roadmap

Save to `.devflow/features/roadmap.md`.

## Example

```
User: /devflow-roadmap

User: /devflow-roadmap --export md
```
