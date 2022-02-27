import requests
from bs4 import BeautifulSoup
import re


def create_soup(url):
    my_header = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
    AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

    res = requests.get(url, headers=my_header)
    res.raise_for_status()

    soup = BeautifulSoup(res.text, "lxml")

    return soup


def print_news(index, title, link):
    print("{}. {}".format(index + 1, title))
    print("  (링크 : {})".format(link))


def scrape_weather():
    print("[오늘의 날씨]")

    url = "https://search.naver.com/search.naver?where=nexearch&sm=top_hty\
    &fbm=1&ie=utf8&query=%EC%88%98%EC%9B%90+%EB%82%A0%EC%94%A8"

    soup = create_soup(url)

    # 오늘 날씨 요약
    today_weather = soup.find("p", attrs={"class": "summary"}).get_text()[-3:]
    compare_with_yesterday = soup.find("p", attrs={"class": "summary"}).get_text()[:-3]

    # 기온
    curr_temp = soup.find("div", attrs={"class": "temperature_text"}).get_text()
    min_temp = soup.find("span", attrs={"class": "lowest"}).get_text()  # 최저 온도
    max_temp = soup.find("span", attrs={"class": "highest"}).get_text()  # 최고 온도

    # 강수 확률
    morning_rain_prob = soup.find_all("span", attrs={"class": "weather_left"})[0].get_text().strip()
    afternoon_rain_prob = soup.find_all("span", attrs={"class": "weather_left"})[1].get_text().strip()

    # 미세먼지
    today_items = soup.find_all("li", attrs={"class": re.compile("^item_today")})
    fine_dust = today_items[0].get_text().strip()
    ultrafine_dust = today_items[1].get_text().strip()

    # 출력
    print(today_weather, ",", compare_with_yesterday)
    print("기온 : {} ( {} / {} )".format(curr_temp, min_temp, max_temp))
    print("강수 확률 : {} / {}".format(morning_rain_prob, afternoon_rain_prob))
    print("대기 상태 : {} / {}".format(fine_dust, ultrafine_dust))
    print()


def scrape_headline_news():
    print("[언론사 별 1위 뉴스]")

    url = "https://news.naver.com/main/ranking/popularDay.naver?mid=etc&sid1=111"

    soup = create_soup(url)

    ranking_news_boxes = soup.find_all("div", attrs={"class": "rankingnews_box"}, limit=5)
    # 혹은, ranking_news_boxes = soup.find_all("div", attrs={"class": "rankingnews_box"})[:3] 으로 해도됨.

    for ranking_news_box in ranking_news_boxes:
        news_paper_info = ranking_news_box.find("strong", attrs={"class": "rankingnews_name"}).get_text().strip()
        rank_1_info = ranking_news_box.find_all("li")[0]
        rank_1_title = rank_1_info.find("a", attrs={"class": "list_title nclicks('RBP.rnknws')"}).get_text().strip()
        rank_1_url = rank_1_info.a["href"]

        print(news_paper_info + " : " + rank_1_title)
        print("  (링크 : {})".format(rank_1_url))

    print()


def scrape_it_news():
    print("[IT 뉴스]")

    url = "https://news.naver.com/main/list.naver?mode=LS2D&mid=shm&sid1=105&sid2=230"

    soup = create_soup(url)

    newses = soup.find("ul", attrs={"class": "type06_headline"}).find_all("li", limit=5)

    for idx, news in enumerate(newses):
        img = news.find("dt", attrs={"class": "photo"})

        if img:  # image가 있을 경우, a 태그가 두개임 (두번 째 a에 텍스트가 있음.)
            news = news.find_all("a")[1]
        else:  # image가 없을 경우, a 태그가 한개임 (첫번 째 a에 텍스트가 있음.)
            news = news.find_all("a")[0]

        title = news.get_text().strip()
        news_url = news["href"]

        print_news(idx, title, news_url)

    print()


def scrape_english():
    print("[오늘의 영어 회화]")

    url = "https://www.hackers.co.kr/?c=s_eng/eng_contents/I_others_english\
    &keywd=haceng_submain_lnb_eng_I_others_english&logger_kw=haceng_submain_lnb_eng_I_others_english"

    soup = create_soup(url)

    texts = soup.find_all("div", attrs={"id": re.compile("^conv_kor_t")})

    kor_texts = []
    eng_texts = []

    for idx, text in enumerate(texts):
        if idx < len(texts) // 2:
            kor_texts.append(text.get_text().strip())
        elif idx >= len(texts) // 2:
            eng_texts.append(text.get_text().strip())

    print("(영어 지문)")
    for eng_text in eng_texts:
        print(eng_text)

    print()

    print("(한글 지문)")
    for kor_text in kor_texts:
        print(kor_text)

    print()

    # 다른 방식 (나도코딩 선생님 강의 방식. 4줄로 끝나므로 내 코드보다 좋은 것 같음)
    # for text in texts[len(texts)//2 :]:
    #    print(text.get_text().strip()
    # for text in texts[: len(texts)//2]:
    #    print(text.get_text().strip()


if __name__ == "__main__":  # project.py 에서 실행 될 경우에만 해당 함수가 수행 됨.
    scrape_weather()  # 오늘의 날씨 정보 가져오기.
    scrape_headline_news()  # 헤드라인 뉴스 정보 가져오기
    scrape_it_news()  # IT 뉴스 정보 가져오기
    scrape_english()
