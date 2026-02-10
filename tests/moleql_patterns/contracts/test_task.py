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

from moleql_patterns.contracts import AsyncTask, Task, TaskBase, TaskDataDeserializationError

from ._task_shared import (
    AsyncTaskExample,
    AsyncTaskWithoutDataCls,
    AsyncTaskWithoutExec,
    ExampleTaskData,
    SyncTask,
    TaskWithoutDataCls,
    TaskWithoutExec,
)


# =========================================================
# CLASS TEST TASK BASE INIT
# =========================================================
class TestTaskBaseInit:
    def test_base_class_is_abstract(self) -> None:
        with pytest.raises(TypeError):
            TaskBase({"correlation_id": "test"})

    def test_missing_task_data_cls_raises(self) -> None:
        with pytest.raises(TaskDataDeserializationError):
            TaskWithoutDataCls({"correlation_id": "test"})

    def test_missing_task_data_cls_raises_for_async(self) -> None:
        with pytest.raises(TaskDataDeserializationError):
            AsyncTaskWithoutDataCls({"correlation_id": "test"})

    def test_init_sets_task_data(self) -> None:
        task = SyncTask({"correlation_id": "test"})

        assert isinstance(task.task_data, ExampleTaskData)


# =========================================================
# CLASS TEST TASK EXEC
# =========================================================
class TestTaskExec:
    def test_exec_returns_value(self) -> None:
        task = SyncTask({"correlation_id": "test"})

        result = task.exec()

        assert result == "ok"

    def test_base_exec_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            Task.exec(object())

    def test_exec_is_required(self) -> None:
        with pytest.raises(TypeError):
            TaskWithoutExec({"correlation_id": "test"})


# =========================================================
# CLASS TEST ASYNC TASK EXEC
# =========================================================
class TestAsyncTaskExec:
    def test_exec_returns_value(self) -> None:
        task = AsyncTaskExample({"correlation_id": "test"})

        result = asyncio.run(task.exec())

        assert result == "ok"

    def test_base_exec_raises(self) -> None:
        with pytest.raises(NotImplementedError):
            asyncio.run(AsyncTask.exec(object()))

    def test_exec_is_required(self) -> None:
        with pytest.raises(TypeError):
            AsyncTaskWithoutExec({"correlation_id": "test"})
