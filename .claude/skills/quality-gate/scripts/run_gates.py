#!/usr/bin/env python3
"""
Quality Gate Runner - Execute all quality checks and report results.

Usage:
    python run_gates.py [--fix] [--gate NAME] [--strict] [--src PATH]

Exit codes:
    0 - All gates passed
    1 - One or more gates failed
    2 - Configuration error
"""

import argparse
import ast
import subprocess
import sys
from dataclasses import dataclass
from enum import Enum
from pathlib import Path
from typing import Optional


class GateStatus(Enum):
    """Status of a quality gate."""
    PASS = "PASS"
    FAIL = "FAIL"
    SKIP = "SKIP"


@dataclass
class GateResult:
    """Result of running a quality gate."""
    name: str
    status: GateStatus
    details: str
    output: str = ""


def run_command(cmd: list[str], capture: bool = True) -> tuple[int, str, str]:
    """Run a command and return exit code, stdout, stderr."""
    try:
        result = subprocess.run(
            cmd,
            capture_output=capture,
            text=True,
            timeout=300  # 5 minute timeout
        )
        return result.returncode, result.stdout, result.stderr
    except FileNotFoundError:
        return -1, "", f"Command not found: {cmd[0]}"
    except subprocess.TimeoutExpired:
        return -2, "", "Command timed out"


def check_tool_available(tool: str) -> bool:
    """Check if a tool is available via uv run."""
    code, _, _ = run_command(["uv", "run", "which", tool])
    if code != 0:
        # Try direct which
        code, _, _ = run_command(["which", tool])
    return code == 0


def run_test_gate() -> GateResult:
    """Run pytest and return result."""
    if not check_tool_available("pytest"):
        return GateResult("Test Gate", GateStatus.SKIP, "pytest not installed")

    code, stdout, stderr = run_command(["uv", "run", "pytest", "-v", "--tb=short"])

    if code == 0:
        # Count passed tests
        lines = stdout.split("\n")
        for line in lines:
            if "passed" in line:
                return GateResult("Test Gate", GateStatus.PASS, line.strip(), stdout)
        return GateResult("Test Gate", GateStatus.PASS, "All tests passed", stdout)
    elif code == 5:  # No tests collected
        return GateResult("Test Gate", GateStatus.PASS, "No tests found (0 collected)", stdout)
    else:
        # Extract failure summary
        lines = stdout.split("\n")
        for line in lines:
            if "failed" in line.lower() or "error" in line.lower():
                return GateResult("Test Gate", GateStatus.FAIL, line.strip(), stdout)
        return GateResult("Test Gate", GateStatus.FAIL, "Tests failed", stdout + stderr)


def run_type_gate(src_path: str) -> GateResult:
    """Run mypy --strict and return result."""
    if not check_tool_available("mypy"):
        return GateResult("Type Gate", GateStatus.SKIP, "mypy not installed")

    if not Path(src_path).exists():
        return GateResult("Type Gate", GateStatus.SKIP, f"{src_path}/ not found")

    code, stdout, stderr = run_command(["uv", "run", "mypy", "--strict", src_path])

    if code == 0:
        return GateResult("Type Gate", GateStatus.PASS, "No type errors", stdout)
    else:
        # Count errors
        error_count = stdout.count(": error:")
        if error_count > 0:
            return GateResult("Type Gate", GateStatus.FAIL, f"{error_count} type errors", stdout)
        return GateResult("Type Gate", GateStatus.FAIL, "Type check failed", stdout + stderr)


def run_lint_gate(src_path: str, fix: bool = False) -> GateResult:
    """Run ruff check and return result."""
    if not check_tool_available("ruff"):
        return GateResult("Lint Gate", GateStatus.SKIP, "ruff not installed")

    if not Path(src_path).exists():
        return GateResult("Lint Gate", GateStatus.SKIP, f"{src_path}/ not found")

    cmd = ["uv", "run", "ruff", "check", src_path]
    if fix:
        cmd.append("--fix")

    code, stdout, stderr = run_command(cmd)

    if code == 0:
        if fix and "Fixed" in stdout:
            return GateResult("Lint Gate", GateStatus.PASS, "Issues auto-fixed", stdout)
        return GateResult("Lint Gate", GateStatus.PASS, "No lint violations", stdout)
    else:
        # Count violations
        lines = [l for l in stdout.split("\n") if l.strip()]
        violation_count = len([l for l in lines if src_path in l])
        return GateResult("Lint Gate", GateStatus.FAIL, f"{violation_count} violations", stdout)


def run_doc_gate(src_path: str) -> GateResult:
    """Check docstring coverage and return result."""
    if not Path(src_path).exists():
        return GateResult("Doc Gate", GateStatus.SKIP, f"{src_path}/ not found")

    missing: list[str] = []

    for py_file in Path(src_path).rglob("*.py"):
        try:
            tree = ast.parse(py_file.read_text())
            for node in ast.walk(tree):
                if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
                    # Skip private/magic methods
                    if node.name.startswith("_"):
                        continue
                    # Check for docstring
                    docstring = ast.get_docstring(node)
                    if not docstring:
                        missing.append(f"{py_file}:{node.lineno} {node.name}")
        except SyntaxError:
            pass  # Skip files with syntax errors

    if not missing:
        return GateResult("Doc Gate", GateStatus.PASS, "All public functions documented")
    else:
        details = f"{len(missing)} missing docstrings"
        output = "Missing docstrings:\n" + "\n".join(f"  {m}" for m in missing[:10])
        if len(missing) > 10:
            output += f"\n  ... and {len(missing) - 10} more"
        return GateResult("Doc Gate", GateStatus.FAIL, details, output)


def print_report(results: list[GateResult], strict: bool = False) -> int:
    """Print formatted report and return exit code."""
    print()
    print("╔" + "═" * 60 + "╗")
    print("║" + "QUALITY GATE REPORT".center(60) + "║")
    print("╠" + "═" * 60 + "╣")
    print("║  Gate        │ Status  │ Details" + " " * 24 + "║")
    print("╠" + "─" * 14 + "┼" + "─" * 9 + "┼" + "─" * 35 + "╣")

    failed = 0
    skipped = 0

    for result in results:
        if result.status == GateStatus.PASS:
            status = "✅ PASS"
        elif result.status == GateStatus.FAIL:
            status = "❌ FAIL"
            failed += 1
        else:
            status = "⏭ SKIP"
            skipped += 1
            if strict:
                failed += 1

        name = result.name.ljust(12)
        details = result.details[:33].ljust(33)
        print(f"║  {name}│ {status} │ {details}║")

    print("╠" + "═" * 60 + "╣")

    if failed == 0:
        overall = "✅ PASS"
        summary = "All gates passed"
    else:
        overall = "❌ FAIL"
        summary = f"{failed} gate(s) failed"
        if skipped > 0 and not strict:
            summary += f", {skipped} skipped"

    print(f"║  {'OVERALL'.ljust(12)}│ {overall} │ {summary.ljust(33)}║")
    print("╚" + "═" * 60 + "╝")
    print()

    # Print detailed output for failures
    for result in results:
        if result.status == GateStatus.FAIL and result.output:
            print(f"─── {result.name} Details ───")
            print(result.output[:500])  # Limit output
            if len(result.output) > 500:
                print("... (truncated)")
            print()

    # Recommendations
    if failed > 0:
        print("📋 Recommendations:")
        for result in results:
            if result.status == GateStatus.FAIL:
                if "Test" in result.name:
                    print("  • Fix failing tests before committing")
                elif "Type" in result.name:
                    print("  • Run: uv run mypy --strict src/ to see all type errors")
                elif "Lint" in result.name:
                    print("  • Run: uv run ruff check src/ --fix to auto-fix issues")
                elif "Doc" in result.name:
                    print("  • Add docstrings to listed functions")
            elif result.status == GateStatus.SKIP:
                if "pytest" in result.details:
                    print("  • Install pytest: uv add --dev pytest")
                elif "mypy" in result.details:
                    print("  • Install mypy: uv add --dev mypy")
                elif "ruff" in result.details:
                    print("  • Install ruff: uv add --dev ruff")
        print()
    else:
        print("✨ All quality gates passed! Safe to commit.")
        print()

    return 0 if failed == 0 else 1


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Run quality gates")
    parser.add_argument("--fix", action="store_true", help="Auto-fix lint issues")
    parser.add_argument("--gate", choices=["test", "type", "lint", "doc"], help="Run specific gate")
    parser.add_argument("--strict", action="store_true", help="Treat SKIP as FAIL")
    parser.add_argument("--src", default="src", help="Source directory (default: src/)")

    args = parser.parse_args()

    results: list[GateResult] = []

    # Run gates
    if args.gate is None or args.gate == "test":
        print("🧪 Running Test Gate...")
        results.append(run_test_gate())

    if args.gate is None or args.gate == "type":
        print("📝 Running Type Gate...")
        results.append(run_type_gate(args.src))

    if args.gate is None or args.gate == "lint":
        print("🔍 Running Lint Gate...")
        results.append(run_lint_gate(args.src, args.fix))

    if args.gate is None or args.gate == "doc":
        print("📚 Running Doc Gate...")
        results.append(run_doc_gate(args.src))

    return print_report(results, args.strict)


if __name__ == "__main__":
    sys.exit(main())
