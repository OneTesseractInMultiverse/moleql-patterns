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

"""Base classes for decoupled, testable API operations.

Design goals:
- Dependencies are injected via the concrete class constructor.
- Logic is unit-testable without running an HTTP server.
- Access checks are explicit and mandatory for every operation.

Usage:
    class CreateUser(APIOperation[User]):
        def __init__(self, repo: UserRepo, current_user: User) -> None:
            self._repo = repo
            self._current_user = current_user

        def verify_access(self) -> None:
            if not self._current_user.is_admin:
                raise AccessDeniedError("Only admins can create users.")

        def _execute(self) -> User:
            return self._repo.create_user(...)

    class CreateUserAsync(AsyncAPIOperation[User]):
        def __init__(self, repo: UserRepo, current_user: User) -> None:
            self._repo = repo
            self._current_user = current_user

        def verify_access(self) -> None:
            if not self._current_user.is_admin:
                raise AccessDeniedError("Only admins can create users.")

        async def _execute_async(self) -> User:
            return await self._repo.create_user(...)
"""

from abc import ABC, abstractmethod

from pydantic import BaseModel

__all__ = ["APIOperation", "AsyncAPIOperation", "AccessDeniedError"]


class AccessDeniedError(PermissionError):
    """Raised when an operation is not permitted for the current principal."""


class APIOperation[ResultT: BaseModel](ABC):
    """Synchronous base class for API operations with explicit access checks.

    Concrete classes should:
    - Accept dependencies via ``__init__``.
    - Implement ``verify_access`` to enforce authorization.
    - Implement ``_execute`` with the operation logic.
    - Return a Pydantic ``BaseModel`` from ``execute``.
    """

    @abstractmethod
    def verify_access(self) -> None:
        """Validate permissions for this operation.

        Implementations should raise ``AccessDeniedError`` (or ``PermissionError``)
        when the current principal is not authorized.
        """
        raise NotImplementedError

    @abstractmethod
    def _execute(self) -> ResultT:
        """Execute the operation logic synchronously."""
        raise NotImplementedError

    def execute(self) -> ResultT:
        """Execute synchronously with access checks."""
        self.verify_access()
        return self._execute()


class AsyncAPIOperation[ResultT: BaseModel](ABC):
    """Asynchronous base class for API operations with explicit access checks.

    Concrete classes should:
    - Accept dependencies via ``__init__``.
    - Implement ``verify_access`` to enforce authorization.
    - Implement ``_execute_async`` with the operation logic.
    - Return a Pydantic ``BaseModel`` from ``execute_async``.
    """

    @abstractmethod
    def verify_access(self) -> None:
        """Validate permissions for this operation.

        Implementations should raise ``AccessDeniedError`` (or ``PermissionError``)
        when the current principal is not authorized.
        """
        raise NotImplementedError

    @abstractmethod
    async def _execute_async(self) -> ResultT:
        """Execute the operation logic asynchronously."""
        raise NotImplementedError

    async def execute_async(self) -> ResultT:
        """Execute asynchronously with access checks."""
        self.verify_access()
        return await self._execute_async()
