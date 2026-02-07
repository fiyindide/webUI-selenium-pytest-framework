
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from pages.base_page import BasePage  # ← Import from base_page now

class LabcorpResultPage(BasePage):
    SEARCH_INPUT = (By.ID, 'typehead')
    SEARCH_RESULTS = (By.CSS_SELECTOR, '[data-ph-at-id="jobs-list-item"]')

    def getResultTexts(self):
        results = self.find_all_present(self.SEARCH_RESULTS)
        return [result.text for result in results]

    def getSearchInputValue(self):
        search_input = self.get_attribute(self.SEARCH_INPUT, "value")
        return search_input

    def getPageTitle(self):
        return self.browser.title