# MIT License
#
# Copyright (c) 2026 Pedro Guzmán
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in all
# copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
# SOFTWARE.

from datetime import UTC, datetime
from typing import Any

import pytest

from moleql_patterns.structural import Entity


# =========================================================
# CLASS USER ENTITY
# =========================================================
class UserEntity(Entity[int]):
    pass


# =========================================================
# CLASS BASE ENTITY
# =========================================================
class BaseEntity(Entity[str]):
    pass


# =========================================================
# CLASS DERIVED ENTITY
# =========================================================
class DerivedEntity(BaseEntity):
    pass


# =========================================================
# CLASS TEST ENTITY INIT SUBCLASS
# =========================================================
class TestEntityInitSubclass:
    def test_base_init_subclass_noop(self) -> None:
        result = Entity.__pydantic_init_subclass__()

        assert result is None

    def test_requires_concrete_id_type(self) -> None:
        with pytest.raises(TypeError):
            type("BadEntity", (Entity,), {})

    def test_rejects_any_id_type(self) -> None:
        with pytest.raises(TypeError):
            type("AnyEntity", (Entity[Any],), {})

    def test_allows_concrete_id_type(self) -> None:
        now = datetime.now(UTC)

        entity = UserEntity(id=1, created_at=now, updated_at=now)

        assert entity.id == 1

    def test_inherits_id_type_from_base(self) -> None:
        assert DerivedEntity.__entity_id_type__ is str
