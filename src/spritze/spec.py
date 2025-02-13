"""Structures to specify Conditions for matching ParameterDescriptions to
a Provider.
"""

from collections.abc import Awaitable, Callable
from contextlib import (
    AbstractAsyncContextManager,
    AbstractContextManager,
)
from dataclasses import dataclass
from enum import Enum
from types import FunctionType, ModuleType
from typing import TypeAlias

from .custom_types import TypeAnnotation


class ConditionParams(Enum):
    """The parameters that can be used in a Condition."""

    TYPE_ = "type_"
    LABELS = "labels"
    TAGS = "tags"
    MODULE = "module"
    TARGET = "target"


@dataclass
class DICondition:
    """Specification of conditions to match a ParameterDescription."""

    type_: TypeAnnotation | None = None
    labels: frozenset[str] | None = None
    tags: frozenset[str] | None = None
    module: ModuleType | None = None
    target: FunctionType | type | None = None


@dataclass
class Provider[D]:
    """Instructions for constructing a dependency based on a simple callable."""

    constructor: Callable[..., D]
    as_singelton: bool = False


@dataclass
class AsyncProvider[D]:
    """Instructions for constructing a dependency based on a coroutine."""

    constructor: Callable[..., Awaitable[D]]
    as_singelton: bool = False


@dataclass
class ContextProvider[D]:
    """Instructions for constructing a dependency based on a context manager."""

    constructor: Callable[..., AbstractContextManager[D]]
    as_singelton: bool = False


@dataclass
class AsyncContextProvider[D]:
    """Instructions for constructing a dependency based on an async context manager."""

    constructor: Callable[..., AbstractAsyncContextManager[D]]
    as_singelton: bool = False


class LiteralProvider:
    """Description of a object that is passed "as is". Hence this is not a
    constructor for a dependency this is the already constructed dependency itself.
    """

    def __init__(self, literal: object):
        self.literal = literal

    def __repr__(self):  # noqa: D105
        return f"LiteralProvider({self.literal})"

    def __str__(self):  # noqa: D105
        return repr(self)


ProviderSpec: TypeAlias = (
    Provider | AsyncProvider | ContextProvider | AsyncContextProvider | LiteralProvider
)


class DISpec:
    """A specification that describes how Conditions (for matching
    ParametersDescriptions) are associated to Providers (to provide instances of the
    required dependencies).
    """

    def __init__(
        self,
        map: dict[DICondition, ProviderSpec],
    ):
        self.map = map

    def add(self, condition: DICondition, provider: ProviderSpec):
        """Add a condition-provider pair to the spec."""
        self.map[condition] = provider

    def used_condition_params(self) -> set[ConditionParams]:
        """Summarizes which parameters are used in the contained Conditions."""
        return {
            param
            for param in ConditionParams
            if any(getattr(cond, param.value) is not None for cond in self.map)
        }

    def used_providers(self) -> set[type]:
        """Summarizes which types of providers are used in the contained Providers."""
        return {type(provider) for provider in self.map.values()}

    def __repr__(self):  # noqa: D105
        return f"DISpec({self.map})"

    def __str__(self):  # noqa: D105
        return repr(self)
