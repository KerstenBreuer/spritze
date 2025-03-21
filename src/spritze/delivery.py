"""A mechanism to deliver (set and get) the dependency context."""

from contextlib import contextmanager
from contextvars import ContextVar

from .context import DIContext

_di_context_var: ContextVar[DIContext | None] = ContextVar(
    "dependency_context", default=None
)


@contextmanager
def set_dependency_context(value: DIContext):
    """Set the dependency context."""
    token = _di_context_var.set(value)
    yield
    _di_context_var.reset(token)


def get_dependency_context() -> DIContext:
    """Get the dependency context."""
    if (dep_context := _di_context_var.get()) is None:
        raise RuntimeError("No dependency context set")

    return dep_context
