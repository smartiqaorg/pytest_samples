import sys
import os
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../..")

import pytest
from faker import Faker

from mbox import Message

# В текущем файле продемонстрируем работу пользовательского маркера с параметром (@pytest.mark.num_messages())

# Для работы тестов из данного файла необходимо установить пакет Faker: pip3 install faker.
# С его помощью будем генерировать рандомные данные для сообщений. Краткий обзор функций:
# Faker is a Python package that generates fake data for you. Whether you need to bootstrap your database,
# create good-looking XML documents, fill-in your persistence to stress test it,
# or anonymize data taken from a production service, Faker is for you.
@pytest.fixture(scope="module")
def faker():
    faker = Faker()
    faker.seed_instance(101)
    return faker


@pytest.fixture(scope="function")
def mbox_with_messages(mbox, request, faker):
    # 1. Чистим маилбокс
    mbox.clear()
    # 2. Если тест помечен маркером num_messages, то получаем объект маркера (иначе None)
    num_messages_marker = request.node.get_closest_marker("num_messages")
    if (not num_messages_marker) or (len(num_messages_marker.args) == 0):
        return mbox
    # 3. Забираем первый аргумент маркера
    num_messages = num_messages_marker.args[0]
    # 4. Создаем нужное количество сообщений с рандомными данными из Faker
    for _ in range(num_messages):
        # Message(frm='Chloe Sanford', to='Julie Alvarado', subj='Play.', content='True magazine situation forget just.', state='Unread')
        message = Message(frm=faker.name(), to=faker.name(), subj=faker.sentence(nb_words=2), content=faker.sentence())
        mbox.add_message(message)
    return mbox


def test_no_messages_no_mark(mbox_with_messages):
    assert mbox_with_messages.count() == 0


@pytest.mark.num_messages
def test_no_messages(mbox_with_messages):
    assert mbox_with_messages.count() == 0


@pytest.mark.num_messages(0)
def test_zero_messages(mbox_with_messages):
    assert mbox_with_messages.count() == 0


@pytest.mark.num_messages(3)
def test_three_messages(mbox_with_messages):
    assert mbox_with_messages.count() == 3


@pytest.mark.num_messages(20)
def test_twenty_messages(mbox_with_messages):
    assert mbox_with_messages.count() == 20