#!/usr/bin/env python

from os.path import abspath, dirname
import sys


from django.conf import settings


if not settings.configured:
    settings.configure(
        INSTALLED_APPS=["partial_include", "tests"],
        DATABASES={
            "default": {
                "ENGINE": "django.db.backends.sqlite3",
            },
        },
    )


def runtests(*test_args):
    if not test_args:
        test_args = ["tests"]

    parent = dirname(dirname(abspath(__file__)))
    sys.path.insert(0, parent)

    from django.test.simple import DjangoTestSuiteRunner
    failures = DjangoTestSuiteRunner(
        verbosity=1,
        interactive=True,
        failfast=False,
    ).run_tests(test_args)
    sys.exit(failures)


if __name__ == "__main__":
    runtests()
