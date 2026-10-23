# AI assistance log — TrustVault

Record the prompts actually used during development. Edit this file honestly; do not claim prompts or tests that did not happen.

## Prompt 1
Help me plan a Flask document-sharing app with registration, login, roles, company-level data isolation, secure file upload, document sharing, audit logs, and SHA-256 integrity checks.

## Prompt 2
Explain each generated or modified section of the TrustVault code in beginner-friendly language and help me test it.

## Changes and corrections
- Add each real error encountered and the fix made.
- Add any features changed after testing.

## Testing
- [ ] Registration and login
- [ ] Normal user cannot open admin audit page
- [ ] Users in different companies cannot see each other's documents
- [ ] Only owner can share a document
- [ ] Only owner, authorized recipient, or same-company admin can download
- [ ] SHA-256 integrity check succeeds on unchanged file
- [ ] Live URL tested in a private/incognito window
