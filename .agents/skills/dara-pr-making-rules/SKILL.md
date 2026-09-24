---
name: dara-pr-making-rules
description: Apply Dara's rules when preparing a bug-fix PR and babysitting it until CI and code-review bots are green.
---

# Dara's PR Making Rules

1. Reproduce the problem before editing code. Record the setup, steps, and expected and actual behavior. Capture artifacts if necessary: for visual changes or behavior best demonstrated, record the before state with images or video.
2. Make the smallest clean fix. Judge mergeability by scope: trim unnecessary changes, and reorganize code only where needed to make the fix clean.
3. If there is a previous issue in the current work, confirm its computer-use test still passes. Then repeat this problem's reproduction steps through computer use, confirm it is resolved, and capture a comparable after artifact when needed. Run the repo's required checks.
4. Open one ready-for-review PR following the repo's PR guidelines and template. Include the reproduction steps and verification results. Showcase visual or interaction changes with the captured images or video; when attaching media, follow [Uploading PR artifacts](references/uploading-artifacts.md). State any verification blockers explicitly.
5. Babysit the PR after opening it. Wait for the repo's code-review bots, address actionable feedback and failing required checks, test, commit, push, and trigger re-review. Repeat until required checks pass and every review bot has completed successfully on the latest commit with no actionable unresolved review threads. Keep fixes tightly scoped. If a bot or check is stalled or unavailable, report the blocker rather than declaring green. Leave the PR open for merging.
