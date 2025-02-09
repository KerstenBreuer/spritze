"""Inspect objects for properties to be injected."""

import inspect
from collections.abc import Iterable
from dataclasses import dataclass
from types import FunctionType, ModuleType, NoneType
from typing import Any, Callable, Protocol, TypeAlias


class NoTypeAnnotation:
    """To distinguish between None and not available."""


NominalTypeAnnotation: TypeAlias = type | None

StructuralTypeAnnotation: TypeAlias = Any

TypeAnnotation: TypeAlias = (
    NominalTypeAnnotation | StructuralTypeAnnotation | type[NoTypeAnnotation]
)


@dataclass
class ParameterDescription:
    """Describes an parameter to a callable that shall be dependency injected."""

    name: str
    type_: TypeAnnotation
    requires_structural_subtyping: bool = False

    # currently not in use:
    module: ModuleType | None = None
    target: FunctionType | type | None = None


def check_structural_subtyping_requirement(type_: TypeAnnotation) -> bool:
    """Predict if a type annotation is using structural subtyping."""
    if isinstance(type_, type):
        if issubclass(type_, Protocol):  # type: ignore
            return True

        return False

    if type_ is None or isinstance(type_, NoneType) or type_ is NoTypeAnnotation:
        return False

    return True


def describe_parameters(target: Callable) -> Iterable[ParameterDescription]:
    """Analyze a callable and extract information on parameters that are relevant for
    DI.
    """
    signature = inspect.signature(target)
    parameters = signature.parameters

    for name, param in parameters.items():
        type_ = (
            NoTypeAnnotation
            if param.annotation is inspect.Parameter.empty
            else param.annotation
        )
        requires_structural_subtyping = check_structural_subtyping_requirement(type_)

        yield ParameterDescription(
            name=name,
            type_=type_,
            requires_structural_subtyping=requires_structural_subtyping,
        )
