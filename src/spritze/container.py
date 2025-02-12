"""Mock up of a container"""

from abc import ABC
from typing import Callable

from .spec import (
    AsyncContextProvider,
    AsyncProvider,
    Condition,
    ContextProvider,
    DISpec,
    LiteralProvider,
    Provider,
)


class DIMatcher(ABC):  # noqa: B024
    """Implementations of this class are responsible for matching ParameterDescription
    objects to DIRecords.
    """

    pass


class DIContext:
    """A resolver for dependency injection records active in a specific context."""

    def __init__(self, spec: DISpec, matcher: DIMatcher):
        self.spec = spec
        self.matcher = matcher

    def resolve(self, subject: Callable) -> object:
        """Resolves a callable by automatically constructing and wiring all its
        dependencies.
        """
        raise NotImplementedError


class GeneralDIContainer:
    """A general-purpose DI Container."""

    def __init__(
        self,
        map: dict[
            Condition,
            Provider
            | AsyncProvider
            | ContextProvider
            | AsyncContextProvider
            | LiteralProvider,
        ],
    ):
        self.spec = DISpec(map)

    def add(
        self,
        condition: Condition,
        provider: Provider
        | AsyncProvider
        | ContextProvider
        | AsyncContextProvider
        | LiteralProvider,
    ):
        """Add a condition-provider pair to the spec."""
        self.spec.add(condition=condition, provider=provider)

    def __enter__(self) -> DIContext:
        """Create a new DIContext scoped toward a with block."""
        raise NotImplementedError

    def __exit__(self, exc_type, exc_value, traceback):
        """Clean up the DIContext."""
        raise NotImplementedError
