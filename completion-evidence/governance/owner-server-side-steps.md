# Owner Server-Side Steps

The following work must be completed by the repository owner in GitHub before
product completion branches are created.

## Bootstrap Pull Request

1. Push `governance/gate-integrity-hardening`.
2. Open a pull request into `main`.
3. Add the `governance-change` label.
4. Review the diff line by line.
5. Approve after the latest push.
6. Merge only after unchanged existing checks pass.
7. Record the merged `main` SHA as the hardened protected base.

The bootstrap pull request cannot be protected by Gate Integrity until
`gate-integrity.yml` exists on `main`.

## Branch Rulesets

Configure rulesets or branch protection for:

- `main`
- `release/*`
- `Mac/iOS`
- `windows-cpp`

Required settings:

- require pull requests;
- prohibit direct pushes;
- prohibit force pushes;
- prohibit branch deletion;
- require at least one approval;
- require CODEOWNER approval;
- dismiss stale approvals after new commits;
- require latest-push approval;
- require all conversations resolved;
- require up-to-date branches;
- require no bypass actors;
- require linear history unless separately approved by the owner;
- restrict ruleset edits to owner-controlled governance changes.

Required checks:

- Alignment check
- Canonical semantic integrity check
- Math integrity check
- Check for AI Attribution
- Docs maintenance check
- Wiki maintenance check
- Gate Integrity
- Release Readiness when present

## Tag Rulesets

Make release tags immutable:

- `aps-v*`
- `aps-ios-v*`
- `aps-macos-v*`
- `aps-windows-v*`

Block tag force updates and tag deletion.

## Evidence To Capture

- ruleset name and ID;
- branch and tag target patterns;
- required check list;
- required review and CODEOWNER settings;
- latest-push approval setting;
- bypass actor list showing none;
- force-push and deletion settings;
- CODEOWNERS contents;
- timestamp;
- hardened protected base SHA;
- owner confirmation.
