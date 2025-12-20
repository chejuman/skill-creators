#!/usr/bin/env node

/**
 * iTerm Control Script (v2.0)
 *
 * Enhanced utilities to control iTerm terminal instances via AppleScript.
 * Supports split panes, window layouts, and advanced session control.
 *
 * Usage:
 *   node iterm_control.js open [message]
 *   node iterm_control.js execute <command>
 *   node iterm_control.js read
 *   node iterm_control.js lines [num]
 *   node iterm_control.js close
 *   node iterm_control.js split-h [command]     # Split horizontally
 *   node iterm_control.js split-v [command]     # Split vertically
 *   node iterm_control.js window [title]        # Create new window
 *   node iterm_control.js list                  # List all sessions
 *   node iterm_control.js focus <name>          # Focus session by name
 *   node iterm_control.js send-keys <keys>      # Send keyboard input
 *
 * Examples:
 *   node iterm_control.js open "Starting dev server"
 *   node iterm_control.js execute "npm run dev"
 *   node iterm_control.js split-v "npm run test:watch"
 *   node iterm_control.js focus "Backend"
 */

import { exec } from "node:child_process";
import { promisify } from "node:util";

const execPromise = promisify(exec);

/**
 * Execute AppleScript to control iTerm
 * Uses heredoc to avoid escaping issues with quotes and special characters
 */
async function executeITermScript(script) {
  const launchScript = `
  tell application "iTerm"
    activate
  end tell
  `;

  try {
    // Launch/activate iTerm using heredoc to avoid escaping issues
    await execPromise(`osascript <<'APPLESCRIPT_EOF'\n${launchScript}\nAPPLESCRIPT_EOF`);

    // Wait briefly for iTerm to be ready
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Execute the actual script using heredoc
    const modifiedScript = script.replace(/iTerm2/g, "iTerm");
    const { stdout } = await execPromise(`osascript <<'APPLESCRIPT_EOF'\n${modifiedScript}\nAPPLESCRIPT_EOF`);
    return stdout.trim();
  } catch (error) {
    console.error("iTerm AppleScript error:", error.message);
    throw error;
  }
}

/**
 * Open a new iTerm terminal window/tab
 */
async function openTerminal(message = "Terminal ready") {
  // Escape message to prevent AppleScript syntax errors
  const escapedMessage = message.replace(/\\/g, '\\\\').replace(/"/g, '\\"');

  const script = `
  tell application "iTerm"
    activate
    tell current window
      create tab with default profile
      tell current session
        write text "echo \\"${escapedMessage}\\""
      end tell
    end tell
  end tell
  `;

  try {
    await executeITermScript(script);
    console.log("✅ Terminal opened successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to open terminal:", error.message);
    return false;
  }
}

/**
 * Escape command for safe AppleScript execution
 * AppleScript has specific escaping rules: backslashes and double quotes within strings
 */
function escapeForAppleScript(text) {
  // In AppleScript strings, backslashes and double quotes need special handling
  // Backslash is used for escaping, double quotes are escaped with \"
  return text
    .replace(/\\/g, '\\\\')    // Escape backslashes first (\ becomes \\)
    .replace(/"/g, '\\"');      // Escape double quotes (" becomes \")
}

/**
 * Execute a command in the current iTerm session
 * Supports complex commands with proper escaping
 */
async function executeCommand(command) {
  // Escape the command for AppleScript
  const escapedCommand = escapeForAppleScript(command);

  const script = `
  tell application "iTerm"
    tell current session of current window
      write text "${escapedCommand}"
    end tell
  end tell
  `;

  try {
    await executeITermScript(script);
    console.log(`✅ Command executed: ${command}`);
    return true;
  } catch (error) {
    console.error("❌ Failed to execute command:", error.message);
    return false;
  }
}

/**
 * Close the current iTerm window
 */
async function closeTerminal() {
  const script = `
  tell application "iTerm"
    close current window
  end tell
  `;

  try {
    await executeITermScript(script);
    console.log("✅ Terminal closed successfully");
    return true;
  } catch (error) {
    console.error("❌ Failed to close terminal:", error.message);
    return false;
  }
}

/**
 * Get current iTerm session text
 */
async function getSessionText() {
  const script = `
  tell application "iTerm"
    tell current session of current window
      contents
    end tell
  end tell
  `;

  try {
    const output = await executeITermScript(script);
    return output;
  } catch (error) {
    console.error("❌ Failed to get session text:", error.message);
    return null;
  }
}

/**
 * Get the last N lines of iTerm session text
 */
async function getLastLines(numLines = 50) {
  const script = `
  tell application "iTerm"
    tell current session of current window
      set allText to contents
      return allText
    end tell
  end tell
  `;

  try {
    const output = await executeITermScript(script);
    if (!output) return null;

    const lines = output.split('\n');
    const lastLines = lines.slice(-numLines).join('\n');
    return lastLines;
  } catch (error) {
    console.error("❌ Failed to get last lines:", error.message);
    return null;
  }
}

/**
 * Create a new iTerm window
 */
async function createWindow(title = "New Window") {
  const escapedTitle = escapeForAppleScript(title);

  const script = `
  tell application "iTerm"
    activate
    create window with default profile
    tell current window
      tell current session
        set name to "${escapedTitle}"
      end tell
    end tell
  end tell
  `;

  try {
    await executeITermScript(script);
    console.log(`✅ Window created: ${title}`);
    return true;
  } catch (error) {
    console.error("❌ Failed to create window:", error.message);
    return false;
  }
}

/**
 * Split pane horizontally (left/right)
 */
async function splitHorizontally(command = null) {
  const script = `
  tell application "iTerm"
    tell current session of current window
      split horizontally with default profile
    end tell
    ${command ? `
    tell current session of current window
      write text "${escapeForAppleScript(command)}"
    end tell
    ` : ''}
  end tell
  `;

  try {
    await executeITermScript(script);
    console.log(`✅ Split horizontally${command ? `: ${command}` : ''}`);
    return true;
  } catch (error) {
    console.error("❌ Failed to split:", error.message);
    return false;
  }
}

/**
 * Split pane vertically (top/bottom)
 */
async function splitVertically(command = null) {
  const script = `
  tell application "iTerm"
    tell current session of current window
      split vertically with default profile
    end tell
    ${command ? `
    tell current session of current window
      write text "${escapeForAppleScript(command)}"
    end tell
    ` : ''}
  end tell
  `;

  try {
    await executeITermScript(script);
    console.log(`✅ Split vertically${command ? `: ${command}` : ''}`);
    return true;
  } catch (error) {
    console.error("❌ Failed to split:", error.message);
    return false;
  }
}

/**
 * List all sessions in all windows
 */
async function listSessions() {
  const script = `
  tell application "iTerm"
    set sessionList to ""
    repeat with w in windows
      set windowName to name of w
      repeat with t in tabs of w
        repeat with s in sessions of t
          set sessionName to name of s
          set sessionList to sessionList & windowName & " | " & sessionName & "\\n"
        end repeat
      end repeat
    end repeat
    return sessionList
  end tell
  `;

  try {
    const output = await executeITermScript(script);
    console.log("📋 Sessions:");
    console.log("─".repeat(50));
    if (output) {
      console.log(output);
    } else {
      console.log("No sessions found");
    }
    return output;
  } catch (error) {
    console.error("❌ Failed to list sessions:", error.message);
    return null;
  }
}

/**
 * Focus on a session by name
 */
async function focusSession(sessionName) {
  const escapedName = escapeForAppleScript(sessionName);

  const script = `
  tell application "iTerm"
    activate
    repeat with w in windows
      repeat with t in tabs of w
        repeat with s in sessions of t
          if name of s contains "${escapedName}" then
            select t
            select s
            return true
          end if
        end repeat
      end repeat
    end repeat
    return false
  end tell
  `;

  try {
    const result = await executeITermScript(script);
    if (result === "true") {
      console.log(`✅ Focused on: ${sessionName}`);
      return true;
    } else {
      console.log(`⚠️ Session not found: ${sessionName}`);
      return false;
    }
  } catch (error) {
    console.error("❌ Failed to focus session:", error.message);
    return false;
  }
}

/**
 * Send keyboard keys (for Ctrl+C, etc.)
 */
async function sendKeys(keys) {
  // Map common key names to AppleScript key codes
  const keyMap = {
    'ctrl+c': 'key code 8 using control down',
    'ctrl+d': 'key code 2 using control down',
    'ctrl+z': 'key code 6 using control down',
    'enter': 'key code 36',
    'escape': 'key code 53',
    'tab': 'key code 48'
  };

  const keyCommand = keyMap[keys.toLowerCase()] || `keystroke "${escapeForAppleScript(keys)}"`;

  const script = `
  tell application "System Events"
    tell process "iTerm2"
      ${keyCommand}
    end tell
  end tell
  `;

  try {
    await execPromise(`osascript <<'APPLESCRIPT_EOF'\n${script}\nAPPLESCRIPT_EOF`);
    console.log(`✅ Sent keys: ${keys}`);
    return true;
  } catch (error) {
    console.error("❌ Failed to send keys:", error.message);
    return false;
  }
}

/**
 * Set session name
 */
async function setSessionName(name) {
  const escapedName = escapeForAppleScript(name);

  const script = `
  tell application "iTerm"
    tell current session of current window
      set name to "${escapedName}"
    end tell
  end tell
  `;

  try {
    await executeITermScript(script);
    console.log(`✅ Session named: ${name}`);
    return true;
  } catch (error) {
    console.error("❌ Failed to set name:", error.message);
    return false;
  }
}

// CLI interface
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case "open":
      const message = args[1] || "Terminal ready";
      await openTerminal(message);
      break;

    case "execute":
    case "exec":
      if (!args[1]) {
        console.error("❌ Error: Command required");
        console.log("Usage: node iterm_control.js execute <command>");
        process.exit(1);
      }
      await executeCommand(args[1]);
      break;

    case "close":
      await closeTerminal();
      break;

    case "read":
    case "get":
      const text = await getSessionText();
      if (text) {
        console.log("📄 Session output:");
        console.log(text);
      }
      break;

    case "lines":
    case "tail":
      const numLines = parseInt(args[1]) || 50;
      const lastLines = await getLastLines(numLines);
      if (lastLines) {
        console.log(`📄 Last ${numLines} lines:`);
        console.log(lastLines);
      }
      break;

    case "window":
      await createWindow(args[1] || "New Window");
      break;

    case "split-h":
      await splitHorizontally(args[1]);
      break;

    case "split-v":
      await splitVertically(args[1]);
      break;

    case "list":
      await listSessions();
      break;

    case "focus":
      if (!args[1]) {
        console.error("❌ Session name required");
        process.exit(1);
      }
      await focusSession(args[1]);
      break;

    case "send-keys":
    case "keys":
      if (!args[1]) {
        console.error("❌ Keys required (e.g., ctrl+c, enter)");
        process.exit(1);
      }
      await sendKeys(args[1]);
      break;

    case "name":
      if (!args[1]) {
        console.error("❌ Name required");
        process.exit(1);
      }
      await setSessionName(args[1]);
      break;

    default:
      console.log(`
iTerm Control Script v2.0

Basic Commands:
  open [message]              Open new terminal tab
  execute <command>           Execute command in current session
  read                        Read current session text
  lines [num]                 Read last N lines (default: 50)
  close                       Close current terminal window

Window & Pane Management:
  window [title]              Create new window
  split-h [command]           Split horizontally (left/right)
  split-v [command]           Split vertically (top/bottom)

Session Control:
  list                        List all sessions
  focus <name>                Focus session by name
  name <name>                 Set current session name
  send-keys <keys>            Send keys (ctrl+c, enter, etc.)

Examples:
  node iterm_control.js open "Dev environment ready"
  node iterm_control.js execute "npm run dev"
  node iterm_control.js split-v "npm run test:watch"
  node iterm_control.js focus "Backend"
  node iterm_control.js send-keys ctrl+c
      `);
      break;
  }
}

// Export functions for use as a module
export {
  // Basic operations
  openTerminal,
  executeCommand,
  closeTerminal,
  getSessionText,
  getLastLines,
  executeITermScript,
  // Window & Pane management
  createWindow,
  splitHorizontally,
  splitVertically,
  // Session control
  listSessions,
  focusSession,
  sendKeys,
  setSessionName
};

// Run CLI if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
  });
}
