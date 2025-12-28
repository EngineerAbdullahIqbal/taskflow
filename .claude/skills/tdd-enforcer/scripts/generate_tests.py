#!/usr/bin/env python3
"""
Test Template Generator - Create test file stubs from source code.

Usage:
    python generate_tests.py <source_file> [--output PATH]

Exit codes:
    0 - Test file generated successfully
    1 - Error generating tests
    2 - Source file not found
"""

import argparse
import ast
import sys
from dataclasses import dataclass
from pathlib import Path
from typing import Optional


@dataclass
class FunctionSignature:
    """Information about a function signature."""
    name: str
    args: list[str]
    returns: Optional[str]
    is_method: bool
    class_name: Optional[str]
    docstring: Optional[str]


def extract_signatures(file_path: Path) -> list[FunctionSignature]:
    """Extract function signatures from a Python file."""
    signatures: list[FunctionSignature] = []

    try:
        tree = ast.parse(file_path.read_text())

        for node in ast.walk(tree):
            if isinstance(node, ast.ClassDef):
                if not node.name.startswith("_"):
                    # Add class itself
                    signatures.append(FunctionSignature(
                        name=node.name,
                        args=[],
                        returns=None,
                        is_method=False,
                        class_name=None,
                        docstring=ast.get_docstring(node)
                    ))

                    # Add public methods
                    for item in node.body:
                        if isinstance(item, (ast.FunctionDef, ast.AsyncFunctionDef)):
                            if not item.name.startswith("_"):
                                args = [a.arg for a in item.args.args if a.arg != "self"]
                                returns = None
                                if item.returns:
                                    returns = ast.unparse(item.returns)

                                signatures.append(FunctionSignature(
                                    name=item.name,
                                    args=args,
                                    returns=returns,
                                    is_method=True,
                                    class_name=node.name,
                                    docstring=ast.get_docstring(item)
                                ))

            elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
                # Skip if inside a class (already handled)
                if not any(isinstance(parent, ast.ClassDef) for parent in ast.walk(tree)):
                    if not node.name.startswith("_"):
                        args = [a.arg for a in node.args.args]
                        returns = None
                        if node.returns:
                            returns = ast.unparse(node.returns)

                        signatures.append(FunctionSignature(
                            name=node.name,
                            args=args,
                            returns=returns,
                            is_method=False,
                            class_name=None,
                            docstring=ast.get_docstring(node)
                        ))

    except SyntaxError as e:
        print(f"Syntax error in {file_path}: {e}")

    return signatures


def generate_test_content(module_name: str, signatures: list[FunctionSignature]) -> str:
    """Generate test file content."""
    lines = [
        '"""',
        f'Tests for {module_name}.',
        '',
        'Following TDD: Write these tests FIRST, then implement.',
        '"""',
        '',
        'import pytest',
        '',
        f'from src.{module_name} import *',
        '',
        '',
    ]

    classes_seen: set[str] = set()

    for sig in signatures:
        if sig.class_name and sig.class_name not in classes_seen:
            classes_seen.add(sig.class_name)
            lines.append(f'class Test{sig.class_name}:')
            lines.append(f'    """Tests for {sig.class_name} class."""')
            lines.append('')

        if sig.is_method:
            # Method test
            test_name = f"test_{sig.name}"
            lines.append(f'    def {test_name}(self) -> None:')
            lines.append(f'        """Test {sig.class_name}.{sig.name}."""')
            lines.append('        # Arrange')
            lines.append(f'        instance = {sig.class_name}()')
            lines.append('')
            lines.append('        # Act')
            if sig.args:
                args_str = ", ".join(f"{a}=..." for a in sig.args)
                lines.append(f'        result = instance.{sig.name}({args_str})')
            else:
                lines.append(f'        result = instance.{sig.name}()')
            lines.append('')
            lines.append('        # Assert')
            lines.append('        assert result is not None  # TODO: Add specific assertion')
            lines.append('')

        elif sig.class_name is None and not sig.is_method:
            if sig.name[0].isupper():
                # Class test
                lines.append(f'class Test{sig.name}:')
                lines.append(f'    """Tests for {sig.name} class."""')
                lines.append('')
                lines.append(f'    def test_{sig.name.lower()}_creation(self) -> None:')
                lines.append(f'        """Test {sig.name} can be instantiated."""')
                lines.append('        # Arrange & Act')
                lines.append(f'        instance = {sig.name}()')
                lines.append('')
                lines.append('        # Assert')
                lines.append('        assert instance is not None')
                lines.append('')
            else:
                # Function test
                test_name = f"test_{sig.name}"
                lines.append(f'def {test_name}() -> None:')
                lines.append(f'    """Test {sig.name} function."""')
                lines.append('    # Arrange')
                if sig.args:
                    for arg in sig.args:
                        lines.append(f'    {arg} = ...  # TODO: Set up test data')
                lines.append('')
                lines.append('    # Act')
                if sig.args:
                    args_str = ", ".join(sig.args)
                    lines.append(f'    result = {sig.name}({args_str})')
                else:
                    lines.append(f'    result = {sig.name}()')
                lines.append('')
                lines.append('    # Assert')
                if sig.returns:
                    lines.append(f'    assert isinstance(result, {sig.returns})  # TODO: Add specific assertion')
                else:
                    lines.append('    assert result is not None  # TODO: Add specific assertion')
                lines.append('')
                lines.append('')

    return "\n".join(lines)


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Generate test templates")
    parser.add_argument("source", help="Source file to generate tests for")
    parser.add_argument("--output", "-o", help="Output directory (default: tests/unit/)")

    args = parser.parse_args()

    source_path = Path(args.source)

    if not source_path.exists():
        print(f"Error: Source file not found: {source_path}")
        return 2

    # Extract module name
    module_name = source_path.stem

    # Determine output path
    if args.output:
        output_dir = Path(args.output)
    else:
        output_dir = Path("tests/unit")

    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"test_{module_name}.py"

    # Check if file exists
    if output_path.exists():
        print(f"Warning: Test file already exists: {output_path}")
        print("Appending new tests...")

    # Extract signatures
    signatures = extract_signatures(source_path)

    if not signatures:
        print(f"No public functions found in {source_path}")
        return 0

    # Generate content
    content = generate_test_content(module_name, signatures)

    # Write file
    if output_path.exists():
        # Append new tests
        existing = output_path.read_text()
        content = existing + "\n\n# === NEW TESTS ===\n\n" + content

    output_path.write_text(content)

    print(f"Generated: {output_path}")
    print()
    print("Template includes:")
    for sig in signatures:
        if sig.is_method:
            print(f"  - test_{sig.name} ({sig.class_name}.{sig.name})")
        else:
            print(f"  - test_{sig.name}")
    print()
    print("Next steps:")
    print("  1. Fill in test data (replace ... with actual values)")
    print("  2. Add specific assertions")
    print("  3. Run: uv run pytest to verify tests FAIL (RED)")
    print("  4. Implement the code")
    print("  5. Run: uv run pytest to verify tests PASS (GREEN)")

    return 0


if __name__ == "__main__":
    sys.exit(main())
