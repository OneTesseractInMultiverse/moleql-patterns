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

from moleql_patterns.contracts import (
    AsyncTask as ContractsAsyncTask,
)
from moleql_patterns.contracts import (
    Task as ContractsTask,
)
from moleql_patterns.contracts import (
    TaskBase as ContractsTaskBase,
)
from moleql_patterns.contracts import (
    TaskDataDeserializationError as ContractsTaskDataDeserializationError,
)
from moleql_patterns.task import AsyncTask, Task, TaskBase, TaskDataDeserializationError


# =========================================================
# CLASS TEST TASK MODULE EXPORTS
# =========================================================
class TestTaskModuleExports:
    def test_task_base_reexport(self) -> None:
        assert TaskBase is ContractsTaskBase

    def test_task_reexport(self) -> None:
        assert Task is ContractsTask

    def test_async_task_reexport(self) -> None:
        assert AsyncTask is ContractsAsyncTask

    def test_task_data_deserialization_error_reexport(self) -> None:
        assert TaskDataDeserializationError is ContractsTaskDataDeserializationError
