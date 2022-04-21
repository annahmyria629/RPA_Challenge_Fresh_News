from RPA.Browser.Selenium import Selenium
from datetime import timedelta, datetime
import selenium.common.exceptions as s
import SeleniumLibrary.errors as se
from utils import Utils
import typing
import pathlib


class Scrapper:
    def __init__(self) -> None:
        self.browser = Selenium()
        # self.browser.set_selenium_speed(value=timedelta(seconds=1))
        a = timedelta(seconds=5)
        self.browser.set_selenium_timeout(value=timedelta(seconds=5))

    def open_browser(self, url: str) -> None:
        try:
            self.browser.open_available_browser(url)
            # self.browser.open_browser(url=url, browser="safari")
            self.browser.maximize_browser_window()
        except Exception:
            print("Unable to open to browser and go to url")

    def close_browser(self) -> None:
        self.browser.close_browser()

    def enter_search_phase(self, phase: str) -> None:
        try:
            search_button = "//button[@data-test-id='search-button']"
            search_button_alt1 = "//button[@data-testid='nav-button']"
            if self.browser.is_element_visible(search_button):
                self.browser.click_element(locator=search_button)
            else:
                self.browser.click_element(locator=search_button_alt1)
            search_input_field = "//input[@data-testid='search-input']"
            self.browser.input_text(locator=search_input_field, text=phase)
            self.browser.press_keys(search_input_field, "ENTER")
            self.browser.wait_until_page_contains(text="Date Range", error="Page with search results was not loaded")
            # try:
            #     self.browser.select_frame("3pCheckIframeId")
            #     self.browser.unselect_frame()
            #     self.browser.wait_until_page_contains("Date Range", timeout=timedelta(seconds=20), error="no")
            # except Exception as e:
            #     pass
        except s.WebDriverException:
            raise Exception("Something goes wrong")

    def set_date_range(self, number_of_months: int) -> None:
        date_button = "//button[@data-testid='search-date-dropdown-a']"
        self.browser.click_button_when_visible(locator=date_button)
        specific_dates_button = "//button[@value='Specific Dates']"
        self.browser.click_button_when_visible(locator=specific_dates_button)
        date_start_input_field = "//input[@id='startDate']"
        date_end_input_field = "//input[@id='endDate']"
        date_of_end = datetime.today().strftime("%m/%d/%Y")
        date_of_start = None
        if number_of_months == 0 or number_of_months == 1:
            date_of_start = datetime.today().replace(day=1).strftime("%m/%d/%Y")
        else:
            date_of_start = datetime.today().replace(day=1, month=datetime.today().month - number_of_months + 1) \
                .strftime("%m/%d/%Y")
        if self.browser.does_page_contain_textfield(locator=date_start_input_field) and \
                self.browser.does_page_contain_textfield(locator=date_end_input_field):
            self.browser.input_text(locator=date_end_input_field, text=date_of_end)
            self.browser.input_text(locator=date_start_input_field, text=date_of_start)
        self.browser.click_button_when_visible(locator=date_button)
        # self.browser.set_selenium_implicit_wait(value=timedelta(seconds=5))
        # # self.browser.wait_until_element_is_enabled()
        # date_range_span = "//button[@data-testid='search-date-dropdown-a']/label/span[2]/span[1][@text='Date Range: ']"
        # date_range_label = "//button[@facet-name='date']/label"
        # self.browser.wait_until_page_contains_element(locator=date_range_span, error="Date was not set")
        # date_range_label_text = self.browser.get_text(locator=date_range_label)
        # if f"Date Range: {date_of_start}–{date_of_end}" not in date_range_label_text:
        #     raise AssertionError("Date range was not set correctly")

    def set_news_section(self, category_section: str) -> bool:
        print("Start of setting section filter")
        section_button = "//div[@data-testid='section']/button[@data-testid='search-multiselect-button']"
        self.browser.click_button_when_visible(locator=section_button)
        print("click on button")
        # sections = browser_lib.get_webelements(locator="//ul[@data-testid='multi-select-dropdown-list']/li")
        sections_list_locator = "//*[@data-testid='section']//li"
        self.browser.wait_until_page_contains_element(locator=sections_list_locator,
                                                      error="Sections dropdown in not visible")
        section_locator = f"//input[@data-testid='DropdownLabelCheckbox' and contains(@value, " \
                                  f"'{category_section}')]"
        if self.browser.does_page_contain_element(section_locator):
            self.browser.click_element(section_locator)
            print("section_locator")
            self.browser.click_element(locator=section_button)
        else:
            section_locator_alt = f"//button[contains(@value, '{category_section}')]"
            if self.browser.does_page_contain_button(section_locator_alt):
                self.browser.click_button(locator=section_locator_alt)
                print("section_locator_alt")
            else:
                print("No such section")
        print("End of setting section filter")

        # print("wait until")
        # sections_list = self.browser.get_webelements(locator=sections_list_locator)
        # # if self.browser.does_page_contain_element(sections):
        # print("list  ")
        # try:
        #     sections_list_items = [re.sub("\W?\d", "", str(item.text)) for item in sections_list]
        # except Exception as e:
        #     t = type(e)
        #     a = e
        #     sections_list_items = [re.sub("\W?\d", "", str(item.text)) for item in sections_list]
        # print("list was formed")
        # if category_section in sections_list_items:
        #     print("Such section exists")
        #     section_locator = f"//input[@data-testid='DropdownLabelCheckbox' and contains(@value, " \
        #                       f"'{category_section}')]"
        #     if self.browser.does_page_contain_element(section_locator):
        #         self.browser.click_element(section_locator)
        #         print("section_locator")
        #         self.browser.click_element(locator=section_button)
        #     else:
        #         section_locator_alt = f"//button[contains(@value, '{category_section}')]"
        #         if self.browser.does_page_contain_button(section_locator_alt):
        #             self.browser.click_button(locator=section_locator_alt)
        #             print("section_locator_alt")
        #         else:
        #             print("Unable to set section filter")
        # else:
        #     print("no such section")
        # print("End of setting section filter")

    def set_news_category(self, category_section):
        print("Start of setting category filter")
        type_button = "//div[@data-testid='type']/button[@data-testid='search-multiselect-button']"
        self.browser.click_button_when_visible(locator=type_button)
        # types = browser_lib.get_webelements(locator="//ul[@data-testid='multi-select-dropdown-list']/li")
        types_list_locator = "//*[@data-testid='type']//li"
        self.browser.wait_until_page_contains_element(locator=types_list_locator,
                                                      error="Categories dropdown in not visible")
        # types_list = self.browser.get_webelements(locator="//*[@data-testid='type']//li")
        # self.browser.set_selenium_implicit_wait(value=timedelta(seconds=2))
        # types_list_items = [re.sub("\W?\d", "", str(item.text)).lower() for item in types_list]
        # self.browser.set_selenium_speed(value=timedelta(seconds=0))
        # if category_section.lower() in types_list_items:
        #     print("Its a type")
        type_locator = f"//input[@data-testid='DropdownLabelCheckbox' and " \
                       f"@value='{category_section.replace(' ', '').lower()}']"
        if self.browser.does_page_contain_element(type_locator):
            self.browser.click_element(type_locator)
            self.browser.click_button_when_visible(locator=type_button)
        else:
            type_locator_alt = f"//button[@value='{category_section.replace(' ', '').lower()}']"
            if self.browser.does_page_contain_element(type_locator_alt):
                self.browser.click_element(type_locator_alt)
            else:
                # self.browser.click_button_when_visible(locator=type_button)
                print("no such category")
        print("End of setting category filter")

    def sort_news_by_newest(self):
        sort_select = "//select[@data-testid='SearchForm-sortBy']"
        self.browser.select_from_list_by_value(sort_select, "newest")

    def get_web_element_text(self, locator: str) -> str:
        if self.browser.does_page_contain_element(locator=locator):
            web_element = self.browser.get_webelement(locator=locator)
            return web_element.text
        else:
            return ""

    def get_results(self, search_phrase: str, folder_to_save_images: str) -> typing.List:
        result_data = []
        paging_button = "//button[@data-testid='search-show-more-button']"
        try:
            while self.browser.does_page_contain_button(locator=paging_button):
                self.browser.scroll_element_into_view(locator=paging_button)
                self.browser.click_button(locator=paging_button)
        except Exception as e:
            print(type(e))
            print(str(e))

        self.browser.set_selenium_implicit_wait(value=timedelta(seconds=10))
        res_count = len(self.browser.get_webelements(locator="//ol[@data-testid='search-results']/li["
                                                             "@data-testid='search-bodega-result']"))
        print("Records count:" + str(res_count))
        for i in range(res_count):
            try:
                tmp = []
                date_locator = f"//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']" \
                               f"[{i + 1}]//span[@data-testid]"
                title_locator = f"//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']" \
                                f"[{i + 1}]//h4"
                description_locator = f"//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']" \
                                      f"[{i + 1}]//a/p"
                image_locator = f"//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']" \
                                f"[{i + 1}]//img"
                # date = self.browser.get_webelement(locator=date_locator)
                # title = self.browser.get_webelement(locator=title_locator)
                # description = self.browser.get_webelement(locator=description_locator)
                date = self.get_web_element_text(date_locator)
                title = self.get_web_element_text(title_locator)
                description = self.get_web_element_text(description_locator)
                image_filename = None
                if self.browser.does_page_contain_element(locator=image_locator):
                    image = self.browser.get_webelement(
                        locator=f"//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result']"
                                f"[{i + 1}]//img")
                    image_src = self.browser.get_element_attribute(image, "src")
                    image_filename = Utils.get_image_name(image_src)
                    if image_filename is not None:
                        Utils.save_image(image_src, image_filename, folder_to_save_images)
                if "ago" in date:
                    date = datetime.today().strftime("%B %d")
                tmp.append(date)
                tmp.append(title)
                tmp.append(description)
                tmp.append(image_filename)
                substring_count = title.lower().count(search_phrase) + description.lower().count(search_phrase)
                tmp.append(substring_count)
                money_occur = Utils.check_text_on_money_occurrence(title)
                if not money_occur:
                    money_occur = Utils.check_text_on_money_occurrence(description)
                tmp.append(money_occur)
                result_data.append(tmp)
            except Exception as e:
                print(str(e))

        return result_data


if __name__ == '__main__':
    # g_search_phrase = "Biden"
    # g_number_of_months = "1"
    # g_category_section = "Article"
    header = ["date", "title", "description", "image_filename", "phrase_occurrence", "money_value_occurrence"]
    g_url = "https://www.nytimes.com"
    input_vars = Utils.get_input_vars()
    g_search_phrase = input_vars.get("g_search_phrase", "")
    g_number_of_months = input_vars.get("g_number_of_months", "")
    g_category_section = input_vars.get("g_category_section", "")
    exc = []
    if not g_search_phrase:
        exc.append("Search phrase is empty")
    elif not g_number_of_months:
        exc.append("Search period is empty")
    elif not g_category_section:
        exc.append("Search category/section is empty")

    if exc:
        raise AssertionError(",".join(exc))

    g_number_of_months = int(g_number_of_months)

    output_folder = Utils.create_folder(pathlib.Path(__file__).parent.resolve(), "output")
    images_folder = Utils.create_folder(output_folder, "images")

    browser = Scrapper()
    browser.open_browser(g_url)
    try:
        browser.enter_search_phase(phase=g_search_phrase)
        browser.set_date_range(g_number_of_months)
        browser.set_news_section(g_category_section)
        browser.set_news_category(g_category_section)
        browser.sort_news_by_newest()
        results = browser.get_results(g_search_phrase, images_folder)
        Utils.write_result_to_file(pathlib.Path(output_folder).joinpath("result.csv"), results, header)
        print("End")
    except (se.ElementNotFound, AssertionError) as e:
        print(str(e))
    except Exception as e:
        print(str(e))
