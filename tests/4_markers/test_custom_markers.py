import sys
import os
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../..")

import pytest

from mbox import Message, MessageState, InvalidIdError

# Чтобы не получать от pytest варнинги на тему несуществующих маркеров, необходимо их зарегистрировать.
# Это можно сделать двумя способами:
# 1. Добавить секцию в файле pytest.ini (должен лежать в корне проекта)
# [pytest]
# markers =
#     smoke: Main positive tests
#     exception: Exception handling tests
#
# 2. Зарегистрировать их динамически в хуке pytest_configure() - мы используем данный способ (см файл conftest.py)
# MARKERS = dict(smoke='Main positive tests', exception='Exception handling tests')
# def pytest_configure(config):
#     for marker, test_type in MARKERS.items():
#         config.addinivalue_line("markers", f"{marker}: this is for {test_type}")


# Примеры запуска тестов:

# [1] pytest -v -m smoke
# ============= test session starts ==========
# collected 33 items / 31 deselected / 2 selected
# tests/4_markers/test_custom_markers.py::test_read_message PASSED
# tests/4_markers/test_custom_markers.py::TestAnswerMessage::test_answer_message_from_unread[Read] PASSED

# [2] pytest -v -m "smoke and read"
# ============= test session starts ==========
# collected 33 items / 32 deselected / 1 selected
# tests/4_markers/test_custom_markers.py::test_read_message PASSED

# [3] pytest -v -m "answer or read"
# ============= test session starts ==========
# collected 33 items / 27 deselected / 6 selected
# tests/4_markers/test_custom_markers.py::test_read_message PASSED
# tests/4_markers/test_custom_markers.py::test_read_message_non_existent PASSED
# tests/4_markers/test_custom_markers.py::TestAnswerMessage::test_answer_message_from_unread[Unread] PASSED
# tests/4_markers/test_custom_markers.py::TestAnswerMessage::test_answer_message_from_unread[Read] PASSED
# tests/4_markers/test_custom_markers.py::TestAnswerMessage::test_answer_message_from_unread[Forwarded] PASSED
# tests/4_markers/test_custom_markers.py::TestAnswerMessage::test_answer_message_non_existent PASSED

# [4] pytest -v -m "(answer or read) and (not smoke)"
# ============= test session starts ==========
# collected 33 items / 29 deselected / 4 selected
# tests/4_markers/test_custom_markers.py::test_read_message_non_existent PASSED
# tests/4_markers/test_custom_markers.py::TestAnswerMessage::test_answer_message_from_unread[Unread] PASSED
# tests/4_markers/test_custom_markers.py::TestAnswerMessage::test_answer_message_from_unread[Forwarded] PASSED
# tests/4_markers/test_custom_markers.py::TestAnswerMessage::test_answer_message_non_existent PASSED


# Тест проверяет, что после прочтения непрочитанного сообщения его статус становится READ
# [ Маркеры ] read, smoke
@pytest.mark.read
@pytest.mark.smoke
def test_read_message(clean_mbox):
    message = Message(state=MessageState.UNREAD)
    id = clean_mbox.add_message(message)
    clean_mbox.read_message(id)
    message_from_mbox = clean_mbox.get_message(id)
    assert message_from_mbox.state == MessageState.READ


# Тест проверяет, что соответствующая ошибка выбрасывается при попытке чтения несуществующего сообщения
# [ Маркеры ] read, exception
@pytest.mark.read
@pytest.mark.exception
def test_read_message_non_existent(clean_mbox):
    non_existent_id = 999
    with pytest.raises(InvalidIdError):
        clean_mbox.read_message(non_existent_id)


@pytest.mark.answer
class TestAnswerMessage:
    # Тест проверяет, что после ответа на непрочитанное/прочитанное/пересланное сообщение его статус становится ANSWERED
    # [ Маркеры Тест 1 ] answer (наследуется от класса)
    # [ Маркеры Тест 2 ] answer (наследуется от класса), smoke (указывается при параметризации)
    # [ Маркеры Тест 3 ] answer (наследуется от класса)
    @pytest.mark.parametrize("start_state",
                             [
                                 MessageState.UNREAD,
                                 pytest.param(MessageState.READ, marks=pytest.mark.smoke),
                                 MessageState.FORWARDED,
                             ])
    def test_answer_message_from_unread(self, clean_mbox, start_state):
        message = Message(state=start_state)
        id = clean_mbox.add_message(message)
        clean_mbox.answer_message(id)
        message_from_mbox = clean_mbox.get_message(id)
        assert message_from_mbox.state == MessageState.ANSWERED

    # Тест проверяет, что соответствующая ошибка выбрасывается при попытке ответить на несуществующее сообщение
    # [ Маркеры ] answer (наследуется от класса), exception
    @pytest.mark.exception
    def test_answer_message_non_existent(self, clean_mbox):
        non_existent_id = 999
        with pytest.raises(InvalidIdError):
            clean_mbox.answer_message(non_existent_id)
