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

"""Structural entity base class for repository-style modeling.

This module defines ``Entity``, a Pydantic-compatible base class for domain
entities that will be persisted and retrieved via repositories. The class
enforces a concrete ID type per subclass to keep repository interfaces
type-safe and explicit.

Design goals:
- Ensure each entity declares a concrete ``id`` type (e.g., ``Entity[int]``).
- Remain fully compatible with Pydantic validation and serialization.
- Keep the contract small and explicit to support repository abstractions.

Usage:
    class User(Entity[int]):
        name: str

    user = User(id=1, name="Ada", created_at=now, updated_at=now)
"""

import typing
from datetime import datetime
from typing import Any

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["Entity"]


# =========================================================
# CLASS ENTITY
# =========================================================
class Entity[IdT](BaseModel):
    """Base class for entities with a concrete ID type.

    Subclasses must supply a concrete type argument for ``IdT`` (e.g., ``int``,
    ``str``, ``uuid.UUID``). Using ``Any`` or omitting the type argument is
    rejected to prevent ambiguous repository contracts.
    """

    model_config = ConfigDict(extra="forbid")

    id: IdT = Field(..., description="Entity identifier.")
    created_at: datetime
    updated_at: datetime

    __entity_id_type__: type | None = None

    @classmethod
    def __pydantic_init_subclass__(cls, **kwargs: Any) -> None:
        """Capture and validate the concrete ID type for subclasses."""
        super().__pydantic_init_subclass__(**kwargs)
        if cls is Entity:
            return

        id_field = cls.model_fields.get("id")
        id_type = id_field.annotation if id_field else None

        if id_type is Any or isinstance(id_type, typing.TypeVar) or id_type is None:
            raise TypeError("Entity subclasses must specify a concrete id type, e.g., Entity[int].")

        cls.__entity_id_type__ = id_type
