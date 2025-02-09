"""Mock up of a container"""

from abc import ABC
from collections.abc import Sequence
from dataclasses import dataclass
from types import FunctionType, ModuleType
from typing import Callable


class DIMatcher(ABC):  # noqa: B024
    """Implementations of this class are responsible for matching ParameterDescription
    objects to DIRecords.
    """

    pass


@dataclass
class DIRecord:
    """A record of a dependency injection."""

    constructor: Callable
    singleton: bool = False
    # Matching information
    match_type: type | None = None
    match_names: Sequence[str] | None = None
    match_module: ModuleType | None = None
    match_target: FunctionType | type | None = None
    priority: int = 0


class DIContext:
    """A resolver for dependency injection records active in a specific context."""

    def __init__(self, records: Sequence[DIRecord], matcher: DIMatcher):
        self.records = records

    def resolve(self, subject: Callable) -> object:
        """Resolves a callable by automatically constructing and wiring all its
        dependencies.
        """
        raise NotImplementedError


class DIContainer:
    """A container for dependency injection records."""

    def __init__(self):
        self.records: list

    def add(  # noqa: PLR0913
        self,
        constructor: Callable,
        *,
        singleton: bool = False,
        match_type: type | None = None,
        match_names: Sequence[str] | None = None,
        match_module: ModuleType | None = None,
        match_target: FunctionType | type | None = None,
        priority: int = 0,
    ) -> None:
        """Add a record to the container."""
        record = DIRecord(
            constructor=constructor,
            singleton=singleton,
            match_type=match_type,
            match_names=match_names,
            match_module=match_module,
            match_target=match_target,
            priority=priority,  # priority might control the order of inclusion in the records
        )
        self.records.append(record)

    def add_literal(  # noqa: PLR0913
        self,
        literal: object,
        *,
        singleton: bool = False,
        match_type: type | None = None,
        match_names: Sequence[str] | None = None,
        match_module: ModuleType | None = None,
        match_target: FunctionType | type | None = None,
        priority: int = 0,
    ) -> None:
        """Add a literal to the container."""
        self.add(
            constructor=lambda: literal,
            singleton=singleton,
            match_type=match_type,
            match_names=match_names,
            match_module=match_module,
            match_target=match_target,
            priority=priority,
        )

    def __enter__(self) -> DIContext:
        """Create a new DIContext scoped toward a with block."""
        raise NotImplementedError
