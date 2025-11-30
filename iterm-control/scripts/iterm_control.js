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
 */
async function executeITermScript(script) {
  const launchScript = `
  tell application "iTerm"
    activate
  end tell
  `;

  try {
    // Launch/activate iTerm
    await execPromise(`osascript -e '${launchScript}'`);

    // Wait briefly for iTerm to be ready
    await new Promise((resolve) => setTimeout(resolve, 500));

    // Execute the actual script
    const modifiedScript = script.replace(/iTerm2/g, "iTerm");
    const { stdout } = await execPromise(`osascript -e '${modifiedScript}'`);
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
 * Execute a command in the current iTerm session
 */
async function executeCommand(command) {
  const escapedCommand = command.replace(/"/g, '\\"').replace(/'/g, "'\\''");

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
      get text
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

    default:
      console.log(`
iTerm Control Script

Usage:
  node iterm_control.js open [message]          - Open new terminal with optional message
  node iterm_control.js execute <command>       - Execute command in current session
  node iterm_control.js read                    - Read current session text
  node iterm_control.js close                   - Close current terminal window

Examples:
  node iterm_control.js open "Dev environment ready"
  node iterm_control.js execute "npm run dev"
  node iterm_control.js read
  node iterm_control.js close
      `);
      break;
  }
}

// Export functions for use as a module
export { openTerminal, executeCommand, closeTerminal, getSessionText, executeITermScript };

// Run CLI if called directly
if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
  });
}
