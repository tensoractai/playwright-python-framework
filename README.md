# Playwright Python Automation Framework

A scalable end-to-end test automation framework built using **Python**, **Playwright**, **Pytest**, and **Allure Reporting**, with CI/CD support for **GitHub Actions** (Jenkins-style parameterized execution).

---

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Repository Setup & Installation](#repository-setup--installation)
3. [Environment Configuration (.env)](#environment-configuration-env)
   - [1. ObjectwaysSanity Suite](#1-objectwayssanity-suite)
   - [2. newCompanySanity Suite](#2-newcompanysanity-suite)
   - [3. Other Module Suites](#3-other-module-suites)
   - [Sample .env Template](#sample-env-template)
4. [Running Tests Locally](#running-tests-locally)
5. [Generating & Viewing Allure Reports](#generating--viewing-allure-reports)
6. [GitHub Actions Workflow (Jenkins-Style Dispatch)](#github-actions-workflow-jenkins-style-dispatch)

---

## Prerequisites

Before running the automation suite, ensure the following software is installed on your system:

| Tool | Version Requirement | Description |
| :--- | :--- | :--- |
| **Python** | `3.10+` (e.g., Python 3.11 or 3.12) | Core programming language |
| **Node.js / npm** | `v16+` (Optional, for Allure CLI) | Required to install `allure-commandline` globally |
| **Java JDK** | `JDK 11` or `JDK 17+` | Required by Allure to generate HTML reports |
| **Git** | Latest | Version control |

---

## Repository Setup & Installation

Follow these steps to clone the repository and set up your local development environment:

### Step 1: Clone the Repository
```bash
git clone <repository_url>
cd playwright-python-framework
```

### Step 2: Create & Activate Virtual Environment
- **Windows (PowerShell / Command Prompt):**
  ```powershell
  python -m venv venv
  .\venv\Scripts\activate
  ```
- **macOS / Linux:**
  ```bash
  python3 -m venv venv
  source venv/bin/activate
  ```

### Step 3: Install Python Dependencies
Install all required packages from `requirements.txt`:
```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Step 4: Install Playwright Browsers
Install Chromium browser binaries and dependencies:
```bash
playwright install --with-deps chromium
```

### Step 5: Install Allure Commandline Tool (for Reports)
- **Via npm:**
  ```bash
  npm install -g allure-commandline --save-dev
  ```
- **Via Scoop (Windows):**
  ```bash
  scoop install allure
  ```
- **Via Homebrew (macOS):**
  ```bash
  brew install allure
  ```

---

## Environment Configuration (.env)

The framework relies on environment variables stored in a `.env` file at the repository root. Create a `.env` file in the root directory before running tests.

Depending on the test suite folder you plan to run, populate the required credentials:

### 1. ObjectwaysSanity Suite (`tests/objectwaysSanity`)
Required inputs:
* **URL**: Target web application environment.
* **Company Admin**: Username & Password.
* **Annotator 1**: Username & Password.
* **Annotator 2**: Email & Password.
* **Reviewer 1**: Username & Password.

### 2. newCompanySanity Suite (`tests/newCompanySanity`)
Required inputs:
* **URL**: Target web application environment.
* **Superuser**: Username & Password (used as `company_Username` / `company_Password` when logging into the Super User org).
* **OTP Email & Password**: Email credentials for OTP authentication (`MICROSOFT_OTP_EMAIL`).

### 3. Other Module Suites (`datasets`, `files`, `projects`, `templates`, `users`, `workflows`, `AnnotatorReviewer`)
Required inputs:
* **URL**: Target web application environment.
* **Company Admin**: Username & Password.

---

### Sample `.env` Template

Create a file named `.env` in the root of your project with the following structure:

> **Note**: For `newCompanySanity`, set `company_Username` and `company_Password` to your Superuser credentials.

---

## Running Tests Locally

### Run Specific Test Folders via Pytest

- **ObjectwaysSanity Suite:**
  ```bash
  pytest tests/objectwaysSanity --alluredir=allure-results
  ```
- **New Company Sanity Suite:**
  ```bash
  pytest tests/newCompanySanity --alluredir=allure-results
  ```
- **Workflows Suite:**
  ```bash
  pytest tests/workflows --alluredir=allure-results
  ```
- **All Test Suites:**
  ```bash
  pytest tests/ --alluredir=allure-results
  ```

### Run via Test Runner Script

You can also execute tests using `run_tests.py`:
```bash
python run_tests.py
```

To run in Headless mode locally:
- **Windows (PowerShell):**
  ```powershell
  $env:HEADLESS="true"; python run_tests.py
  ```
- **Linux / macOS:**
  ```bash
  HEADLESS=true python run_tests.py
  ```

---

## Generating & Viewing Allure Reports

After executing tests, generate and view the Allure report:

1. **Serve Live Allure Report in Browser:**
   ```bash
   allure serve allure-results
   ```
2. **Generate Static HTML Allure Report:**
   ```bash
   allure generate allure-results --clean -o allure-report
   ```
   Open `allure-report/index.html` in your web browser.

---

## GitHub Actions Workflow (Jenkins-Style Dispatch)

The framework uses a single unified workflow file located at `.github/workflows/playwright.yml`, functioning like a **Jenkins parameterized build job**.

### Workflow Inputs Guide

When triggering a run manually via **GitHub Actions -> Playwright Automation Tests (Jenkins-Style) -> Run workflow**, each field is explicitly labeled with tags indicating which module requires it:

1. **`1️⃣ SELECT MODULE / SUITE`**: Pick test suite (`objectwaysSanity`, `newCompanySanity`, `AnnotatorReviewer`, `datasets`, `files`, `projects`, `templates`, `users`, `workflows`, or `all`).
2. **`2️⃣ TARGET URL`**: Target QA/Staging environment URL *(All Modules)*.
3. **`3️⃣ / 4️⃣ COMPANY ADMIN EMAIL & PASSWORD`**: Company Admin credentials *(ObjectwaysSanity, AnnotatorReviewer & Other Modules)*.
4. **`5️⃣ / 6️⃣ SUPERUSER EMAIL & PASSWORD`**: Superuser credentials *(newCompanySanity ONLY)*.
5. **`7️⃣ / 8️⃣ ANNOTATOR 1 EMAIL & PASSWORD`**: Annotator 1 credentials *(ObjectwaysSanity & AnnotatorReviewer ONLY)*.
6. **`9️⃣ / 🔟 ANNOTATOR 2 EMAIL & PASSWORD`**: Annotator 2 credentials *(ObjectwaysSanity & AnnotatorReviewer ONLY)*.
7. **`1️⃣1️⃣ / 1️⃣2️⃣ REVIEWER 1 EMAIL & PASSWORD`**: Reviewer 1 credentials *(ObjectwaysSanity & AnnotatorReviewer ONLY)*.
8. **`1️⃣3️⃣ / 1️⃣4️⃣ OTP EMAIL & PASSWORD`**: OTP authentication credentials *(ObjectwaysSanity & newCompanySanity ONLY)*.
9. **`1️⃣5️⃣ COMPANY NAME`**: Company name *(ObjectwaysSanity, AnnotatorReviewer & Other Modules)*.

---

### How to Trigger a Run Manually:

1. Navigate to your repository on **GitHub**.
2. Click on the **Actions** tab.
3. Select **Playwright Automation Tests (Jenkins-Style)** from the left sidebar.
4. Click **Run workflow** dropdown on the right.
5. Select your target module in **SELECT MODULE / SUITE** and fill in the required credential fields for that module.
6. Click **Run workflow**.

---

### Accessing Test Reports in GitHub Actions:

Once the workflow finishes executing:
1. Click on the completed workflow run.
2. Scroll down to the **Artifacts** section.
3. Download the `allure-report-<suite>` zip file to view the interactive Allure HTML report.


