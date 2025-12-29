# EARS Format Reference

## Easy Approach to Requirements Syntax

EARS provides structured patterns for writing unambiguous requirements.

## Patterns

### 1. Ubiquitous Requirements (Always True)

```
The {system} SHALL {response}
```

**Example:** The system SHALL encrypt all stored passwords using bcrypt.

### 2. Event-Driven Requirements

```
WHEN {event} THEN {system} SHALL {response}
```

**Example:** WHEN a user submits the login form THEN the system SHALL validate credentials within 2 seconds.

### 3. Conditional Requirements

```
IF {precondition} THEN {system} SHALL {response}
```

**Example:** IF the user is authenticated THEN the system SHALL display the dashboard.

### 4. State-Driven Requirements

```
WHILE {state} THEN {system} SHALL {response}
```

**Example:** WHILE the session is active THEN the system SHALL refresh the auth token every 15 minutes.

### 5. Optional Feature Requirements

```
WHERE {feature} THEN {system} SHALL {response}
```

**Example:** WHERE two-factor authentication is enabled THEN the system SHALL require OTP verification.

### 6. Complex Requirements

```
WHEN {event} AND {condition} THEN {system} SHALL {response}
```

**Example:** WHEN a payment is submitted AND the amount exceeds $1000 THEN the system SHALL require additional verification.

## Best Practices

| Practice                      | Description                       |
| ----------------------------- | --------------------------------- |
| One requirement per statement | Avoid compound requirements       |
| Use active voice              | "System SHALL" not "It should be" |
| Avoid ambiguous terms         | Not "quickly", but "within 200ms" |
| Include measurable criteria   | Specific numbers, thresholds      |
| Reference data models         | Link to defined entities          |

## Template

```markdown
### FR-{N}: {Requirement Name}

- **EARS Format**: {PATTERN} {content}
- **Priority**: High / Medium / Low
- **Source**: User request / Implicit / Research
- **Acceptance Criteria**:
  - [ ] Criterion 1
  - [ ] Criterion 2
```
