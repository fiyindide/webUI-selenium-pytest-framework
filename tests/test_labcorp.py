from pages.labcorpSearch import LabcorpSearchPage
from pages.labcorpResult import LabcorpResultPage


def test_labcorpJobSearch(browser):
    search_page = LabcorpSearchPage(browser)
    result_page = LabcorpResultPage(browser)

    PHRASE = "Georgia"

    # 1. Navigation Flow
    search_page.load()
    search_page.clickCareersButton()

    # 2. Action: Search by Location
    search_page.searchLocation(PHRASE)

    # 3. Assertion: Verify Input Persistence
    # Ensures the search box actually registered and kept the 'PHRASE'
    assert PHRASE == result_page.getSearchInputValue()

    # 4. Assertion: Verify Job Results
    texts = result_page.getResultTexts()

    # Ensure at least some results were returned
    assert len(texts) >= 1

    for text in texts:
        # Use .lower() to prevent case-sensitivity from failing your test
        # e.g., 'georgia' should match 'Georgia'
        assert PHRASE.lower() in text.lower(), f"Expected '{PHRASE}' to be in result text: {text}"

    # 5. Assertion: Verify Page Title
    # This uses the corrected get_page_title() method from your Result class
    assert "results" in result_page.getPageTitle().lower()