# [ 1 ] Запуск через плагин pytest-cov
pytest --cov=mbox tests
  # platform darwin -- Python 3.9.16, pytest-7.4.2, pluggy-1.3.0
  # rootdir: /Users/tati/Git Repos/pytest_samples
  # plugins: Faker-19.6.2, cov-4.1.0
  # collected 38 items
  #
  # tests/1_basics/test_message_basics.py
  # tests/2_fixtures/test_message_count.py
  # tests/3_parametrization/test_parametrize.py
  # tests/4_markers/test_builtin_markers.py .ssxXF
  # tests/4_markers/test_custom_markers.py
  # tests/4_markers/test_custom_markers_with_params.py
  #
  # ========== FAILURES ============
  #____________ test_xfail_strict ___________
  # [XPASS(strict)] Strict demo
  #
  # ---------- coverage: platform darwin, python 3.9.16-final-0 ----------
  # Name      Stmts   Miss  Cover
  # -----------------------------
  # mbox.py      83      3    96%
  # -----------------------------
  # TOTAL        83      3    96%
  #
  # ========== short test summary info ===========
  # FAILED tests/4_markers/test_builtin_markers.py::test_xfail_strict
  # ============ 1 failed, 33 passed, 2 skipped, 1 xfailed, 1 xpassed in 0.57s ============

# [ 2 ] Запуск напрямую через coverage
coverage run --source=mbox -m pytest tests
coverage report
  # =========== test session starts =========
  #platform darwin -- Python 3.9.16, pytest-7.4.2, pluggy-1.3.0
  #rootdir: /Users/tati/Git Repos/pytest_samples
  #plugins: Faker-19.6.2, cov-4.1.0
  #collected 38 items
  #
  #tests/1_basics/test_message_basics.py ......
  #tests/2_fixtures/test_message_count.py .....
  #tests/3_parametrization/test_parametrize.py ..........
  #tests/4_markers/test_builtin_markers.py .ssxXF
  #tests/4_markers/test_custom_markers.py ......
  #tests/4_markers/test_custom_markers_with_params.py .....
  #
  # ======== FAILURES =========
  # _________ test_xfail_strict __________
  # [XPASS(strict)] Strict demo
  # ========== short test summary info ==========
  # FAILED tests/4_markers/test_builtin_markers.py::test_xfail_strict
  # ============ 1 failed, 33 passed, 2 skipped, 1 xfailed, 1 xpassed in 0.59s =============
  # Name      Stmts   Miss  Cover
  # -----------------------------
  # mbox.py      83      3    96%
  # -----------------------------
  # TOTAL        83      3    96%


# [ 3 ] Запуск через плагин pytest-cov с выводом номеров строк, которые не покрыты тестами
pytest --cov=mbox --cov-report=term-missing tests
  # ---------- coverage: platform darwin, python 3.9.16-final-0 ----------
  # Name      Stmts   Miss  Cover   Missing
  # ---------------------------------------
  # mbox.py      83      3    96%   98-100
  # ---------------------------------------
  # TOTAL        83      3    96%

# [ 4 ] Аналогичный запуск через утилиту coverage с выводом номеров строк, которые не покрыты тестами
coverage report --show-missing

# [ 5 ] Запуск через плагин pytest-cov с отчетом в формате html
# Отчет бует лежать в htmlcov/index.html
pytest --cov=mbox --cov-report=html tests

# [ 6 ] Запуск через coverage с отчетом в формате html
coverage html
# Wrote HTML report to htmlcov/index.html

# [ 7 ] Проверка покрытия самих тестов
pytest --cov=tests tests

