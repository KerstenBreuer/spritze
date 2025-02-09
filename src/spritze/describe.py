"""Inspect objects for properties to be injected."""

import inspect
from collections.abc import Iterable
from dataclasses import dataclass
from types import FunctionType, ModuleType
from typing import Any, Callable, TypeAlias


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
    uses_structural_subtyping: bool = False

    # currently not in use:
    module: ModuleType | None = None
    target: FunctionType | type | None = None


def is_structural_subtype(type_: TypeAnnotation) -> bool:
    """Check if a type annotation is using structural subtyping."""
    if isinstance(type_, (NominalTypeAnnotation)) or type_ is NoTypeAnnotation:
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
        uses_structural_subtyping = is_structural_subtype(type_)

        yield ParameterDescription(
            name=name,
            type_=type_,
            uses_structural_subtyping=uses_structural_subtyping,
        )
