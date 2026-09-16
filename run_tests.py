
# If you want to run testcases you can use the following command in the terminal:
# python run_tests.py
# Generate allure reports after test execution using the following command in the terminal:
# allure serve allure-results

import os
import shutil
import subprocess
import sys
from glob import glob

# Browser Configuration
HEADLESS = False
SLOW_MO = 500
VIEWPORT = {
    "width": 1260,
    "height": 900
}
DEFAULT_TIMEOUT = 3000
NAVIGATION_TIMEOUT = 30000


TEST_FILES = [
            "tests/workflows/TC_02*.py"
            ]

if __name__ == "__main__":
    # Delete old reports
    for folder in ["allure-results", "allure-report", "reports"]:
        if os.path.exists(folder):
            shutil.rmtree(folder)
    # Run tests
    test_files = []
    for test_path in TEST_FILES:
        if "*" in test_path:
            test_files.extend(glob(test_path))
        else:
            test_files.append(test_path)
    if not test_files:
        print("No test files found.")
        sys.exit(1)
    print("Tests to execute:")
    for test in test_files:
        print(f"  {test}")
    subprocess.run(
        [sys.executable, "-m", "pytest", "-v", "--alluredir=allure-results"]
        + test_files
    )
    # Generate Allure report
    subprocess.run(
        "allure generate allure-results --clean -o allure-report",
        shell=True
    )