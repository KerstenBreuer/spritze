"""Tests the describe module."""

from typing import Callable, Protocol

import pytest

from spritze.describe import NoTypeAnnotation, ParameterDescription, describe_parameters


class Foo:
    """An example for nominal type annotation."""

    pass


class Bar:
    """Another example for nominal type annotation."""

    pass


class ExampleProtocol(Protocol):
    """An example for a protocol."""

    def foo(self) -> None:
        """A method that must be implemented."""
        ...


NO_TYPE_ANNOTATION_PARAMETER_EXAMPLE = [
    ParameterDescription(name="a", type_=NoTypeAnnotation),
    ParameterDescription(name="b", type_=NoTypeAnnotation),
]

PRIMITIVE_PARAMETER_EXAMPLE = [
    ParameterDescription(name="a", type_=int),
    ParameterDescription(name="b", type_=str),
]

NOMINAL_PARAMETER_EXAMPLE = [
    ParameterDescription(name="a", type_=Foo),
    ParameterDescription(name="b", type_=Bar),
]

GENERIC_PARAMETER_EXAMPLE = [
    ParameterDescription(name="a", type_=list[int], requires_structural_subtyping=True),
    ParameterDescription(
        name="b", type_=dict[str, int], requires_structural_subtyping=True
    ),
]

PROTOCOL_PARAMETER_EXAMPLE = [
    ParameterDescription(
        name="a", type_=ExampleProtocol, requires_structural_subtyping=True
    ),
]

# fmt: off
lambda_with_no_type_annotation = lambda a, b: None
# fmt: on


def fun_with_primitive_types(a: int, b: str) -> None:
    """A function with primitive types."""
    pass


class ClassWithPrimitiveTypes:
    """A class with primitive types."""

    def __init__(self, a: int, b: str) -> None:
        pass


def fun_with_nominal_types(a: Foo, b: Bar) -> None:
    """A function with nominal types."""
    pass


def fun_with_protocol(a: ExampleProtocol) -> None:
    """A function using an implementation of a protocol."""
    pass


def fun_with_generic_types(a: list[int], b: dict[str, int]) -> None:
    """A function with generic types."""
    pass


@pytest.mark.parametrize(
    "target, expected_parameters",
    [
        (lambda_with_no_type_annotation, NO_TYPE_ANNOTATION_PARAMETER_EXAMPLE),
        (fun_with_primitive_types, PRIMITIVE_PARAMETER_EXAMPLE),
        (ClassWithPrimitiveTypes, PRIMITIVE_PARAMETER_EXAMPLE),
        (fun_with_nominal_types, NOMINAL_PARAMETER_EXAMPLE),
        (fun_with_generic_types, GENERIC_PARAMETER_EXAMPLE),
        (fun_with_protocol, PROTOCOL_PARAMETER_EXAMPLE),
    ],
)
def test_describe_parameters(
    target: Callable, expected_parameters: list[ParameterDescription]
):
    """Test the describe_parameters function."""
    assert list(describe_parameters(target)) == expected_parameters
