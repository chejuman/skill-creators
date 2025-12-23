#!/usr/bin/env python3
"""Template: Detect secrets in user prompts."""

import json
import sys
import re

try:
    data = json.load(sys.stdin)
except json.JSONDecodeError:
    sys.exit(0)

prompt = data.get("prompt", "")

SECRET_PATTERNS = [
    (r"(?i)api[_-]?key\s*[:=]\s*['\"]?[\w-]+", "API Key"),
    (r"(?i)password\s*[:=]\s*['\"]?[\w-]+", "Password"),
    (r"(?i)secret\s*[:=]\s*['\"]?[\w-]+", "Secret"),
    (r"(?i)token\s*[:=]\s*['\"]?[\w-]+", "Token"),
    (r"(?i)bearer\s+[\w-]+", "Bearer Token"),
]

for pattern, secret_type in SECRET_PATTERNS:
    if re.search(pattern, prompt):
        output = {
            "decision": "block",
            "reason": f"Security: {secret_type} detected. Remove sensitive data."
        }
        print(json.dumps(output))
        sys.exit(0)

sys.exit(0)
