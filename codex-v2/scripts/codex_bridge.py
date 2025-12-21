#!/usr/bin/env python3
"""
Codex Bridge v2.1 - Async CLI wrapper for OpenAI Codex.
Features: async execution, retry logic, health check, batch processing, config support.

Improvements in v2.1:
- Fixed CLI command construction (resume placement, image handling, sandbox mapping)
- Robust JSON streaming parser with raw_decode
- Retry logic handles failed Results (not just exceptions)
- Config validation with type checking
- Jittered exponential backoff
- Enhanced error diagnostics with returncode
"""
from __future__ import annotations

import argparse
import asyncio
import json
import logging
import random
import shutil
import sys
import time
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path
from typing import Any

# Configure logging
logging.basicConfig(
    format="%(asctime)s [%(levelname)s] %(message)s",
    level=logging.WARNING
)
logger = logging.getLogger(__name__)

# Sandbox value mapping: user-friendly -> Codex CLI actual values
SANDBOX_MAP = {
    "read-only": "read-only",
    "workspace-write": "workspace-write",
    "full-access": "danger-full-access",
}

VALID_SANDBOXES = set(SANDBOX_MAP.keys())


class ErrorType(Enum):
    VALIDATION = "validation"
    NETWORK = "network"
    TIMEOUT = "timeout"
    EXECUTION = "execution"


@dataclass
class Config:
    """Configuration with defaults and file loading."""
    sandbox: str = "read-only"
    timeout: int = 300
    retries: int = 3
    verbose: bool = False

    def validate(self) -> list[str]:
        """Validate config values. Returns list of error messages."""
        errors = []
        if self.sandbox not in VALID_SANDBOXES:
            errors.append(f"Invalid sandbox: {self.sandbox}. Valid: {VALID_SANDBOXES}")
        if not isinstance(self.timeout, int) or self.timeout <= 0:
            errors.append(f"Invalid timeout: {self.timeout}. Must be positive integer.")
        if not isinstance(self.retries, int) or self.retries < 0:
            errors.append(f"Invalid retries: {self.retries}. Must be non-negative integer.")
        return errors

    @classmethod
    def load(cls, path: Path | None = None) -> Config:
        """Load config from file or use defaults."""
        config = cls()

        # Config file search order
        search_paths = [
            path,
            Path.cwd() / ".codex-bridge.json",
            Path.home() / ".config" / "codex-bridge.json",
        ]

        # Known config keys for validation
        known_keys = {"sandbox", "timeout", "retries", "verbose"}

        for p in search_paths:
            if p and p.exists():
                try:
                    data = json.loads(p.read_text())

                    # Warn about unknown keys
                    unknown = set(data.keys()) - known_keys
                    if unknown:
                        logger.warning(f"Unknown config keys ignored: {unknown}")

                    # Apply known keys with type validation
                    if "sandbox" in data and isinstance(data["sandbox"], str):
                        config.sandbox = data["sandbox"]
                    if "timeout" in data and isinstance(data["timeout"], int):
                        config.timeout = data["timeout"]
                    if "retries" in data and isinstance(data["retries"], int):
                        config.retries = data["retries"]
                    if "verbose" in data and isinstance(data["verbose"], bool):
                        config.verbose = data["verbose"]

                    logger.info(f"Loaded config from {p}")
                    break
                except (json.JSONDecodeError, OSError) as e:
                    logger.warning(f"Failed to load config from {p}: {e}")

        return config


@dataclass
class Result:
    """Execution result container."""
    success: bool
    session_id: str | None = None
    response: str = ""
    duration_ms: int = 0
    error: dict[str, Any] | None = None
    all_messages: list[dict] = field(default_factory=list)
    returncode: int | None = None

    def to_dict(self, include_all: bool = False) -> dict[str, Any]:
        if self.success:
            result = {
                "success": True,
                "session_id": self.session_id,
                "response": self.response,
                "duration_ms": self.duration_ms,
            }
        else:
            result = {"success": False, "error": self.error}
            if self.duration_ms:
                result["duration_ms"] = self.duration_ms

        if include_all and self.all_messages:
            result["all_messages"] = self.all_messages

        return result

    def is_retryable(self) -> bool:
        """Check if this failed result should be retried."""
        if self.success:
            return False
        if not self.error:
            return True
        error_type = self.error.get("type", "")
        return error_type in {
            ErrorType.TIMEOUT.value,
            ErrorType.NETWORK.value,
            ErrorType.EXECUTION.value,
        }


def validate_params(prompt: str | None, cd: str | None, batch: str | None) -> str | None:
    """Validate required parameters. Returns error message or None."""
    if batch:
        if not Path(batch).exists():
            return f"Batch file not found: {batch}"
        return None

    if not prompt:
        return "Missing required parameter: --prompt"
    if not cd:
        return "Missing required parameter: --cd"
    if not Path(cd).is_dir():
        return f"Directory not found: {cd}"

    return None


def find_codex() -> str | None:
    """Find codex executable in PATH."""
    return shutil.which("codex")


async def health_check() -> dict[str, Any]:
    """Check Codex CLI availability and authentication."""
    codex_path = find_codex()

    if not codex_path:
        return {
            "success": False,
            "error": "Codex CLI not found. Install with: npm i -g @openai/codex"
        }

    try:
        proc = await asyncio.create_subprocess_exec(
            codex_path, "--version",
            stdout=asyncio.subprocess.PIPE,
            stderr=asyncio.subprocess.PIPE
        )
        stdout, _ = await asyncio.wait_for(proc.communicate(), timeout=10)
        version = stdout.decode().strip()

        return {
            "success": True,
            "codex_path": codex_path,
            "version": version
        }
    except asyncio.TimeoutError:
        return {"success": False, "error": "Codex version check timed out"}
    except Exception as e:
        return {"success": False, "error": str(e)}


def build_command(
    codex_path: str,
    prompt: str,
    cd: str,
    config: Config,
    session_id: str | None = None,
    images: list[str] | None = None,
    model: str | None = None,
    yolo: bool = False,
) -> list[str]:
    """Build Codex CLI command with correct argument placement.

    For new sessions: codex exec --json --sandbox <mode> --cd <dir> ... -- <prompt>
    For resume: codex exec --json --sandbox <mode> --cd <dir> ... resume <session_id> <prompt>
    """
    cmd: list[str] = [codex_path, "exec"]

    # Map sandbox to Codex CLI value
    sandbox_value = SANDBOX_MAP.get(config.sandbox, config.sandbox)

    # Common options for exec (must come before subcommand)
    cmd.extend(["--json"])
    cmd.extend(["--sandbox", sandbox_value])
    cmd.extend(["--cd", cd])
    cmd.extend(["--skip-git-repo-check"])

    for img in images or []:
        cmd.extend(["--image", img])

    if model:
        cmd.extend(["--model", model])
    if yolo:
        cmd.append("--dangerously-bypass-approvals-and-sandbox")

    if session_id:
        # Resume mode: codex exec <options> resume <session_id> <prompt>
        cmd.extend(["resume", session_id, prompt])
    else:
        # New session: codex exec <options> -- <prompt>
        cmd.extend(["--", prompt])

    return cmd


async def run_codex(
    prompt: str,
    cd: str,
    config: Config,
    session_id: str | None = None,
    images: list[str] | None = None,
    model: str | None = None,
    yolo: bool = False,
    all_messages: bool = False,
) -> Result:
    """Execute Codex CLI with async streaming and retry logic."""
    start_time = time.monotonic()
    codex_path = find_codex()

    if not codex_path:
        return Result(
            success=False,
            error={"type": ErrorType.VALIDATION.value, "message": "Codex CLI not found"}
        )

    # Validate config
    config_errors = config.validate()
    if config_errors:
        return Result(
            success=False,
            error={"type": ErrorType.VALIDATION.value, "message": "; ".join(config_errors)}
        )

    cmd = build_command(codex_path, prompt, cd, config, session_id, images, model, yolo)
    logger.debug(f"Executing: {' '.join(cmd)}")

    # Execute with retry logic (handles both exceptions AND failed Results)
    last_result: Result | None = None
    last_error: str | None = None
    error_type = ErrorType.EXECUTION

    for attempt in range(config.retries + 1):
        try:
            result = await _execute_codex(cmd, config.timeout, all_messages)

            # Success - return immediately
            if result.success:
                result.duration_ms = int((time.monotonic() - start_time) * 1000)
                return result

            # Failed Result - check if retryable
            last_result = result
            last_error = (result.error or {}).get("message", "Unknown failure")
            error_type_str = (result.error or {}).get("type", ErrorType.EXECUTION.value)
            try:
                error_type = ErrorType(error_type_str)
            except ValueError:
                error_type = ErrorType.EXECUTION

            if attempt < config.retries and result.is_retryable():
                wait_time = (2 ** attempt) + random.uniform(0, 1)  # Jittered backoff
                logger.info(f"Retry {attempt + 1}/{config.retries} after {wait_time:.1f}s (Result failed)")
                await asyncio.sleep(wait_time)
                continue

            # Not retryable or no more retries
            result.duration_ms = int((time.monotonic() - start_time) * 1000)
            if result.error:
                result.error["retries_attempted"] = attempt
            return result

        except asyncio.TimeoutError:
            last_error = f"Execution timed out after {config.timeout}s"
            error_type = ErrorType.TIMEOUT
        except OSError as e:
            last_error = f"Failed to start process: {e}"
            error_type = ErrorType.EXECUTION
        except Exception as e:
            last_error = str(e)
            error_type = ErrorType.EXECUTION

        if attempt < config.retries:
            wait_time = (2 ** attempt) + random.uniform(0, 1)  # Jittered backoff
            logger.info(f"Retry {attempt + 1}/{config.retries} after {wait_time:.1f}s")
            await asyncio.sleep(wait_time)

    return Result(
        success=False,
        duration_ms=int((time.monotonic() - start_time) * 1000),
        error={
            "type": error_type.value,
            "message": last_error,
            "retries_attempted": config.retries,
        }
    )


async def _execute_codex(cmd: list[str], timeout: int, include_all: bool) -> Result:
    """Internal async execution with robust JSON streaming."""
    proc = await asyncio.create_subprocess_exec(
        *cmd,
        stdin=asyncio.subprocess.DEVNULL,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.STDOUT,
    )

    messages: list[dict] = []
    agent_parts: list[str] = []
    thread_id: str | None = None
    saw_turn_completed = False
    decoder = json.JSONDecoder()
    buf = ""
    last_raw_lines: list[str] = []

    async def read_stream():
        nonlocal buf, thread_id, saw_turn_completed

        while True:
            try:
                chunk = await asyncio.wait_for(
                    proc.stdout.read(4096),
                    timeout=1.0
                )
            except asyncio.TimeoutError:
                # Check if process is still running
                if proc.returncode is not None:
                    break
                continue

            if not chunk:
                break

            text = chunk.decode("utf-8", errors="replace")
            buf += text

            # Keep last few raw lines for diagnostics
            for line in text.splitlines():
                if line.strip():
                    last_raw_lines.append(line.strip())
                    if len(last_raw_lines) > 5:
                        last_raw_lines.pop(0)

            # Parse JSON objects from buffer
            while True:
                buf = buf.lstrip()
                if not buf or buf[0] != "{":
                    # Find next JSON object
                    idx = buf.find("{")
                    if idx == -1:
                        buf = ""
                        break
                    buf = buf[idx:]

                try:
                    data, end_idx = decoder.raw_decode(buf)
                    buf = buf[end_idx:]
                except json.JSONDecodeError:
                    # Incomplete JSON - need more data
                    break

                messages.append(data)

                # Extract session ID
                if data.get("thread_id"):
                    thread_id = data["thread_id"]

                # Extract agent response (preserve newlines)
                item = data.get("item") or {}
                if item.get("type") == "agent_message":
                    agent_parts.append(item.get("text", ""))

                # Mark turn completed but don't terminate immediately
                if data.get("type") == "turn.completed":
                    saw_turn_completed = True

    try:
        await asyncio.wait_for(read_stream(), timeout=timeout)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()
        return Result(
            success=False,
            all_messages=messages if include_all else [],
            error={
                "type": ErrorType.TIMEOUT.value,
                "message": f"Execution timed out after {timeout}s",
                "last_output": last_raw_lines[-3:] if last_raw_lines else [],
            }
        )

    # Wait for process to complete
    try:
        await asyncio.wait_for(proc.wait(), timeout=5)
    except asyncio.TimeoutError:
        proc.kill()
        await proc.wait()

    returncode = proc.returncode
    agent_response = "".join(agent_parts)

    if not thread_id:
        return Result(
            success=False,
            returncode=returncode,
            all_messages=messages if include_all else [],
            error={
                "type": ErrorType.EXECUTION.value,
                "message": "No session ID received",
                "returncode": returncode,
                "last_output": last_raw_lines[-3:] if last_raw_lines else [],
            }
        )

    if not agent_response:
        return Result(
            success=False,
            session_id=thread_id,
            returncode=returncode,
            all_messages=messages if include_all else [],
            error={
                "type": ErrorType.EXECUTION.value,
                "message": "No response received",
                "returncode": returncode,
                "last_output": last_raw_lines[-3:] if last_raw_lines else [],
            }
        )

    return Result(
        success=True,
        session_id=thread_id,
        response=agent_response,
        returncode=returncode,
        all_messages=messages if include_all else [],
    )


async def run_batch(batch_file: str, config: Config) -> dict[str, Any]:
    """Process multiple prompts from JSON file."""
    try:
        tasks = json.loads(Path(batch_file).read_text())
    except (json.JSONDecodeError, OSError) as e:
        return {"success": False, "error": f"Failed to load batch file: {e}"}

    if not isinstance(tasks, list):
        return {"success": False, "error": "Batch file must contain a JSON array"}

    results = []
    succeeded = 0
    failed = 0

    for i, task in enumerate(tasks):
        prompt = task.get("prompt", "")
        cd = task.get("cd", "")

        if not prompt or not cd:
            results.append({"index": i, "success": False, "error": "Missing prompt or cd"})
            failed += 1
            continue

        result = await run_codex(
            prompt=prompt,
            cd=cd,
            config=config,
            session_id=task.get("session_id"),
        )

        result_dict = result.to_dict()
        result_dict["index"] = i
        results.append(result_dict)

        if result.success:
            succeeded += 1
        else:
            failed += 1

    return {
        "success": failed == 0,
        "results": results,
        "summary": {"total": len(tasks), "succeeded": succeeded, "failed": failed}
    }


def parse_args() -> argparse.Namespace:
    """Parse command line arguments."""
    parser = argparse.ArgumentParser(
        description="Codex Bridge v2.1 - Async CLI wrapper for OpenAI Codex"
    )

    # Required (unless health-check or batch)
    parser.add_argument("--prompt", help="Task instruction for Codex")
    parser.add_argument("--cd", help="Workspace root directory")

    # Execution options
    parser.add_argument("--session-id", help="Resume previous session")
    parser.add_argument("--sandbox", choices=list(VALID_SANDBOXES),
                        help="Sandbox policy (default: from config or read-only)")
    parser.add_argument("--timeout", type=int, help="Max execution time in seconds")
    parser.add_argument("--retries", type=int, help="Retry attempts on failure")

    # Features
    parser.add_argument("--health-check", action="store_true", help="Check Codex CLI availability")
    parser.add_argument("--batch", metavar="FILE", help="Process multiple prompts from JSON file")
    parser.add_argument("--config", metavar="FILE", help="Load settings from config file")
    parser.add_argument("--verbose", action="store_true", help="Enable debug logging")
    parser.add_argument("--all-messages", action="store_true", help="Include full message trace")

    # Advanced
    parser.add_argument("--image", action="append", default=[], help="Attach image files")
    parser.add_argument("--model", help="Specify model (use only when requested)")
    parser.add_argument("--yolo", action="store_true", help="Bypass approvals")

    return parser.parse_args()


async def main() -> int:
    """Main entry point."""
    args = parse_args()

    # Configure logging
    if args.verbose:
        logging.getLogger().setLevel(logging.DEBUG)

    # Load configuration
    config_path = Path(args.config) if args.config else None
    config = Config.load(config_path)

    # Override config with CLI args
    if args.sandbox:
        config.sandbox = args.sandbox
    if args.timeout:
        config.timeout = args.timeout
    if args.retries is not None:
        config.retries = args.retries
    if args.verbose:
        config.verbose = True

    # Health check mode
    if args.health_check:
        result = await health_check()
        print(json.dumps(result, indent=2))
        return 0 if result["success"] else 1

    # Batch mode
    if args.batch:
        result = await run_batch(args.batch, config)
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0 if result["success"] else 1

    # Validate required params
    error = validate_params(args.prompt, args.cd, args.batch)
    if error:
        result = {"success": False, "error": {"type": "validation", "message": error}}
        print(json.dumps(result, indent=2))
        return 1

    # Single execution
    result = await run_codex(
        prompt=args.prompt,
        cd=args.cd,
        config=config,
        session_id=args.session_id,
        images=args.image if args.image else None,
        model=args.model,
        yolo=args.yolo,
        all_messages=args.all_messages,
    )

    print(json.dumps(result.to_dict(args.all_messages), indent=2, ensure_ascii=False))
    return 0 if result.success else 1


if __name__ == "__main__":
    sys.exit(asyncio.run(main()))
