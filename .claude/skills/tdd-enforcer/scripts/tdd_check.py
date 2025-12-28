#!/usr/bin/env python3
"""
TDD Compliance Checker - Detect code without corresponding tests.

Usage:
    python tdd_check.py <src_path> [--strict] [--tests PATH]

Exit codes:
    0 - All functions have tests (or non-strict mode)
    1 - Missing tests found (strict mode)
    2 - Configuration error
"""

import argparse
import ast
import sys
from dataclasses import dataclass, field
from pathlib import Path


@dataclass
class FunctionInfo:
    """Information about a function."""
    name: str
    line: int
    module: str


@dataclass
class ModuleReport:
    """Report for a single module."""
    module: str
    functions: list[FunctionInfo] = field(default_factory=list)
    tested: list[str] = field(default_factory=list)

    @property
    def missing(self) -> list[FunctionInfo]:
        """Get functions without tests."""
        return [f for f in self.functions if f.name not in self.tested]

    @property
    def coverage(self) -> float:
        """Get test coverage percentage."""
        if not self.functions:
            return 100.0
        return (len(self.tested) / len(self.functions)) * 100


def extract_functions(file_path: Path) -> list[FunctionInfo]:
    """Extract all public functions from a Python file."""
    functions: list[FunctionInfo] = []

    try:
        tree = ast.parse(file_path.read_text())
        module = str(file_path)

        for node in ast.walk(tree):
            if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip private functions
                if not node.name.startswith("_"):
                    functions.append(FunctionInfo(
                        name=node.name,
                        line=node.lineno,
                        module=module
                    ))
            elif isinstance(node, ast.ClassDef):
                # Skip private classes
                if not node.name.startswith("_"):
                    functions.append(FunctionInfo(
                        name=node.name,
                        line=node.lineno,
                        module=module
                    ))
                    # Also get public methods
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if not item.name.startswith("_"):
                                functions.append(FunctionInfo(
                                    name=f"{node.name}.{item.name}",
                                    line=item.lineno,
                                    module=module
                                ))
    except SyntaxError:
        pass

    return functions


def find_test_functions(test_dir: Path) -> set[str]:
    """Find all test function names in test directory."""
    tested: set[str] = set()

    if not test_dir.exists():
        return tested

    for test_file in test_dir.rglob("test_*.py"):
        try:
            tree = ast.parse(test_file.read_text())

            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                    if node.name.startswith("test_"):
                        # Extract the function being tested
                        # test_add_task -> add_task
                        # test_TaskManager_add_task -> TaskManager.add_task
                        name = node.name[5:]  # Remove 'test_'

                        # Handle class.method format
                        if "_" in name:
                            parts = name.split("_", 1)
                            if parts[0][0].isupper():  # Likely a class
                                tested.add(f"{parts[0]}.{parts[1]}")

                        tested.add(name)
        except SyntaxError:
            pass

    return tested


def analyze_module(src_file: Path, tested: set[str]) -> ModuleReport:
    """Analyze a module for test coverage."""
    functions = extract_functions(src_file)

    report = ModuleReport(module=str(src_file))
    report.functions = functions

    for func in functions:
        # Check various naming patterns
        name = func.name
        if name in tested:
            report.tested.append(name)
        elif name.replace(".", "_") in tested:
            report.tested.append(name)
        # Check without class prefix
        elif "." in name and name.split(".")[-1] in tested:
            report.tested.append(name)

    return report


def print_report(reports: list[ModuleReport], strict: bool) -> int:
    """Print formatted report and return exit code."""
    print()
    print("TDD Compliance Report")
    print("═" * 55)
    print(f"{'Module':<20}│ {'Functions':>9} │ {'Tested':>6} │ Status")
    print("─" * 20 + "┼" + "─" * 11 + "┼" + "─" * 8 + "┼" + "─" * 13)

    total_functions = 0
    total_tested = 0
    all_missing: list[tuple[str, FunctionInfo]] = []

    for report in reports:
        total_functions += len(report.functions)
        total_tested += len(report.tested)

        status = "✅ PASS" if not report.missing else "❌ FAIL"
        module_name = report.module
        if len(module_name) > 18:
            module_name = "..." + module_name[-15:]

        print(f"{module_name:<20}│ {len(report.functions):>9} │ {len(report.tested):>6} │ {status}")

        for func in report.missing:
            all_missing.append((report.module, func))

    print("═" * 55)

    coverage = (total_tested / total_functions * 100) if total_functions > 0 else 100
    print(f"Overall: {total_functions} functions, {total_tested} tested ({coverage:.0f}%)")
    print()

    if all_missing:
        print("Missing tests:")
        current_module = ""
        for module, func in all_missing:
            if module != current_module:
                print(f"  {module}:")
                current_module = module
            print(f"    - {func.name} (line {func.line})")
        print()

        print("📋 Recommendations:")
        print("  • Write tests BEFORE implementing these functions (TDD)")
        print("  • Run: /tdd-enforcer generate <module> to create test templates")
        print("  • Each test should follow: test_<function_name>")
        print()

        if strict:
            print("❌ TDD compliance check FAILED (strict mode)")
            return 1
    else:
        print("✅ All public functions have corresponding tests!")
        print()

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Check TDD compliance")
    parser.add_argument("src", help="Source directory to check")
    parser.add_argument("--strict", action="store_true", help="Exit with error if tests missing")
    parser.add_argument("--tests", default="tests", help="Test directory (default: tests/)")

    args = parser.parse_args()

    src_path = Path(args.src)
    test_path = Path(args.tests)

    if not src_path.exists():
        print(f"Error: Source path not found: {src_path}")
        return 2

    # Find all tested functions
    tested = find_test_functions(test_path)

    # Analyze each Python file
    reports: list[ModuleReport] = []

    if src_path.is_file():
        reports.append(analyze_module(src_path, tested))
    else:
        for py_file in sorted(src_path.rglob("*.py")):
            if "__pycache__" not in str(py_file):
                reports.append(analyze_module(py_file, tested))

    if not reports:
        print("No Python files found to analyze.")
        return 0

    return print_report(reports, args.strict)


if __name__ == "__main__":
    sys.exit(main())
