"""DI Context"""

from typing import Callable

from .spec import DISpec

# Idea:the DIContext is just delegating to other classes for:
# - DependencyRegistry:
#     - to store all instanciated dependencies (especially important for singletons)
#     - (async) context manager for managing setup and teardown of dependencies
#       (The context manager interface might actually be implemented by a Factory class
#        that return the DependencyRegistry upon enter.)
# - MatchMaker:
#     - to match subjects to DIConditions and thus to associated Providers
# - Providers:
#     - which are actually responsible for constructing the dependencies


class DIContext:
    """A resolver for dependency injection records active in a specific context."""

    def __init__(self, *, spec: DISpec):
        self.spec = spec

    def resolve(self, subject: Callable) -> object:
        """Resolves a callable by automatically constructing and wiring all its
        dependencies.
        """
        raise NotImplementedError
