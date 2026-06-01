# Changelog

## v0.3.1 - Project Positioning Polish

Release date: 2026-06-01

### Changed

- Updated the project display title to `Excel to Neo4j Knowledge Graph` while keeping the historical repository slug unchanged.
- Reworked the root English and Chinese README introductions to position the project as both a legacy py2neo v3 example and a modern Neo4j GraphRAG/vector-search example.
- Updated GitHub repository metadata to use the clearer project description.

## v0.3.0 - Modern Neo4j GraphRAG Example

Release date: 2026-06-01

### Added

- Added `examples/modern_invoice_graphrag/`, a modern invoice graph example based on the original Excel dataset idea.
- Added official Neo4j Python driver integration through a new CLI.
- Added Neo4j vector index and `db.index.vector.queryNodes` search Cypher.
- Added deterministic local embeddings for keyless demos and CI.
- Added optional `neo4j-graphrag[openai]` requirements for production GraphRAG embedding paths.
- Added English and Simplified Chinese documentation for the modern example.
- Added offline unit tests for invoice normalization, embeddings, and Cypher.

### Changed

- Linked the modern example from the root English and Chinese README files.
- Extended maintenance checks to compile and test the modern example.

## v0.2.2 - README Language Split

Release date: 2026-06-01

### Changed

- Reworked `README.md` as the English-first project entry point for international open-source review.
- Moved the full Simplified Chinese documentation to `README.zh-CN.md`.
- Added language switch links between English and Simplified Chinese documentation.

## v0.2.1 - OSS Maintenance Metadata

Release date: 2026-06-01

### Added

- Added MIT license.
- Added contributing guide, security policy, support policy, and code of conduct.
- Added issue templates for bug reports, compatibility questions, and sample-data requests.
- Added pull request template and CODEOWNERS.
- Added lightweight GitHub Actions maintenance check for Python syntax.
- Linked project governance files from the README.

## v0.2.0 - Maintenance Restart

Release date: 2026-06-01

This release marks the restart of active maintenance for the project.

### Documentation

- Documented the current maintenance status.
- Added compatibility notes for the original Python 3.6 / Neo4j 3.x / py2neo v3 environment.
- Added quick-start notes for the demo Excel file, local path configuration, and Neo4j credentials.
- Added a roadmap for issue triage, reproducible examples, tests, and modernization.

### Maintenance

- Started triaging historical issues in batches.
- Kept the project scope focused on the legacy py2neo v3 knowledge graph example while modernization work is evaluated.
