import sys
import os
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../..")

from mbox import Message


# Фикстуры для данных тестов лежат в файле conftest.py.

# Фикстура clean_mbox() передается параметром в каждый из тестов.
# С точки зрения функционала она удаляет сообщения из базы между тестами.
# Без нее тест test_three() упал бы, т.к. test_two() так же добавляет сообщения в базу.
# Обратите внимание, что внутри себя фикстура clean_mbox() также параметром получает объект mbox_obj через фикстуру mbox()


def test_empty(clean_mbox):
    assert clean_mbox.count() == 0


def test_two_messages(clean_mbox):
    clean_mbox.add_message(Message(subj='First'))
    clean_mbox.add_message(Message(subj='Second'))
    # Содержимое маилбокса после добавления двух сообщений
    # (venv) tati@tk T % cat tmpyz2s7_zc/smartiqa.mbox
    # From MAILER-DAEMON Tue Sep 19 09:12:44 2023
    # From: Unknown sender
    # To: Unknown recipient
    # Subject: First
    #
    # This is default text
    #
    # From MAILER-DAEMON Tue Sep 19 09:12:44 2023
    # From: Unknown sender
    # To: Unknown recipient
    # Subject: Second
    #
    # This is default text
    assert clean_mbox.count() == 2


def test_three_messages(clean_mbox):
    clean_mbox.add_message(Message(subj='First'))
    clean_mbox.add_message(Message(subj='Second'))
    clean_mbox.add_message(Message(subj='Third'))
    assert clean_mbox.count() == 3


# В данном тесте сообщения берем из фикстуры some_messages()
def test_multiple_messages(clean_mbox, some_messages):
    for msg in some_messages:
        clean_mbox.add_message(msg)
    assert clean_mbox.count() == len(some_messages)


# Здесь в качестве параметра принимаем объект заполненного сообщениями маилбокса (фикстура non_empty_mbox())
def test_non_empty(non_empty_mbox):
    assert non_empty_mbox.count() > 0
