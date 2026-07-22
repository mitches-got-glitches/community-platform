---
name: commit
description: Create atomic, Conventional-Commits-formatted git commit(s) for the current changes in this repo. Use when the user asks to commit changes, split a diff into logical commits, or write/check a commit message.
---

# Commit

Follow this repo's [commit conventions guide](../../../docs/guides/commit-conventions.md):
atomic commits (one logical change per commit), formatted as Conventional Commits.

## Current state
- Status: !`git status`
- Diff (staged + unstaged): !`git diff HEAD`
- Recent log style: !`git log --oneline -10`

## Procedure
1. Read the diff above. Group the changes into the smallest set of **atomic** commits:
   each commit does one describable thing, and the repo is in a working state after
   every commit. Don't split one logical change into "half a fix."
2. If unrelated changes are mixed together, commit them separately — never bundle
   unrelated concerns for convenience.
3. Stage only what belongs to each commit (`git add <path>`, or `git add -p` for
   partial-file splits) — never `git add -A`/`git add .` blindly.
4. Write each message as:
   ```
   <type>(<scope>): <description>

   [optional body — the why, not the what]

   [optional footer — e.g. Refs: #<issue>]
   ```
   - `type`: feat, fix, docs, chore, refactor, style, test, build, ci, perf, revert.
   - `scope`: match this repo's issue-label vocabulary where it fits — infra, nextcloud,
     backups, security, collab, monitoring, onboarding, governance, docs.
   - `description`: imperative, lower-case, no trailing period.
   - Mark breaking changes with `!` before the colon or a `BREAKING CHANGE:` footer —
     applies if a change reverses an ADR decision or obsoletes a documented runbook.
5. End every message with the `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>`
   trailer, per this repo's standing git instructions.
6. If the split into commits isn't obvious from the request, state the planned commits
   (and order) before running anything. Create them one at a time via a heredoc commit
   message, and check `git status` after the last one.

Never amend, force-push, or use `--no-verify` unless explicitly asked. Only commit when
the user has actually asked for a commit — loading this skill is not, by itself, that ask.
