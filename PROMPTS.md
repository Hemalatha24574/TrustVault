## Testing
- [x] Registration and login
- [x] Normal user cannot open admin audit page (HTTP 403)
- [x] Different-company dashboard showed no documents
- [ ] Only owner can share a document
- [ ] Only owner, authorized recipient, or same-company admin can download
- [x] SHA-256 integrity check succeeds on unchanged file (confirmed in audit event)

Record the prompts actually used during development. Edit this file honestly; do not claim prompts or tests that did not happen.

## Prompt 1
Help me plan a Flask document-sharing app with registration, login, roles, company-level data isolation, secure file upload, document sharing, audit logs, and SHA-256 integrity checks.

## Prompt 2
Explain each generated or modified section of the TrustVault code in beginner-friendly language and help me test it.

## Changes and corrections
- Registered three accounts on the live Render website.
- Uploaded sample.txt and shared it with another user in the same company.
- Verified that the recipient could see and download the shared document.
- Confirmed the audit trail recorded upload, share, and download events.
- Confirmed the download audit event reported integrity verified.
- Confirmed a normal user received HTTP 403 when opening the admin audit page.
- Confirmed the OtherCompany dashboard showed no documents.

## Testing
- [x] Registration and login
- [x] Normal user cannot open admin audit page (HTTP 403)
- [x] Different-company dashboard showed no documents
- [ ] Only owner can share a document
- [ ] Only owner, authorized recipient, or same-company admin can download
- [x] SHA-256 integrity check succeeds on unchanged file(confirmed in audit event)
- [x] Live URL tested in a private/incognito window; login and dashboard worked
