import sys
import os
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../..")

import pytest

from mbox import Message


def test_fields():
    m = Message('Tatyana', 'Evgeniy', "Tatyana's letter to Onegin", "I write this to you - what more can be said...")
    assert m.frm == 'Tatyana'
    assert m.to == 'Evgeniy'
    assert m.subj == "Tatyana's letter to Onegin"
    assert m.content == "I write this to you - what more can be said..."


def test_defaults():
    m = Message()
    assert m.frm == 'Unknown sender'
    assert m.to == 'Unknown recipient'
    assert m.subj == 'Default subj'
    assert m.content == 'This is default text'


def test_equal():
    m1 = Message('Tatyana', 'Evgeniy', "Tatyana's letter to Onegin", "...")
    m2 = Message('Tatyana', 'Evgeniy', "Tatyana's letter to Onegin", "...")
    assert m1 == m2


def test_different():
    m1 = Message('Tatyana', 'Evgeniy', "Tatyana's letter to Onegin", "...")
    m2 = Message('Evgeniy', 'Tatyana', "Onegin's letter to Tatyana", "...")
    assert m1 != m2


# Намеренно поломаем тест, чтобы посмотреть, какой вывод даст pytest при разных способах запуска
# def test_different_broken():
#     m1 = Message('Tatyana', 'Evgeniy', "Tatyana's letter to Onegin", "...")
#     m2 = Message('Evgeniy', 'Tatyana', "Onegin's letter to Tatyana", "...")
#     assert m1 == m2

# Способ запуска 1
# pytest tests/test_message_basics.py
# __________ test_different ____________
#
#     def test_different_broken():
#         m1 = Message('Tatyana', 'Evgeniy', "Tatyana's letter to Onegin", "...")
#         m2 = Message('Evgeniy', 'Tatyana', "Onegin's letter to Tatyana", "...")
# >       assert m1 == m2
# E       AssertionError: assert Message(frm='...content='...') == Message(frm='...content='...')
# E
# E         Omitting 1 identical items, use -vv to show
# E         Differing attributes:
# E         ['frm', 'to', 'subj']
# E
# E         Drill down into differing attribute frm:
# E           frm: 'Tatyana' != 'Evgeniy'...
# E
# E         ...Full output truncated (12 lines hidden), use '-vv' to show

# Способ запуска 2
# pytest -vv tests/test_message_basics.py
# _______________ test_different _____________
#
#     def test_different_broken():
#         m1 = Message('Tatyana', 'Evgeniy', "Tatyana's letter to Onegin", "...")
#         m2 = Message('Evgeniy', 'Tatyana', "Onegin's letter to Tatyana", "...")
# >       assert m1 == m2
# E       assert Message(frm='Tatyana', to='Evgeniy', subj="Tatyana's letter to Onegin", content='...')
# == Message(frm='Evgeniy', to='Tatyana', subj="Onegin's letter to Tatyana", content='...')
# E
# E         Matching attributes:
# E         ['content']
# E         Differing attributes:
# E         ['frm', 'to', 'subj']
# E
# E         Drill down into differing attribute frm:
# E           frm: 'Tatyana' != 'Evgeniy'
# E           - Evgeniy
# E           + Tatyana
# E
# E         Drill down into differing attribute to:
# E           to: 'Evgeniy' != 'Tatyana'
# E           - Tatyana
# E           + Evgeniy
# E
# E         Drill down into differing attribute subj:
# E           subj: "Tatyana's letter to Onegin" != "Onegin's letter to Tatyana"
# E           - Onegin's letter to Tatyana
# E           + Tatyana's letter to Onegin

# Текущий тест проверяет, что мы получим соответствующий TypeError, если мы передаем параметр не того типа.
# Например, bool вместо ожидаемого str.
def test_field_type():
    # Ожидаемая ошибка: "TypeError: The field `frm` has `<class 'bool'>` type instead of `<class 'str'>`"
    # 1. Можно проверить текст ошибки через регулярное выражение
    with pytest.raises(TypeError, match="The field `.*` has `.*` type instead of `.*"):
        Message(frm=True)
    # 2. А можно - через данные в самом эксепшене
    with pytest.raises(TypeError) as e:
        Message(frm=True)
    assert "The field `frm` has `<class 'bool'>` type" in str(e)


# Тест разбит на секции Given-When-Then
def test_from_dict():
    # GIVEN an ordinary message
    frm = "Tatyana"
    to = "Evgeniy"
    subj = "Tatyana's letter to Onegin"
    content = "..."
    m1 = Message(frm, to, subj, content)
    # When I create one more message with the dict
    m2 = Message.from_dict(dict(frm=frm, to=to, subj=subj, content=content))
    # THEN both messages are the same
    assert m1 == m2
