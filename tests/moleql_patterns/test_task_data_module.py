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
    TaskData as ContractsTaskData,
)
from moleql_patterns.contracts import (
    TaskDeserializationError as ContractsTaskDeserializationError,
)
from moleql_patterns.contracts import (
    TaskSerializationError as ContractsTaskSerializationError,
)
from moleql_patterns.task_data import TaskData, TaskDeserializationError, TaskSerializationError


# =========================================================
# CLASS TEST TASK DATA MODULE EXPORTS
# =========================================================
class TestTaskDataModuleExports:
    def test_task_data_reexport(self) -> None:
        assert TaskData is ContractsTaskData

    def test_task_serialization_error_reexport(self) -> None:
        assert TaskSerializationError is ContractsTaskSerializationError

    def test_task_deserialization_error_reexport(self) -> None:
        assert TaskDeserializationError is ContractsTaskDeserializationError
