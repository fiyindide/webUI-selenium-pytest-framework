import json
import pytest
import selenium.webdriver
import os
from datetime import datetime
from applitools.selenium import Eyes, BatchInfo

# Generate a timestamp (e.g., 2026-02-26_10-05)
timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M")

# Create a Batch object with the timestamp in the name
labcorp_batch = BatchInfo(f"Labcorp Project - {timestamp}")

@pytest.fixture(scope='session')
def config():
  # Read the file
  with open('config.json') as config_file:
    config_data = json.load(config_file)

  # Assert only the browser value
  assert config_data['browser'] in ['Firefox', 'Chrome', 'Headless Chrome']

  return config_data


@pytest.fixture
def browser(config):
  # Prepare Chrome Options (Used for both Chrome and Headless Chrome)
  chrome_opts = selenium.webdriver.ChromeOptions()
  # The 'Nuclear Option' for videos:
  chrome_opts.add_argument("--disable-background-networking")
  chrome_opts.add_argument("--mute-audio")
  # Block actual media rendering
  chrome_opts.add_argument("--blink-settings=videosEnabled=false")

  # Initialize the WebDriver instance
  if config['browser'] == 'Firefox':
    b = selenium.webdriver.Firefox()

  elif config['browser'] == 'Chrome':
    # Use the options we prepared above
    b = selenium.webdriver.Chrome(options=chrome_opts)

  elif config['browser'] == 'Headless Chrome':
    chrome_opts.add_argument('--headless')
    b = selenium.webdriver.Chrome(options=chrome_opts)

  else:
    raise Exception(f'Browser "{config["browser"]}" is not supported')

  b.maximize_window()
  yield b
  b.quit()


@pytest.hookimpl(hookwrapper=True)
def pytest_runtest_makereport(item, call):
  # Execute all other hooks to obtain the report object
  outcome = yield
  report = outcome.get_result()

  # We only care about actual test failures (not setup/teardown)
  if report.when == "call" and report.failed:
    driver = item.funcargs.get("browser")
    if driver:
      screenshots_dir = "screenshots"
      os.makedirs(screenshots_dir, exist_ok=True)

      timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
      test_name = item.name
      screenshot_path = f"{screenshots_dir}/{test_name}_{timestamp}.png"

      driver.save_screenshot(screenshot_path)

      print(f"\n Screenshot saved to: {screenshot_path}")


@pytest.fixture
def eyes(config):
  # Check if the visual test is toggled on
  if not config.get('run_visual_test', False):
    return None  # Do not initialize Applitools
  # creates the session object
  eyes = Eyes()
  # authenticate Applitools cloud with the api key
  eyes.api_key = config['applitools_api_key']
  # link the session to the shared batch
  eyes.batch = labcorp_batch
  # automatically saves new tests as baseline
  eyes.save_new_tests = True
  # eyes.force_full_page_screenshot = True 
  return eyes