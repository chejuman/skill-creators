# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the **iTerm Control Skill** - a Claude Code skill that enables programmatic control of iTerm terminal instances via AppleScript on macOS.

**Purpose:** Automate terminal operations, manage multiple development servers, and coordinate complex workflows involving parallel processes.

**Platform:** macOS only (requires iTerm and AppleScript)

## Project Structure

```
iterm-skill/
├── CLAUDE.md                     # This file - guidance for Claude Code
├── README.md                     # User-facing documentation
├── iterm-control/                # The actual skill directory
│   ├── SKILL.md                  # Skill documentation for Claude Code
│   └── scripts/                  # Executable scripts
│       ├── iterm_control.js      # Core iTerm control utilities
│       ├── multi_terminal.js     # Multi-terminal manager
│       ├── example-config.json   # Example configuration
│       └── package.json          # Node.js package metadata
└── iterm-control.zip             # Packaged skill for distribution
```

## Development Commands

### Testing Scripts

```bash
# Test basic iTerm control
cd iterm-control/scripts
node iterm_control.js open "Test message"
node iterm_control.js execute "echo 'test'"
node iterm_control.js read
node iterm_control.js close

# Test multi-terminal
node multi_terminal.js run "echo 'terminal 1'" "echo 'terminal 2'"
node multi_terminal.js start example-config.json
```

### Packaging the Skill

```bash
# Re-package after making changes
python3 ~/.claude/skills/skill-creator/scripts/package_skill.py \
  ./iterm-control \
  .
```

This validates and creates `iterm-control.zip`.

### Installing/Updating

```bash
# Install to Claude Code skills directory
unzip -o iterm-control.zip -d ~/.claude/skills/

# Make scripts executable
chmod +x ~/.claude/skills/iterm-control/scripts/*.js
```

## Architecture

### Core Components

1. **iterm_control.js** - Base iTerm automation
   - `openTerminal(message)` - Open new terminal tab
   - `executeCommand(command)` - Execute command in current session
   - `closeTerminal()` - Close current window
   - `getSessionText()` - Read session output
   - `executeITermScript(script)` - Low-level AppleScript execution

2. **multi_terminal.js** - Multi-session orchestration
   - `createMultiTerminalWindow(terminals)` - Create window with multiple tabs
   - `runCommandsInTabs(commands)` - Quick parallel execution
   - Config-based setup for complex environments

### Key Design Patterns

**AppleScript Integration:**
- All iTerm control uses AppleScript via `osascript` command
- Scripts include timing delays for reliability (iTerm activation, tab creation)
- Command escaping for shell safety (quotes, special characters)
- Error handling with descriptive messages

**Module Structure:**
- ES modules (`type: "module"` in package.json)
- Dual-use: CLI commands + importable functions
- Main detection via `import.meta.url`

**Progressive Execution:**
- Multi-terminal creates window first, then tabs sequentially
- Brief delays between operations for stability
- Tab naming happens during command execution

## Common Workflows

### Adding New iTerm Operations

To add a new iTerm control function:

1. Add function to `iterm_control.js`:
```javascript
async function newOperation() {
  const script = `
  tell application "iTerm"
    tell current session of current window
      # Your AppleScript here
    end tell
  end tell
  `;
  await executeITermScript(script);
}
```

2. Export the function
3. Add CLI command handling in `main()`
4. Update SKILL.md documentation
5. Re-package the skill

### Modifying Multi-Terminal Behavior

The `multi_terminal.js` script controls:
- Window creation
- Tab creation and naming
- Command execution timing
- Configuration parsing

Key timing values:
- Post-launch delay: 500ms
- Tab creation delay: 300ms
- Post-execution delay: 200ms

Adjust these if terminals aren't fully initializing.

## Skill Development Notes

### Skill Requirements

Per skill-creator guidelines:
- ✅ SKILL.md < 200 lines
- ✅ Concise, trigger-rich description in frontmatter
- ✅ Scripts in `scripts/` directory
- ✅ No unnecessary references/ or assets/ directories
- ✅ Example files included

### When Claude Code Triggers This Skill

The skill description includes keywords that trigger automatic activation:
- "iTerm terminal instances"
- "multiple terminal sessions"
- "parallel dev servers"
- "monitoring command outputs"
- "automating iTerm window/tab operations"

Claude Code will proactively use this skill when users ask about these scenarios.

## Platform Limitations

**macOS Only:**
- Requires AppleScript (macOS-exclusive)
- Requires iTerm (macOS terminal app)

**Not Supported:**
- Linux (no iTerm, no AppleScript)
- Windows (no iTerm, no AppleScript)

For cross-platform needs, recommend shell scripting or tmux instead.

## Credits

Based on [iTerm-MCP-Server](https://github.com/rishabkoul/iTerm-MCP-Server) by Rishab Koul.

Adapted as a Claude Code skill with enhanced workflows and multi-terminal management.
