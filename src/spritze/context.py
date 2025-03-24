"""DI Context"""

from typing import Callable

from .describe import describe_parameters
from .match import DIMatchMaker
from .spec import LiteralProvider, Provider

# Idea:the DIContext is just delegating to other classes for:
# - DependencyRegistry:
#     - to store all instanciated dependencies (especially important for singletons)
#     - (async) context manager for managing setup and teardown of dependencies
#       (The context manager interface might actually be implemented by a Factory class
#        that return the DependencyRegistry upon enter.)
# - MatchMaker:
#     - to match subjects to DIConditions and thus to associated Providers
# - Providers:
#     - which are actually responsible for constructing the dependencies


class DIContext:
    """A resolver for dependency injection records active in a specific context."""

    def __init__(self, *, matcher: DIMatchMaker):
        self._matcher = matcher

    def resolve(self, subject: Callable) -> object:
        """Resolves a callable by automatically constructing and wiring all its
        dependencies.
        """
        param_specs = describe_parameters(subject)

        args = []
        kwargs = {}
        for param_spec in param_specs:
            provider = self._matcher.match(param_spec)

            if isinstance(provider, LiteralProvider):
                value = provider.literal

            elif isinstance(provider, Provider):
                if provider.as_singelton:
                    raise NotImplementedError

                value = self.resolve(provider.constructor)

            else:
                raise NotImplementedError

            if param_spec.kwargs_enabled:
                kwargs[param_spec.name] = value
            else:
                args.append(value)

        return subject(*args, **kwargs)
