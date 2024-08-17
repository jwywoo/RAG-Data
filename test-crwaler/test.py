from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


from selenium.webdriver.common.keys import Keys


from time import sleep

driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))

url = "https://map.naver.com/"
driver.get(url)
place_dict = {}
# naver map searching
search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
search.send_keys('성북구')
search.send_keys(Keys.ENTER)

sleep(2)
# checking '가볼만한 곳'
ul = driver.find_element(By.CSS_SELECTOR, '#sub_panel > div > div.panel_content > div > div > div > div > div.scroll_box > div.end_area > div:nth-child(3) > ul')
# #sub_panel > div > div.panel_content > div > div > div > div > div.scroll_box > div.end_area > div:nth-child(3) > ul > li:nth-child(1) > button > strong
places = ul.find_elements(By.TAG_NAME, 'li')


for i in range(len(places)):
    place = places[i]
    place.click()
    sleep(5)
    # driver.switch_to.default_content()
    driver.switch_to.frame('entryIframe')
    # location #_title > div > span.GHAhO
    location = driver.find_element(By.CSS_SELECTOR, "div > span.GHAhO")
    print("장소:" , location.text)
    # description
    description = driver.find_element(By.CSS_SELECTOR, "div > span.lnJFt")
    print("desc: ",description.text)
    # detail link
    share_button = driver.find_element(By.CSS_SELECTOR, "#_btp\.share")
    share_button.click()
    sleep(2)

    detail_link = driver.find_element(By.CSS_SELECTOR, "div._spi_release_ly._spi_card_ly.spi_card.spi_wide.nv_notrans > div.spi_copyurl > a._spi_input_copyurl._spi_copyurl_txt.spi_copyurl_url").text
    print("detail link: ", detail_link)

    close_button = driver.find_element(By.CSS_SELECTOR, "div._spi_release_ly._spi_card_ly.spi_card.spi_wide.nv_notrans > a")
    close_button.click()
    sleep(2)
    # address
    address = driver.find_element(By.CSS_SELECTOR, "div.place_section_content > div > div.O8qbU.tQY7D > div > a > span.LDgIH")
    print("address: ",address.text)
    tabs = driver.find_element(By.CSS_SELECTOR, 'div.flicking-camera')
    
    a_tags = tabs.find_elements(By.TAG_NAME, 'a')
    review_tab = None
    info_tab = None
    for a_tag in a_tags:
        if (a_tag.text == '리뷰'):
            review_tab = a_tag
        elif (a_tag.text == '정보'):
            info_tab = a_tag

    review_tab.click()
    sleep(2)
    review_ul = driver.find_element(By.CSS_SELECTOR, "div.place_section.k1QQ5 > div.place_section_content > ul")
    review_li = review_ul.find_elements(By.TAG_NAME, "li")
    
    reviews = []
    for review in review_li:
        reviews.append(review.find_element(By.CSS_SELECTOR, "div.pui__vn15t2 > a").text)
    print('reviews: ',reviews)
    info_tab.click()
    sleep(2)
    info_divs = driver.find_element(By.CSS_SELECTOR, "div[data-nclicks-area-code=\"inf\"]").text
    info = info_divs
    print("info: ", info)
    driver.execute_script("window.history.back();")
    driver.execute_script("window.history.back();")
    sleep(5)
    driver.execute_script("window.history.back();")
    driver.execute_script("window.history.back();")
    sleep(5)
    driver.execute_script("window.history.back();")
    sleep(5)
    driver.switch_to.default_content()
    ul = driver.find_element(By.CSS_SELECTOR, '#sub_panel > div > div.panel_content > div > div > div > div > div.scroll_box > div.end_area > div:nth-child(3) > ul')
    places = ul.find_elements(By.TAG_NAME, 'li')

driver.quit()