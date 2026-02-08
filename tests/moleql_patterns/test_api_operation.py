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

import asyncio

import pytest
from pydantic import BaseModel

from moleql_patterns.api_operation import AccessDeniedError, APIOperation


class _ExampleResult(BaseModel):
    value: int


class _AccessDeniedOperation(APIOperation[_ExampleResult]):
    def verify_access(self) -> None:
        raise AccessDeniedError("denied")

    async def _execute_async(self) -> _ExampleResult:
        return _ExampleResult(value=1)


class _FlagOperation(APIOperation[_ExampleResult]):
    def __init__(self) -> None:
        self.access_checked = False

    def verify_access(self) -> None:
        self.access_checked = True

    async def _execute_async(self) -> _ExampleResult:
        return _ExampleResult(value=1)


class _MissingVerifyAccess(APIOperation[_ExampleResult]):
    async def _execute_async(self) -> _ExampleResult:
        return _ExampleResult(value=1)


class _MissingExecuteAsync(APIOperation[_ExampleResult]):
    def verify_access(self) -> None:
        return None


class _BaseVerifyAccessOperation(APIOperation[_ExampleResult]):
    def verify_access(self) -> None:
        return APIOperation.verify_access(self)

    async def _execute_async(self) -> _ExampleResult:
        return _ExampleResult(value=1)


class _BaseExecuteAsyncOperation(APIOperation[_ExampleResult]):
    def verify_access(self) -> None:
        return None

    async def _execute_async(self) -> _ExampleResult:
        return await APIOperation._execute_async(self)


class TestVerifyAccess:
    def test_verify_access_blocks_execution(self) -> None:
        operation = _AccessDeniedOperation()

        with pytest.raises(AccessDeniedError):
            asyncio.run(operation.execute_async())

    def test_verify_access_base_raises(self) -> None:
        operation = _BaseVerifyAccessOperation()

        with pytest.raises(NotImplementedError):
            asyncio.run(operation.execute_async())

    def test_verify_access_is_required(self) -> None:
        with pytest.raises(TypeError):
            _MissingVerifyAccess()

    def test_verify_access_runs(self) -> None:
        operation = _FlagOperation()

        asyncio.run(operation.execute_async())

        assert operation.access_checked is True


class TestExecuteAsync:
    def test_execute_async_returns_model(self) -> None:
        operation = _FlagOperation()

        result = asyncio.run(operation.execute_async())

        assert isinstance(result, _ExampleResult)

    def test_execute_async_base_raises(self) -> None:
        operation = _BaseExecuteAsyncOperation()

        with pytest.raises(NotImplementedError):
            asyncio.run(operation.execute_async())

    def test_execute_async_is_required(self) -> None:
        with pytest.raises(TypeError):
            _MissingExecuteAsync()
