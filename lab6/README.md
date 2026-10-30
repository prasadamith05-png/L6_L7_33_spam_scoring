# L6_L7_33 — Spam Scoring Filter

**Lab 6: Code and Branch Coverage Analysis**

## About

A Python module that scores messages for spam signals, classifies them, and summarises the state of an inbox. This project achieves **100% Statement Coverage** and **100% Branch Coverage** with comprehensive unit test suites, detailed analysis reports, and terminal execution screenshots.

## Deliverables & Files

| File | Description |
|------|-------------|
| `spam_scoring.py` | The application module under test |
| `CodeCoverageTest_spam_scoring.py` | Targeted test cases achieving 100% code coverage |
| `BranchCoverageTest_spam_scoring.py` | Targeted test cases achieving 100% branch coverage |
| `test_spam_scoring.py` | Complete test suite covering all cases |
| `code_coverage_report.png` | Terminal output screenshot for code coverage |
| `branch_coverage_report.png` | Terminal output screenshot for branch coverage |
| `COVERAGE_REPORT.md` | Comprehensive coverage analysis and branch breakdown report |

## Running Coverage

```powershell
# 1. Run tests and measure line coverage:
coverage erase
coverage run -m pytest CodeCoverageTest_spam_scoring.py
coverage report -m

# 2. Run tests and measure branch coverage:
coverage erase
coverage run --branch -m pytest BranchCoverageTest_spam_scoring.py
coverage report -m
```
