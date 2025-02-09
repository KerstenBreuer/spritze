"""Some experiments"""
# ruff: noqa
from dataclasses import dataclass
from typing import Annotated, Protocol, TypeVar

DILiteral = Annotated
DIClass = type


class SomeClass:
    pass


class SomeOtherClass(SomeClass):
    pass


T = TypeVar("T", covariant=True)


class DICallable(Protocol[T]):
    def __call__(self, *args, **kwargs) -> T:
        pass


@dataclass
class Experiment:
    lit_: str = "lit"
    class_: DIClass[SomeClass] = SomeOtherClass  # type: ignore
    class2_: DICallable[SomeClass] = SomeOtherClass
    callable_: DICallable[SomeClass] = lambda: SomeOtherClass()
