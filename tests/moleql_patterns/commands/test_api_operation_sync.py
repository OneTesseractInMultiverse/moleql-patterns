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

import pytest

from moleql_patterns.commands import AccessDeniedError

from ._api_operation_shared import (
    ExampleResult,
    SyncAccessDeniedOperation,
    SyncBaseExecuteOperation,
    SyncBaseVerifyAccessOperation,
    SyncFlagOperation,
    SyncMissingExecute,
    SyncMissingVerifyAccess,
)


# =========================================================
# CLASS TEST API OPERATION VERIFY ACCESS
# =========================================================
class TestAPIOperationVerifyAccess:
    def test_verify_access_blocks_execution(self) -> None:
        operation = SyncAccessDeniedOperation()

        with pytest.raises(AccessDeniedError):
            operation.execute()

    def test_verify_access_base_raises(self) -> None:
        operation = SyncBaseVerifyAccessOperation()

        with pytest.raises(NotImplementedError):
            operation.execute()

    def test_verify_access_is_required(self) -> None:
        with pytest.raises(TypeError):
            SyncMissingVerifyAccess()

    def test_verify_access_runs(self) -> None:
        operation = SyncFlagOperation()

        operation.execute()

        assert operation.access_checked is True


# =========================================================
# CLASS TEST API OPERATION EXECUTE
# =========================================================
class TestAPIOperationExecute:
    def test_execute_returns_model(self) -> None:
        operation = SyncFlagOperation()

        result = operation.execute()

        assert isinstance(result, ExampleResult)

    def test_execute_base_raises(self) -> None:
        operation = SyncBaseExecuteOperation()

        with pytest.raises(NotImplementedError):
            operation.execute()

    def test_execute_is_required(self) -> None:
        with pytest.raises(TypeError):
            SyncMissingExecute()
