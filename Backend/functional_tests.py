import time
from django.test import LiveServerTestCase
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webelement import WebElement
from selenium.common.exceptions import WebDriverException
from typing import Protocol, cast
from browser import get_browser

MAX_WAIT = 5


class Support(Protocol):
    def get_attribute(self, name: str) -> str | None:
        ...

    def find_elements(self, by: str, value: str | None = None) -> list[WebElement]:
        ...


class NewVisitorTest(LiveServerTestCase):
    def setUp(self) -> None:
        self.browser = get_browser()

    def tearDown(self) -> None:
        self.browser.quit()

    def wait_for_row_in_list_table(self, row_text: str, contains: bool = True) -> None:
        start_time: float = time.time()
        while True:
            try:
                table: WebElement = self.browser.find_element(By.ID, "id_list_table")
                rows: list[WebElement] = cast(Support, table).find_elements(
                    By.TAG_NAME, "tr"
                )

                if contains:
                    self.assertIn(row_text, [row.text for row in rows])
                else:
                    self.assertNotIn(row_text, [row.text for row in rows])
                return
            except WebDriverException:
                if time.time() - start_time > MAX_WAIT:
                    raise
                time.sleep(0.5)

    def test_can_start_a_habit_tracker(self) -> None:
        # Edith has heard about a cool new online habit tracker app
        # She goes to check out its home page
        self.browser.get(self.live_server_url)

        # She notices the page title and header mention Habit Tracker
        self.assertIn(
            "Habit Tracker",
            self.browser.title,
        )

        header_text: WebElement = self.browser.find_element(By.TAG_NAME, "h1")
        self.assertIn(
            "Habit Tracker",
            header_text.text,
        )

        # She is invited to enter a habit straight away
        input_box: WebElement = self.browser.find_element(By.ID, "id_new_item")
        self.assertEqual(
            cast(Support, input_box).get_attribute("placeholder"),
            "Enter a habit you wish to track",
        )

        # She types "Do 30 minutes of exercise daily" into a text box
        input_box.send_keys("Do 30 minutes of exercise daily")

        # When she hits enter, the page updates, and now the page lists
        # "1. Do 30 minutes of exercise daily" as an item into a table
        input_box.send_keys(Keys.ENTER)
        self.wait_for_row_in_list_table("1. Do 30 minutes of exercise daily")

        # There is still a textbox inviting her to add another item.
        # She adds "Do 20 minutes of meditation every day"
        input_box.send_keys("Do 20 minutes of meditation every day")

        assert False, "Complete the Functional Tests"
