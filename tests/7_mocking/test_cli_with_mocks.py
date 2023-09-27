from typer.testing import CliRunner
import mbox_cli
from mbox_cli import app
import shlex
from unittest import mock
import mbox

import pytest

from mbox import MBox

# В данном файле тестируем CLI интерфейс модуля mbox (хранится в файле)
# Так как функционал самого модуля mbox уже протестирован ранее, то на текущем этапе наша задача - протестировать только работу CLI
# Чтобы изолировать функционал mbox - используем моки

runner = CliRunner()


# Обертка, которая возволяет нам просто передавать название команды интерфейса (например, 'add') для ее вызова
def mbox_cli_wrapper(command_string):
    command_list = shlex.split(command_string)
    output = runner.invoke(app, command_list).stdout.rstrip().split('\n')[-1]
    return output


""" [ 1 ] ======== Мокаем атрибут ========= """


# Тестируемая команда: 'version'
# Мокаем атрибут __version__ модуля mbox, чтобы он имел значение "1.2.5".
def test_version():
    with mock.patch.object(mbox, "__version__", "1.2.5"):
        result = mbox_cli_wrapper("version")
        # Проверяем, что CLI вывела в консоль именно указанное нами значение
        assert result == "1.2.5"


""" [ 2 ] ======== Мокаем классы и методы ======== """


# Тестируемая команда: 'path'
# Проверяем, что CLI выведет указанный путь до маилбокса. Тест можно написать в нескольких вариантах:

# Вариант 1. Замокаем метод path()
def test_path_v1():
    with mock.patch.object(MBox, 'path') as mocked_path:
        mocked_path.return_value = 'fake_path'
        result = mbox_cli_wrapper("path")
    assert result == 'fake_path'


# Вариант 2. Замокаем весь класс MBox
def test_path_v2():
    # with mock.patch('mbox_cli.MBox', autospec=True) as mocked_mbox_class:  # Аналог записи
    with mock.patch.object(mbox_cli, 'MBox', autospec=True) as mocked_mbox_class:
        mocked_mbox_class.return_value.path.return_value = 'fake_path'
        result = mbox_cli_wrapper("path")
    assert result == 'fake_path'


# Вариант 3. Снова замокаем весь класс MBox, но теперь создание мока вынесем в отдельную фикстуру.
# Обратите внимание, что она нам еще пригодится в других тестах.
@pytest.fixture()
def mocked_mbox_object():
    with mock.patch.object(mbox_cli, 'MBox', autospec=True) as MockedMboxClass:
        # Возвращаем экземпляр(!) замоканного класса (return_value для класса эквивалентно созданию объекта этого класса)
        yield MockedMboxClass.return_value


def test_path_v3(mocked_mbox_object):
    mocked_mbox_object.path.return_value = 'fake_path'
    result = mbox_cli_wrapper("path")
    assert result == 'fake_path'


""" [ 3 ] ======== Используем метод assert_called_with() ======== """


# Тестируемая команда: 'add'
# Проверяем, что при создании письма через CLI будет вызван API метод add_message() с нужным параметром
def test_add(mocked_mbox_object):
    frm = 'Anna K'
    to = 'Andrew L'
    subj = 'Additional changes'
    content = 'Im writing to inform you that...'
    mbox_cli_wrapper(f"add '{frm}' '{to}' '{subj}' '{content}'")
    expected_message = mbox.Message(frm, to, subj, content)
    mocked_mbox_object.add_message.assert_called_with(expected_message)


""" [ 4 ] ======== Закладываем ошибки с помощью атрибута side_effect ======== """


# Тестируемая команда: 'delete'
# Проверяем, что в консоли будет напечатано правильное сообщение,
# если при удалении будет выброшено исключение InvalidIdError
def test_delete_invalid(mocked_mbox_object):
    mocked_mbox_object.remove_message.side_effect = mbox.InvalidIdError
    output = mbox_cli_wrapper("delete 100")
    assert "Error: Invalid message id 100" in output
