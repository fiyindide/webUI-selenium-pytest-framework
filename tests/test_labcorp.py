from pages.labcorpSearch import LabcorpSearchPage
from pages.labcorpResult import LabcorpResultPage


def test_labcorpJobSearch(browser, eyes):
    # Without passing eyes into the page objects, you get a session with no checkpoints even when "run_visual_test": true
    search_page = LabcorpSearchPage(browser, eyes)
    result_page = LabcorpResultPage(browser, eyes)

    PHRASE = "Georgia"
    ABBREVIATION = "GA"

    try:
        if eyes:
            # Start Visual Session (webDriver, appName, testName, viewport_size)
            eyes.open(browser, "Labcorp", "Job Search Visual Test V2",
                      viewport_size={'width': 1200, 'height': 800})

        # 1. Navigation Flow
        search_page.load()
        search_page.visual_check("Homepage")

        search_page.clickCareersButton()
        search_page.visual_check("Careers Landing Page")

        # 2. Action: Search by Location
        search_page.searchLocation(PHRASE)

        # 3. Assertion: Verify Input Persistence
        # Ensures the search box actually registered and kept the 'PHRASE'
        assert PHRASE == result_page.getSearchInputValue()
        result_page.visual_check("Search Results Page")

        # 4. Assertion: Verify Job Results
        texts = result_page.getResultTexts()

        # Ensure at least some results were returned
        assert len(texts) >= 1

        for text in texts:
            assert PHRASE.lower() in text.lower() or ABBREVIATION in text

            # 5. Assertion: Verify Page Title
        assert "results" in result_page.getPageTitle().lower()

    finally:
        if eyes:
            results = eyes.close(False)
            print(f"Visual results: {results.url}")