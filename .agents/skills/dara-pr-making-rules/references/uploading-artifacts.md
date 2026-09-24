# Attachments

Use `gh --attach` for images/video; check command help for availability.

```sh
gh pr edit PR_NUMBER --attach ./before.png --attach ./after.png
gh pr edit PR_NUMBER --attach ./demo.mp4
```

These append media. For placement, use `--body-file` with the full PR description and matching local Markdown references; `gh` substitutes uploaded URLs. Put video references in their own paragraph.

**Access.** Requires repository write access and OAuth/PAT authentication; GitHub App tokens are unsupported. Otherwise use browser attachments or report the blocker.

**Verify.** Confirm media renders. After partial failure, inspect existing uploads before retrying.

[GitHub attachment docs](https://docs.github.com/en/github-cli/github-cli/attaching-files-with-github-cli)
