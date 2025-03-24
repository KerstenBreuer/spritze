"""Mock up of a container"""

from collections.abc import Generator
from contextlib import contextmanager

from .context import DIContext
from .delivery import set_dependency_context
from .match import DIMatchMaker
from .spec import DISpec


class GeneralDIContainer:
    """A general-purpose DI Container."""

    def __init__(
        self,
        spec: DISpec,
    ):
        self.spec = spec
        self._matcher = DIMatchMaker(spec=self.spec)

    @contextmanager
    def apply(self) -> Generator[DIContext, None, None]:
        """Creates a new DIContext and makes it available (via the delivery mechanism)
        in scope of a with-statement context.
        """
        di_context = DIContext(matcher=self._matcher)
        with set_dependency_context(di_context):
            yield di_context
