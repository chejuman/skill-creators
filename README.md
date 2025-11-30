# iTerm Control Skill

A Claude Code skill for controlling iTerm terminal instances via AppleScript on macOS. Automate terminal operations, manage multiple development servers, and coordinate complex workflows.

## Features

- 🖥️ **Terminal Control** - Open, close, and manage iTerm windows/tabs
- ⚡ **Command Execution** - Run commands in specific terminal sessions
- 📊 **Output Monitoring** - Read and analyze terminal output
- 📁 **Efficient File Writing** - Create files with iTerm feedback (no escaping issues)
- 🔄 **Multi-Terminal Management** - Coordinate multiple terminals simultaneously
- 🎯 **Parallel Workflows** - Run frontend, backend, database, and logs in parallel
- 📝 **Configuration-Based** - Define terminal setups with JSON configs

## Installation

### Quick Install

```bash
# Extract the skill to Claude Code skills directory
unzip iterm-control.zip -d ~/.claude/skills/
```

### Manual Install

```bash
# Create skills directory if it doesn't exist
mkdir -p ~/.claude/skills/

# Copy the skill
cp -r iterm-control ~/.claude/skills/
```

## Requirements

- **Platform:** macOS only
- **Terminal:** iTerm (https://iterm2.com/)
- **Runtime:** Node.js (for scripts)
- **Permissions:** AppleScript must be enabled

## Usage

### Claude Code Integration

Once installed, Claude Code will automatically use this skill when you ask for:

- "Open multiple terminals for my dev servers"
- "Run frontend and backend simultaneously in iTerm"
- "Start my development environment with terminals"
- "Execute this command in a new iTerm window"

### Direct Script Usage

#### Basic Terminal Control

```bash
# Navigate to scripts directory
cd ~/.claude/skills/iterm-control/scripts

# Open new terminal
node iterm_control.js open "Dev server ready"

# Execute command
node iterm_control.js execute "npm run dev"

# Read terminal output
node iterm_control.js read

# Close terminal
node iterm_control.js close
```

#### Efficient File Writing

Write files with automatic iTerm feedback (much faster than heredoc):

```bash
# Simple content
node iterm_control.js write memo.txt "Quick note here"

# Large content via stdin (recommended for big files)
cat << 'EOF' | node iterm_control.js write report.txt --stdin
# System Analysis Report

Generated: 2025-11-30

... large content with special characters ...
no escaping issues!
EOF

# Pipe command output to file
fastfetch | node iterm_control.js write system-info.txt --stdin
```

**Benefits:**
- ⚡ Much faster than heredoc/echo methods
- ✅ No shell escaping issues
- ✅ Works with any file size
- ✅ iTerm shows file creation notification and preview

#### Multi-Terminal Management

**Quick parallel commands:**
```bash
cd ~/.claude/skills/iterm-control/scripts

node multi_terminal.js run \
  "cd frontend && npm run dev" \
  "cd backend && npm run dev" \
  "docker-compose up -d"
```

**Using configuration file:**

Create `my-dev-setup.json`:
```json
{
  "terminals": [
    {
      "name": "Frontend",
      "command": "cd ~/projects/myapp/frontend && npm run dev"
    },
    {
      "name": "Backend",
      "command": "cd ~/projects/myapp/backend && npm run dev"
    },
    {
      "name": "Database",
      "command": "docker-compose up postgres redis"
    },
    {
      "name": "Logs",
      "command": "tail -f ~/projects/myapp/logs/app.log"
    }
  ]
}
```

Run:
```bash
node multi_terminal.js start my-dev-setup.json
```

## Use Cases

### Parallel Development Servers

Run multiple development servers simultaneously:

```bash
node multi_terminal.js run \
  "cd web && npm start" \
  "cd api && npm run dev" \
  "npm run test:watch"
```

### Full-Stack Development Environment

Create a comprehensive development setup:

```json
{
  "terminals": [
    {"name": "React App", "command": "cd client && npm start"},
    {"name": "Node API", "command": "cd server && npm run dev"},
    {"name": "MongoDB", "command": "mongod --dbpath ./data"},
    {"name": "Redis", "command": "redis-server"},
    {"name": "Test Runner", "command": "npm run test:watch"},
    {"name": "Build Monitor", "command": "npm run build:watch"}
  ]
}
```

### Monitoring and Logging

Set up monitoring terminals:

```bash
node multi_terminal.js run \
  "tail -f logs/access.log" \
  "tail -f logs/error.log" \
  "htop" \
  "watch -n 1 'docker ps'"
```

## Script Reference

### `iterm_control.js`

Core iTerm automation utilities.

**Commands:**
- `open [message]` - Open new terminal tab with optional message
- `execute <command>` - Execute command in current session
- `read` - Read current terminal output
- `close` - Close current terminal window

**Programmatic Usage:**
```javascript
import { openTerminal, executeCommand, getSessionText } from './iterm_control.js';

await openTerminal("Starting build");
await executeCommand("npm run build");
const output = await getSessionText();
```

### `multi_terminal.js`

Manage multiple terminal sessions.

**Commands:**
- `start <config.json>` - Load terminals from configuration file
- `run <cmd1> <cmd2> ...` - Quick parallel command execution

**Programmatic Usage:**
```javascript
import { createMultiTerminalWindow } from './multi_terminal.js';

const terminals = [
  {name: "Server", command: "npm start"},
  {name: "Tests", command: "npm test"}
];

await createMultiTerminalWindow(terminals);
```

## Technical Details

### AppleScript Integration

The skill uses AppleScript to control iTerm:
- Automatically handles `iTerm` vs `iTerm2` naming
- Escapes commands for shell safety
- Includes timing delays for reliability
- Comprehensive error handling

### Platform Compatibility

- ✅ macOS (native AppleScript support)
- ❌ Linux (no iTerm/AppleScript)
- ❌ Windows (no iTerm/AppleScript)

For cross-platform terminal automation, consider using shell scripting or terminal multiplexers like tmux.

## Extending the Skill

Add custom iTerm operations by creating new scripts or extending existing ones:

```javascript
import { executeITermScript } from './iterm_control.js';

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

## Troubleshooting

### "osascript: not found"
- Ensure you're on macOS
- AppleScript is a macOS-only feature

### "iTerm got an error"
- Verify iTerm is installed
- Check that iTerm is not configured to block AppleScript
- Try running iTerm first, then execute commands

### Scripts not executing
- Ensure Node.js is installed: `node --version`
- Make scripts executable: `chmod +x scripts/*.js`
- Check file paths are correct

### Permission denied
- Grant Terminal/iTerm permissions in System Preferences > Security & Privacy > Automation

## Development

### Project Structure

```
iterm-control/
├── SKILL.md                      # Skill documentation for Claude Code
└── scripts/
    ├── iterm_control.js          # Core iTerm control utilities
    ├── multi_terminal.js         # Multi-terminal manager
    ├── example-config.json       # Example configuration
    └── package.json              # Node.js package metadata
```

### Testing

Test scripts manually:

```bash
# Test basic control
node scripts/iterm_control.js open "Test terminal"

# Test multi-terminal
node scripts/multi_terminal.js run "echo 'test 1'" "echo 'test 2'"
```

## License

MIT

## Credits

Based on [iTerm-MCP-Server](https://github.com/rishabkoul/iTerm-MCP-Server) by Rishab Koul.

Adapted as a Claude Code skill for enhanced developer workflows.
