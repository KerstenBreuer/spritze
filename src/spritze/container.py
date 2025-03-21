"""Mock up of a container"""

from collections.abc import Generator
from contextlib import contextmanager

from .context import DIContext
from .delivery import set_dependency_context
from .spec import DICondition, DISpec, ProviderSpec


class GeneralDIContainer:
    """A general-purpose DI Container."""

    def __init__(
        self,
        map: dict[DICondition, ProviderSpec],
    ):
        self.spec = DISpec(map)

    @contextmanager
    def new_context(self) -> Generator[DIContext, None, None]:
        """Creates a new DIContext and makes it available (via the delivery mechanism)
        in scope of a with-statement context.
        """
        di_context = DIContext(spec=self.spec)
        with set_dependency_context(di_context):
            yield di_context
