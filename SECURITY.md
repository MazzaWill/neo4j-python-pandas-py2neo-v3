# Security Policy

## Supported Versions

This project is maintained as a legacy educational example for py2neo v3 and Neo4j 3.x.

| Version | Supported |
| --- | --- |
| v0.2.x | Maintenance and documentation support |
| Older snapshots | Not actively supported |

The dependency set is intentionally legacy. Known dependency risk is tracked in the public modernization issue so users can understand the tradeoff before running old packages.

## Reporting A Vulnerability

Please do not post exploitable security details in a public issue.

Report security concerns by opening a private GitHub security advisory for this repository if available. If that is not available, open a public issue with a minimal description that says a security report is available and avoid including exploit details.

Please include:

- affected file or dependency
- affected version
- impact summary
- reproduction notes, if safe to share privately
- suggested fix or mitigation, if known

## Maintenance Expectations

Security fixes will be evaluated against the legacy compatibility goal. If a safe dependency update breaks the original py2neo v3 environment, the fix may be documented as a migration path rather than merged into the legacy baseline immediately.
