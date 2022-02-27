import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import requests
from bs4 import BeautifulSoup

# 헤드리스 크롬 : 눈에 보이진 않지만 실행은 됨.
options = webdriver.ChromeOptions()
options.headless = True
options.add_argument("window-size=1920x1080")  # 해당 크기에 맞춰서 브라우저를 띄운 후 동작
options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) \
AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

s = Service(r"C:\Users\Home\Desktop\PythonWorkspace\chromedriver.exe")
browser = webdriver.Chrome(service=s, options=options)
browser.maximize_window()

# 페이지 이동
url = "https://play.google.com/store/movies/collection\
/cluster?clp=0g4XChUKD3RvcHNlbGxpbmdfcGFpZBAHGAQ%3D:S:ANO1ljJvXQM\
&gsr=ChrSDhcKFQoPdG9wc2VsbGluZ19wYWlkEAcYBA%3D%3D:S:ANO1ljK7jAA&hl=ko&gl=US"

browser.get(url)

# 높이가 변하지 않을 때 까지 scroll 을 내려야 함.

# 2 초에 한 번씩 scroll 내릴 예정
interval = 2

# 현재 문서의 높이 저장
prev_height = browser.execute_script("return document.body.scrollHeight")

# 반복 수행
while True:
    # scroll 을 가장 아래로 내림
    browser.execute_script("window.scrollTo(0, document.body.scrollHeight)")

    # page 로딩 대기
    time.sleep(interval)

    # 현재 문서의 높이 저장
    curr_height = browser.execute_script("return document.body.scrollHeight")

    if curr_height == prev_height:
        break

    prev_height = curr_height

print("스크롤 완료")

browser.get_screenshot_as_file("google_movie.png")

soup = BeautifulSoup(browser.page_source, "lxml")

# movies = soup.find_all("div", attrs={"class": ["ImZGtf mpg5gc", "Vpfmgd"]})  # 리스트에 있는 것을 모두 가져옴.
movies = soup.find_all("div", attrs={"class": "Vpfmgd"})
print(len(movies))


for movie in movies:
    title = movie.find("div", attrs={"class": "WsMG1c nnK0zc"}).get_text()

    # 할인 전 가격
    original_price = movie.find("span", attrs={"class": "SUZt4c djCuy"})

    if original_price:
        original_price = original_price.get_text()
    else:
        # print(title, "할인되지 않은 영화는 제외합니다.")
        # print("-" * 120)
        continue

    sale_price = movie.find("span", attrs={"class": "VfPpfd ZdBevf i5DZme"}).get_text()

    link = movie.find("a", attrs={"class": "JC71ub"})["href"]

    # 올바른 링크 : https://play.google.com + link

    print(f"제목: {title}")
    print(f"할인 전 금액: {original_price}")
    print(f"할인 후 금액: {sale_price}")
    print(f"링크 :", "https://play.google.com" + link)
    print("-" * 120)

time.sleep(2)
browser.quit()
