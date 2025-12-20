---
name: iterm-control
description: Advanced iTerm terminal automation for macOS. Use when managing multiple terminal sessions, running parallel dev servers, monitoring processes, auto-restarting failed services, or coordinating complex development workflows. Supports session ID tracking, state persistence, process monitoring, and comprehensive terminal control via AppleScript.
---

# iTerm Control v2.0

Comprehensive iTerm terminal automation with session management, process monitoring, and advanced control.

## Overview

This skill provides complete iTerm automation through three integrated scripts:
- **iterm_control.js** - Core terminal operations (open, execute, split, focus)
- **session_manager.js** - ID-based session tracking with persistence
- **process_monitor.js** - Health monitoring and auto-restart

**Platform:** macOS only (requires iTerm)

## Quick Start

### Basic Terminal Control

```bash
# Open terminal and run command
node scripts/iterm_control.js open "Dev Server"
node scripts/iterm_control.js execute "npm run dev"

# Split panes for multi-service setup
node scripts/iterm_control.js split-v "npm run test:watch"
```

### Session Management

```bash
# Create tracked session
node scripts/session_manager.js create "Backend" --group dev --command "npm run dev"
node scripts/session_manager.js create "Frontend" --group dev --command "npm start"

# List and manage sessions
node scripts/session_manager.js list --group dev
node scripts/session_manager.js execute <sessionId> "git pull"
```

### Process Monitoring

```bash
# Check session health
node scripts/process_monitor.js status

# Watch with auto-restart
node scripts/process_monitor.js watch <sessionId> --restart
```

## Core Scripts

### iterm_control.js (v2.0)

Basic and advanced terminal operations.

| Command | Description |
|---------|-------------|
| `open [message]` | Open new terminal tab |
| `execute <command>` | Execute command in current session |
| `read` | Read entire session output |
| `lines [num]` | Read last N lines (default: 50) |
| `close` | Close current window |
| `window [title]` | Create new window |
| `split-h [command]` | Split horizontally (left/right) |
| `split-v [command]` | Split vertically (top/bottom) |
| `list` | List all sessions |
| `focus <name>` | Focus session by name |
| `name <name>` | Set current session name |
| `send-keys <keys>` | Send keys (ctrl+c, enter, etc.) |

**Examples:**
```bash
node scripts/iterm_control.js window "Development"
node scripts/iterm_control.js execute "cd ~/project && npm run dev"
node scripts/iterm_control.js split-v "npm run test:watch"
node scripts/iterm_control.js send-keys ctrl+c
node scripts/iterm_control.js focus "Backend"
```

### session_manager.js

ID-based session tracking with persistence and grouping.

| Command | Description |
|---------|-------------|
| `create <name> [--group <g>] [--command <c>]` | Create named session |
| `list [--group <group>]` | List all sessions |
| `get <sessionId>` | Get session info |
| `execute <sessionId> <command>` | Execute in specific session |
| `read <sessionId> [--lines <num>]` | Read session output |
| `close <sessionId>` | Close session |
| `save <filepath>` | Save state to file |
| `restore <filepath>` | Restore state from file |
| `group-start <group>` | Start all sessions in group |
| `group-stop <group>` | Stop all sessions in group |

**Session Registry:**
Sessions are stored in `~/.iterm-sessions/sessions.json` with:
- Unique session ID
- Name and group
- Associated command
- Creation timestamp
- Current status

**Examples:**
```bash
# Create dev environment
node scripts/session_manager.js create "API" --group backend --command "cd api && npm run dev"
node scripts/session_manager.js create "Web" --group frontend --command "cd web && npm start"
node scripts/session_manager.js create "DB" --group backend --command "docker-compose up postgres"

# Manage groups
node scripts/session_manager.js group-stop backend
node scripts/session_manager.js group-start backend

# Save/restore state
node scripts/session_manager.js save ~/dev-state.json
node scripts/session_manager.js restore ~/dev-state.json
```

### process_monitor.js

Health monitoring, failure detection, and auto-restart.

| Command | Description |
|---------|-------------|
| `status` | Show all session status |
| `check <sessionId>` | Check specific session health |
| `watch <sessionId> [--restart] [--interval <ms>]` | Continuous monitoring |
| `restart <sessionId>` | Restart session command |
| `logs <sessionId> [--lines <num>] [--output <file>]` | Collect logs |
| `collect-all [--output <dir>]` | Collect all session logs |

**Health Detection:**
- Detects running status (listening, ready, compiled)
- Detects errors (ECONNREFUSED, EADDRINUSE, npm ERR!)
- Auto-restart on failure (up to 3 attempts)

**Examples:**
```bash
# Check all sessions
node scripts/process_monitor.js status

# Watch with auto-restart
node scripts/process_monitor.js watch <sessionId> --restart --interval 10000

# Collect logs
node scripts/process_monitor.js collect-all --output ~/logs/
```

### multi_terminal.js

Quick multi-terminal setup from config.

**Config File:**
```json
{
  "terminals": [
    {"name": "Frontend", "command": "cd frontend && npm run dev"},
    {"name": "Backend", "command": "cd backend && npm run dev"},
    {"name": "Logs", "command": "tail -f logs/app.log"}
  ]
}
```

**Usage:**
```bash
node scripts/multi_terminal.js start dev-config.json
node scripts/multi_terminal.js run "npm run dev" "npm run test:watch"
```

## Common Workflows

### Full-Stack Development Setup

```bash
# Create development workspace
node scripts/iterm_control.js window "Full-Stack Dev"

# Set up services with session tracking
node scripts/session_manager.js create "API" --group fullstack --command "cd api && npm run dev"
node scripts/session_manager.js create "Web" --group fullstack --command "cd web && npm start"
node scripts/session_manager.js create "DB" --group fullstack --command "docker-compose up -d"

# Monitor all services
node scripts/process_monitor.js status
```

### Microservices Environment

```bash
# Start all microservices from config
node scripts/multi_terminal.js start microservices.json

# Or create individually with groups
node scripts/session_manager.js create "Auth" --group services --command "cd auth && npm run dev"
node scripts/session_manager.js create "Users" --group services --command "cd users && npm run dev"
node scripts/session_manager.js create "Orders" --group services --command "cd orders && npm run dev"

# Save state for later
node scripts/session_manager.js save ~/.iterm-sessions/microservices.json
```

### Automated Testing Workflow

```bash
# Set up test environment
node scripts/iterm_control.js window "Testing"
node scripts/session_manager.js create "Tests" --group testing --command "npm run test:watch"
node scripts/session_manager.js create "E2E" --group testing --command "npm run e2e"

# Watch for failures and auto-restart
node scripts/process_monitor.js watch <testSessionId> --restart
```

### Build and Deploy

```bash
# Execute build in tracked session
node scripts/session_manager.js execute <sessionId> "npm run build"

# Wait and check output
sleep 30
node scripts/process_monitor.js check <sessionId>

# Collect build logs
node scripts/process_monitor.js logs <sessionId> --output build.log
```

## Technical Notes

**AppleScript Compatibility:**
- All scripts handle iTerm/iTerm2 naming differences
- Commands are escaped for safe AppleScript execution
- Heredoc syntax prevents quote escaping issues

**Session Persistence:**
- Sessions stored in `~/.iterm-sessions/sessions.json`
- Logs stored in `~/.iterm-sessions/logs/`
- State can be saved/restored across sessions

**Error Detection Patterns:**
- Running: `listening on`, `ready`, `compiled successfully`
- Errors: `ECONNREFUSED`, `EADDRINUSE`, `npm ERR!`, `error:`

**Keyboard Input:**
- Supports: `ctrl+c`, `ctrl+d`, `ctrl+z`, `enter`, `escape`, `tab`
- Custom keystrokes via AppleScript

## Sources

- [iTerm2 Scripting Documentation](https://iterm2.com/documentation-scripting.html)
- [iTerm2 Python API](https://iterm2.com/python-api/)
- [PM2 Process Manager](https://pm2.keymetrics.io/)
