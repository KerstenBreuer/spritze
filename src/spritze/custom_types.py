"""Custom types"""

from typing import Any, TypeAlias


class NoTypeAnnotation:
    """To distinguish between None and not available."""


NominalTypeAnnotation: TypeAlias = type

StructuralTypeAnnotation: TypeAlias = Any

TypeAnnotation: TypeAlias = (
    NominalTypeAnnotation | StructuralTypeAnnotation | type[NoTypeAnnotation]
)
