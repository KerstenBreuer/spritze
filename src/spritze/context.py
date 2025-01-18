"""Use a context var to store dependencies."""

from contextlib import contextmanager
from contextvars import ContextVar

from .models import DepsByTypeDict

_dependency_context: ContextVar[DepsByTypeDict | None] = ContextVar(
    "dependency_context", default=None
)


@contextmanager
def set_dependency_context(value: DepsByTypeDict):
    """Set the dependency context."""
    token = _dependency_context.set(value)
    yield
    _dependency_context.reset(token)


def get_dependency_context() -> DepsByTypeDict:
    """Get the dependency context."""
    if (dep_context := _dependency_context.get()) is None:
        raise RuntimeError("No dependency context set")

    return dep_context
