# TDD Patterns Reference

Quick reference for Test-Driven Development patterns in Python.

## Red-Green-Refactor Cycle

```
1. RED    → Write failing test (defines expected behavior)
2. GREEN  → Write minimal code to pass
3. REFACTOR → Improve code, keep tests green
```

## Test Naming Convention

```python
# Function tests
def test_<function_name>() -> None:
    ...

# Class method tests
def test_<ClassName>_<method_name>() -> None:
    ...

# Behavior-specific tests
def test_<function>_<scenario>() -> None:
    ...
```

## Arrange-Act-Assert Pattern

```python
def test_add_task_returns_task_with_id() -> None:
    # Arrange - Set up test data
    service = TaskService()
    title = "Test Task"

    # Act - Execute the behavior
    result = service.add_task(title)

    # Assert - Verify outcome
    assert result.id is not None
    assert result.title == title
```

## Common Fixtures

```python
import pytest

@pytest.fixture
def service() -> TaskService:
    """Fresh service instance for each test."""
    return TaskService()

@pytest.fixture
def sample_task(service: TaskService) -> Task:
    """Pre-created task for tests that need existing data."""
    return service.add_task("Sample", "Description")
```

## Testing Edge Cases

| Case | Test Pattern |
|------|-------------|
| Empty input | `test_func_with_empty_input` |
| None value | `test_func_with_none` |
| Invalid type | `test_func_with_invalid_type_raises` |
| Boundary | `test_func_at_boundary` |
| Not found | `test_func_when_not_found` |

## Exception Testing

```python
def test_delete_task_not_found_raises() -> None:
    service = TaskService()

    with pytest.raises(TaskNotFoundError):
        service.delete_task(999)
```

## Parametrized Tests

```python
@pytest.mark.parametrize("title,expected", [
    ("Valid", True),
    ("", False),
    ("   ", False),
])
def test_validate_title(title: str, expected: bool) -> None:
    assert validate_title(title) == expected
```

## TDD Anti-Patterns to Avoid

1. **Writing tests after code** - Defeats TDD purpose
2. **Testing implementation details** - Test behavior, not internals
3. **Overly complex setup** - Keep tests simple
4. **Multiple assertions testing different things** - One concept per test
5. **Skipping the RED phase** - Always see the test fail first

## TaskFlow-Specific Patterns

### Service Layer Tests
```python
def test_task_service_add_task() -> None:
    storage = InMemoryStorage()
    service = TaskService(storage)

    task = service.add_task("Title", "Description")

    assert task.id is not None
    assert storage.get(task.id) == task
```

### Storage Protocol Tests
```python
def test_storage_implements_protocol() -> None:
    storage = InMemoryStorage()

    # Verify protocol compliance
    assert hasattr(storage, 'add')
    assert hasattr(storage, 'get')
    assert hasattr(storage, 'update')
    assert hasattr(storage, 'delete')
    assert hasattr(storage, 'list_all')
```
