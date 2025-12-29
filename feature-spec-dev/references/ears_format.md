# EARS Format Reference

Easy Approach to Requirements Syntax for unambiguous requirements.

## Core Patterns

### 1. Ubiquitous (Always Active)

```
The [system] SHALL [action]
```

**Example:**

```
The authentication service SHALL encrypt all passwords using bcrypt.
```

### 2. Event-Driven (Triggered by Event)

```
WHEN [event] THEN [system] SHALL [response]
```

**Example:**

```
WHEN user submits login form THEN authentication service SHALL validate credentials within 200ms.
```

### 3. State-Driven (While in State)

```
WHILE [state] THEN [system] SHALL [behavior]
```

**Example:**

```
WHILE user session is active THEN system SHALL refresh token every 15 minutes.
```

### 4. Unwanted (Exception Handling)

```
IF [precondition] THEN [system] SHALL [response]
```

**Example:**

```
IF login fails 3 consecutive times THEN system SHALL lock account for 15 minutes.
```

### 5. Optional (Feature Flags)

```
WHERE [feature is enabled] [system] SHALL [behavior]
```

**Example:**

```
WHERE 2FA is enabled system SHALL require OTP after password validation.
```

### 6. Complex (Combined)

```
WHILE [state] WHEN [event] IF [precondition] THEN [system] SHALL [response]
```

**Example:**

```
WHILE user is authenticated WHEN session timeout occurs IF user has unsaved changes THEN system SHALL prompt to save before logout.
```

## Keywords

| Keyword   | Meaning                          |
| --------- | -------------------------------- |
| SHALL     | Mandatory requirement            |
| SHOULD    | Recommended but not mandatory    |
| MAY       | Optional capability              |
| WILL      | Statement of fact (not testable) |
| SHALL NOT | Prohibited behavior              |

## Quality Checklist

- [ ] Single requirement per statement
- [ ] Measurable and testable
- [ ] No ambiguous terms (avoid "fast", "user-friendly")
- [ ] Complete with all conditions specified
- [ ] Consistent terminology throughout

## Requirement Hierarchy

```
REQ-1.0 Feature Name
├── REQ-1.1 Functional Requirement
│   ├── REQ-1.1.1 Sub-requirement
│   └── REQ-1.1.2 Sub-requirement
├── REQ-1.2 Non-Functional Requirement
└── REQ-1.3 Constraint
```

## User Story Integration

```
As a [role], I want [feature], so that [benefit].

Acceptance Criteria:
- WHEN [action] THEN system SHALL [response]
- IF [condition] THEN system SHALL [behavior]
```
