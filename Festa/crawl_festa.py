from selenium import webdriver
import time
from .models import Event

def crawl_festa_return_url_list():
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # Chome 드라이버 추출하기
    chromedriver = "D:\downloads\chromedriver_win32 (2)\chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options) #'chromedriver.exe'

    # chromedriver = '/usr/lib/chromium-browser/chromedriver'
    # browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)  # 'chromedriver.exe'

    url = 'https://festa.io/events'

    browser.get(url)
    time.sleep(2)

    # selector = 'a.EventCard__Card-sc-1fkxjid-0'
    # element = browser.find_elements_by_css_selector(selector)#[1].find_element_by_css_selector('div > h1').get_attribute('innerText')
    # print('개수',len(element))


    ##
    SCROLL_PAUSE_TIME = 3
    # Get scroll height
    last_height = browser.execute_script("return document.body.scrollHeight")

    result = Event.objects.all()
    result_list = list(result)
    event_links = [e.external_link for e in result_list]

    count = 0
    url_list = []
    while True:
        count += 1
        if count > 7-4: # 오래된 데이터가 많아서 이정도만 스크롤해도 되더라
            break
        # Scroll down to bottom
        browser.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        # Wait to load page
        time.sleep(SCROLL_PAUSE_TIME)

        # Calculate new scroll height and compare with last scroll height
        new_height = browser.execute_script("return document.body.scrollHeight")
        if new_height == last_height:
            break
        last_height = new_height

        ## my script here
    #root > div > div:nth-child(1) > div.Responsive__MobileView-yfth06-1.fhlCWu > div > div:nth-child(4) > div:nth-child(2) > div > div > a
        selector = '#root > div > div'#:nth-child(1) >
        element = browser.find_elements_by_css_selector(selector)[0]
        selector = 'div.Responsive__DesktopView-yfth06-0.jdVFLa > div > div'#:nth-child(3) > # 여기 count 셌다가 range(row_count,n+1) 로 가자
        element = element.find_elements_by_css_selector(selector)#[count-1] # []하면 not iterable

    print('전체 행 길이: ', len(element))
    # 여기까지 len(element)-2 루프돌면서,
    col_count = 0
    for e in range(2,len(element)): # element[e]로 접근 ?
        col_list = element[e].find_elements_by_css_selector('div') # 열의 4개가 딸려오겠지
        # col_list_content = element[e].find_elements_by_css_selector('div').get_attribute('innerText') # 열의 4개가 딸려오겠지

        print('열 길이: ', len(col_list))
        # print('내용물?', col_list_content)

        for col in col_list: # 생각보다 이벤트 별로 없다.. 페스타 말고 다른 곳도 크롤링해오기,,,
            a_link_list = col.find_elements_by_css_selector('div > div > a')
            for a_link in a_link_list:
                href_link = a_link.get_attribute('href')
                if 'events' in href_link and href_link not in url_list:

                    if href_link in event_links:
                        print('이 다음 존재하는 이벤트들')
                        return url_list

                    print(href_link)
                    url_list.append(href_link) ## 담는다

    browser.quit()
    return url_list
