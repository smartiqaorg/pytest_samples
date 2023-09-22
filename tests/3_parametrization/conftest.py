import sys
import os
from tempfile import TemporaryDirectory
from pathlib import Path
sys.path.append(f"{os.path.dirname(os.path.abspath(__file__))}/../..")

import pytest

from mbox import MBox


# Фикстура создает маилбокс для тестов и удаляет его после завершения работы.
@pytest.fixture(scope='module')
def mbox():
    with TemporaryDirectory() as mb_dir:  # {str} '/var/folders/16/1js1t0tj6x5fm2twrq82tj_w0000gn/T/tmpwyh3cxh8'
        mb_path = Path(mb_dir)  # {PosixPath} '/var/folders/16/1js1t0tj6x5fm2twrq82tj_w0000gn/T/tmpwyh3cxh8'
        mbox_obj = MBox(mb_path)
        yield mbox_obj
        mbox_obj.close()


# Фикстура удаляет сообщения из базы, что позволяет каждому тесту начинать работу с чистой базы.
@pytest.fixture
def clean_mbox(mbox):
    mbox.clear()
    return mbox
