# Quality Gate Criteria

## Gate 1: research_complete

**Phase**: After hierarchical research

**Required Checks**:

- [ ] Tech stack research document exists
- [ ] Market trends research document exists
- [ ] Open source research document exists
- [ ] Security research document exists
- [ ] Competitor research document exists

**Optional Checks**:

- [ ] Research synthesis document exists
- [ ] Source credibility scores recorded

**Pass Threshold**: 80% (all required + some optional)

**Failure Actions**:

1. Identify missing research areas
2. Run focused `/devflow2-research --focus <area>`
3. Retry gate

---

## Gate 2: analysis_complete

**Phase**: After multi-perspective analysis

**Required Checks**:

- [ ] User perspective analysis complete
- [ ] Technical perspective analysis complete
- [ ] Business perspective analysis complete
- [ ] Risk perspective analysis complete
- [ ] Feasibility score calculated

**Optional Checks**:

- [ ] Risk matrix generated
- [ ] Go/No-Go recommendation provided

**Pass Threshold**: 100% required

**Failure Actions**:

1. Run missing perspective analysis
2. Calculate feasibility if missing
3. Retry gate

---

## Gate 3: plan_validated

**Phase**: After development planning

**Required Checks**:

- [ ] Features selected from backlog
- [ ] Tasks generated (5-10 per feature)
- [ ] Dependencies mapped
- [ ] Effort estimates provided

**Optional Checks**:

- [ ] Risk mitigation strategies defined
- [ ] Critical path identified
- [ ] Predictions calculated

**Pass Threshold**: 80%

**Failure Actions**:

1. Select features if backlog empty
2. Generate task breakdown
3. Add effort estimates
4. Retry gate

---

## Gate 4: version_ready

**Phase**: Before version advancement

**Required Checks**:

- [ ] All previous gates passed

**Optional Checks**:

- [ ] Retrospective completed
- [ ] Knowledge base updated
- [ ] Velocity recorded

**Pass Threshold**: 60%

**Failure Actions**:

1. Complete any failed gates
2. Run retrospective
3. Update knowledge
4. Retry gate

---

## Quality Metrics

### Pass Rate Calculation

```
Pass Rate = (Passed Checks / Total Checks) × 100
```

### Gate Score

```
Gate Score = (Required Pass × 0.7) + (Optional Pass × 0.3)
```

### Overall Workflow Quality

```
Quality = Average(All Gate Scores)
```

## Failure Handling

### Soft Failure

- Optional checks missing
- Pass rate slightly below threshold
- Action: Proceed with warning

### Hard Failure

- Required checks missing
- Pass rate significantly below threshold
- Action: Block progression, require fixes

### Override

- `/devflow2-gate <name> --force`
- Logs override reason
- Reduces confidence scores
