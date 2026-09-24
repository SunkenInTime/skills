# Uploading PR artifacts

Use GitHub CLI's `--attach` flag for images and videos. Check `gh pr edit --help` for support; it shipped in v2.99.0. If absent, update through the official installation method.

Write the PR description to a Markdown file, with labeled before/after image references such as `![Before](./before.png)`. For a video player, put `![](./demo.mp4)` in its own paragraph. Pass the same paths to `--attach`; GitHub CLI replaces the local references with uploaded URLs.

```sh
gh pr create --title 'Fix the reported problem' --body-file ./pr-body.md --attach ./before.png --attach ./after.png
```

To append a recording while preserving an existing PR body:

```sh
gh pr edit PR_NUMBER --attach ./demo.mp4
```

Repeat `--attach` for multiple files. Uploads require write access to the target repository and an OAuth token or supported personal access token; GitHub App tokens are unsupported. For an upstream contribution without write access, use GitHub's browser attachment UI if available, or report the upload blocker.

After uploading, inspect the PR and confirm the media renders. On partial failure, inspect what succeeded before retrying; a failed command can still create the PR or attach some files.

Sources: [GitHub attachment guide](https://docs.github.com/en/github-cli/github-cli/attaching-files-with-github-cli), [CLI attachment requirements](https://github.com/cli/cli/blob/trunk/skills/gh/SKILL.md).
