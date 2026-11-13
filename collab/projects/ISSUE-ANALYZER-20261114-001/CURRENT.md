# Issue Analyzer — canonical dependency cleanup & first PUBLIC distribution

- updated_at: 2026-11-14 KST
- work_id: ISSUE-ANALYZER-20261114-001
- skill: issue-analyzer
- source_package: user supplied v0.11.49 (prior v0.11.48 preserved)
- local_candidate: issue-analyzer_v0_11_50_1114.zip
- package_size_bytes: 472290
- package_sha256: 597679ac819dd63b8344ec61d2dd4e1f8d699ba92c2dabcef436420376123aca
- local_package_crc_manifest: PASS (183 files, 182 per-file SHA-256 records)
- source_static_security_scan: PASS for specified key/token/IP/path patterns; not a universal non-disclosure proof
- change: remove obsolete knowledge provider alias and references from package; canonical ownership/slte role configuration remains; defaults to l1sw-dev-knowledge, parser defaults to sdm2-parser
- self_test: PARTIAL_PASS (7 new canonical tests, 7 parser tests and other focused regressions PASS; full runner INCOMPLETE at 120-second tool limit)
- independent_review: NOT_RUN (Claude code review has not been requested or executed)
- host_e2e: NOT_RUN (no proof of installed child skill ownership-resolve/query or sdm2-parser compatibility)
- delivery_repository: PUBLIC wonhwipark/L1Work, branch main, REPOSITORY ROOT
- intended_public_path: issue-analyzer_v0_11_50_1114.zip
- private_zip_upload: NOT_AUTHORIZED_AS_DELIVERY / NOT_POSTED; PRIVATE is for non-restricted work context and review metadata only
- public_release: NOT_POSTED (binary upload not supported by currently available GitHub connector; current release gates / independent review also outstanding)
- source_file_custody: ZIP remains in current ChatGPT conversation; no source ZIP committed to PRIVATE
- activation: NOT_RUN (public release != installation/activation)
- cutover: MIGRATION_NOT_CUTOVER; ACTIVE_PROVIDER=NONE (unchanged)

## User direction accepted (2026-11-14)
The first distribution of issue-analyzer is **PUBLIC L1Work/main root**, not the PRIVATE CoWork repository. Do not redirect a failed PUBLIC delivery to PRIVATE ZIP posting. Keep code editing/tests, independent Claude review, publication, host installation and E2E as separate status gates. The user approved the target repository; this does not backfill a missing review, remote commit, or host installation receipt.

## Verification and next action
The obsolete provider name has no file-level or runtime reference in the locally regenerated archive. An old explicit canonical skill name in an existing host is not silently rewritten; inspect the effective provider/role settings and replace as needed. Host skill API compatibility is not inferred from naming alone.
Next: complete missing full regression/review, then use a binary-capable public publisher to post the exact 472290-byte ZIP to L1Work/main root and read it back by SHA-256. Do not claim remote publication without that receipt.
