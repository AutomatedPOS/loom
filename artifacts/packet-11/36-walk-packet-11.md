# Walk packet 11 — 2026-09-02

Sitting 10, part 2.

## Locks

- Local commit hook is advisory. It warns. It does not block.
- Hard gate is GitHub Actions on the pull request into the branch
  the renderer reads, with branch protection.
- Public repo.
- CODEOWNERS per folder.
- Schema sits beside the file it validates. Same commit, relative path.
- Python is the reference validator. PowerShell and VALIDATE.md are
  conformance targets, not peers.
- The shuttle opens a pull request. Not write-in-place.

## Process faults recorded this sitting

See the pain-log artifact. Nodes `pain-29`, `pain-30`, `pain-31`.
