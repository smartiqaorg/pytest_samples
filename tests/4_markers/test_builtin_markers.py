import sys
import os
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../..")
from packaging.version import parse

import pytest

from mbox import Message, MessageState

# Далее демонстрируем работу со следующими встроенными маркерами:
# 1) @pytest.mark.skip()
# 2) @pytest.mark.skipif()
# 3) @pytest.mark.xfail() в трех вариантах прохождения - падающий тест, успешный и успешный с флагом strict

# Пример запуска:
# pytest -vv tests/4_markers/test_builtin_markers.py
# ============ test session starts ===========
# collected 6 items
# tests/4_markers/test_builtin_markers.py::test_message_as_dict PASSED
# tests/4_markers/test_builtin_markers.py::test_message_as_string_v1_skip SKIPPED (Message doesn't support 'as string' representation yet)
# tests/4_markers/test_builtin_markers.py::test_message_as_string_v2_skipif SKIPPED (Message 'as string' representation is not supported in 1.x)
# tests/4_markers/test_builtin_markers.py::test_message_as_string_v3_xfail XFAIL (Message 'as string' representation is not supported in 1.x)
# tests/4_markers/test_builtin_markers.py::test_xpass XPASS (XPASS demo)
# tests/4_markers/test_builtin_markers.py::test_xfail_strict FAILED
# ======== FAILURES =======
# ______ test_xfail_strict _____
# [XPASS(strict)] Strict demo
# =========== short test summary info ===========
# FAILED tests/4_markers/test_builtin_markers.py::test_xfail_strict
# ========= 1 failed, 1 passed, 2 skipped, 1 xfailed, 1 xpassed in 0.09


# Общая фикстура, которая создает сообщение для нескольких тестов ниже
@pytest.fixture(scope="module")
def message():
    frm = 'Pavel'
    to = 'Alex'
    subj = 'Morning meeting'
    content = 'Lets meet at 10AM'
    state = MessageState.READ
    return Message(frm, to, subj, content, state)


# [ PASSED test ] Проверяет, что метод to_dict() возвращает правильное представление сообщения в виде словаря.
def test_message_as_dict(message):
    dict_from_message = message.to_dict()
    expected_dict = dict(frm=message.frm, to=message.to, subj=message.subj, content=message.content, state=message.state,
                         id=message.id)
    assert dict_from_message == expected_dict


# [ SKIPPED test ] Пропускаем тест с указанием причины - метод to_string() еще не реализован в текущей версии Message.
# Тест будет в любом случае пропускаться, даже если версия Message изменится и метод to_string() будет заимплементирован.
@pytest.mark.skip(reason="Message doesn't support 'as string' representation yet")
def test_message_as_string_v1_skip(message):
    str_from_message = message.to_string()
    expected_str = f"from: {message.frm}, to: {message.to}, subj: {message.subj}, content: {message.content}, state: {message.state}"
    assert str_from_message == expected_str


# [ SKIPPED test ] В данном случае тест будет пропущен, только если версия Message < 2.0.0
@pytest.mark.skipif(condition=parse(Message.__version__()).major < 2,
                    reason="Message 'as string' representation is not supported in 1.x")
def test_message_as_string_v2_skipif(message):
    str_from_message = message.to_string()
    expected_str = f"from: {message.frm}, to: {message.to}, subj: {message.subj}, content: {message.content}, state: {message.state}"
    assert str_from_message == expected_str


# [ XFAIL test ] Тест будет запущен в любом случае и ОЖИДАЕМО упадет на версии ниже 2.0.0 (со статусом XFAIL)
# Если версия будет >= 2.0.0 и тест все равно упадет, то он получит статус реально упавшего теста FAILED (не XFAIL)
@pytest.mark.xfail(condition=parse(Message.__version__()).major < 2,
                   reason="Message 'as string' representation is not supported in 1.x")
def test_message_as_string_v3_xfail(message):
    str_from_message = message.to_string()
    expected_str = f"from: {message.frm}, to: {message.to}, subj: {message.subj}, content: {message.content}, state: {message.state}"
    assert str_from_message == expected_str


# [ XPASS test ] Если тест имеет метку @pytest.mark.xfail и при этом НЕ падает, то он получает статус XPASS
@pytest.mark.xfail(reason="XPASS demo")
def test_xpass():
    m1 = Message()
    m2 = Message()
    assert m1 == m2


# [ FAILED test ] Тест, который ОБЯЗАТЕЛЬНО должен упасть
# Тест будет считаться упавшим (получит статус FAILED), если выполнены следующие условия:
# 1) Тест помечен маркером @pytest.mark.xfail
# 2) В маркере указан параметр strict=True
# 3) Тест при этом НЕ упал (хотя мы ожидали, что упадет)
@pytest.mark.xfail(reason="Strict demo", strict=True)
def test_xfail_strict():
    m1 = Message()
    m2 = Message()
    assert m1 == m2
