# Wiki Source Directory

This directory stores the version-controlled source for the GitHub Wiki pages for `flynn33/ASH-Pattern-System`.

This file (`wiki/README.md`) is the repo-side directory readme: it is not part of the required wiki page set. The on-push sync mirrors the whole `wiki/` directory into the GitHub Wiki, so this file is pushed there too, but GitHub renders `Home.md` (not this file) as the wiki landing page.

- Keep page names stable.
- Update wiki pages when canonical docs/specs/governance/handoff-templates or the CI surfaces (`.github/workflows`, `.github/scripts`) materially change. See the [Wiki Maintenance Playbook](Wiki-Maintenance-Playbook) for the authoritative update-trigger list.
- Validate with: `python3 .github/scripts/wiki_maintenance_check.py`

See also: [Wiki Maintenance Playbook](Wiki-Maintenance-Playbook).
