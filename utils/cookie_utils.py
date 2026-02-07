from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException

def accept_cookies_if_present(driver, locator, timeout=5):
    """
    Clicks cookie accept button if present.
    Does nothing if not found.
    """
    try:
        WebDriverWait(driver, timeout).until(
            EC.element_to_be_clickable(locator)
        ).click()
    except TimeoutException:
        pass  # Cookie banner not shown
