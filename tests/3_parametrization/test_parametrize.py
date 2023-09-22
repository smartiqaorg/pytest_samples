import sys
import os
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../..")

import pytest

from mbox import Message, MessageState


""" 0. Тест без параметризации """


# В цикле перебираем список с сообщениями и для каждого проверяем, что правильно сменился статус
#
# Запуск (обратите вимание, что запускается всего 1 тест):
# pytest -vv tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_loop
# ============ test session starts ===========
# collected 1 item
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_loop PASSED
def test_check_answered_state_with_loop(clean_mbox):
    messages = [
        Message(subj='First', state=MessageState.UNREAD),
        Message(subj='Second', state=MessageState.READ),
        Message(subj='Third')
    ]
    for msg in messages:
        id = clean_mbox.add_message(msg)
        clean_mbox.answer_message(id)
        assert clean_mbox.get_message(id).state == MessageState.ANSWERED


""" 1. Параметризованный тест """


# Тест запускается 3 раза с разными значениями параметров.
# Первый раз будет запущен со следующими значениями: subj='First' state=MessageState.UNREAD

# Запуск (обратите внимание, что текущий параметризованный тест запускается в 3 этапа):
# pytest -vv tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_function_parametrization
# ============ test session starts ===========
# collected 3 items
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_function_parametrization[First-Unread] PASSED   [ 33%]
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_function_parametrization[Second-Read] PASSED    [ 66%]
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_function_parametrization[Third-Answered] PASSED [100%]
# ============ 3 passed in 0.03s =============
@pytest.mark.parametrize('subj,state',
                         [('First', MessageState.UNREAD),
                          ('Second', MessageState.READ),
                          ('Third', MessageState.ANSWERED)])
def test_check_answered_state_with_function_parametrization(clean_mbox, subj, state):
    message = Message(subj=subj, state=state)
    id = clean_mbox.add_message(message)
    clean_mbox.answer_message(id)
    assert clean_mbox.get_message(id).state == MessageState.ANSWERED


""" 2. Тест, который принимает в качестве параметра параметризованную фикстуру message_data() """


# Тест также запускается 3 раза с разными значениями параметров.
# При первом запуске message_data=['First', MessageState.UNREAD]

# Запуск (текущий тест так же запускается в 3 этапа):
# pytest -vv tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_fixture_parametrization
# ============ test session starts ===========
# collected 3 items
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_fixture_parametrization[message_data0] PASSED
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_fixture_parametrization[message_data1] PASSED
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_fixture_parametrization[message_data2] PASSED
@pytest.fixture(params=[['First', MessageState.UNREAD], ['Second', MessageState.READ], ['Third', MessageState.ANSWERED]])
def message_data(request):
    return request.param


def test_check_answered_state_with_fixture_parametrization(clean_mbox, message_data):
    message = Message(subj=message_data[0], state=message_data[1])
    id = clean_mbox.add_message(message)
    clean_mbox.answer_message(id)
    assert clean_mbox.get_message(id).state == MessageState.ANSWERED


""" 3. Тест с параметризацией через хук pytest_generate_tests """


# При запуске (каждого) теста вызывается хук pytest_generate_tests()
# и проверяется, есть ли у будущего теста в параметрах имена фикстур subj_from_hook и state_from_hook.
# У нашего теста такие фикстуры есть, значит добавляется параметризация.
def pytest_generate_tests(metafunc):
    if ("subj_from_hook" in metafunc.fixturenames) and ("state_from_hook" in metafunc.fixturenames):
        metafunc.parametrize("subj_from_hook,state_from_hook",
                             [('First', MessageState.UNREAD),
                              ('Second', MessageState.READ),
                              ('Third', MessageState.ANSWERED)])


# Тест также запускается 3 раза с разными значениями параметров.
# При первом запуске subj_from_hook='First' state_from_hook=MessageState.UNREAD

# Запуск:
# pytest -vv tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_hook_parametrization
# ============ test session starts ===========
# collected 3 items
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_hook_parametrization[First-Unread] PASSED
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_hook_parametrization[Second-Read] PASSED
# tests/3_parametrization/test_parametrize.py::test_check_answered_state_with_hook_parametrization[Third-Answered] PASSED
def test_check_answered_state_with_hook_parametrization(clean_mbox, subj_from_hook, state_from_hook):
    message = Message(subj=subj_from_hook, state=state_from_hook)
    id = clean_mbox.add_message(message)
    clean_mbox.answer_message(id)
    assert clean_mbox.get_message(id).state == MessageState.ANSWERED
