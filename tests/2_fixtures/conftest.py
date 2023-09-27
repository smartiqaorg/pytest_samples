import sys
import os
import time
from tempfile import TemporaryDirectory
from pathlib import Path
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../..")

import pytest

from mbox import MBox, Message


# Добавление дополнительных параметров для запуска pytest
def pytest_addoption(parser):
    parser.addoption("--func-scope", action="store_true", default=False, help="New mailbox for each test")


# Фикстура создает маилбокс для тестов и удаляет его после завершения работы.
# Имеет scope=module, т.е. ее первая часть (код до yield) будет вызвана перед всеми тестами внутри данного файла.
# Вторая часть (код после yield) будет вызвана после выполнения всех тестов.
@pytest.fixture(scope='module')
def mbox():
    # 1. Создаем временную директорию
    with TemporaryDirectory() as mb_dir:  # {str} '/var/folders/16/1js1t0tj6x5fm2twrq82tj_w0000gn/T/tmpwyh3cxh8'
        mb_path = Path(mb_dir)  # {PosixPath} '/var/folders/16/1js1t0tj6x5fm2twrq82tj_w0000gn/T/tmpwyh3cxh8'
        # 2. Создаем файл ящика smartiqa.mbox во временной папке
        mbox_obj = MBox(mb_path)
        yield mbox_obj
        # 3. Удаляем файл smartiqa.mbox
        mbox_obj.clear_and_close()


# Функция (НЕ фикстура), которая определяет скоуп на основе наличия/отсутствия параметра --func-scope
def mbox_scope(fixture_name, config):
    if config.getoption("--func-scope", None):
        return "function"
    return "session"


# Фикстура по функционалу идентична вышеидущей фикстуре mbox().
# Единственное отличие - ее скоуп определяется значением, возвращаемым из функции mbox_scope()
@pytest.fixture(scope=mbox_scope)
def mbox_with_dynamic_scope():
    # 1. Создаем временную директорию
    with TemporaryDirectory() as mb_dir:  # {str} '/var/folders/16/1js1t0tj6x5fm2twrq82tj_w0000gn/T/tmpwyh3cxh8'
        mb_path = Path(mb_dir)  # {PosixPath} '/var/folders/16/1js1t0tj6x5fm2twrq82tj_w0000gn/T/tmpwyh3cxh8'
        # 2. Создаем файл ящика smartiqa.mbox во временной папке
        mbox_obj = MBox(mb_path)
        yield mbox_obj
        # 3. Удаляем файл smartiqa.mbox
        mbox_obj.clear_and_close()


# Фикстура удаляет сообщения из базы, что позволяет каждому тесту начинать работу с чистой базы.
# Имеет скоуп function, а значит будет вызываться перед каждым тестом.
@pytest.fixture
def clean_mbox(mbox):
    mbox.clear()
    return mbox

# Вариация предыдущей фикстуры.
# Позволяет динамически (с помощью параметра --func-scope) менять скоуп фикстуры mbox_with_dynamic_scope()
# Как результат, мы можем создавать базу один раз за запуск, а можем - перед каждым тестом.
# Чтобы запустить:
# 1. Нужно РАСкомментировать текущую фиктуру и ЗАкомментировать предыдущую
# 2. Вызвать с помощью команды: pytest --setup-show --func-scope tests/2_fixtures/test_message_count.py
# @pytest.fixture
# def clean_mbox(mbox_with_dynamic_scope):
#     mbox_with_dynamic_scope.clear()
#     return mbox_with_dynamic_scope


# Фикстура возвращает тестовые данные
# Имеет скоуп session, то есть запускается единожды при старте тестов
@pytest.fixture(scope="session")
def some_messages():
    return [
        Message('Pavel', 'Alex', 'Morning meeting'),
        Message('Polina', 'Boris', 'Account mistakes'),
        Message('Milana', 'Ekaterina', 'Coffee break'),
        Message('Elena', 'Nikita', 'Dismissal')
    ]


# Фикстура возвращает объект маилбокса, заранее заполненный тестовыми данными
# Имеет скоуп function, так как маилбокс нужно заполнять заново перед каждым тестом (после кажого теста маилбокс чистится)
@pytest.fixture(scope="function")
def non_empty_mbox(mbox, some_messages):
    for msg in some_messages:
        mbox.add_message(msg)
    return mbox


# Фикстура добавляет в конце теста текущее время
# Обратите внимание на параметр autouse - он указывает, что все тесты будут автоматически использовать данную фикстуру.
# Также важно: при запуске нужно указать флаг -s (--capture=no), чтобы pytest перестал перехватывать вывод в консоль
# Пример запуска: pytest -v -s tests/2_fixtures/test_message_count.py
# ========= test session starts ==========

# tests/2_fixtures/test_message_count.py::test_empty PASSED
# Test duration : 0.001 seconds
#
# tests/2_fixtures/test_message_count.py::test_two_messages PASSED
# Test duration : 0.005 seconds
#
# tests/2_fixtures/test_message_count.py::test_three_messages PASSED
# Test duration : 0.007 seconds
#
# tests/2_fixtures/test_message_count.py::test_multiple_messages PASSED
# Test duration : 0.008 seconds
#
# tests/2_fixtures/test_message_count.py::test_non_empty PASSED
# Test duration : 0.008 seconds
@pytest.fixture(autouse=True)
def footer():
    start = time.time()
    yield
    stop = time.time()
    diff = round(stop - start, 3)
    print(f"\nTest duration : {diff} seconds")
