#!/usr/bin/env node

/**
 * iTerm Control Script
 *
 * Provides utilities to control iTerm terminal instances via AppleScript.
 * Can be used standalone or as a helper for Claude Code workflows.
 *
 * Usage:
 *   node iterm_control.js open [message]
 *   node iterm_control.js execute <command> [terminalId]
 *   node iterm_control.js close
 *
 * Examples:
 *   node iterm_control.js open "Starting dev server"
 *   node iterm_control.js execute "npm run dev"
 *   node iterm_control.js close
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

    default:
      console.log(`
iTerm Control Script

Usage:
  node iterm_control.js open [message]          - Open new terminal with optional message
  node iterm_control.js execute <command>       - Execute command in current session
  node iterm_control.js read                    - Read current session text
  node iterm_control.js lines [num]             - Read last N lines (default: 50)
  node iterm_control.js close                   - Close current terminal window

Examples:
  node iterm_control.js open "Dev environment ready"
  node iterm_control.js execute "npm run dev"
  node iterm_control.js read
  node iterm_control.js lines 100
  node iterm_control.js close
      `);
      break;
  }
}

// Export functions for use as a module
export { openTerminal, executeCommand, closeTerminal, getSessionText, getLastLines, executeITermScript };

// Run CLI if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
  });
}
