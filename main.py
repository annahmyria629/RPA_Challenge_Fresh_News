import time

search_phrase = "ukraine"
category_section = "Arts"
number_of_months = 1

url = "https://www.nytimes.com"

from RPA.Browser.Selenium import Selenium
from datetime import timedelta, datetime
import selenium.common.exceptions as s
import requests
import re


browser_lib = Selenium()


def open_the_website(url):
    try:
        browser_lib.open_available_browser(url)
        browser_lib.maximize_browser_window()
    except Exception:
        print("Unable to connect to browser")


def search_for(phase):
    try:
        time.sleep(5)
        search_button = "//button[@data-test-id='search-button']"
        if browser_lib.is_element_visible(search_button):
            print("search button is visible")
            browser_lib.click_element(locator=search_button)
        else:
            print("search button alt is visible")
            search_button_alt1 = "//button[@data-testid='nav-button']"
            browser_lib.click_element(locator=search_button_alt1)
        browser_lib.set_browser_implicit_wait(timedelta(2))
        search_input_field = "//input[@data-testid='search-input']"
        browser_lib.input_text(locator=search_input_field, text=phase)
        browser_lib.press_keys(search_input_field, "ENTER")
        try:
            browser_lib.select_frame("3pCheckIframeId")
            browser_lib.unselect_frame()
            browser_lib.wait_until_page_contains("Date Range", timeout=timedelta(seconds=20), error="no")
        except Exception as e:
            pass
    except s.WebDriverException:
        raise Exception("Something goes wrong")


def set_category_section(category_section):
    type_button = "//div[@data-testid='type']/button[@data-testid='search-multiselect-button']"
    browser_lib.click_element(locator=type_button)
    # types = browser_lib.get_webelements(locator="//ul[@data-testid='multi-select-dropdown-list']/li")
    types = browser_lib.get_webelements(locator="//*[@data-testid='type']//li")

    types_list = [re.sub("\W?\d", "", str(item.text)).lower() for item in types]
    if category_section.lower() in types_list:
        print("Its a type")
        type_locator = f"//input[@data-testid='DropdownLabelCheckbox' and " \
                       f"@value='{category_section.replace(' ', '').lower()}']"
        browser_lib.click_element(type_locator)
        browser_lib.click_element(type_button)
    else:
        time.sleep(2)
        print("Its a section")
        section_button = "//div[@data-testid='section']/button[@data-testid='search-multiselect-button']"
        browser_lib.click_element(locator=section_button)
        # sections = browser_lib.get_webelements(locator="//ul[@data-testid='multi-select-dropdown-list']/li")
        sections = browser_lib.get_webelements(locator="//*[@data-testid='section']//li")
        if browser_lib.does_page_contain_element(sections):
            print("sections list exists")
            sections_list = [re.sub("\W?\d", "", str(item.text)) for item in sections]
            print(sections_list)
            if category_section in sections_list:
                print("Such category exists")
                try:
                    print("in try")
                    section_locator = f"//input[@data-testid='DropdownLabelCheckbox' and contains(@value, " \
                                      f"'{category_section}')]"
                    browser_lib.click_element(section_locator)
                    print("section_locator")
                except:
                    print("in except")
                    section_locator_alt = f"//button[contains(@value, '{category_section}')]"
                    browser_lib.click_button(locator=section_locator_alt)
                    print("section_locator_alt")
                finally:
                    browser_lib.click_element(locator=section_button)
                # section_locator = f"//input[@data-testid='DropdownLabelCheckbox' and contains(@value, '{category_section}')]"
                # if browser_lib.does_page_contain_element(section_locator, count=1):
                #
                #     browser_lib.click_element(section_locator)
                # else:
                #     section_locator_alt = f"//button[contains(@value, '{category_section}')]"
                #     if browser_lib.does_page_contain_button(section_locator_alt):
                #         # browser_lib.select_checkbox(section_locator_alt)
                #         print("section_locator_alt")
                #         browser_lib.click_button(locator=section_locator_alt)
                #     else:
                #         print("cant find category")
        else:
            print("sections list doesnt exist")
        print("i will click on section")
        browser_lib.click_element(locator=section_button)


def set_date_range(number_of_months):
    date_button = "//button[@data-testid='search-date-dropdown-a']"
    browser_lib.page_should_contain_button(date_button, message="Unable to find Date Range button")
    browser_lib.click_element(locator=date_button)
    specific_dates_button = "//button[@value='Specific Dates']"
    browser_lib.click_element(locator=specific_dates_button)
    date_start = "//input[@id='startDate']"
    date_end = "//input[@id='endDate']"
    browser_lib.input_text(locator=date_end, text=datetime.today().strftime("%m/%d/%Y"))
    if number_of_months == 0 or number_of_months == 1:
        date_of_start = datetime.today().replace(day=1)
    else:
        date_of_start = datetime.today().replace(day=1, month=datetime.today().month - number_of_months + 1)
    browser_lib.input_text(locator=date_start, text=date_of_start.strftime("%m/%d/%Y"))
    browser_lib.click_element(locator=date_button)
    time.sleep(3)


def sort_news_by_newest():
    sort_select = "//select[@data-testid='SearchForm-sortBy']"
    browser_lib.select_from_list_by_value(sort_select, "newest")


def check_text_on_money_occurrence(input_str):
    regex = "(\$\d+(?:\,?\d+)*(?:\.?\d+))|(\d+\s*dollar(?:s)?)|(\d+\s*USD)"
    return True if re.search(regex, input_str) is not None else False


def get_image_name(src):
    split_item = None
    if ".jpg" in src:
        split_item = ".jpg"
    elif ".png" in src:
        split_item = ".png"
    else:
        return None
    if split_item is not None:
        return src.split(".jpg")[0].split("/")[-1] + ".jpg"


def get_results(search_phrase):
    result_data = []
    browser_lib.click_element(locator="//button[@data-testid='search-show-more-button']")
    while browser_lib.does_page_contain_button("//button[@data-testid='search-show-more-button']"):
        browser_lib.click_element(locator="//button[@data-testid='search-show-more-button']")
        break

    time.sleep(5)
    res_count = len(browser_lib.get_webelements(locator="//ol[@data-testid='search-results']/li["
                                              "@data-testid='search-bodega-result']"))
    print("Records count:" + str(res_count))
    for i in range(res_count):
        tmp = []
        date = browser_lib.get_webelement(
            locator=f"//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result'][{i + 1}]"
                    f"//span[@data-testid]")
        title = browser_lib.get_webelement(
            locator=f"//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result'][{i + 1}]//h4")
        description = browser_lib.get_webelement(
            locator=f"//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result'][{i + 1}]//a/p")
        image = browser_lib.get_webelement(
            locator=f"//ol[@data-testid='search-results']/li[@data-testid='search-bodega-result'][{i + 1}]//img")
        image_src = browser_lib.get_element_attribute(image, "src")
        image_filename = get_image_name(image_src)
        if image_filename is not None:
            save_image(image_src, image_filename)
        d = date.text
        if "ago" in d:
            d = datetime.today().strftime("%B %d")
        tmp.append(d)
        tmp.append(str(title.text))
        tmp.append(str(description.text))
        tmp.append(image_filename)
        substring_count = str(title.text).lower().count(search_phrase) + str(description.text).lower()\
            .count(search_phrase)
        tmp.append(substring_count)
        money_occur = check_text_on_money_occurrence(str(title.text))
        if not money_occur:
            money_occur = check_text_on_money_occurrence(str(description.text))
        tmp.append(money_occur)
        result_data.append(tmp)
        if i == 12:
            break

    return result_data


def write_result_to_file(data):
    import csv

    header = ["date", "title", "description", "image_filename", "phrase_occurrence", "money_value_occurrence"]

    with open('result.csv', 'w', encoding='UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(header)
        for item in data:
            writer.writerow(item)


def close_browser():
    browser_lib.close_browser()


def save_image(image_src, image_filename):
    with open(image_filename, 'wb') as handle:
        response = requests.get(image_src, stream=True)

        if not response.ok:
            print(response)

        for block in response.iter_content(1024):
            if not block:
                break

            handle.write(block)


if __name__ == '__main__':
    open_the_website(url)
    search_for(search_phrase)
    set_date_range(number_of_months)
    set_category_section(category_section)
    sort_news_by_newest()
    res = get_results(search_phrase)
    write_result_to_file(res)
    close_browser()
