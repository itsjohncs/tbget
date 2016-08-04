#!/usr/bin/env python

import argparse
import os
import pkg_resources
import re
import sys

import tbget

def get_test_case(name):
    """Returns a test case file object by name.

    This works even if we're in a zip file!
    """
    expected_name = re.sub(r"\.txt", ".expected.txt", name)

    case = pkg_resources.resource_stream("tbget.tests", name)
    expected = pkg_resources.resource_stream("tbget.tests", expected_name)
    return case, expected


def get_all_test_case_names():
    tests = pkg_resources.resource_listdir("tbget", "tests")
    return [i for i in tests if i.endswith(".txt") and
                                not i.endswith(".expected.txt")]


def run_tests():
    num_failures = 0
    for test_case_name in get_all_test_case_names():
        case, expected = get_test_case(test_case_name)
        result = tbget.extract_traceback(case)

        if result.strip() == expected.read().decode("utf-8").strip():
            print "PASS:", test_case_name
        else:
            num_failures += 1
            print "FAIL:", test_case_name
