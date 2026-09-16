import os
import pytest
import allure
from playwright.sync_api import sync_playwright

from run_tests import (
    HEADLESS,
    SLOW_MO,
    VIEWPORT,
    DEFAULT_TIMEOUT,
    NAVIGATION_TIMEOUT,
)

@pytest.fixture
def page():
    with sync_playwright() as p:
        browser = p.chromium.launch(
            headless=HEADLESS,
            slow_mo=SLOW_MO
        )
        context = browser.new_context(
            viewport=VIEWPORT,
            ignore_https_errors=True
        )
        context.set_default_timeout(DEFAULT_TIMEOUT)
        context.set_default_navigation_timeout(NAVIGATION_TIMEOUT)
        page = context.new_page()
        yield page
        context.close()
        browser.close()


@pytest.hookimpl(tryfirst=True)
def pytest_runtest_setup(item):
    folder_name = os.path.basename(os.path.dirname(str(item.fspath)))
    file_name = os.path.splitext(os.path.basename(str(item.fspath)))[0]

    allure.dynamic.parent_suite(folder_name)
    allure.dynamic.suite(file_name)

@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_call(item):
    test_path = os.path.normpath(str(item.fspath))
    # Get testcase folder name: datasets / files
    pytest.current_test_folder = os.path.basename(
        os.path.dirname(test_path)
    )
    # Get testcase file name without .py
    pytest.current_test_file = os.path.splitext(
        os.path.basename(test_path)
    )[0]
    yield
    pytest.current_test_folder = None
    pytest.current_test_file = None