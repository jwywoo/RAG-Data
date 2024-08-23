import json
import os

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.common.exceptions import WebDriverException

from time import sleep

from crawling_enum.gu_dong_enum import GuDongEnum

from crawler_methods import description_get, rating_get, detail_link_get, address_get, reviews_get, info_get, switch_to_frame, place_dict_generator, place_type_get, place_name_get, place_link_get

url = "https://map.naver.com/"

gu_dong = GuDongEnum.seongbuk_gu_dong
gu = gu_dong.value['gu']
dong_list = gu_dong.value['dong']

categories = [
    # '음식점',
    # '카페',
    '가볼만한곳'
]

# Json file
JSON_DIR_PATH = 'json/gu_dong_json/'
file_path = os.path.join(JSON_DIR_PATH, "SeongBuk_common.json")
os.makedirs(JSON_DIR_PATH, exist_ok=True)

if os.path.exists(file_path):
    with open(file_path, 'r', encoding='utf-8') as json_file:
        data = json.load(json_file)
else:
    data = []

# Duplication Check
dup_check = []
dup_check_current = []
for row in data:
    dup_check.append(row['location'])

print(len(dup_check))
try:
    # Driver
    driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
    # Supporting vars
    current_percentage = 0
    pages_to_search = ["1", "2", "3"]
    print("")
    print(f"{gu} Crawling: Started")
    print("")
    updated_json = []
    for dong_index in range(len(dong_list)):
        for category_index in range(len(categories)):
            # Searching for results of category in gu-dong
            dong = dong_list[dong_index] 
            category = categories[category_index]
            search_input = gu + " " + dong + " " + category
            print(search_input)
            driver.get(url = url)
            search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
            search.send_keys(search_input)
            search.send_keys(Keys.ENTER)
            sleep(10)

            # Results
            # Scroll down to bottom
            switch_to_frame(driver, frame_name='searchIframe')
            body = driver.find_element(By.CSS_SELECTOR, 'body')
            body.click()
            for i in range(200):
                body.send_keys(Keys.PAGE_DOWN)
            

            # Page
            page_tabs = driver.find_element(By.CSS_SELECTOR, "div.XUrfU > div.zRM9F")
            searched_pages = page_tabs.find_elements(By.TAG_NAME, "a")
            for page_index in range(len(searched_pages)):
                switch_to_frame(driver, frame_name='searchIframe')
                page = searched_pages[page_index]
                if (page.text not in pages_to_search):
                    continue
                print("Current Page: ", page.text)
                page.click()
                sleep(2)

                # List of places from selected pages
                li_ul = driver.find_element(By.CSS_SELECTOR, "div.Ryr1F > ul")
                places_li = li_ul.find_elements(By.TAG_NAME, "li")

                for place_index in range(len(places_li)):
                    place = places_li[place_index]
                    switch_to_frame(driver, "searchIframe")
                    place_name = place_name_get(driver, place)
                    if (place_name in dup_check or place_name in dup_check_current):
                        print("already crawled")
                        continue
                    print(place_name)
                    dup_check_current.append(place_name)
                    # Getting Place Data
                    switch_to_frame(driver, "searchIframe")
                    place_link = place_link_get(driver=driver, place=place)
                    place_link.click()
                    sleep(2)

                    # searchIframe to entryIframe
                    switch_to_frame(driver, "entryIframe")
                    # address and boundary check
                    address = address_get(driver=driver)
                    if (gu not in address.split(" ")):
                        print(f"Out of {gu}!")
                        continue

                    # place type
                    place_type = place_type_get(driver=driver)
                    print(place_type)

                    # Rating
                    sleep(2)
                    rating = rating_get(driver=driver)
                    
                    # Description
                    sleep(2)
                    description = description_get(driver=driver)
                    
                    # Detail Link
                    sleep(2)
                    detail_link = detail_link_get(driver=driver)
                    
                    # Reviews
                    reviews = reviews_get(driver)
                    
                    # Info
                    info = info_get(driver)
                    updated_json.append(
                        place_dict_generator(
                            ad_gu=gu,
                            ad_dong=dong,
                            address=address,
                            place_type=place_type,
                            location=place_name,
                            description=description,
                            rating=rating,
                            share_link=detail_link,
                            reviews=reviews,
                            info=info
                        )
                    )
                    switch_to_frame(driver, "searchIframe")
        
        # Dong Crawling Done
        print(f"{dong} Crawling Done")
        print(f"Saving {len(updated_json)} Data")
        for new_row in updated_json:
            data.append(new_row)
        print(f"Current Data: {len(data)}")
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)

        # New data, updated_json and dup_check   
        print("List reset")
        updated_json = []
        dup_check = []
        if os.path.exists(file_path):
            with open(file_path, 'r', encoding='utf-8') as json_file:
                data = json.load(json_file)
        else:
            data = []
        for row in data:
            dup_check.append(row['location'])
        print(f"Updated Json List: {len(updated_json)}")
        print(f"Duplication Check: {len(dup_check)}")

    print(f"{gu} Crawling: Done!")
    driver.quit()

# Saving crawled data if there is any bad news 
except WebDriverException as e:
    print(e)
    print("Updated: ", len(updated_json))
    if (len(updated_json) != 0):
        for new_row in updated_json:
            data.append(new_row)
        with open(file_path, 'w', encoding='utf-8') as json_file:
            json.dump(data, json_file, indent=4, ensure_ascii=False)
        sleep(10)
    driver.quit()


