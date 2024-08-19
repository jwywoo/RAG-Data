from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys

from time import sleep

url = "https://map.naver.com/"

gu = '성북구'

dong_list = [
    "성북동",
    "삼선동",
    "동선동",
    "돈암1동",
    "돈암2동",
    "안암동",
    "보문동",
    "정릉1동",
    "정릉2동",
    "정릉3동",
    "정릉4동",
    "길음1동",
    "길음2동",
    "종암동",
    "월곡1동",
    "월곡2동",
    "장위1동",
    "장위2동",
    "장위3동",
    "석관동"
]

categories = [
    '음식점',
    '카페',
]

# 중복방지 필요
# searchIframe 
#   scroll down
#   get name -> duplication check
# li -> entryIframe(similar logic as gu_crawler)
# after checking li
# hit next page and repeat 
# Dup check
searched_names = set()
for dong in dong_list:
    for category in categories:
        search_input = gu + " " + dong + " " + category
        driver = webdriver.Chrome(service= Service(ChromeDriverManager().install()))
        driver.get(url = url)
        search = driver.find_element(By.CSS_SELECTOR, 'div.input_box > input.input_search')
        search.send_keys(search_input)
        search.send_keys(Keys.ENTER)
        sleep(2)
        # Search results
        driver.switch_to.default_content()
        driver.switch_to.frame('searchIframe')
        # Results scrolling down
        body = driver.find_element(By.CSS_SELECTOR, 'body')
        body.click()
        for i in range(100):
            body.send_keys(Keys.PAGE_DOWN)
        page_tabs = driver.find_element(By.CSS_SELECTOR, "div.XUrfU > div.zRM9F")
        searched_pages = page_tabs.find_elements(By.TAG_NAME, "a")
        for page in searched_pages:
            page.click()
            sleep(2)
            li_ul = driver.find_element(By.CSS_SELECTOR, "div.Ryr1F > ul")
            places_li = li_ul.find_elements(By.TAG_NAME, "li")
            for place in places_li:
                # Return to all
                driver.switch_to.default_content()
                driver.switch_to.frame('searchIframe')
                place_name = place.find_element(By.CSS_SELECTOR, "div.CHC5F > a.tzwk0 > div > div > span.place_bluelink.TYaxT").text
                if (place_name in searched_names):
                    continue
                searched_names.add(place_name)
                
                # Go to specific
                place_link = place.find_element(By.CSS_SELECTOR, "div.CHC5F > a.tzwk0")
                place_link.click()
                sleep(3)
                driver.switch_to.default_content()
                driver.switch_to.frame("entryIframe")
                
                # Rating
                rating = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.dAsGb > span.PXMot.LXIwF").text
                print(rating)
                
                # description
                description = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.dAsGb > div"
                ).text
                print(description)

                # detail_link
                # Opening Modal
                open_modal = driver.find_element(
                    By.CSS_SELECTOR,
                    "#_btp\\.share"
                )
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
                print(detail_link)
                # Tabs
                tabs = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.flicking-camera"
                )
                a_tags = tabs.find_elements(By.TAG_NAME, 'a')
                home_tab = None 
                reviews_tab = None
                info_tab = None
                for a_tag in a_tags:
                    if (a_tag.text == '리뷰'):
                        reviews_tab = a_tag
                    if (a_tag.text == '정보'):
                        info_tab = a_tag
                    if (a_tag.text == "홈"):
                        home_tab = a_tag
                # Home
                # address
                home_tab.click()
                sleep(2)
                address = driver.find_element(
                    By.CSS_SELECTOR,
                    "div.place_section_content > div > div.O8qbU.tQY7D > div > a > span.LDgIH"
                    ).text
                print(address)
                # Reviews - tab - reviews
                reviews_tab.click()
                sleep(2)
                review_ul = WebDriverWait(driver, 10).until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, "div.place_section.k1QQ5 > div.place_section_content > ul"))
                )

            
                review_li = review_ul.find_elements(By.TAG_NAME, "li")
                reviews = []
                for review in review_li:
                    reviews.append(review.find_element(By.CSS_SELECTOR, "div.pui__vn15t2 > a").text)
                print(reviews)
                # Info - tab - info
                info_tab.click()
                sleep(2)
                info = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((
                    By.CSS_SELECTOR, 
                    'div[data-nclicks-area-code="inf"]'))
                ).text
                print(info)
                # exit
                exit_button = driver.find_element(By.CSS_SELECTOR, "header > a.mKQJy")
                exit_button.click()
                sleep(2)
        driver.quit()
        break
    break