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

"""Task data contract for background job execution.

This module provides a small, validated parameter object for background tasks
intended to be executed by worker systems (e.g., Celery, Dramatiq). It standardizes
payload shape, enforces correlation IDs, and provides explicit serialization
helpers.

Design notes:
- Keep task input explicit and immutable where possible.
- Prefer "tell, don't ask" by providing methods that act on the data.
- Validate eagerly to keep failures close to the task producer.
"""

from typing import Any, Self

from pydantic import BaseModel, ConfigDict, Field

__all__ = ["TaskData", "TaskSerializationError", "TaskDeserializationError"]


# =========================================================
# CLASS TASK SERIALIZATION ERROR
# =========================================================
class TaskSerializationError(RuntimeError):
    """Raised when a task payload cannot be serialized."""


# =========================================================
# CLASS TASK DESERIALIZATION ERROR
# =========================================================
class TaskDeserializationError(RuntimeError):
    """Raised when a task payload cannot be deserialized."""


# =========================================================
# CLASS TASK DATA
# =========================================================
class TaskData(BaseModel):
    """Base class for task payloads with correlation and serialization helpers.

    Subclasses should add task-specific fields and behavior. Keep them as pure
    data contracts with explicit validation.
    """

    model_config = ConfigDict(extra="forbid")

    correlation_id: str = Field(
        ...,
        min_length=1,
        description="Correlation ID used to trace requests across producers and workers.",
    )

    def __init__(self, **data: Any) -> None:
        if self.__class__ is TaskData:
            raise TypeError("TaskData is abstract. Subclass it and add task-specific fields.")
        super().__init__(**data)

    def to_payload(self) -> dict[str, Any]:
        """Serialize to a transport-friendly dictionary."""
        try:
            return self.model_dump()
        except Exception as exc:
            raise TaskSerializationError("Failed to serialize task data.") from exc

    @classmethod
    def from_payload(cls, payload: dict[str, Any]) -> Self:
        """Create an instance from a serialized payload."""
        try:
            return cls.model_validate(payload)
        except Exception as exc:
            raise TaskDeserializationError("Failed to deserialize task data.") from exc
