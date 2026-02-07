# """
# This module contains shared fixtures.
import json
import pytest
import selenium.webdriver
import os
from datetime import datetime

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
  # Initialize the WebDriver instance
  if config['browser'] == 'Firefox':
    b = selenium.webdriver.Firefox()
  elif config['browser'] == 'Chrome':
    b = selenium.webdriver.Chrome()
  elif config['browser'] == 'Headless Chrome':
    opts = selenium.webdriver.ChromeOptions()
    opts.add_argument('--headless')  # Recommended to use --headless
    b = selenium.webdriver.Chrome(options=opts)
  else:
    raise Exception(f'Browser "{config["browser"]}" is not supported')

  b.maximize_window()

  # REMOVED: b.implicitly_wait()
  # Your BasePage explicit waits now handle timing

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
