# ADVANCED LEVEL — LESSON 10: Advanced Fixture Patterns
#
# Patterns covered:
#   - Factory fixtures: return a callable, not a value
#   - Fixtures with finalizers (request.addfinalizer)
#   - Parametrized fixtures (not the same as parametrized tests!)
#   - Fixtures that read pytest config / CLI options

import pytest
import tempfile
import os


# --- Factory fixture ---
# Instead of returning one object, return a function that creates many

@pytest.fixture
def make_temp_file(tmp_path):
    """Factory: call it multiple times to create multiple temp files."""
    created = []

    def _make(name, content=""):
        f = tmp_path / name
        f.write_text(content)
        created.append(f)
        return f

    yield _make

    # cleanup: could do extra work here, but tmp_path auto-cleans


# --- Fixture with request.addfinalizer ---
# Use when you can't use yield (e.g., inside a loop or conditional)

@pytest.fixture
def managed_resource(request):
    resources = []

    def cleanup():
        for r in resources:
            r["closed"] = True  # simulate closing

    request.addfinalizer(cleanup)

    def allocate(name):
        r = {"name": name, "closed": False}
        resources.append(r)
        return r

    return allocate


# --- Parametrized fixture ---
# Runs every test that uses this fixture ONCE PER PARAM VALUE

@pytest.fixture(params=["sqlite", "postgres", "mysql"])
def db_backend(request):
    """Each test using this fixture runs 3 times — once per backend."""
    return {"backend": request.param, "connected": True}


# --- Fixture reading CLI options ---
# Add --env option:  pytest --env=staging

def pytest_addoption(parser):
    parser.addoption("--env", default="test", help="Target environment")


@pytest.fixture
def env(request):
    return request.config.getoption("--env")
