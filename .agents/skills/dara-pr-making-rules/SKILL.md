---
name: dara-pr-making-rules
description: Prepare bug-fix PRs and babysit CI and review bots until green.
---

# Dara's PR Making Rules

1. **Reproduce.** Before editing, record setup, steps, and expected versus actual behavior.
2. **Scope.** Make the smallest clean diff. Trim unrelated changes; reorganize only as needed for the fix.
3. **Verify.** Rerun the previous issue's computer-use test, if applicable, then verify this fix through the original reproduction. Run required checks.
4. **Artifacts.** Visual changes require comparable before-and-after screenshots in the PR. Add video when needed to demonstrate interaction changes. Other artifacts are optional. For uploads, read [Attachments](references/uploading-artifacts.md).
5. **PR.** Open one ready-for-review PR using the repo's guidelines and template. Include reproduction, verification, and any blockers.
6. **Babysit.** Wait for review bots; fix actionable feedback and CI failures, test, push, and request re-review. Repeat until green: required checks pass, bot reviews cover the latest commit, and no actionable review threads remain unresolved. Report stalled checks or unavailable bots as blockers. Leave the PR open.
