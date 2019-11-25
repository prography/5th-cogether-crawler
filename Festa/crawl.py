import time
from selenium import webdriver
import datetime

# import psycopg2
# from config import config
from .crawl_festa import crawl_festa_return_url_list
from .models import Event, Category


def get_event_title(browser):
    # 이벤트 제목
    # root > div > div.Responsive__DesktopView-yfth06-0.jdVFLa > div.Container-sc-1mgur4j-0.ffASDH > div.EventInfoPage__TopInfoRow-sc-1ya0yur-0.jvWmTd > div.PrimaryEventInfo__Wrapper-sc-86u3sj-0.kMCeVa > h1
    selector = '#root > div > div.Responsive__MobileView-yfth06-1.fhlCWu > div'
    # root > div > div.Responsive__MobileView-yfth06-1.fhlCWu > div:nth-child(2) > div > h1
    element = browser.find_elements_by_css_selector(selector)[1].find_element_by_css_selector('div > h1').get_attribute(
        'innerText')
    # print('이벤트 제목:\n', element, sep='\n')
    return element


def get_event_date(browser):
    ## 이벤트 날짜
    selector = '#root > div > div.Responsive__MobileView-yfth06-1.fhlCWu > div'
    element = browser.find_elements_by_css_selector(selector)[1]
    selector = 'div > div.PrimaryEventInfo__DateInfo-sc-86u3sj-3.kGxvaa > div.PrimaryEventInfo__TextBlock-sc-86u3sj-7.PrimaryEventInfo__MetaText-sc-86u3sj-9.kxaXWz'
    element = element.find_element_by_css_selector(selector).get_attribute('innerText')
    # print('이벤트 날짜:\n', element, sep='\n')

    element = element.replace('\n', ' ')
    word_pm = '오후'  # 하드코딩 철자 오류는 피하자
    word_am = '오전'
    flag = True  # 49, False이면 짧 날짜 형식

    if len(element) > 40:
        flag = True
    else:
        flag = False
    string = element.split('-')
    date = []
    for s in string:
        s = s.strip()

        # 오전/오후 -> AM/PM으로 변경
        if s.find(word_pm) >= 0:
            s = s.replace(word_pm, 'PM')
        elif s.find(word_am) >= 0:
            s = s.replace(word_am, 'AM')
        if flag:
            if len(s) < 25:  # ex. PM 04:30
                s = string[0][:6] + s  # 년월일 까지 붙이고
                s = s[:14] + s[18:]
            else:  # 14 인덱스까지
                s = s[:14] + s[18:]
        else:
            if len(s) < 10:  # ex. PM 04:30
                s = string[0][:14] + s  # 년월일 까지 붙이고
            else:  # 14 인덱스까지
                s = s[:14] + s[18:]

        d = datetime.datetime.strptime(s, '%Y년 %m월 %d일 %p %I:%M')
        date.append(d)
        # print(d)
    return date


def get_event_host(browser):
    ## 이벤트 주최측
    selector = '#root > div > div.Responsive__MobileView-yfth06-1.fhlCWu > div'
    element = browser.find_elements_by_css_selector(selector)[1]
    selector = 'div > div.PrimaryEventInfo__OrganizerInfo-sc-86u3sj-4.fSzxOw > a > div > div.PrimaryEventInfo__TextBlock-sc-86u3sj-7.PrimaryEventInfo__MetaText-sc-86u3sj-9.PrimaryEventInfo__HostText-sc-86u3sj-10.bJmkce'
    element = element.find_element_by_css_selector(selector).get_attribute('innerText')
    # print('이벤트 주최측:\n', element, sep='\n')
    return element


def get_event_content(browser):
    ## 이벤트 내용
    selector = '#root > div > div.Responsive__MobileView-yfth06-1.fhlCWu > div.UserContentArea-sc-1w8buon-0.kUPCzS > p'
    element = browser.find_elements_by_css_selector(selector)
    string = ''
    for item in element:
        string += item.get_attribute('innerText') + '\n'
    # print('이벤트 내용:\n', string, sep='\n')
    return string


def get_event_location(browser):
    ## 이벤트 장소
    selector = '#root > div > div.Responsive__MobileView-yfth06-1.fhlCWu > div.LocationInfo__Wrapper-sc-1lbdfrz-0.gMXpUi > div.Container-sc-1mgur4j-0.LocationInfo__InfoContainer-sc-1lbdfrz-6.ibaBVD > div'
    element = browser.find_elements_by_css_selector(selector)
    string = ''
    for item in element:
        string += item.get_attribute('innerText') + '\n'
    # print('이벤트 장소:\n', string, sep='\n')
    return string


def get_event_tickey_price(browser):
    ## 이벤트 티켓 비용
    selector = '#root > div > div.Responsive__MobileView-yfth06-1.fhlCWu > div'
    element = browser.find_elements_by_css_selector(selector)[4]
    selector = 'div.EventInfoPage__TicketList-sc-1ya0yur-3.hbdnpp > div > div > span.tickets__PriceSpan-sc-1d0zp6o-4.jNpMGV'
    element = element.find_element_by_css_selector(selector).get_attribute('innerText')
    print('이벤트 티켓 비용:\n', element, sep='\n')


def crawl_url_list():
    url_list = crawl_festa_return_url_list()
    print(len(url_list))
    category = Category.objects.get(pk=2) # conference
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')
    # Chome 드라이버 추출하기
    chromedriver = "D:\downloads\chromedriver_win32 (2)\chromedriver.exe"
    browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)  # 'chromedriver.exe'

    # chromedriver = '/usr/lib/chromium-browser/chromedriver'
    # browser = webdriver.Chrome(executable_path=chromedriver, chrome_options=options)  # 'chromedriver.exe'


    # 밖에서 url_list 받아오면 되나 ? 아니지 같이 크롤링해야지.. 그럼 전체 url 받아오는건 다른 곳에서 test해야 겠다!
    # url_list = ['https://festa.io/events/666', 'https://festa.io/events/707']
    # url_list += ['https://festa.io/events/699','https://festa.io/events/711','https://festa.io/events/735']

    try:
        # read connection parameters
        # params = config()
        # conn = psycopg2.connect(**params)  # 무슨 문법 ?
        # # create a cursor
        # cur = conn.cursor()
        # stmt = 'select title from event_event'  # 모든 title 가져오기
        # cur.execute(stmt)
        # result = cur.fetchall()
        result = Event.objects.all()
        result_list = list(result)
        event_titles = [e.title for e in result_list]

        # def crawling():
        # stmt_id = 31
        for url_event in url_list:
            print(len(url_list))

            browser.get(url_event)
            time.sleep(2)

            title = get_event_title(browser)
            title = title.replace("'", '"')
            # print(element)
            host = get_event_host(browser)
            host = host.replace("'", '"')
            # print(element)
            content = get_event_content(browser)
            content = content.replace("'", '"')
            # print(element)
            date_list = get_event_date(browser)  # list 출력되는지 확인

            # print(element)
            location = get_event_location(browser)
            location = location.replace("'", '"')
            # print(element)
            # title, host, content, date_list, location

            # title_tuple = (title,)
            if title in event_titles:
                print(title, 'is exist')
                continue

            Event.objects.create(title=title,host=host,content=content,start_at=date_list[0] ,end_at=date_list[1] ,external_link=url_event , location=location, category=category)

            # stmt = "INSERT INTO event_event (id,title,host,content,image,category_id,created_at,updated_at,start_at,end_at,external_link,location) VALUES ("
            # stmt += f"'{stmt_id}','{title}','{host}','{content}','',1, '{datetime.datetime.now()}','{datetime.datetime.now()}', '{date_list[0]}','{date_list[1]}' ,'{url_event}','{location}')"
            # cur.execute(stmt)
            # print(stmt_id, 'ok')
            # stmt_id += 1

        # conn.commit()  # commit 해야 변화되나 ?
        # cur.close()

    except (Exception, ) as error:
        print('db error', error)

    finally:
        # if conn is not None:
        #     conn.close()
            print('database connection closed')


