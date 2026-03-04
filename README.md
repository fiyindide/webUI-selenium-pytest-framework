# WebUI Selenium Pytest Framework

A Python-based test automation framework for web UI functional and visual validation of the Labcorp careers job search workflow. Built using Selenium WebDriver, Applitools Eyes, and pytest, following the Page Object Model (POM) design pattern.

---

## Table of Contents

- [What This Project Tests](#what-this-project-tests)
- [Tech Stack](#tech-stack)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Configuration](#configuration)
- [Project Structure](#project-structure)
- [Page Objects](#page-objects)
- [Test Description](#test-description)
- [How to Run](#how-to-run)
- [Visual Testing Dashboard](#visual-testing-dashboard)
- [How Visual Testing Works](#how-visual-testing-works)
- [Screenshots on Failure](#screenshots-on-failure)

---

## What This Project Tests

This project automates and visually validates the job search workflow on [labcorp.com](https://labcorp.com). Starting from the Labcorp homepage, the test navigates to the careers portal, performs a location-based job search, and validates both the functional correctness and visual appearance of the results.

The test suite covers:

- **Functional testing** — verifying that the job search returns relevant results, the search input persists correctly, and the results page title is accurate
- **Visual testing** — capturing snapshots of the web pages at key journey points and sending them to Applitools Eyes for AI-powered visual comparison against a baseline

---

## Tech Stack

| Tool | Purpose |
|---|---|
| Python 3.12 | Core programming language |
| pytest | Test framework and test runner |
| Selenium WebDriver 4.x | Browser automation |
| Applitools Eyes (eyes-selenium) | Visual validation |
| Google Chrome | Browser used for test execution |

---

## Prerequisites

Before running this project, ensure the following are installed on your machine:

### 1. Python 3.12
Download from [python.org](https://www.python.org/downloads/)

Verify installation:
```bash
python --version
# Expected: Python 3.12.x
```

### 2. Google Chrome
Download from [google.com/chrome](https://www.google.com/chrome/)

> Selenium Manager (included in Selenium 4.6+) automatically manages ChromeDriver. No manual ChromeDriver installation is required.

### 3. Applitools Account
Sign up for a free account at [applitools.com](https://applitools.com) to obtain your API key. An API key is only required when `run_visual_test` is set to `true` in `config.json`.

---

## Installation

### 1. Clone the repository
```bash
git clone https://github.com/YOUR_USERNAME/webUI-selenium-pytest-framework.git
cd webUI-selenium-pytest-framework
```

### 2. Create and activate a virtual environment

**Windows (PowerShell):**
```powershell
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> If you get a PowerShell execution policy error, run this first:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Set up configuration
Copy the example config and add your Applitools API key:
```bash
copy config.example.json config.json
```
Then open `config.json` and replace `YOUR_APPLITOOLS_API_KEY_HERE` with your actual Applitools API key.

> If you only want to run functional tests without visual testing, set `"run_visual_test": false` — no API key is needed in that case.

---

## Configuration

The project is driven by `config.json` in the root directory:

```json
{
  "browser": "Chrome",
  "applitools_api_key": "YOUR_APPLITOOLS_API_KEY_HERE",
  "run_visual_test": true
}
```

| Key | Description | Options |
|---|---|---|
| `browser` | Browser to run tests in | `Chrome`, `Firefox`, `Headless Chrome` |
| `applitools_api_key` | Your Applitools API key | String |
| `run_visual_test` | Enable or disable visual testing | `true`, `false` |

> **Toggling visual tests off:** Set `"run_visual_test": false` to run only functional assertions without sending results to Applitools. All Selenium interactions and assertions still run normally.

---

## Project Structure

```
webUI-selenium-pytest-framework/
│
├── pages/
│   ├── base_page.py          # Shared Selenium actions and visual check method
│   ├── labcorpSearch.py      # Page object for labcorp.com homepage and careers navigation
│   └── labcorpResult.py      # Page object for careers search results page
│
├── tests/
│   └── test_labcorp.py       # Main test suite
│
├── utils/
│   ├── cookie_utils.py       # Handles optional cookie banner acceptance
│   └── window_utils.py       # Handles switching to newly opened browser windows
│
├── screenshots/              # Failure screenshots saved here (auto-created)
│
├── conftest.py               # pytest fixtures: browser, eyes, config
├── config.example.json       # Safe config template for new users
├── requirements.txt          # Python dependencies
└── README.md
```

---

## Page Objects

### `BasePage`
The foundation class inherited by all page objects. Abstracts Selenium boilerplate and provides reusable methods across the framework:

| Method | Description |
|---|---|
| `find_visible(locator)` | Waits for element to be visible before returning it |
| `find_present(locator)` | Waits for element to be present in DOM |
| `find_all_present(locator)` | Waits for multiple elements to be present in DOM |
| `click(locator)` | Waits for element to be clickable then clicks it |
| `type(locator, text)` | Clears field and types text into a visible input |
| `get_text(locator)` | Returns the visible text of an element |
| `get_attribute(locator, attribute)` | Returns a specified attribute value of an element |
| `visual_check(tag)` | Captures an Applitools snapshot if Eyes is initialized |

### `LabcorpSearchPage`
Handles interactions on the Labcorp homepage and careers navigation:

| Method | Description |
|---|---|
| `load()` | Navigates to labcorp.com and handles cookie banner if present |
| `clickCareersButton()` | Clicks the careers link using JavaScript and switches to the new window |
| `searchLocation(location)` | Waits for careers URL and types location into the search input |

### `LabcorpResultPage`
Handles assertions on the careers search results page:

| Method | Description |
|---|---|
| `getResultTexts()` | Returns a list of all job listing text results |
| `getSearchInputValue()` | Returns the current value of the search input field |
| `getPageTitle()` | Returns the browser page title |

### Utilities

**`cookie_utils.py`** — `accept_cookies_if_present(driver, locator, timeout=5)`
Clicks the cookie accept button if it appears within the timeout period. Uses a shorter timeout (5s) than the default to fail fast when no banner is present, avoiding unnecessary slowdown on every test run.

**`window_utils.py`** — `switch_to_new_window(driver, timeout=10)`
Waits for a second browser window or tab to open, then switches focus to it. Handles the race condition that occurs when a new window opens asynchronously.

---

## Test Description

### `test_labcorpJobSearch` (`test_labcorp.py`)

A single end-to-end test that covers the complete job search user journey on the Labcorp careers portal.

**Test flow:**

```
1. Load labcorp.com
   └── Visual checkpoint: "Homepage"

2. Click Careers link
   └── Switch to new window
   └── Visual checkpoint: "Careers Landing Page"

3. Search by location ("Georgia")

4. Assert search input persists the search phrase

5. Assert at least one result is returned
   └── Visual checkpoint: "Search Results Page"

6. Assert each result contains "Georgia" or "GA"

7. Assert page title contains "results"
```

**Assertions:**

| Assertion | Description |
|---|---|
| `PHRASE == result_page.getSearchInputValue()` | Search input persists the entered phrase |
| `len(texts) >= 1` | At least one job result is returned |
| `PHRASE.lower() in text.lower() or ABBREVIATION in text` | Each result is relevant to the searched location |
| `"results" in result_page.getPageTitle().lower()` | Page title confirms results are displayed |

---

## How to Run

### Run all tests
```bash
pytest tests/ -v
```

### Run the job search test specifically
```bash
pytest tests/test_labcorp.py::test_labcorpJobSearch -v
```

### Run with print output visible
```bash
pytest tests/ -v -s
```

### Run headless (no browser window)
Update `config.json`:
```json
{
  "browser": "Headless Chrome"
}
```

### Run without visual testing
Update `config.json`:
```json
{
  "run_visual_test": false
}
```

---

## Visual Testing Dashboard

When `run_visual_test` is `true`, results are sent to your Applitools Eyes dashboard at [eyes.applitools.com](https://eyes.applitools.com).

**Dashboard structure:**
```
Batch: "Labcorp Project - YYYY-MM-DD_HH-MM"
└── Test: "Job Search Visual Test V2"
    ├── Step 1: Homepage
    ├── Step 2: Careers Landing Page
    └── Step 3: Search Results Page
```

**First run:** All steps are saved as the baseline and marked as **New**. Review and approve them on the Applitools dashboard to establish the visual baseline.

**Subsequent runs:** New screenshots are compared against the approved baseline using AI-powered visual comparison. Any structural or layout differences are flagged for review.

---

## How Visual Testing Works

Applitools Eyes uses AI-powered visual comparison rather than pixel-by-pixel matching. This project uses `MatchLevel.LAYOUT` which validates the structural layout and positioning of elements while ignoring dynamic content such as changing job listings, timestamps, or background videos.

**Why `MatchLevel.LAYOUT`?**

The Labcorp careers site contains dynamic content — job listings change frequently and the homepage may contain background video. A pixel-perfect comparison would produce false failures on every run due to this dynamic content. `LAYOUT` mode catches genuine visual regressions like broken layouts, shifted elements, or missing components while ignoring acceptable dynamic differences.

**Visual checkpoint placement:**

| Checkpoint | What it validates |
|---|---|
| Homepage | Initial page load, navigation structure, cookie banner handling |
| Careers Landing Page | Correct window switch, careers portal layout |
| Search Results Page | Results grid structure, search input state, page layout |

---

## Screenshots on Failure

When any test fails, a screenshot is automatically saved to the `screenshots/` folder:

```
screenshots/
└── test_labcorpJobSearch_2026-02-27_14-23-45.png
```

Screenshot filenames include the test name and timestamp for easy identification. This is handled automatically by a pytest hook in `conftest.py` and requires no additional configuration.
