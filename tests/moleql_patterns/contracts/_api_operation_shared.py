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

from pydantic import BaseModel

from moleql_patterns.contracts import AccessDeniedError, APIOperation, AsyncAPIOperation


# =========================================================
# CLASS EXAMPLE RESULT
# =========================================================
class ExampleResult(BaseModel):
    value: int


# =========================================================
# CLASS SYNC ACCESS DENIED OPERATION
# =========================================================
class SyncAccessDeniedOperation(APIOperation[ExampleResult]):
    def verify_access(self) -> None:
        raise AccessDeniedError("denied")

    def _execute(self) -> ExampleResult:
        return ExampleResult(value=1)


# =========================================================
# CLASS SYNC FLAG OPERATION
# =========================================================
class SyncFlagOperation(APIOperation[ExampleResult]):
    def __init__(self) -> None:
        self.access_checked = False

    def verify_access(self) -> None:
        self.access_checked = True

    def _execute(self) -> ExampleResult:
        return ExampleResult(value=1)


# =========================================================
# CLASS SYNC MISSING VERIFY ACCESS
# =========================================================
class SyncMissingVerifyAccess(APIOperation[ExampleResult]):
    def _execute(self) -> ExampleResult:
        return ExampleResult(value=1)


# =========================================================
# CLASS SYNC MISSING EXECUTE
# =========================================================
class SyncMissingExecute(APIOperation[ExampleResult]):
    def verify_access(self) -> None:
        return None


# =========================================================
# CLASS SYNC BASE VERIFY ACCESS OPERATION
# =========================================================
class SyncBaseVerifyAccessOperation(APIOperation[ExampleResult]):
    def verify_access(self) -> None:
        return APIOperation.verify_access(self)

    def _execute(self) -> ExampleResult:
        return ExampleResult(value=1)


# =========================================================
# CLASS SYNC BASE EXECUTE OPERATION
# =========================================================
class SyncBaseExecuteOperation(APIOperation[ExampleResult]):
    def verify_access(self) -> None:
        return None

    def _execute(self) -> ExampleResult:
        return APIOperation._execute(self)


# =========================================================
# CLASS ASYNC ACCESS DENIED OPERATION
# =========================================================
class AsyncAccessDeniedOperation(AsyncAPIOperation[ExampleResult]):
    def verify_access(self) -> None:
        raise AccessDeniedError("denied")

    async def _execute_async(self) -> ExampleResult:
        return ExampleResult(value=1)


# =========================================================
# CLASS ASYNC FLAG OPERATION
# =========================================================
class AsyncFlagOperation(AsyncAPIOperation[ExampleResult]):
    def __init__(self) -> None:
        self.access_checked = False

    def verify_access(self) -> None:
        self.access_checked = True

    async def _execute_async(self) -> ExampleResult:
        return ExampleResult(value=1)


# =========================================================
# CLASS ASYNC MISSING VERIFY ACCESS
# =========================================================
class AsyncMissingVerifyAccess(AsyncAPIOperation[ExampleResult]):
    async def _execute_async(self) -> ExampleResult:
        return ExampleResult(value=1)


# =========================================================
# CLASS ASYNC MISSING EXECUTE ASYNC
# =========================================================
class AsyncMissingExecuteAsync(AsyncAPIOperation[ExampleResult]):
    def verify_access(self) -> None:
        return None


# =========================================================
# CLASS ASYNC BASE VERIFY ACCESS OPERATION
# =========================================================
class AsyncBaseVerifyAccessOperation(AsyncAPIOperation[ExampleResult]):
    def verify_access(self) -> None:
        return AsyncAPIOperation.verify_access(self)

    async def _execute_async(self) -> ExampleResult:
        return ExampleResult(value=1)


# =========================================================
# CLASS ASYNC BASE EXECUTE OPERATION
# =========================================================
class AsyncBaseExecuteOperation(AsyncAPIOperation[ExampleResult]):
    def verify_access(self) -> None:
        return None

    async def _execute_async(self) -> ExampleResult:
        return await AsyncAPIOperation._execute_async(self)
