# Copyright 2024 Kersten Henrik Breuer
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""Test the context module."""

from unittest.mock import Mock

import pytest

from spritze.delivery import get_dependency_context, set_dependency_context


def test_simple_context():
    """A very simple example test."""
    mock_context = Mock()
    with pytest.raises(RuntimeError):
        get_dependency_context()

    with set_dependency_context(mock_context):  # type: ignore
        assert get_dependency_context() is mock_context

    with pytest.raises(RuntimeError):
        get_dependency_context()
