#!/usr/bin/env node

/**
 * Multi-Terminal Manager
 *
 * Manages multiple iTerm terminal sessions simultaneously.
 * Useful for running multiple services (frontend, backend, database, etc.)
 *
 * Usage:
 *   node multi_terminal.js start <config.json>
 *   node multi_terminal.js run <command1> <command2> ...
 *
 * Example config.json:
 * {
 *   "terminals": [
 *     {"name": "frontend", "command": "cd frontend && npm run dev"},
 *     {"name": "backend", "command": "cd backend && npm run dev"},
 *     {"name": "logs", "command": "tail -f logs/app.log"}
 *   ]
 * }
 */

import { exec } from "node:child_process";
import { promisify } from "node:util";
import { readFile } from "node:fs/promises";

const execPromise = promisify(exec);

async function executeITermScript(script) {
  const launchScript = `
  tell application "iTerm"
    activate
  end tell
  `;

  try {
    await execPromise(`osascript -e '${launchScript}'`);
    await new Promise((resolve) => setTimeout(resolve, 300));
    const modifiedScript = script.replace(/iTerm2/g, "iTerm");
    const { stdout } = await execPromise(`osascript -e '${modifiedScript}'`);
    return stdout.trim();
  } catch (error) {
    console.error("AppleScript error:", error.message);
    throw error;
  }
}

/**
 * Create a new window with multiple tabs
 */
async function createMultiTerminalWindow(terminals) {
  console.log(`🚀 Creating ${terminals.length} terminal tabs...`);

  // Create new window
  const createWindowScript = `
  tell application "iTerm"
    activate
    create window with default profile
  end tell
  `;

  await executeITermScript(createWindowScript);
  await new Promise((resolve) => setTimeout(resolve, 500));

  // Create tabs and execute commands
  for (let i = 0; i < terminals.length; i++) {
    const terminal = terminals[i];
    const isFirst = i === 0;

    if (!isFirst) {
      // Create new tab (not for the first one, it already exists)
      const createTabScript = `
      tell application "iTerm"
        tell current window
          create tab with default profile
        end tell
      end tell
      `;
      await executeITermScript(createTabScript);
      await new Promise((resolve) => setTimeout(resolve, 300));
    }

    // Set tab name and execute command
    const escapedCommand = terminal.command.replace(/"/g, '\\"').replace(/'/g, "'\\''");
    const tabName = terminal.name || `Tab ${i + 1}`;

    const executeScript = `
    tell application "iTerm"
      tell current session of current window
        set name to "${tabName}"
        write text "${escapedCommand}"
      end tell
    end tell
    `;

    await executeITermScript(executeScript);
    console.log(`  ✅ ${tabName}: ${terminal.command}`);
    await new Promise((resolve) => setTimeout(resolve, 200));
  }

  console.log("✨ All terminals created successfully!");
}

/**
 * Run commands in separate tabs (quick version)
 */
async function runCommandsInTabs(commands) {
  const terminals = commands.map((cmd, idx) => ({
    name: `Command ${idx + 1}`,
    command: cmd,
  }));

  await createMultiTerminalWindow(terminals);
}

/**
 * Load configuration from JSON file
 */
async function loadConfig(configPath) {
  try {
    const content = await readFile(configPath, "utf-8");
    return JSON.parse(content);
  } catch (error) {
    console.error("❌ Failed to load config:", error.message);
    process.exit(1);
  }
}

// CLI interface
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case "start":
      if (!args[1]) {
        console.error("❌ Error: Config file required");
        console.log("Usage: node multi_terminal.js start <config.json>");
        process.exit(1);
      }

      const config = await loadConfig(args[1]);
      if (!config.terminals || !Array.isArray(config.terminals)) {
        console.error("❌ Error: Invalid config format. Expected { terminals: [...] }");
        process.exit(1);
      }

      await createMultiTerminalWindow(config.terminals);
      break;

    case "run":
      if (args.length < 2) {
        console.error("❌ Error: At least one command required");
        console.log("Usage: node multi_terminal.js run <command1> [command2] ...");
        process.exit(1);
      }

      const commands = args.slice(1);
      await runCommandsInTabs(commands);
      break;

    default:
      console.log(`
Multi-Terminal Manager

Usage:
  node multi_terminal.js start <config.json>        - Start terminals from config file
  node multi_terminal.js run <cmd1> <cmd2> ...      - Run commands in separate tabs

Config File Format (JSON):
{
  "terminals": [
    {"name": "Frontend", "command": "cd frontend && npm run dev"},
    {"name": "Backend", "command": "cd backend && npm run dev"}
  ]
}

Examples:
  node multi_terminal.js start dev-config.json
  node multi_terminal.js run "npm run dev" "npm run test:watch" "tail -f logs/app.log"
      `);
      break;
  }
}

export { createMultiTerminalWindow, runCommandsInTabs };

if (import.meta.url === `file://${process.argv[1]}`) {
  main().catch((error) => {
    console.error("Fatal error:", error);
    process.exit(1);
  });
}
