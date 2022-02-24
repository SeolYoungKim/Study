# HTTP method
# GET vs POST
# 1. GET : 어떤 내용을 누구나 볼 수 있게 url로 보내줌 
# ?minPrice=1000&maxPrice=1000000&page=1
# http://www.ddd.com? 뒤에 변수=값 & 변수=값 & 변수=값
# 한 번 전송할 때 보낼 수 있는 data 양이 제한되어있음.
# 웹 스크래핑 할 때 url만 조절해서 얻기 가능

# 2. POST : url이 아닌 http body에 숨겨서 보내줌
# 보안 data(id, pw등)가 이에 해당. 
# 제한이 없어서 큰 파일도 가능. 
# 개인정보, 게시판 글 등 
# url이 변하지 않을 때 POST방식.

import requests
from bs4 import BeautifulSoup
import re

url = "https://www.coupang.com/np/search?q=%EB%85%B8%ED%8A%B8%EB%B6%81&channel=user&component=&eventCategory=SRP&trcid=&traid=&sorter=scoreDesc&minPrice=&maxPrice=&priceRange=&filterType=&listSize=36&filter=&isPriceRange=false&brand=&offerCondition=&rating=0&page=1&rocketAll=false&searchIndexingToken=1=5&backgroundColor="

my_headers = {"User-Agent":"Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36"}

res = requests.get(url, headers=my_headers)
res.raise_for_status()
soup = BeautifulSoup(res.text, "lxml")

items = soup.find_all("li", attrs={"class":re.compile("^search-product")})
# print(items[0].find("div", attrs={"class":"name"}).get_text())

for item in items:

    # 광고 제품 제외
    ad_badge = item.find("span", attrs={"class":"ad-badge-text"})
    if ad_badge:
        print(" [광고 상품은 제외합니다.] ")
        continue  # 광고 상품이라면, continue 를 통해서 아래 구문은 실행하지 않고, 바로 for문으로 넘어감.

    name = item.find("div", attrs={"class":"name"}).get_text()

    # 애플 제품 제외
    if "Apple" in name:
        print(" [Apple 제품은 제외합니다.] ")
        continue

    price = item.find("strong", attrs={"class":"price-value"}).get_text()

    rate = item.find("em", attrs={"class":"rating"})
    rating_total_count = item.find("span", attrs={"class":"rating-total-count"})

    if rate or rating_total_count:  # 값이 있다면
        rate = rate.get_text()
        rating_total_count = rating_total_count.get_text()

        rating_total_count = rating_total_count[1:-1]  # 평점 수 : (25)로 출력. 1번 index부터 -1번 전까지 슬라이싱.
    else:
        rate = "평점 없음"
        rating_total_count = "평점 수 없음"
        print(" [평점이 없는 상품은 제외합니다.] ")
        continue

    # 리뷰 100개 이상, 평점 4.5 이상 되는 것만 조회
    if float(rate) >= 4.5 and int(rating_total_count) >= 100:
        print(name, price, rate, rating_total_count)

    # if rating_total_count:  # 값이 있다면
    #     rate = rate.get_text()
    # else:
    #     rate = "평점 없음"
    
    
