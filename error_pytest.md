Run pytest \
============================= test session starts ==============================
platform linux -- Python 3.12.12, pytest-9.0.2, pluggy-1.6.0 -- /opt/hostedtoolcache/Python/3.12.12/x64/bin/python
cachedir: .pytest_cache
django: version: 6.0.2, settings: assessment_service.settings (from ini)
rootdir: /home/runner/work/backend-assignment-service/backend-assignment-service
configfile: pytest.ini
plugins: django-4.12.0, cov-7.0.0
collecting ... collected 25 items / 1 error

==================================== ERRORS ====================================
____________________ ERROR collecting assignments/tests.py _____________________
import file mismatch:
imported module 'assignments.tests' has this __file__ attribute:
  /home/runner/work/backend-assignment-service/backend-assignment-service/assignments/tests
which is not the same as the test file we want to collect:
  /home/runner/work/backend-assignment-service/backend-assignment-service/assignments/tests.py
HINT: remove __pycache__ / .pyc files and/or use a unique basename for your test file modules
=========================== short test summary info ============================
ERROR assignments/tests.py
!!!!!!!!!!!!!!!!!!!! Interrupted: 1 error during collection !!!!!!!!!!!!!!!!!!!!
=============================== 1 error in 0.25s ===============================
Error: Process completed with exit code 2.