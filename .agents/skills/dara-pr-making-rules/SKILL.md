---
name: dara-pr-making-rules
description: Apply Dara's rules when preparing or reviewing a bug-fix PR.
---

# Dara's PR Making Rules

1. Reproduce the problem before editing code. Record the setup, steps, expected and actual behavior, and capture a before screenshot.
2. Make the smallest clean fix. Judge mergeability by scope: trim unnecessary changes, and reorganize code only where needed to make the fix clean.
3. If there is a previous issue in the current work, confirm its computer-use test still passes. Then repeat this problem's reproduction steps through computer use, confirm it is resolved, and capture a comparable after screenshot. Run the repo's required checks.
4. Prepare one draft PR following the repo's PR guidelines and template. Include the reproduction steps, before-and-after screenshots, and verification results. State any verification blockers explicitly.
