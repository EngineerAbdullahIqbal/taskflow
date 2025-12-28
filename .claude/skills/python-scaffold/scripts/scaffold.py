#!/usr/bin/env python3
"""
Python Scaffold Generator - Create constitution-compliant Python structure.

Usage:
    python scaffold.py module <name>
    python scaffold.py service <name>
    python scaffold.py project <path>

Exit codes:
    0 - Success
    1 - Error
    2 - File exists (without --force)
"""

import argparse
import sys
from pathlib import Path
from typing import NamedTuple


class FileContent(NamedTuple):
    """File path and content to generate."""
    path: Path
    content: str


# Templates
MODULE_TEMPLATE = '''"""
{name} module.

Provides {name} functionality.
"""

from typing import Optional


__all__: list[str] = []
'''

SERVICE_TEMPLATE = '''"""
{name_title} Service implementation.

Handles {name} business logic.
"""

from typing import Optional

from .protocols import {name_title}Protocol


class {name_title}Service:
    """Implementation of {name_title}Protocol."""

    def __init__(self) -> None:
        """Initialize the service."""
        pass
'''

PROTOCOL_TEMPLATE = '''"""
Service protocols (interfaces).

Define abstract interfaces for dependency injection.
"""

from typing import Protocol, runtime_checkable


@runtime_checkable
class {name_title}Protocol(Protocol):
    """Interface for {name} operations."""

    pass
'''

TEST_MODULE_TEMPLATE = '''"""
Tests for {name} module.

Following TDD: Write tests FIRST.
"""

import pytest

from src.{name} import *


class Test{name_title}:
    """Tests for {name} module."""

    def test_placeholder(self) -> None:
        """TODO: Replace with actual tests."""
        # Arrange

        # Act

        # Assert
        assert True  # TODO: Add real assertion
'''

TEST_SERVICE_TEMPLATE = '''"""
Tests for {name_title}Service.

Following TDD: Write tests FIRST.
"""

import pytest

from src.services.{name}_service import {name_title}Service


class Test{name_title}Service:
    """Tests for {name_title}Service."""

    @pytest.fixture
    def service(self) -> {name_title}Service:
        """Create fresh service instance."""
        return {name_title}Service()

    def test_service_creation(self, service: {name_title}Service) -> None:
        """Test service can be instantiated."""
        # Assert
        assert service is not None
'''

INIT_TEMPLATE = '''"""
{description}
"""

__all__: list[str] = []
'''


def to_title(name: str) -> str:
    """Convert name to TitleCase."""
    return "".join(word.capitalize() for word in name.split("_"))


def scaffold_module(name: str, dry_run: bool, force: bool, no_tests: bool) -> int:
    """Create module structure."""
    name_title = to_title(name)

    files: list[FileContent] = [
        FileContent(
            Path(f"src/{name}.py"),
            MODULE_TEMPLATE.format(name=name)
        ),
    ]

    # Check if __init__.py exists, if not create it
    init_path = Path("src/__init__.py")
    if not init_path.exists():
        files.append(FileContent(
            init_path,
            INIT_TEMPLATE.format(description="Source package.")
        ))

    if not no_tests:
        files.append(FileContent(
            Path(f"tests/unit/test_{name}.py"),
            TEST_MODULE_TEMPLATE.format(name=name, name_title=name_title)
        ))

    return _write_files(files, dry_run, force)


def scaffold_service(name: str, dry_run: bool, force: bool, no_tests: bool) -> int:
    """Create service structure."""
    name_title = to_title(name)

    files: list[FileContent] = [
        FileContent(
            Path("src/services/__init__.py"),
            INIT_TEMPLATE.format(description="Service layer.")
        ),
        FileContent(
            Path(f"src/services/{name}_service.py"),
            SERVICE_TEMPLATE.format(name=name, name_title=name_title)
        ),
        FileContent(
            Path("src/services/protocols.py"),
            PROTOCOL_TEMPLATE.format(name=name, name_title=name_title)
        ),
    ]

    if not no_tests:
        files.append(FileContent(
            Path(f"tests/unit/test_{name}_service.py"),
            TEST_SERVICE_TEMPLATE.format(name=name, name_title=name_title)
        ))

    return _write_files(files, dry_run, force)


def scaffold_project(path: str, dry_run: bool, force: bool, no_tests: bool) -> int:
    """Create full project structure."""
    base = Path(path)

    dirs = [
        base,
        base / "services",
        Path("tests"),
        Path("tests/unit"),
        Path("tests/integration"),
    ]

    files: list[FileContent] = [
        FileContent(
            base / "__init__.py",
            INIT_TEMPLATE.format(description="Source package.")
        ),
        FileContent(
            base / "services" / "__init__.py",
            INIT_TEMPLATE.format(description="Service layer.")
        ),
        FileContent(
            Path("tests/__init__.py"),
            INIT_TEMPLATE.format(description="Test package.")
        ),
        FileContent(
            Path("tests/unit/__init__.py"),
            INIT_TEMPLATE.format(description="Unit tests.")
        ),
        FileContent(
            Path("tests/integration/__init__.py"),
            INIT_TEMPLATE.format(description="Integration tests.")
        ),
        FileContent(
            Path("tests/conftest.py"),
            '"""Pytest configuration and fixtures."""\n\nimport pytest\n'
        ),
    ]

    if dry_run:
        print("Would create directories:")
        for d in dirs:
            print(f"  {d}/")
    else:
        for d in dirs:
            d.mkdir(parents=True, exist_ok=True)
            print(f"Created: {d}/")

    return _write_files(files, dry_run, force)


def _write_files(files: list[FileContent], dry_run: bool, force: bool) -> int:
    """Write files, checking for existence."""
    for fc in files:
        if fc.path.exists() and not force:
            print(f"Exists (skip): {fc.path}")
            continue

        if dry_run:
            print(f"Would create: {fc.path}")
        else:
            fc.path.parent.mkdir(parents=True, exist_ok=True)
            fc.path.write_text(fc.content)
            print(f"Created: {fc.path}")

    return 0


def main() -> int:
    """Main entry point."""
    parser = argparse.ArgumentParser(description="Python scaffold generator")
    parser.add_argument("command", choices=["module", "service", "project"],
                        help="What to scaffold")
    parser.add_argument("name", help="Name of module/service or path for project")
    parser.add_argument("--dry-run", action="store_true", help="Show what would be created")
    parser.add_argument("--force", action="store_true", help="Overwrite existing files")
    parser.add_argument("--no-tests", action="store_true", help="Skip test generation")

    args = parser.parse_args()

    if args.command == "module":
        return scaffold_module(args.name, args.dry_run, args.force, args.no_tests)
    elif args.command == "service":
        return scaffold_service(args.name, args.dry_run, args.force, args.no_tests)
    elif args.command == "project":
        return scaffold_project(args.name, args.dry_run, args.force, args.no_tests)

    return 1


if __name__ == "__main__":
    sys.exit(main())
