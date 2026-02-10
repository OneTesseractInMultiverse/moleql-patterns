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

"""Task commands for synchronous and asynchronous background workers.

These base classes standardize how task payloads are validated and executed.
They are intentionally abstract to enforce consistent task construction and
execution patterns across different worker backends (e.g., Celery, Dramatiq).

Example:
    class SendEmailData(TaskData):
        recipient: str
        subject: str

    class SendEmailTask(Task[SendEmailData]):
        task_data_cls = SendEmailData

        def __init__(self, payload: dict[str, Any], mailer: Mailer) -> None:
            self._mailer = mailer
            super().__init__(payload)

        def exec(self) -> str:
            self._mailer.send(self.task_data.recipient, self.task_data.subject)
            return "sent"
"""

from abc import ABC, abstractmethod
from typing import Any

from .task_data import TaskData

__all__ = ["TaskBase", "Task", "AsyncTask", "TaskDataDeserializationError"]


# =========================================================
# CLASS TASK DATA DESERIALIZATION ERROR
# =========================================================
class TaskDataDeserializationError(Exception):
    """Raised when a task is missing its required task_data_cls contract."""


# =========================================================
# CLASS TASK BASE
# =========================================================
class TaskBase[TaskDataT: TaskData](ABC):
    """Base class for task execution with validated payloads."""

    task_data_cls: type[TaskDataT]
    task_data: TaskDataT

    def __init__(self, task_data: dict[str, Any]) -> None:
        if self.__class__ is TaskBase:
            raise TypeError("TaskBase is abstract. Subclass it and define task_data_cls.")
        self._verify_task_data_class_is_set()
        self.task_data = self.task_data_cls.from_payload(task_data)

    def _verify_task_data_class_is_set(self) -> None:
        if not hasattr(self, "task_data_cls") or self.task_data_cls is None:
            raise TaskDataDeserializationError("task_data_cls must be defined on the Task class")


# =========================================================
# CLASS TASK
# =========================================================
class Task[TaskDataT: TaskData](TaskBase[TaskDataT], ABC):
    """Synchronous task contract with explicit dependency injection.

    This pattern provides a consistent interface for background tasks while
    enforcing constructor-based dependency injection. Concrete tasks should
    declare their dependencies (database connections, API clients, caches, etc.)
    in the ``__init__`` signature, then pass the task payload to ``super().__init__``.
    """

    @abstractmethod
    def exec(self) -> Any:
        """Execute the task synchronously."""
        raise NotImplementedError


# =========================================================
# CLASS ASYNC TASK
# =========================================================
class AsyncTask[TaskDataT: TaskData](TaskBase[TaskDataT], ABC):
    """Asynchronous task contract with explicit dependency injection.

    This pattern provides a consistent interface for background tasks while
    enforcing constructor-based dependency injection. Concrete tasks should
    declare their dependencies (database connections, API clients, caches, etc.)
    in the ``__init__`` signature, then pass the task payload to ``super().__init__``.
    """

    @abstractmethod
    async def exec(self) -> Any:
        """Execute the task asynchronously."""
        raise NotImplementedError
