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

from moleql_patterns.contracts import AccessDeniedError

from ._api_operation_shared import (
    AsyncAccessDeniedOperation,
    AsyncBaseExecuteOperation,
    AsyncBaseVerifyAccessOperation,
    AsyncFlagOperation,
    AsyncMissingExecuteAsync,
    AsyncMissingVerifyAccess,
    ExampleResult,
)


# =========================================================
# CLASS TEST ASYNC API OPERATION VERIFY ACCESS
# =========================================================
class TestAsyncAPIOperationVerifyAccess:
    def test_verify_access_blocks_execution(self) -> None:
        operation = AsyncAccessDeniedOperation()

        with pytest.raises(AccessDeniedError):
            asyncio.run(operation.execute_async())

    def test_verify_access_base_raises(self) -> None:
        operation = AsyncBaseVerifyAccessOperation()

        with pytest.raises(NotImplementedError):
            asyncio.run(operation.execute_async())

    def test_verify_access_is_required(self) -> None:
        with pytest.raises(TypeError):
            AsyncMissingVerifyAccess()

    def test_verify_access_runs(self) -> None:
        operation = AsyncFlagOperation()

        asyncio.run(operation.execute_async())

        assert operation.access_checked is True


# =========================================================
# CLASS TEST ASYNC API OPERATION EXECUTE ASYNC
# =========================================================
class TestAsyncAPIOperationExecuteAsync:
    def test_execute_async_returns_model(self) -> None:
        operation = AsyncFlagOperation()

        result = asyncio.run(operation.execute_async())

        assert isinstance(result, ExampleResult)

    def test_execute_async_base_raises(self) -> None:
        operation = AsyncBaseExecuteOperation()

        with pytest.raises(NotImplementedError):
            asyncio.run(operation.execute_async())

    def test_execute_async_is_required(self) -> None:
        with pytest.raises(TypeError):
            AsyncMissingExecuteAsync()
