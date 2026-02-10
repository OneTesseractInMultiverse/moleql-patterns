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

import pytest

from moleql_patterns.structural import Entity, EntityRepository


# =========================================================
# CLASS NOTE ENTITY
# =========================================================
class NoteEntity(Entity[int]):
    title: str


# =========================================================
# CLASS NOTE REPOSITORY
# =========================================================
class NoteRepository(EntityRepository[int, NoteEntity, dict[str, str] | None]):
    def __init__(self) -> None:
        self._items: dict[int, NoteEntity] = {}

    def add(self, entity: NoteEntity) -> None:
        self._items[entity.id] = entity

    def get(self, entity_id: int) -> NoteEntity | None:
        return self._items.get(entity_id)

    def list(self, query: dict[str, str] | None = None) -> list[NoteEntity]:
        return list(self._items.values())

    def update(self, entity: NoteEntity) -> None:
        self._items[entity.id] = entity

    def remove(self, entity: NoteEntity) -> None:
        self._items.pop(entity.id, None)


# =========================================================
# CLASS TEST ENTITY REPOSITORY INIT
# =========================================================
class TestEntityRepositoryInit:
    def test_base_class_is_abstract(self) -> None:
        with pytest.raises(TypeError):
            EntityRepository()


# =========================================================
# CLASS TEST ENTITY REPOSITORY ADD
# =========================================================
class TestEntityRepositoryAdd:
    def test_add_base_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            EntityRepository.add(object(), object())

    def test_add_stores_entity(self) -> None:
        repo = NoteRepository()
        now = datetime.now(UTC)
        entity = NoteEntity(id=1, title="note", created_at=now, updated_at=now)

        repo.add(entity)

        assert repo.get(1) is entity


# =========================================================
# CLASS TEST ENTITY REPOSITORY GET
# =========================================================
class TestEntityRepositoryGet:
    def test_get_base_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            EntityRepository.get(object(), 1)

    def test_get_returns_none(self) -> None:
        repo = NoteRepository()

        result = repo.get(1)

        assert result is None


# =========================================================
# CLASS TEST ENTITY REPOSITORY LIST
# =========================================================
class TestEntityRepositoryList:
    def test_list_base_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            EntityRepository.list(object())

    def test_list_returns_items(self) -> None:
        repo = NoteRepository()
        now = datetime.now(UTC)
        entity = NoteEntity(id=1, title="note", created_at=now, updated_at=now)
        repo.add(entity)

        items = repo.list()

        assert items == [entity]

    def test_list_accepts_query(self) -> None:
        repo = NoteRepository()
        now = datetime.now(UTC)
        entity = NoteEntity(id=1, title="note", created_at=now, updated_at=now)
        repo.add(entity)

        items = repo.list({"title": "note"})

        assert items == [entity]


# =========================================================
# CLASS TEST ENTITY REPOSITORY UPDATE
# =========================================================
class TestEntityRepositoryUpdate:
    def test_update_base_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            EntityRepository.update(object(), object())

    def test_update_overwrites_entity(self) -> None:
        repo = NoteRepository()
        now = datetime.now(UTC)
        entity = NoteEntity(id=1, title="note", created_at=now, updated_at=now)
        repo.add(entity)
        updated = NoteEntity(id=1, title="new", created_at=now, updated_at=now)

        repo.update(updated)

        assert repo.get(1) is updated


# =========================================================
# CLASS TEST ENTITY REPOSITORY REMOVE
# =========================================================
class TestEntityRepositoryRemove:
    def test_remove_base_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            EntityRepository.remove(object(), object())

    def test_remove_deletes_entity(self) -> None:
        repo = NoteRepository()
        now = datetime.now(UTC)
        entity = NoteEntity(id=1, title="note", created_at=now, updated_at=now)
        repo.add(entity)

        repo.remove(entity)

        assert repo.get(1) is None
