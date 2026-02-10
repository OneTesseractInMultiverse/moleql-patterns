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

"""Repository contract for entity storage.

EntityRepository defines a technology agnostic interface for entity storage.
Concrete repositories receive dependencies in their constructors through injection.
Those dependencies include database connections and other persistent stores.
Concrete repositories implement each method in this contract.
Concrete repositories hold the technology details.
This base class allows repository instances to be injected across application logic.
That decouples business logic from the persistence layer.
Liskov's substitution principle allows the swap of implementations.
"""

from abc import ABC, abstractmethod
from collections.abc import Sequence
from typing import Any

from .entity import Entity

__all__ = ["EntityRepository"]


# =========================================================
# CLASS ENTITY REPOSITORY
# =========================================================
class EntityRepository[IdT, EntityT: Entity, QueryT: Any](ABC):
    """Repository contract with domain focused method names.

    Concrete repositories receive dependencies in their constructors through injection.
    Concrete repositories implement each method in this contract.
    The base contract is technology agnostic and stable across adapters.
    This supports dependency injection in application logic.
    Liskov's substitution principle allows one repository to replace another.
    """

    @abstractmethod
    def add(self, entity: EntityT) -> None:
        """Add a new entity."""
        raise NotImplementedError

    @abstractmethod
    def get(self, entity_id: IdT) -> EntityT | None:
        """Return an entity by id or None."""
        raise NotImplementedError

    @abstractmethod
    def list(self, query: QueryT = None) -> Sequence[EntityT]:
        """Return entities for a query or all entities."""
        raise NotImplementedError

    @abstractmethod
    def update(self, entity: EntityT) -> None:
        """Persist entity updates."""
        raise NotImplementedError

    @abstractmethod
    def remove(self, entity: EntityT) -> None:
        """Remove an entity."""
        raise NotImplementedError
