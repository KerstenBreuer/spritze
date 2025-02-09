"""Dependency injection container."""

from typing import Any, Callable, TypeVar

from .describe import describe_parameters

DepTypeMap = dict[type, Callable]

I = TypeVar("I")
R = TypeVar("R")


class TypeContainer:
    """A Container for Dependency Injection."""

    type_map: DepTypeMap

    def __init__(self, type_map: DepTypeMap | None = None):
        self.type_map = type_map or {}

    def resolve_class(self, cls: type[I]) -> I:
        """Resolve a class by automatically constructing and wiring all it's dependencies."""
        return self.resolve(cls)

    def resolve_function(self, fun: Callable[..., R]) -> R:
        """Resolve a function by automatically constructing and wiring all it's dependencies."""
        return self.resolve(fun)

    def resolve(self, callable_: Callable) -> Any:
        """Resolve a callable by automatically constructing and wiring all it's dependenciey."""
        parameter_types = describe_parameters(callable_)

        resolved_parameter: dict[str, object] = {}
        for parameter_name, parameter_type in parameter_types.items():  # type: ignore
            if parameter_type not in self.type_map:
                raise ValueError(f"Type {parameter_type} not found in type map.")

            resolved_value = self.type_map[parameter_type]

            if not isinstance(resolved_value, parameter_type):
                if not callable(parameter_type):
                    raise ValueError(f"Type {parameter_type} is not callable.")

                resolved_value = self.resolve(parameter_type)

            resolved_parameter[parameter_name] = resolved_value

        # ToDo: Handle positional-only arguments
        return callable_(**resolved_parameter)
