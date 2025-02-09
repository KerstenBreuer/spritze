"""Test injection in a pure OOP scenario."""


class B:
    """A test class."""

    def __init__(self, x: int):
        self.x = x


class A:
    """A test class."""

    def __init__(self, b: "B"):
        self.b = b


# def test_resolve_class():
#     """Test resolving a class."""
#     container = TypeContainer({B: B(42)})
#     a = container.resolve_class(A)
#     assert a.b.x == 42
