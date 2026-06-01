# Contributing

Thanks for helping maintain `neo4j-python-pandas-py2neo-v3`.

This repository is maintained as a legacy py2neo v3 / Neo4j 3.x educational example. Contributions should keep that baseline clear unless they are explicitly scoped as modernization work.

## Scope

Good contributions include:

- documentation improvements
- setup notes for the supported legacy environment
- reproducible bug reports
- small fixes that keep the py2neo v3 example working
- tests or smoke checks for Excel extraction and relationship generation
- clearly documented migration notes for newer Python, pandas, Neo4j, or py2neo versions

Avoid broad rewrites unless they are discussed in an issue first.

## Before Opening An Issue

Search existing issues first. If you are reporting a bug or compatibility problem, include:

- Python version
- Neo4j version
- py2neo version
- operating system
- installation command
- command you ran
- full traceback or screenshot
- whether you used `Invoice_data_Demo.xls` or custom data

## Pull Requests

1. Open an issue first for behavior changes or dependency modernization.
2. Keep pull requests focused on one topic.
3. Update README or CHANGELOG when behavior, setup, or compatibility changes.
4. Prefer small, reviewable diffs over large rewrites.
5. Explain how you tested the change.

## Legacy Compatibility

The known baseline remains Python 3.6.5, Windows 10, Neo4j 3.x, and py2neo 3. Modern dependency support is tracked separately so legacy users do not lose a working reference example without a migration path.
