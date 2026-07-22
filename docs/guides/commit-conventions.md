# Commit conventions

Two combined disciplines govern commits in this repo: **atomic commits** and the
**Conventional Commits** message format. For a bus-factor-1 project, `git log` is part
of the documentation — a clean history is how a second admin (or future-you) understands
*why* the infra evolved, not just what changed.

Sources: [Atomic Git Commits](https://dev.to/samuelfaure/how-atomic-git-commits-dramatically-increased-my-productivity-and-will-increase-yours-too-4a84) (Samuel Faure) · [Conventional Commits v1.0.0](https://www.conventionalcommits.org/en/v1.0.0/).

## Atomic commits

A commit is atomic when it does **one, describable thing**, and the repo is left in a
working state afterwards — "as small as possible, but complete." Size isn't the
criterion; scope is.

- **One concern per commit.** If you can't summarise it in one sentence, it's probably
  two commits.
- **Complete, not fragmented.** Don't split a single logical change into a "part 1 that
  breaks things, part 2 that fixes them" — each commit should leave things working.
- **Unrelated changes go in separate commits**, even if you noticed them in the same
  sitting (a docs fix spotted while working on infra is its own commit).
- **Plan before staging.** Think of the work as a staircase you can't see the top of —
  focus on the next step, commit it, move to the next. Break the task into that sequence
  before you start typing.
- **Stage deliberately**: `git add <specific files>` or `git add -p` for partial-file
  splits — not `git add -A`/`git add .`, which pulls in whatever else happens to be dirty.

**Why bother:** atomic commits are independently revertible, make code review tractable
(a reviewer assesses one concern, not a pile), and are what makes `git bisect` actually
useful. One feature/task can still span several commits — that's normal — it just means
one PR, several atomic commits, not one giant one.

## Conventional Commits format

```
<type>[optional scope]: <description>

[optional body]

[optional footer(s)]
```

**Type** — `fix` (patches a bug) and `feat` (new feature) are the two the spec singles
out; everything else follows the common (Angular) convention: `build`, `chore`, `ci`,
`docs`, `style`, `refactor`, `perf`, `test`, `revert`. This repo is infra/docs-heavy, so
expect to reach for `docs`, `chore`, `refactor`, and `ci` more often than `feat`/`fix` —
the full set stays available for when app-layer work happens (e.g. Nextcloud
customisation).

**Scope** — a noun for the area touched, in parentheses: `feat(parser): ...`. In this
repo, prefer the same vocabulary as the GitHub issue `area:` labels, so scopes and issue
labels line up: `infra`, `nextcloud`, `backups`, `security`, `collab`, `monitoring`,
`onboarding`, `governance`, `docs`.

**Description** — imperative, lower-case, no trailing period: `add restore runbook`, not
`Added the restore runbook.`.

**Body** — free-form, one blank line after the description. Explain *why*, not *what* —
the diff already shows what changed.

**Footer** — `Token: value` lines, one blank line after the body. Multi-word tokens use
hyphens (`Acked-by`, `Depends-on`), except `BREAKING CHANGE` which stays as-is. In this
repo, reference the relevant GitHub issue: `Refs: #12` (mirrors the `Parent: #1` /
`Depends on: #10` style already used in issue bodies).

**Breaking changes** — mark with `!` before the colon (`refactor(infra)!: ...`) **or** a
`BREAKING CHANGE:` footer (or both). Rare here, but applies when a change reverses an ADR
decision or obsoletes a documented runbook/procedure. Everything in the spec is
case-insensitive **except** `BREAKING CHANGE`, which must be uppercase.

## Applied in this repo

- Existing history already leans this way informally
  (`docs: add disaster-recovery restore runbook (DOC-2)`) — this guide makes it the
  standard rather than a coincidence.
- Still follow the repo's standing git safety rules: only commit when explicitly asked,
  never `--amend` a commit that's already been pushed, review the staged diff before
  committing, keep the `Co-Authored-By: Claude Sonnet 5 <noreply@anthropic.com>` trailer.
- The [`/commit`](../../.claude/skills/commit/SKILL.md) skill applies this guide
  automatically when drafting commits in this repo.

## Examples

```
feat(collab): enable Collectives wiki app

fix(backups): correct BorgBase prune schedule cron syntax

Refs: #20
```

```
docs(infra): record OpenTofu VPS provisioning decision

Refs: #10
```

```
refactor(infra)!: replace manual Hetzner Console setup with OpenTofu

BREAKING CHANGE: rebuilding the VPS now requires `tofu apply`; the
old manual runbook steps for server creation no longer apply.
```
