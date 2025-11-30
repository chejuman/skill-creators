---
name: iterm-control
description: Control iTerm terminal instances via AppleScript for macOS. Use when managing multiple terminal sessions, running parallel dev servers (frontend/backend), monitoring command outputs, or automating iTerm window/tab operations. Enables opening terminals, executing commands, reading output, and coordinating multiple simultaneous processes.
---

# iTerm Control

Control iTerm terminal instances programmatically via AppleScript on macOS.

## Overview

This skill provides utilities to automate iTerm terminal operations through AppleScript. Use it to manage multiple terminal sessions, run commands in parallel, monitor outputs, and coordinate complex development workflows that require multiple simultaneous processes.

**Platform:** macOS only (requires iTerm and AppleScript)

## When to Use This Skill

Trigger this skill when:
- Running multiple development servers simultaneously (frontend + backend + database)
- Monitoring command outputs from long-running processes
- Automating terminal workflows that require multiple tabs or windows
- Coordinating parallel processes in separate terminal sessions
- Setting up development environments with predefined command sequences

## Quick Start

### Basic Terminal Control

Open a terminal and execute a command:

```javascript
import { openTerminal, executeCommand } from './scripts/iterm_control.js';

// Open new terminal tab
await openTerminal("Dev server starting");

// Execute command in current session
await executeCommand("npm run dev");
```

### CLI Usage

Use the scripts directly from command line:

```bash
# Open new terminal
node scripts/iterm_control.js open "Ready for development"

# Execute command
node scripts/iterm_control.js execute "npm install"

# Read session output
node scripts/iterm_control.js read

# Close current window
node scripts/iterm_control.js close
```

## Core Operations

### Opening Terminals

Create new terminal tabs or windows with optional initialization messages:

```javascript
await openTerminal("Backend server");
await executeCommand("cd backend && npm run dev");
```

**CLI:**
```bash
node scripts/iterm_control.js open "Starting service"
```

### Executing Commands

Run commands in the current iTerm session. Commands are automatically escaped for AppleScript compatibility:

```javascript
await executeCommand("npm run test");
await executeCommand("docker-compose up -d");
```

**CLI:**
```bash
node scripts/iterm_control.js execute "git status"
```

### Managing Multiple Terminals

Use `multi_terminal.js` to create coordinated terminal sessions:

**From Config File:**

Create `dev-config.json`:
```json
{
  "terminals": [
    {"name": "Frontend", "command": "cd frontend && npm run dev"},
    {"name": "Backend", "command": "cd backend && npm run dev"},
    {"name": "Logs", "command": "tail -f logs/app.log"}
  ]
}
```

Run:
```bash
node scripts/multi_terminal.js start dev-config.json
```

**Quick Commands:**
```bash
node scripts/multi_terminal.js run "npm run dev" "npm run test:watch" "tail -f app.log"
```

This creates a new iTerm window with multiple tabs, each running a different command.

### Reading Session Output

Retrieve text from the current terminal session:

```javascript
const output = await getSessionText();
console.log(output);
```

**CLI:**
```bash
node scripts/iterm_control.js read
```

## Available Scripts

### `iterm_control.js`
Core iTerm automation utilities.

**Functions:**
- `openTerminal(message)` - Open new terminal tab
- `executeCommand(command)` - Execute command in current session
- `closeTerminal()` - Close current window
- `getSessionText()` - Read session output
- `executeITermScript(script)` - Execute custom AppleScript

**CLI Commands:**
- `open [message]` - Open terminal
- `execute <command>` - Run command
- `read` - Get session text
- `close` - Close window

### `multi_terminal.js`
Manage multiple terminal sessions simultaneously.

**Functions:**
- `createMultiTerminalWindow(terminals)` - Create window with multiple tabs
- `runCommandsInTabs(commands)` - Quick parallel command execution

**CLI Commands:**
- `start <config.json>` - Load terminals from config
- `run <cmd1> <cmd2> ...` - Run commands in parallel tabs

### `example-config.json`
Template configuration showing multi-terminal setup structure.

## Common Workflows

### Parallel Development Servers

Start frontend, backend, and database simultaneously:

```bash
node scripts/multi_terminal.js run \
  "cd frontend && npm run dev" \
  "cd backend && npm run dev" \
  "docker-compose up postgres"
```

### Development Environment Setup

Create config for your project:

```json
{
  "terminals": [
    {"name": "API", "command": "cd api && npm run dev"},
    {"name": "Web", "command": "cd web && npm start"},
    {"name": "Tests", "command": "npm run test:watch"},
    {"name": "Logs", "command": "tail -f logs/combined.log"}
  ]
}
```

Save as `dev-setup.json` and run:
```bash
node scripts/multi_terminal.js start dev-setup.json
```

### Monitoring and Automation

Programmatically control terminals for complex workflows:

```javascript
import { openTerminal, executeCommand, getSessionText } from './scripts/iterm_control.js';

// Start build process
await openTerminal("Build monitor");
await executeCommand("npm run build");

// Wait and check output
await new Promise(resolve => setTimeout(resolve, 5000));
const output = await getSessionText();

if (output.includes("Build successful")) {
  console.log("✅ Build completed successfully");
}
```

### Custom AppleScript Integration

Execute custom AppleScript for advanced control:

```javascript
import { executeITermScript } from './scripts/iterm_control.js';

const customScript = `
tell application "iTerm"
  tell current session of current window
    set name to "Custom Session"
    write text "echo 'Custom automation'"
  end tell
end tell
`;

await executeITermScript(customScript);
```

## Technical Notes

**AppleScript Compatibility:**
- Scripts automatically replace `iTerm2` references with `iTerm` for compatibility
- Commands are escaped to handle quotes and special characters
- Brief delays are included for iTerm activation and command execution

**Platform Requirements:**
- macOS only
- iTerm must be installed
- AppleScript must be enabled

**Error Handling:**
- All operations include try-catch blocks
- Errors are logged with descriptive messages
- CLI commands exit with appropriate status codes

**Process Management:**
- Each script execution is independent
- No persistent state between CLI invocations
- For state management, use as Node.js module

## Extending the Skill

Add custom iTerm operations by creating new scripts in `scripts/` or extending existing utilities. All functions use the base `executeITermScript()` for AppleScript execution, making it easy to add new automation capabilities.

Example custom operation:

```javascript
async function splitPaneVertically() {
  const script = `
  tell application "iTerm"
    tell current session of current window
      split vertically with default profile
    end tell
  end tell
  `;
  await executeITermScript(script);
}
```
