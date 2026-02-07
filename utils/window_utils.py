from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

def switch_to_new_window(driver, timeout=10):
    """
    Switches to the newly opened browser window or tab.
    """
    original_window = driver.current_window_handle

    WebDriverWait(driver, timeout).until(
        EC.number_of_windows_to_be(2)
    )

    for window in driver.window_handles:
        if window != original_window:
            driver.switch_to.window(window)
            return

    raise RuntimeError("No new window found to switch to")
