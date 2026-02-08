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
from pydantic import ValidationError

from moleql_patterns.contracts import TaskData, TaskDeserializationError, TaskSerializationError


# =========================================================
# CLASS CONCRETE TASK DATA
# =========================================================
class _ConcreteTaskData(TaskData):
    pass


# =========================================================
# CLASS TEST TASK DATA VALIDATION
# =========================================================
class TestTaskDataValidation:
    def test_base_class_is_abstract(self) -> None:
        with pytest.raises(TypeError):
            TaskData()

    def test_requires_correlation_id(self) -> None:
        with pytest.raises(ValidationError):
            _ConcreteTaskData()

    def test_rejects_empty_correlation_id(self) -> None:
        with pytest.raises(ValidationError):
            _ConcreteTaskData(correlation_id="")

    def test_rejects_extra_fields(self) -> None:
        with pytest.raises(ValidationError):
            _ConcreteTaskData(correlation_id="test", extra_field="nope")


# =========================================================
# CLASS TEST TASK DATA TO PAYLOAD
# =========================================================
class TestTaskDataToPayload:
    def test_to_payload_contains_correlation_id(self) -> None:
        data = _ConcreteTaskData(correlation_id="test")

        payload = data.to_payload()

        assert payload == {"correlation_id": "test"}

    def test_to_payload_raises_custom_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def fail(_self: TaskData) -> dict[str, object]:
            raise RuntimeError("boom")

        monkeypatch.setattr(TaskData, "model_dump", fail)

        data = _ConcreteTaskData(correlation_id="test")

        with pytest.raises(TaskSerializationError):
            data.to_payload()


# =========================================================
# CLASS TEST TASK DATA FROM PAYLOAD
# =========================================================
class TestTaskDataFromPayload:
    def test_from_payload_constructs_instance(self) -> None:
        payload = {"correlation_id": "test"}

        data = _ConcreteTaskData.from_payload(payload)

        assert data.correlation_id == "test"

    def test_from_payload_raises_custom_error(self, monkeypatch: pytest.MonkeyPatch) -> None:
        def fail(_cls: type[TaskData], _payload: dict[str, object]) -> TaskData:
            raise RuntimeError("boom")

        monkeypatch.setattr(TaskData, "model_validate", classmethod(fail))

        payload = {"correlation_id": "test"}

        with pytest.raises(TaskDeserializationError):
            _ConcreteTaskData.from_payload(payload)
