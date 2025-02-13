"""Matching ParameterDescriptions to DI Conditions."""

from collections import defaultdict
from typing import TypeAlias

from .custom_types import TypeAnnotation
from .describe import ParameterDescription
from .spec import DISpec, ProviderSpec

_LookupStructure: TypeAlias = dict[
    TypeAnnotation, dict[frozenset[str] | None, dict[str | None, ProviderSpec]]
]


class NoMatchFound(ValueError):
    """Raised when no match is found for a ParameterDescription."""

    def __init__(self, param: ParameterDescription):
        super().__init__(f"No match found for {param}")


class DIMatchMaker:
    """A mechanism to match ParameterDescriptions to DI Conditions."""

    def __init__(self, spec: DISpec):
        self._lookup = self._spec_to_lookup(spec)

    @staticmethod
    def _spec_to_lookup(spec: DISpec) -> _LookupStructure:
        """Transform a DISpec into a lookup structure based on a nested dictionary.
        The first level is the type,
        the second level are the tags (all tags as keys),
        the third level is the label (each label as a separate key),
        the final value is the provider.
        """
        lookup: _LookupStructure = defaultdict(lambda: defaultdict(dict))

        for condition, provider in spec.map.items():
            labels = condition.labels or [None]
            for label in labels:
                lookup[condition.type_][condition.tags][label] = provider

        return lookup

    def match(self, param: ParameterDescription) -> ProviderSpec:
        """Match a ParameterDescription to a DI Condition.

        Raises:
            NoMatchFound: When no match is found.
        """
        # Lookup using type:
        # (If no direct match is found, try to match with conditions that have type
        # disabled - i.e. type is set to None.)
        lookup_by_tags = self._lookup.get(param.type_) or self._lookup.get(None)
        if lookup_by_tags is None:
            raise NoMatchFound(param)

        # Lookup using tags:
        # (If no direct match is found, try to match with conditions that have tags
        # disabled - i.e. tags is set to None.)
        lookup_by_labels = lookup_by_tags.get(param.tags) or lookup_by_tags.get(None)
        if lookup_by_labels is None:
            raise NoMatchFound(param)

        # Lookup using labels:
        for label in param.labels:
            provider = lookup_by_labels.get(label)
            if provider:
                return provider

        # If no match is found, try to match with conditions that have labels disabled:
        provider = lookup_by_labels.get(None)
        if provider:
            return provider

        raise NoMatchFound(param)
