#!/usr/bin/env node

/**
 * iTerm Process Monitor
 *
 * Monitor running processes in iTerm sessions, detect failures, auto-restart.
 *
 * Usage:
 *   node process_monitor.js watch <sessionId> [--restart] [--interval <ms>]
 *   node process_monitor.js check <sessionId>
 *   node process_monitor.js logs <sessionId> [--lines <num>] [--output <file>]
 *   node process_monitor.js collect-all [--output <dir>]
 *   node process_monitor.js status
 */

import { exec } from "node:child_process";
import { promisify } from "node:util";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const execPromise = promisify(exec);

const SESSION_DIR = join(homedir(), ".iterm-sessions");
const SESSION_FILE = join(SESSION_DIR, "sessions.json");
const LOGS_DIR = join(SESSION_DIR, "logs");

// Patterns that indicate process failure
const ERROR_PATTERNS = [
  /error:/i,
  /fatal:/i,
  /exception:/i,
  /failed/i,
  /ECONNREFUSED/i,
  /EADDRINUSE/i,
  /segmentation fault/i,
  /killed/i,
  /npm ERR!/i
];

// Patterns that indicate process is running
const RUNNING_PATTERNS = [
  /listening on/i,
  /server started/i,
  /ready on/i,
  /watching for/i,
  /compiled successfully/i,
  /webpack.*compiled/i,
  /vite.*ready/i,
  /next.*ready/i
];

/**
 * Load session registry
 */
async function loadRegistry() {
  if (existsSync(SESSION_FILE)) {
    const data = await readFile(SESSION_FILE, "utf-8");
    return JSON.parse(data);
  }
  return { sessions: {}, groups: {} };
}

/**
 * Execute AppleScript
 */
async function executeAppleScript(script) {
  const modifiedScript = script.replace(/iTerm2/g, "iTerm");
  const { stdout } = await execPromise(`osascript <<'APPLESCRIPT_EOF'\n${modifiedScript}\nAPPLESCRIPT_EOF`);
  return stdout.trim();
}

/**
 * Get session output
 */
async function getSessionOutput(sessionName, lines = 100) {
  const script = `
  tell application "iTerm"
    repeat with w in windows
      repeat with t in tabs of w
        repeat with s in sessions of t
          if name of s is "${sessionName.replace(/"/g, '\\"')}" then
            return contents of s
          end if
        end repeat
      end repeat
    end repeat
    return ""
  end tell
  `;

  const output = await executeAppleScript(script);
  const outputLines = output.split('\n');
  return outputLines.slice(-lines).join('\n');
}

/**
 * Analyze output for process status
 */
function analyzeOutput(output) {
  const errors = [];
  const status = { running: false, hasErrors: false, lastError: null };

  // Check for running indicators
  for (const pattern of RUNNING_PATTERNS) {
    if (pattern.test(output)) {
      status.running = true;
      break;
    }
  }

  // Check for error patterns
  const lines = output.split('\n');
  for (const line of lines) {
    for (const pattern of ERROR_PATTERNS) {
      if (pattern.test(line)) {
        errors.push(line.trim());
        status.hasErrors = true;
      }
    }
  }

  if (errors.length > 0) {
    status.lastError = errors[errors.length - 1];
  }

  return { status, errors };
}

/**
 * Check session health
 */
async function checkSession(sessionId) {
  const registry = await loadRegistry();
  const session = registry.sessions[sessionId];

  if (!session) {
    console.error(`❌ Session not found: ${sessionId}`);
    return null;
  }

  try {
    const output = await getSessionOutput(session.name, 100);
    const { status, errors } = analyzeOutput(output);

    console.log(`📊 Session Health: ${session.name}`);
    console.log(`   ID: ${sessionId}`);
    console.log(`   Running: ${status.running ? "✅ Yes" : "❌ No"}`);
    console.log(`   Errors: ${status.hasErrors ? `⚠️ ${errors.length} found` : "✅ None"}`);
    if (status.lastError) {
      console.log(`   Last Error: ${status.lastError.substring(0, 80)}...`);
    }

    return { session, status, errors, output };
  } catch (error) {
    console.error("❌ Failed to check session:", error.message);
    return null;
  }
}

/**
 * Restart session command
 */
async function restartSession(sessionId) {
  const registry = await loadRegistry();
  const session = registry.sessions[sessionId];

  if (!session || !session.command) {
    console.error(`❌ Cannot restart: session not found or no command`);
    return false;
  }

  const script = `
  tell application "iTerm"
    repeat with w in windows
      repeat with t in tabs of w
        repeat with s in sessions of t
          if name of s is "${session.name.replace(/"/g, '\\"')}" then
            tell s
              write text "\\x03"
              delay 0.5
              write text "${session.command.replace(/"/g, '\\"')}"
            end tell
            return true
          end if
        end repeat
      end repeat
    end repeat
    return false
  end tell
  `;

  try {
    await executeAppleScript(script);
    console.log(`🔄 Session restarted: ${session.name}`);
    return true;
  } catch (error) {
    console.error("❌ Failed to restart:", error.message);
    return false;
  }
}

/**
 * Watch session and optionally auto-restart
 */
async function watchSession(sessionId, options = {}) {
  const interval = options.interval || 5000;
  const autoRestart = options.restart || false;

  console.log(`👁️ Watching session: ${sessionId}`);
  console.log(`   Interval: ${interval}ms`);
  console.log(`   Auto-restart: ${autoRestart ? "Yes" : "No"}`);
  console.log(`   Press Ctrl+C to stop\n`);

  let restartCount = 0;
  const maxRestarts = 3;

  const check = async () => {
    const result = await checkSession(sessionId);
    if (!result) return;

    const { status } = result;

    if (status.hasErrors && !status.running && autoRestart) {
      if (restartCount < maxRestarts) {
        console.log(`\n⚠️ Process appears failed. Restarting... (${restartCount + 1}/${maxRestarts})`);
        await restartSession(sessionId);
        restartCount++;
      } else {
        console.log(`\n❌ Max restarts (${maxRestarts}) reached. Stopping watch.`);
        process.exit(1);
      }
    }
  };

  await check();
  setInterval(check, interval);
}

/**
 * Collect logs from a session
 */
async function collectLogs(sessionId, options = {}) {
  const lines = options.lines || 500;
  const outputFile = options.output;

  const registry = await loadRegistry();
  const session = registry.sessions[sessionId];

  if (!session) {
    console.error(`❌ Session not found: ${sessionId}`);
    return null;
  }

  try {
    const output = await getSessionOutput(session.name, lines);
    const timestamp = new Date().toISOString().replace(/[:.]/g, "-");

    if (outputFile) {
      await writeFile(outputFile, output);
      console.log(`📝 Logs saved to: ${outputFile}`);
    } else {
      console.log(`📝 Logs from ${session.name} (${lines} lines):`);
      console.log("─".repeat(60));
      console.log(output);
    }

    return output;
  } catch (error) {
    console.error("❌ Failed to collect logs:", error.message);
    return null;
  }
}

/**
 * Collect all session logs
 */
async function collectAllLogs(outputDir) {
  const registry = await loadRegistry();
  const sessions = Object.values(registry.sessions);

  if (sessions.length === 0) {
    console.log("📋 No sessions to collect logs from");
    return;
  }

  const dir = outputDir || LOGS_DIR;
  if (!existsSync(dir)) {
    await mkdir(dir, { recursive: true });
  }

  const timestamp = new Date().toISOString().replace(/[:.]/g, "-");
  console.log(`📦 Collecting logs from ${sessions.length} sessions...`);

  for (const session of sessions) {
    try {
      const output = await getSessionOutput(session.name, 500);
      const filename = `${session.name.replace(/[^a-zA-Z0-9]/g, "_")}_${timestamp}.log`;
      const filepath = join(dir, filename);
      await writeFile(filepath, output);
      console.log(`  ✅ ${session.name} → ${filename}`);
    } catch (error) {
      console.log(`  ❌ ${session.name} - failed`);
    }
  }

  console.log(`\n📁 Logs saved to: ${dir}`);
}

/**
 * Show status of all sessions
 */
async function showStatus() {
  const registry = await loadRegistry();
  const sessions = Object.values(registry.sessions);

  if (sessions.length === 0) {
    console.log("📋 No sessions registered");
    return;
  }

  console.log("📊 Session Status Overview");
  console.log("═".repeat(70));

  for (const session of sessions) {
    try {
      const output = await getSessionOutput(session.name, 50);
      const { status } = analyzeOutput(output);

      const runIcon = status.running ? "🟢" : "⚪";
      const errIcon = status.hasErrors ? "⚠️" : "✅";

      console.log(`${runIcon} ${session.name} (${session.group})`);
      console.log(`   ID: ${session.id}`);
      console.log(`   Running: ${status.running} | Errors: ${status.hasErrors}`);
      console.log("─".repeat(70));
    } catch (error) {
      console.log(`❓ ${session.name} - status unknown`);
    }
  }
}

// CLI
async function main() {
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case "watch":
      const watchOpts = {
        restart: args.includes("--restart"),
        interval: args.includes("--interval")
          ? parseInt(args[args.indexOf("--interval") + 1])
          : 5000
      };
      await watchSession(args[1], watchOpts);
      break;

    case "check":
      await checkSession(args[1]);
      break;

    case "logs":
      const logsOpts = {
        lines: args.includes("--lines")
          ? parseInt(args[args.indexOf("--lines") + 1])
          : 500,
        output: args.includes("--output")
          ? args[args.indexOf("--output") + 1]
          : null
      };
      await collectLogs(args[1], logsOpts);
      break;

    case "collect-all":
      const collectDir = args.includes("--output")
        ? args[args.indexOf("--output") + 1]
        : null;
      await collectAllLogs(collectDir);
      break;

    case "status":
      await showStatus();
      break;

    case "restart":
      await restartSession(args[1]);
      break;

    default:
      console.log(`
iTerm Process Monitor

Commands:
  watch <sessionId> [--restart] [--interval <ms>]   Watch session health
  check <sessionId>                                  Check session status
  logs <sessionId> [--lines <num>] [--output <file>] Collect logs
  collect-all [--output <dir>]                       Collect all logs
  status                                             Show all session status
  restart <sessionId>                                Restart session command
      `);
  }
}

export {
  checkSession,
  watchSession,
  restartSession,
  collectLogs,
  collectAllLogs,
  showStatus
};

main().catch(console.error);
