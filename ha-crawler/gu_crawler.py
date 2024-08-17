import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.keys import Keys


from time import sleep

def location_get(driver):
    try: 
        location = driver.find_element(
        By.CSS_SELECTOR, 
        "div > span.GHAhO").text
    except:
        return "None"
    
    return location

def description_get(driver):
    try:
        description = driver.find_element(
            By.CSS_SELECTOR,
            "div > span.lnJFt").text
    except:
        return "None"
    
    return description

def rating_get(driver):
    try:
        rating = driver.find_element(
            By.CSS_SELECTOR,
            "div.dAsGb > span.PXMot.LXIwF").text
    except:
        return "None"
    
    return rating

def detail_link_get(driver):
    try:
        # Opening Modal
        share_button = driver.find_element(
            By.CSS_SELECTOR,
            "#_btp\\.share")
        share_button.click()
        
        detail_link = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                "div._spi_release_ly._spi_card_ly.spi_card.spi_wide.nv_notrans > div.spi_copyurl > a._spi_input_copyurl._spi_copyurl_txt.spi_copyurl_url"))
                ).text
        
        # Closing Modal
        close_button = driver.find_element(
            By.CSS_SELECTOR,
            "div._spi_release_ly._spi_card_ly.spi_card.spi_wide.nv_notrans > a")
        close_button.click()
    except:
        return "None"

    return detail_link

def address_get(driver):
    try:
        address = driver.find_element(
            By.CSS_SELECTOR,
            "div.place_section_content > div > div.O8qbU.tQY7D > div > a > span.LDgIH").text
    except:
        return "None"

    return address

def reviews_get(driver, review_tab):
    try:
        review_tab.click()
        sleep(2)
        review_ul = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, "div.place_section.k1QQ5 > div.place_section_content > ul"))
        )

    
        review_li = review_ul.find_elements(By.TAG_NAME, "li")
        reviews = []
        for review in review_li:
            reviews.append(review.find_element(By.CSS_SELECTOR, "div.pui__vn15t2 > a").text)
    except:
        return ["None"]

    return reviews

def info_get(driver, info_tab):

    try:
        info_tab.click()
        info = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                'div[data-nclicks-area-code="inf"]'))
            ).text
    except:
        return "None"

    return info

# Crawling begins
# Crawling area & url
gus_place_to_visit = {}
gus = ['성북구','노원구']
url = "https://map.naver.com/"
BACK = "window.history.back();"
JSON_PATH = 'jsons/'
print("crawling begins")
for gu in gus:
    print(gu+" begins")
    file_path = JSON_PATH+gu+'.json'
    if not os.path.exists(file_path):
        os.makedirs(os.path.dirname(file_path),exist_ok=True)
    else:
        continue
    # Driver Activation
    driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
    driver.get(url)
    search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
    search.send_keys(gu)
    search.send_keys(Keys.ENTER)
    sleep(2)
    ul = WebDriverWait(driver, 10).until(
    EC.presence_of_element_located((
        By.CSS_SELECTOR, 
        '#sub_panel > div > div.panel_content > div > div > div > div > div.scroll_box > div.end_area > div:nth-child(3) > ul')))
    places = ul.find_elements(By.TAG_NAME, 'li')
    current_gu_place_to_visit = []
    for i in range(len(places)):
        place = places[i]
        sleep(2)
        place_name = place.find_element(By.CSS_SELECTOR, "button > strong").text
        print(place_name)
        # Next 가볼만한곳
        place.click()
        WebDriverWait(driver, 10).until(
            EC.frame_to_be_available_and_switch_to_it((By.ID, 'entryIframe'))
        )
        
        # Location
        sleep(2)
        location = location_get(driver=driver)
        print('location')
        # Description
        sleep(2)
        description = description_get(driver=driver)
        print('description')
        # Rating
        sleep(2)
        rating = rating_get(driver=driver)
        print('rating')
        # Detail Link
        sleep(2)
        detail_link = detail_link_get(driver=driver)
        print('detail_link')
        # Address
        sleep(2)
        address = address_get(driver=driver)
        print('address')
        # Reviews and Info
        going_back  = 0
        sleep(2)
        try:        
            tabs = driver.find_element(By.CSS_SELECTOR, 'div.flicking-camera')
            a_tags = tabs.find_elements(By.TAG_NAME, 'a')
            review_tab = None
            info_tab = None
            for a_tag in a_tags:
                if (a_tag.text == '리뷰'):
                    review_tab = a_tag
                    going_back += 1
                elif (a_tag.text == '정보'):
                    info_tab = a_tag
                    going_back += 1
        except:
            # Last back
            driver.execute_script(BACK)
            sleep(2)
            driver.switch_to.default_content()
            ul = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((
                By.CSS_SELECTOR, 
                '#sub_panel > div > div.panel_content > div > div > div > div > div.scroll_box > div.end_area > div:nth-child(3) > ul')))
            places = ul.find_elements(By.TAG_NAME, 'li')
            continue

        # Reviews
        reviews = reviews_get(driver=driver, review_tab=review_tab)
        print('reviews')
        # Info
        info = info_get(driver=driver, info_tab=info_tab)
        print('info')

        for i in range (going_back):
            driver.execute_script(BACK)
            driver.execute_script(BACK)
            sleep(2)
        
        # Last back
        driver.execute_script(BACK)
        sleep(2)
        driver.switch_to.default_content()
        ul = WebDriverWait(driver, 10).until(
        EC.presence_of_element_located((
            By.CSS_SELECTOR, 
            '#sub_panel > div > div.panel_content > div > div > div > div > div.scroll_box > div.end_area > div:nth-child(3) > ul')))
        places = ul.find_elements(By.TAG_NAME, 'li')
        if (location == "None"):
            location = place_name
        current_place_to_visit = {
            "location" : gu+" "+location,
            "description" : description,
            "rating": rating,
            "share_link": detail_link,
            "reviews": reviews,
            "info": info,
        }
        current_gu_place_to_visit.append(current_place_to_visit)
    gus_place_to_visit[gu] = current_gu_place_to_visit
    with open(JSON_PATH+gu+'.json', 'w', encoding='utf-8') as json_file:
        json.dump(gus_place_to_visit, json_file,indent=4)
    driver.quit()

print("crawling done")

