"""Mock up of a container"""

from abc import ABC
from collections.abc import Generator
from contextlib import contextmanager
from typing import Callable

from .spec import DICondition, DISpec, ProviderSpec


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
        map: dict[DICondition, ProviderSpec],
    ):
        self.spec = DISpec(map)

    def add(self, condition: DICondition, provider: ProviderSpec):
        """Add a condition-provider pair to the spec."""
        self.spec.add(condition=condition, provider=provider)

    @contextmanager
    def new_context(self) -> Generator[None, None, DIContext]:
        """Get a new DI Context trough a context manager interface."""
        raise NotImplementedError
