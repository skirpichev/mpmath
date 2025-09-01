import os
import sys

import pytest

import mpmath


collect_ignore = ['mpmath/__init__.py',
                  'mpmath/rational.py', 'mpmath/math2.py']


def pytest_report_header(config):
    print("mpmath backend: %s" % mpmath.libmp.backend.BACKEND)
    print("mpmath mp class: %s" % repr(mpmath.mp))
    print("mpmath version: %s" % mpmath.__version__)
    print("Python version: %s" % sys.version)


def pytest_configure(config):
    config.addinivalue_line('markers', 'slow: marks tests as slow')


@pytest.fixture(autouse=True)
def reset_mp_globals():
    from mpmath import mp, iv
    mp.prec = sys.float_info.mant_dig
    mp.pretty = False
    mp.rounding = 'n'
    iv.prec = mp.prec
    iv.pretty = False


@pytest.fixture(autouse=True, scope="session")
def functions_setup_teardown():
    import mpmath
    yield
    stats = mpmath.libmp.backend.stats
    total = sum(stats.values())
    import pprint
    print()
    pprint.pprint({k:v/total for k, v in stats.items()},
                  indent=True, compact=True,
                  sort_dicts=False)
