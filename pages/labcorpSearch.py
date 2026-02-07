
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage  # ← Import BasePage
from utils.window_utils import switch_to_new_window
from utils.cookie_utils import accept_cookies_if_present


class LabcorpSearchPage(BasePage):  # ← Inherit from imported BasePage
    URL = 'https://labcorp.com'
    CAREERS_LINK = (By.CSS_SELECTOR, "a[href*='careers.labcorp.com']")
    SEARCH_INPUT = (By.ID, 'typehead')
    cookie_btn = (By.ID, "onetrust-accept-btn-handler")

    def load(self):
        self.browser.get(self.URL)
        #self.click(self.cookie_btn)
        accept_cookies_if_present(self.browser, self.cookie_btn)



    def clickCareersButton(self):
        element = self.browser.find_element(*self.CAREERS_LINK)
        self.browser.execute_script("arguments[0].click();", element)
        switch_to_new_window(self.browser)

    def searchLocation(self, location):
        self.wait.until(EC.url_contains("careers.labcorp.com"))
        self.type(self.SEARCH_INPUT, location + Keys.ENTER)