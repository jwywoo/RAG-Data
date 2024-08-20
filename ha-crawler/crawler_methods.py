from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep


def description_get(driver):
    switch_to_frame(driver, "entryIframe")
    try:
        description = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.dAsGb > div.XtBbS").text
    except Exception as e:
        print(e)
        return "None"
    
    return description

def rating_get(driver):
    switch_to_frame(driver, "entryIframe")
    try:
        rating = driver.find_element(
            By.CSS_SELECTOR,
            "div.dAsGb > span.PXMot.LXIwF").text
    except Exception as e:
        print(e)
        return "None"
    
    return rating

def detail_link_get(driver):
    switch_to_frame(driver, "entryIframe")
    try:
        open_modal = driver.find_element(
                    By.CSS_SELECTOR,
                    "#_btp\\.share")
        open_modal.click()

        detail_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                "div._spi_release_ly._spi_card_ly.spi_card.spi_wide.nv_notrans > div.spi_copyurl > a._spi_input_copyurl._spi_copyurl_txt.spi_copyurl_url"))
            ).text
                
        close_modal = driver.find_element(
                By.CSS_SELECTOR,
                "div._spi_release_ly._spi_card_ly.spi_card.spi_wide.nv_notrans > a"
            )
        close_modal.click()
    except Exception as e:
        print(e)
        return "None"

    return detail_link

def address_get(driver):
    switch_to_frame(driver, "entryIframe")
    try:
        address = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.place_section_content > div > div.O8qbU.tQY7D > div > a > span.LDgIH"
        ).text
    except Exception as e:
        print(e)
        return "None"

    return address

def tab_selector(driver, tab_needed):
    switch_to_frame(driver, "entryIframe")
    try:
        tabs = driver.find_element(By.CSS_SELECTOR, "div.flicking-camera").find_elements(By.TAG_NAME, "a")
        for tab in tabs:
            if tab.text == tab_needed:
                return tab
    except Exception as e:
        print(e)
        return None

def reviews_get(driver):
    switch_to_frame(driver, "entryIframe")
    tab = tab_selector(driver, "리뷰")
    try:
        tab.click()
        sleep(2)
        review_ul = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.place_section.k1QQ5 > div.place_section_content > ul"))
        )
    
        review_li = review_ul.find_elements(By.TAG_NAME, "li")
        reviews = []
        for review in review_li:
            reviews.append(review.find_element(By.CSS_SELECTOR, "div.pui__vn15t2 > a").text)
        return reviews
    except Exception as e:
        print(e)
        return ["None"]

    return reviews

def info_get(driver):
    switch_to_frame(driver, "entryIframe")
    tab = tab_selector(driver, "정보")
    try:
        tab.click()
        sleep(2)
        info = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                'div[data-nclicks-area-code="inf"]'))
            ).text
        return info
    except Exception as e:
        print(e)
        return "None"

def switch_to_frame(driver, frame_name):
    driver.switch_to.default_content()
    driver.switch_to.frame(frame_name)

def place_dict_generator(ad_gu, ad_dong,address, location, description, rating, share_link, reviews, info):
    return {
        "ad_gu": ad_gu,
        "ad_dong": ad_dong,
        "address": address,
        "location": location,
        "description": description,
        "rating": rating,
        "share_link": share_link,
        "reviews": reviews,
        "info": info
    }