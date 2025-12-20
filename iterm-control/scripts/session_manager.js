#!/usr/bin/env node

/**
 * iTerm Session Manager
 *
 * Advanced session management with ID-based control, state persistence, and grouping.
 *
 * Usage:
 *   node session_manager.js create <name> [--group <group>] [--command <cmd>]
 *   node session_manager.js list [--group <group>]
 *   node session_manager.js get <sessionId>
 *   node session_manager.js execute <sessionId> <command>
 *   node session_manager.js read <sessionId> [--lines <num>]
 *   node session_manager.js close <sessionId>
 *   node session_manager.js save <filepath>
 *   node session_manager.js restore <filepath>
 *   node session_manager.js group-start <group>
 *   node session_manager.js group-stop <group>
 */

import { exec } from "node:child_process";
import { promisify } from "node:util";
import { readFile, writeFile, mkdir } from "node:fs/promises";
import { existsSync } from "node:fs";
import { homedir } from "node:os";
import { join } from "node:path";

const execPromise = promisify(exec);

// Session storage path
const SESSION_DIR = join(homedir(), ".iterm-sessions");
const SESSION_FILE = join(SESSION_DIR, "sessions.json");

// In-memory session registry
let sessionRegistry = {
  sessions: {},
  groups: {}
};

/**
 * Initialize session storage
 */
async function initStorage() {
  if (!existsSync(SESSION_DIR)) {
    await mkdir(SESSION_DIR, { recursive: true });
  }
  if (existsSync(SESSION_FILE)) {
    try {
      const data = await readFile(SESSION_FILE, "utf-8");
      sessionRegistry = JSON.parse(data);
    } catch (e) {
      sessionRegistry = { sessions: {}, groups: {} };
    }
  }
}

/**
 * Save session registry to disk
 */
async function saveRegistry() {
  await writeFile(SESSION_FILE, JSON.stringify(sessionRegistry, null, 2));
}

/**
 * Generate unique session ID
 */
function generateSessionId() {
  return `session_${Date.now()}_${Math.random().toString(36).substr(2, 6)}`;
}

/**
 * Execute AppleScript with heredoc
 */
async function executeAppleScript(script) {
  const modifiedScript = script.replace(/iTerm2/g, "iTerm");
  const { stdout } = await execPromise(`osascript <<'APPLESCRIPT_EOF'\n${modifiedScript}\nAPPLESCRIPT_EOF`);
  return stdout.trim();
}

/**
 * Escape text for AppleScript
 */
function escapeForAppleScript(text) {
  return text.replace(/\\/g, '\\\\').replace(/"/g, '\\"');
}

/**
 * Create a new session with ID tracking
 */
async function createSession(name, options = {}) {
  const sessionId = generateSessionId();
  const group = options.group || "default";
  const command = options.command || null;

  const script = `
  tell application "iTerm"
    activate
    tell current window
      create tab with default profile
      tell current session
        set name to "${escapeForAppleScript(name)}"
        ${command ? `write text "${escapeForAppleScript(command)}"` : ''}
      end tell
    end tell
    return id of current window
  end tell
  `;

  try {
    const windowId = await executeAppleScript(script);

    // Store session info
    sessionRegistry.sessions[sessionId] = {
      id: sessionId,
      name,
      group,
      command,
      windowId,
      createdAt: new Date().toISOString(),
      status: "running"
    };

    // Add to group
    if (!sessionRegistry.groups[group]) {
      sessionRegistry.groups[group] = [];
    }
    sessionRegistry.groups[group].push(sessionId);

    await saveRegistry();
    console.log(`✅ Session created: ${sessionId}`);
    console.log(`   Name: ${name}`);
    console.log(`   Group: ${group}`);
    return sessionId;
  } catch (error) {
    console.error("❌ Failed to create session:", error.message);
    return null;
  }
}

/**
 * List all sessions or sessions in a group
 */
async function listSessions(group = null) {
  await initStorage();

  let sessions = Object.values(sessionRegistry.sessions);
  if (group) {
    const groupIds = sessionRegistry.groups[group] || [];
    sessions = sessions.filter(s => groupIds.includes(s.id));
  }

  if (sessions.length === 0) {
    console.log("📋 No sessions found");
    return [];
  }

  console.log("📋 Sessions:");
  console.log("─".repeat(70));
  for (const session of sessions) {
    console.log(`  ID: ${session.id}`);
    console.log(`  Name: ${session.name} | Group: ${session.group} | Status: ${session.status}`);
    console.log(`  Command: ${session.command || "(none)"}`);
    console.log("─".repeat(70));
  }
  return sessions;
}

/**
 * Get session info by ID
 */
async function getSession(sessionId) {
  await initStorage();
  const session = sessionRegistry.sessions[sessionId];
  if (!session) {
    console.error(`❌ Session not found: ${sessionId}`);
    return null;
  }
  console.log(JSON.stringify(session, null, 2));
  return session;
}

/**
 * Execute command in specific session by focusing on it
 */
async function executeInSession(sessionId, command) {
  await initStorage();
  const session = sessionRegistry.sessions[sessionId];
  if (!session) {
    console.error(`❌ Session not found: ${sessionId}`);
    return false;
  }

  const script = `
  tell application "iTerm"
    activate
    repeat with w in windows
      repeat with t in tabs of w
        repeat with s in sessions of t
          if name of s is "${escapeForAppleScript(session.name)}" then
            select t
            tell s
              write text "${escapeForAppleScript(command)}"
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
    console.log(`✅ Command executed in session ${sessionId}: ${command}`);
    return true;
  } catch (error) {
    console.error("❌ Failed to execute command:", error.message);
    return false;
  }
}

/**
 * Read output from a session
 */
async function readSessionOutput(sessionId, lines = 50) {
  await initStorage();
  const session = sessionRegistry.sessions[sessionId];
  if (!session) {
    console.error(`❌ Session not found: ${sessionId}`);
    return null;
  }

  const script = `
  tell application "iTerm"
    repeat with w in windows
      repeat with t in tabs of w
        repeat with s in sessions of t
          if name of s is "${escapeForAppleScript(session.name)}" then
            return contents of s
          end if
        end repeat
      end repeat
    end repeat
    return ""
  end tell
  `;

  try {
    const output = await executeAppleScript(script);
    const outputLines = output.split('\n');
    const lastLines = outputLines.slice(-lines).join('\n');
    console.log(`📄 Output from ${session.name} (last ${lines} lines):`);
    console.log(lastLines);
    return lastLines;
  } catch (error) {
    console.error("❌ Failed to read session:", error.message);
    return null;
  }
}

/**
 * Close a session
 */
async function closeSession(sessionId) {
  await initStorage();
  const session = sessionRegistry.sessions[sessionId];
  if (!session) {
    console.error(`❌ Session not found: ${sessionId}`);
    return false;
  }

  const script = `
  tell application "iTerm"
    repeat with w in windows
      repeat with t in tabs of w
        repeat with s in sessions of t
          if name of s is "${escapeForAppleScript(session.name)}" then
            close s
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
    session.status = "closed";

    // Remove from group
    const groupSessions = sessionRegistry.groups[session.group] || [];
    sessionRegistry.groups[session.group] = groupSessions.filter(id => id !== sessionId);

    await saveRegistry();
    console.log(`✅ Session closed: ${sessionId}`);
    return true;
  } catch (error) {
    console.error("❌ Failed to close session:", error.message);
    return false;
  }
}

/**
 * Save current session state to file
 */
async function saveState(filepath) {
  await initStorage();
  await writeFile(filepath, JSON.stringify(sessionRegistry, null, 2));
  console.log(`✅ Session state saved to: ${filepath}`);
}

/**
 * Restore session state from file
 */
async function restoreState(filepath) {
  try {
    const data = await readFile(filepath, "utf-8");
    const savedState = JSON.parse(data);

    // Recreate sessions from saved state
    for (const session of Object.values(savedState.sessions)) {
      if (session.status === "running" && session.command) {
        await createSession(session.name, {
          group: session.group,
          command: session.command
        });
      }
    }
    console.log(`✅ Session state restored from: ${filepath}`);
  } catch (error) {
    console.error("❌ Failed to restore state:", error.message);
  }
}

/**
 * Start all sessions in a group
 */
async function startGroup(group) {
  await initStorage();
  const groupSessions = sessionRegistry.groups[group] || [];
  const sessions = groupSessions
    .map(id => sessionRegistry.sessions[id])
    .filter(s => s && s.command);

  if (sessions.length === 0) {
    console.log(`⚠️ No sessions with commands found in group: ${group}`);
    return;
  }

  console.log(`🚀 Starting group: ${group}`);
  for (const session of sessions) {
    await createSession(session.name, {
      group: session.group,
      command: session.command
    });
  }
  console.log(`✅ Group ${group} started with ${sessions.length} sessions`);
}

/**
 * Stop all sessions in a group
 */
async function stopGroup(group) {
  await initStorage();
  const groupSessions = [...(sessionRegistry.groups[group] || [])];

  if (groupSessions.length === 0) {
    console.log(`⚠️ No sessions found in group: ${group}`);
    return;
  }

  console.log(`🛑 Stopping group: ${group}`);
  for (const sessionId of groupSessions) {
    await closeSession(sessionId);
  }
  console.log(`✅ Group ${group} stopped`);
}

// CLI
async function main() {
  await initStorage();
  const args = process.argv.slice(2);
  const command = args[0];

  switch (command) {
    case "create":
      const name = args[1];
      if (!name) {
        console.error("❌ Name required");
        process.exit(1);
      }
      const groupIdx = args.indexOf("--group");
      const cmdIdx = args.indexOf("--command");
      await createSession(name, {
        group: groupIdx > -1 ? args[groupIdx + 1] : undefined,
        command: cmdIdx > -1 ? args[cmdIdx + 1] : undefined
      });
      break;

    case "list":
      const listGroupIdx = args.indexOf("--group");
      await listSessions(listGroupIdx > -1 ? args[listGroupIdx + 1] : null);
      break;

    case "get":
      await getSession(args[1]);
      break;

    case "execute":
    case "exec":
      await executeInSession(args[1], args[2]);
      break;

    case "read":
      const linesIdx = args.indexOf("--lines");
      await readSessionOutput(args[1], linesIdx > -1 ? parseInt(args[linesIdx + 1]) : 50);
      break;

    case "close":
      await closeSession(args[1]);
      break;

    case "save":
      await saveState(args[1]);
      break;

    case "restore":
      await restoreState(args[1]);
      break;

    case "group-start":
      await startGroup(args[1]);
      break;

    case "group-stop":
      await stopGroup(args[1]);
      break;

    default:
      console.log(`
iTerm Session Manager

Commands:
  create <name> [--group <g>] [--command <c>]  Create named session
  list [--group <group>]                        List sessions
  get <sessionId>                               Get session info
  execute <sessionId> <command>                 Execute in session
  read <sessionId> [--lines <num>]              Read session output
  close <sessionId>                             Close session
  save <filepath>                               Save state to file
  restore <filepath>                            Restore state from file
  group-start <group>                           Start all in group
  group-stop <group>                            Stop all in group
      `);
  }
}

export {
  createSession,
  listSessions,
  getSession,
  executeInSession,
  readSessionOutput,
  closeSession,
  saveState,
  restoreState,
  startGroup,
  stopGroup
};

main().catch(console.error);
